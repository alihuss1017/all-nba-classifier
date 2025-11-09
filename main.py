from fastapi import FastAPI
from nba_api.stats.static import players
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd 
import numpy as np 
import pickle
from sklearn.linear_model import LogisticRegression
from preprocessing import Preprocessing
from testing import predictions

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



@app.get("/players")
def get_players():
    X_train, y_train, X_test = Preprocessing(list(range(20, 27)))()
    model = LogisticRegression(class_weight = 'balanced')
    model.fit(X_train[:, 3:], y_train)
    return {'players': list(predictions(model = model, X_test = X_test))}


@app.get("/stats/")
def get_stats():
    players = get_players()
    df = pd.read_csv('data/2026/per_game.csv', encoding = 'utf-8')
    data = []
    for player in list(players['players']):
       data.append(list(df.loc[df['Player'] == player, ['PTS', 'TRB', 'AST']].values[0]))
    
    return {'stats': data}


@app.get("/teams/")
def get_teams():
    players = get_players()
    df = pd.read_csv('data/2026/per_game.csv', encoding = 'utf-8')
    data = []
    for player in list(players['players']):
       data.append(df.loc[df['Player'] == player, 'Team'].values[0])
    
    return {'teams': data}

@app.get("/id")
def get_id():
    player_dict = get_players()
    data = []
    for player in list(player_dict['players']):
        id = players.find_players_by_full_name(player)[0]['id']
        data.append(id)
    
    return {'id': data}