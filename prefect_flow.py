from prefect import task, flow
import numpy as np
import pickle
from scraping import Scraper
from preprocessing import Preprocessing
from sklearn.linear_model import LogisticRegression
from testing import predictions

@task
def scrape_data():
    Scraper([26])()

@task
def preprocess() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    X_train, y_train, X_test = Preprocessing(list(range(20, 27)))()
    return X_train, y_train, X_test

@task 
def train(X_train: np.ndarray, y_train: np.ndarray) -> LogisticRegression:
    model = LogisticRegression(class_weight = 'balanced')
    model.fit(X_train[:, 3:], y_train)

    return model

@task 
def predict(model: LogisticRegression, X_test: np.ndarray) -> list[str]:
    players = list(predictions(model, X_test))
    return players

@flow
def pipeline():
    scrape_data()
    X_train, y_train, X_test = preprocess()
    trained_model = train(X_train, y_train)
    preds = predict(trained_model, X_test)
    with open('predictions.pkl', 'wb') as fname:
        pickle.dump(preds, fname)


pipeline()