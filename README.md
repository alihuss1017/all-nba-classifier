# Live All-NBA Teams Predictor

Predicts the 15 NBA players most likely to make the **1st, 2nd, and 3rd All-NBA Teams** based on historical performance and advanced statistics. The project provides a full-stack solution with real-time predictions, player stats, and visualizations.

![Live All-NBA Teams Predictor](image.png)

## Features

- **Predictive Modeling:** Uses supervised ML models including Random Forest, SVM, Logistic Regression, and XGBoost, with hyperparameter optimization via **Optuna**.
- **Automated Data Pipeline:** Scrapes, preprocesses, trains, and predicts weekly updates using **Prefect**, storing results for live API consumption.
- **Data Sources:**  
  - Historical per-game and advanced stats scraped using **BeautifulSoup**.  
  - Player IDs and headshots fetched via **NBA API**.
- **Backend:** **FastAPI** serves predictions, player stats, and metadata endpoints.
- **Frontend:** **React** app visualizes predicted teams, player probabilities, and stats.

### Installation

1. Clone the repository:  
```bash
git clone https://github.com/alihuss1017/Live-NBA-Team-Classifier.git
cd Live-NBA-Team-
```

2. Set up Python venv:
```bash
python -m venv myenv
source myenv/bin/activate #macOS/Linux
venv\Scripts\activate #Windows
pip install -r requirements.txt
```

3. Run FastAPI backend
```bash
uvicorn main:app --reload
```

4. Start React app
```bash
cd my-react-app
npm install
npm run dev
```

## Architecture

The system follows a modular, end-to-end workflow:

1. **Data Collection:** Scrapes historical NBA stats and advanced metrics weekly using **BeautifulSoup**, and fetches player IDs and headshots from the **NBA API**.  
2. **Preprocessing:** Cleans, normalizes, and structures data into a format suitable for model training and predictions.  
3. **Model Training & Optimization:** Trains multiple ML models (Random Forest, SVM, Logistic Regression, XGBoost) and optimizes hyperparameters with **Optuna**.  
4. **Prediction:** Generates probability scores for 1st, 2nd, and 3rd All-NBA team selections.  
5. **Serving:** Provides a **FastAPI** backend exposing endpoints for predictions, player info, and stats.  
6. **Frontend Visualization:** **React** app displays team predictions, player probabilities, and detailed stats.  
7. **Workflow Orchestration:** **Prefect** automates weekly updates, ensuring the latest predictions are always available.

## Technologies Used

- **Backend:** FastAPI, Python  
- **Frontend:** React, JavaScript, CSS  
- **Data Processing & Modeling:** Pandas, NumPy, Scikit-learn, Optuna  
- **Workflow Orchestration:** Prefect  
- **Web Scraping:** BeautifulSoup  
- **Data Sources:** NBA API  
- **Deployment & Environment:** Python virtual environments, local or cloud-based orchestration
