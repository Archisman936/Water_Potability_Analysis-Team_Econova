💧 Water Potability Analysis – Team ECONOVA
=========================================

🏆 Hackathon Project
-------------------
This project was developed as part of **Sreejan**, a hackathon conducted at **Techno India University** by **Sustainovate**, the **Official Sustainability and Innovation Club of Techno India University**.  
The project focuses on solving real-world sustainability and public health challenges using **AI and data-driven approaches**, and secured **2nd place** in the hackathon.

---

🌍 Project Overview
------------------
**Predicting Water Potability** aims to assess whether river water is safe for drinking by leveraging **machine learning** and **real-world water quality parameters**.

The system:
- Predicts **potability (safe / unsafe)**
- Generates a **water quality score (%)**
- Helps authorities, laboratories, NGOs, and communities take **early preventive action**

This project focuses especially on **Indian rivers**, many of which are severely affected by pollution.

---

🚀 How to Run Locally
---------------------

Follow these steps to view and run the project on your local machine:

### 1. Clone the Repository
```bash
git clone https://github.com/Archisman936/Water-Potability-Analysis---Team-Econova.git
cd Water-Potability-Analysis---Team-Econova
```

### 2. Set Up a Virtual Environment (Recommended)
```bash
python -m venv venv
```
- **Windows**: `venv\Scripts\activate`
- **macOS/Linux**: `source venv/bin/activate`

### 3. Install Dependencies
```bash
pip install fastapi uvicorn pydantic numpy pandas scikit-learn joblib catboost
```

### 4. Run the Backend Server
```bash
cd Backend
python main.py
```
This starts the FastAPI server with Uvicorn at **http://127.0.0.1:8000**.

### 5. Open in Browser
Navigate to **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser to view the application.

> **Note:** The FastAPI backend automatically serves the frontend (`index.html`). No separate frontend server is needed.

### 6. API Documentation
FastAPI provides auto-generated interactive docs:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

🚨 Background & Motivation
-------------------------
- **Massive Health Burden**: Millions are affected annually by water-borne diseases in India.
- **Widespread Contamination**: Indian rivers suffer from industrial waste and sewage pollution.
- **Urgent Need for Action**: Early prediction enables timely preventive measures.

---

📚 Literature Insight
--------------------
Indian rivers—once symbols of purity—are now burdened by:
- Industrial waste
- Sewage discharge
- Chemical contamination

This pollution impacts public health, livelihoods, and ecosystems.  
Predictive analysis empowers **citizens and authorities** to act proactively.

---

🎯 Objectives
-------------
- Develop an **AI-based model** to predict water quality and potability
- Use **real water-quality parameters** with feature engineering
- Provide a **fast and accessible decision-support tool**

---

🧠 Methodology
--------------
- **CatBoost Regressor** for water quality score prediction
- **CatBoost Classifier** for potability prediction
- Feature engineering on real-world water testing data
- **FastAPI backend** serving predictions via REST APIs

---

🛠️ Technical Stack
------------------
**Frontend**
- Tailwind CSS
- JavaScript

**Backend**
- FastAPI

**Machine Learning**
- CatBoost Regressor
- CatBoost Classifier

**Dataset**
- JSON dataset containing river parameters  
- Kaggle dataset used for model training:  
  https://www.kaggle.com/datasets/uom190346a/water-quality-and-potability

---

📈 Results
----------
- Accurate water quality scoring for multiple Indian rivers
- Reliable potability classification
- Interactive frontend for visualization and analysis

---

💬 Discussion & Impact
---------------------
- Helps reduce water-borne diseases
- Assists authorities in prioritizing polluted regions
- Promotes environmental awareness and sustainability

---

🔮 Way Forward
--------------
- Collaboration with environmental agencies
- Expansion to more rivers and seasonal data
- Open usage for future research and policy planning

---

👥 Team ECONOVA
---------------
**LinkedIn Links**

- Nathan Holt – Research  
  https://www.linkedin.com/in/the-nathan-holt/

- Md Zaid Reza – Backend  
  https://www.linkedin.com/in/md-zaid-reza-5703b5395/

- Barun Bhakat – Frontend  
  https://www.linkedin.com/in/barun-bhakat-11617a315/

- Siddhant Kumar Roy – Model  
  https://www.linkedin.com/in/siddhant-kumar-roy-746426336/

- Arham Ali Khan – Backend  
  https://www.linkedin.com/in/arham-ali-khan-8aaa35340/

- Rajtanu Chatterjee – Frontend  
  https://www.linkedin.com/in/rajtanu-chatterjee-b66522329/

- Archisman Chakraborty – Model  
  https://www.linkedin.com/in/archisman-chakraborty-525bb61b6/

---

📖 References
-------------
- Times of India (2025): Polluted River Stretches & Public Health  
- BMC Public Health (2022): Water-Borne Diseases in India  
- Mongabay India (2024): India’s Polluted Rivers  
- Central Pollution Control Board (CPCB): Polluted River Stretches Report

---

🙏 Acknowledgement
-----------------
This project was built with the vision of **leveraging AI for social good**, promoting **safe drinking water**, and supporting **sustainable development goals**.
