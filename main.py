import pandas as pd
from fastapi import FastAPI
from typing import List, Dict
import os
from ai_predictor import predict_today_games

app = FastAPI()

data_dir = os.path.join(os.path.dirname(__file__), 'data')

def load_today_games():
    games_path = os.path.join(data_dir, 'games.csv')
    if not os.path.exists(games_path):
        return []
    df = pd.read_csv(games_path)
    return df.to_dict(orient='records')

@app.get("/games/today")
def get_today_games() -> List[Dict]:
    return load_today_games()

@app.get("/predict/today")
def predict_today_games_api() -> List[Dict]:
    return predict_today_games()

@app.get("/teams")
def get_teams() -> List[str]:
    return ["두산", "LG", "삼성", "SSG", "키움", "롯데", "한화", "KIA", "NC", "KT"] 