from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd 
import numpy as np 
from sklearn.linear_model import LogisticRegression
from preprocessing import Preprocessing

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_top_players():
    model = LogisticRegression()

    X_train, y_train, X_test = Preprocessing(list(range(20,27)))()

    model.fit(X_train[:, 3:], y_train)
    probs = model.predict_proba(X_test[:, 3:])[:, 1]

    indices = np.argsort(probs)[-15:]
    preds = np.zeros_like(probs, dtype = int)
    preds[indices] = 1

    players = X_test[preds == 1][:, 0]

    return players


@app.get("/players")
def get_players():
    return {'players': list(get_top_players())}


@app.get("/stats/")
def get_stats():
    players = get_players()
    df = pd.read_csv('data/2026/per_game.csv', encoding = 'utf-8')
    data = []
    for player in list(players['players']):
       data.append(list(df.loc[df['Player'] == player, ['PTS', 'TRB', 'AST']].values[0]))
    
    return {'data': data}


@app.get("/teams/")
def get_teams():
    players = get_players()
    df = pd.read_csv('data/2026/per_game.csv', encoding = 'utf-8')
    data = []
    for player in list(players['players']):
       data.append(df.loc[df['Player'] == player, 'Team'].values[0])
    
    return {'teams': data}