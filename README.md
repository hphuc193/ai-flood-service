# 🧠 Flood Warning System - AI Prediction Microservice

This repository contains the Artificial Intelligence (AI) Microservice for the Graduation Thesis: **"Application for sharing and early flood warning support using AI"**.

Operating as an independent microservice, this application receives real-time meteorological data (rainfall, water level) from the core Node.js backend, processes it through an Ensemble Machine Learning pipeline, and generates a 24-hour flood risk forecast.

## 🚀 Tech Stack & Libraries
- **Framework:** FastAPI (High-performance, asynchronous Python web framework).
- **Machine Learning:** Scikit-learn (Random Forest Regressor), XGBoost.
- **Data Processing:** Pandas, NumPy.
- **Database ORM:** SQLAlchemy (Connecting to PostgreSQL/Supabase).
- **Server:** Uvicorn (ASGI web server implementation for Python).
- **API Documentation:** Auto-generated Swagger UI.

## 🧠 AI Model Architecture (Ensemble Learning)
To ensure high accuracy and reliability in flood risk prediction, this service implements an **Ensemble Learning** approach:
1. **Random Forest:** Captures complex, non-linear relationships in hydrological data.
2. **XGBoost (Extreme Gradient Boosting):** Optimizes performance and reduces bias through sequential tree building.
3. **Ensemble Mechanism:** The system calculates the arithmetic mean of the predictions from both models to output a final stable `Risk Score` (0 - 100%).

### Risk Level Categorization:
- 🟢 **LOW (0-25%):** Normal situation, no special action required.
- 🟡 **MEDIUM (25-50%):** Needs monitoring, prepare response plans.
- 🟠 **HIGH (50-75%):** High risk, relocate assets, prepare for evacuation.
- 🔴 **EMERGENCY (75-100%):** Imminent flooding, evacuate immediately.

## 📁 Folder Structure
```text
ai-flood-service/
├── main.py               # FastAPI application entry point & API endpoints
├── database.py           # SQLAlchemy setup and database schema definition
├── ai_model.py           # Core ML logic, model loading, and ensemble prediction
├── train_models.py       # Script to generate synthetic data and train .pkl models
├── requirements.txt      # Python dependencies list
├── random_forest.pkl     # Pre-trained Random Forest model (Auto-generated)
├── xgboost.pkl           # Pre-trained XGBoost model (Auto-generated)
└── .env                  # Environment variables (Ignored in Git)
```

## ⚙️ Local Development Setup

### 1. Prerequisites
- Python 3.9+
- PostgreSQL Database (Matched with the Node.js Core Backend)

### 2. Environment Setup
Clone the repository and set up the virtual environment:
```bash
git clone <your-repo-url>
cd ai-flood-service

# Create and activate virtual environment
python -m venv venv
# On Windows: venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables (.env)
Create a `.env` file in the root directory and add your PostgreSQL connection string:
```env
DATABASE_URL="postgresql://[user]:[password]@[host]:6543/postgres"
```

### 5. Train the Models (Initial Setup)
Before running the server, you must train the initial models to generate the `.pkl` files:
```bash
python train_models.py
```
*Note: This script generates simulated hydrological data for prototype testing. In production, real datasets should be used.*

### 6. Run the Server
Start the FastAPI application using Uvicorn:
```bash
uvicorn main:app --reload --port 8000
```
Interactive API documentation (Swagger UI) will be available at: 👉 `http://localhost:8000/docs`

## 🔗 API Endpoints
- `POST /api/ai/predict`: Receives current `rainfall` and `water_level`, calculates the 24-hour forecast, and saves 24 records into the `ai_flood_predictions` table.
- `GET /api/ai/forecast-chart/{location_id}`: Retrieves the 24-hour timeline and chart data for mobile visualization.

## ☁️ Deployment
This microservice is optimized for deployment on **Render** (Web Service).
- **Environment:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
*(Ensure `DATABASE_URL` is configured in the Render Environment Variables settings).*

## 🎓 Acknowledgments
This Microservice is a core technical component of a Software Engineering Graduation Thesis at the University of Management and Technology in Ho Chi Minh City (UMT), under the dedicated supervision of **MSc. Nguyen Le Hoang Dung**.