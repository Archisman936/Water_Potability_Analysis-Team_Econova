from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from pathlib import Path

import json
import joblib
import numpy as np
import pandas as pd

# ------------------------------------------------------
# Suppress scikit-learn version mismatch warnings
# ------------------------------------------------------
import warnings
from sklearn.exceptions import InconsistentVersionWarning

warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

# ======================================================
# Paths (relative to this file)
# ======================================================
BASE_DIR = Path(__file__).resolve().parent

RIVERS_JSON_PATH = BASE_DIR / "rivers_water_quality_updated 2.0.json"
PREPROCESSOR_PATH = BASE_DIR / "preprocessor.joblib"
REGRESSOR_PATH = BASE_DIR / "regressor.joblib"
CLASSIFIER_PATH = BASE_DIR / "classifier.joblib"

# ======================================================
# Load JSON and models
# ======================================================

# Load river data
with open(RIVERS_JSON_PATH, "r", encoding="utf-8") as f:
    rivers_data = json.load(f)

# Assuming JSON structure: { "rivers": [ {...}, {...} ] }
RIVER_LIST = rivers_data["rivers"]

# Index rivers by name
RIVER_INDEX: Dict[str, Dict[str, Any]] = {
    r["name"]: r for r in RIVER_LIST
}

# Load models
preprocessor = joblib.load(PREPROCESSOR_PATH)
regressor = joblib.load(REGRESSOR_PATH)
classifier = joblib.load(CLASSIFIER_PATH)

# Features expected by models
FEATURES = [
    "ph", "Hardness", "Solids", "Chloramines", "Sulfate", "Conductivity",
    "Organic_carbon", "Trihalomethanes", "Turbidity",
    "ph_x_hardness",
    "organic_x_turbidity",
    "solids_ratio",
    "log_solids",
    "log_conductivity",
    "ph_bucket",
    "organic_bucket",
    "hardness_x_conductivity",
    "chloramine_x_trihalo",
    "organic_x_sulfate",
    "solid_density",
    "danger_index",
    "quality_index",
]

# Optional check: ensure preprocessor feature order matches
if hasattr(preprocessor, "feature_names_in_"):
    trained_feats = list(preprocessor.feature_names_in_)
    if trained_feats != FEATURES:
        raise RuntimeError(
            "Preprocessor features mismatch.\n"
            f"Expected: {FEATURES}\n"
            f"Got:      {trained_feats}"
        )

# ======================================================
# Helper: build feature row from river json
# ======================================================

def build_feature_row_from_river(river: Dict[str, Any]) -> pd.DataFrame:
    """
    Create a one-row DataFrame with all engineered features
    from a single river JSON record.
    """

    ph = river.get("ph")
    Hardness = river.get("hardness")
    Solids = river.get("solids")
    Chloramines = river.get("chloroamine")
    Sulfate = river.get("sulphates")
    Conductivity = river.get("conductivity")
    Organic_carbon = river.get("organic_carbon")
    Trihalomethanes = river.get("trichloromethane")
    Turbidity = river.get("turbidity")

    base_row = {
        "ph": ph,
        "Hardness": Hardness,
        "Solids": Solids,
        "Chloramines": Chloramines,
        "Sulfate": Sulfate,
        "Conductivity": Conductivity,
        "Organic_carbon": Organic_carbon,
        "Trihalomethanes": Trihalomethanes,
        "Turbidity": Turbidity,
    }

    temp = pd.DataFrame([base_row])

    # ---- Feature engineering (same as training) ----
    temp["ph_x_hardness"] = temp["ph"] * temp["Hardness"]
    temp["organic_x_turbidity"] = temp["Organic_carbon"] * temp["Turbidity"]
    temp["solids_ratio"] = temp["Solids"] / (temp["Hardness"] + 1)

    temp["log_solids"] = np.log1p(temp["Solids"])
    temp["log_conductivity"] = np.log1p(temp["Conductivity"])

    # ph bucket (fixed bins)
    temp["ph_bucket"] = pd.cut(
        temp["ph"],
        bins=[0, 6, 7, 8.5, 14],
        labels=[0, 1, 2, 3]
    )

    # organic bucket – handle all-NaN case to avoid ValueError
    if temp["Organic_carbon"].notna().any():
        temp["organic_bucket"] = pd.cut(
            temp["Organic_carbon"],
            bins=4,
            labels=False
        )
    else:
        temp["organic_bucket"] = 0

    temp["ph_bucket"] = pd.to_numeric(temp["ph_bucket"], errors="coerce").fillna(0).astype(int)
    temp["organic_bucket"] = pd.to_numeric(temp["organic_bucket"], errors="coerce").fillna(0).astype(int)

    temp["hardness_x_conductivity"] = temp["Hardness"] * temp["Conductivity"]
    temp["chloramine_x_trihalo"] = temp["Chloramines"] * temp["Trihalomethanes"]
    temp["organic_x_sulfate"] = temp["Organic_carbon"] * temp["Sulfate"]
    temp["solid_density"] = temp["Solids"] / (temp["Conductivity"] + 1)

    temp["danger_index"] = (
        temp["Trihalomethanes"] * 0.25 +
        temp["Chloramines"] * 0.20 +
        temp["Organic_carbon"] * 0.15 +
        temp["Turbidity"] * 0.10
    )

    temp["quality_index"] = (
        temp["ph_bucket"] +
        temp["organic_bucket"] +
        temp["solids_ratio"]
    )

    return temp[FEATURES]

# ======================================================
# Pydantic models for API responses
# ======================================================

class RiverOption(BaseModel):
    name: str
    station: Optional[str] = None


class PredictionResult(BaseModel):
    river_name: str
    station: Optional[str]
    input_parameters: Dict[str, Any]
    quality_score: float
    potability_probability: float
    potability_label: str

# ======================================================
# FastAPI app
# ======================================================

app = FastAPI(
    title="River Water Quality API",
    version="1.0.0",
    description="Predict water quality and potability for rivers."
)

# ------------------------------------------------------
# Serve the frontend (index.html)
# ------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    index_path = BASE_DIR / "index.html"
    return index_path.read_text(encoding="utf-8")

# ------------------------------------------------------
# Endpoint: list rivers (for dropdown)
# ------------------------------------------------------
@app.get("/rivers", response_model=List[RiverOption])
def list_rivers():
    return [
        RiverOption(name=r["name"], station=r.get("station"))
        for r in RIVER_LIST
    ]

# ------------------------------------------------------
# Endpoint: predict for a given river name
# ------------------------------------------------------
@app.get("/predict/{river_name}", response_model=PredictionResult)
def predict_for_river(river_name: str):
    river = RIVER_INDEX.get(river_name)
    if river is None:
        raise HTTPException(status_code=404, detail=f"River '{river_name}' not found")

    feature_row = build_feature_row_from_river(river)
    X_prepared = preprocessor.transform(feature_row)

    quality_score = float(regressor.predict(X_prepared)[0])
    proba = float(classifier.predict_proba(X_prepared)[0, 1])
    label_int = int(classifier.predict(X_prepared)[0])
    label_str = "potable" if label_int == 1 else "not potable"

    input_params = {
        "ph": river.get("ph"),
        "hardness": river.get("hardness"),
        "solids": river.get("solids"),
        "sulphates": river.get("sulphates"),
        "conductivity": river.get("conductivity"),
        "turbidity": river.get("turbidity"),
        "trichloromethane": river.get("trichloromethane"),
        "chloroamine": river.get("chloroamine"),
        "organic_carbon": river.get("organic_carbon"),
        "chloride": river.get("chloride"),
        "fluoride": river.get("fluoride"),
        "iron": river.get("iron"),
    }

    return PredictionResult(
        river_name=river["name"],
        station=river.get("station"),
        input_parameters=input_params,
        quality_score=quality_score,
        potability_probability=proba,
        potability_label=label_str,
    )

# ------------------------------------------------------
# Optional: allow `python main.py` to start the server
# ------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
