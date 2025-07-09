import pandas as pd
import os
import xgboost as xgb
from sklearn.model_selection import train_test_split

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def train_xgb_model():
    results_path = os.path.join(DATA_DIR, 'results.csv')
    team_stats_path = os.path.join(DATA_DIR, 'team_stats.csv')
    if not os.path.exists(results_path) or not os.path.exists(team_stats_path):
        return None
    df = pd.read_csv(results_path)
    team_stats = pd.read_csv(team_stats_path)
    teams = list(set(df['home']).union(set(df['away']))
                 .union(set(team_stats['team'])))
    team_map = {name: i for i, name in enumerate(teams)}
    df['home_id'] = df['home'].map(team_map)
    df['away_id'] = df['away'].map(team_map)
    df['winner'] = (df['winner'] == df['home']).astype(int)
    # 최근성적, avg, era 등 피처 추가(예시)
    df = df.merge(team_stats.rename(columns={'team': 'home'}), on='home', how='left', suffixes=('', '_home'))
    df = df.merge(team_stats.rename(columns={'team': 'away'}), on='away', how='left', suffixes=('', '_away'))
    X = df[['home_id', 'away_id', 'avg', 'era', 'avg_away', 'era_away']].fillna(0)
    y = df['winner']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = xgb.XGBClassifier()
    model.fit(X_train, y_train)
    return model, team_map, team_stats

def predict_today_games():
    model_team_stats = train_xgb_model()
    if model_team_stats is None:
        return []
    model, team_map, team_stats = model_team_stats
    games_path = os.path.join(DATA_DIR, 'games.csv')
    if not os.path.exists(games_path):
        return []
    games = pd.read_csv(games_path)
    games['home_id'] = games['home'].map(team_map)
    games['away_id'] = games['away'].map(team_map)
    games = games.merge(team_stats.rename(columns={'team': 'home'}), on='home', how='left', suffixes=('', '_home'))
    games = games.merge(team_stats.rename(columns={'team': 'away'}), on='away', how='left', suffixes=('', '_away'))
    X_pred = games[['home_id', 'away_id', 'avg', 'era', 'avg_away', 'era_away']].fillna(0)
    pred = model.predict(X_pred)
    results = []
    for i, row in games.iterrows():
        results.append({
            'date': row['date'],
            'home': row['home'],
            'away': row['away'],
            'predict_winner': row['home'] if pred[i] == 1 else row['away'],
            'predict_score': {row['home']: 5, row['away']: 3}  # 점수 예측은 임시
        })
    return results 