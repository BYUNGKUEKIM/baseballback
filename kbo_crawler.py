import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime

data_dir = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(data_dir, exist_ok=True)

def fetch_kbo_results():
    # 실제 KBO 공식/비공식 사이트에서 경기 결과 크롤링 (예시: MyKBO)
    # 실제 파싱 로직 필요 (여기선 예시 데이터)
    results = [
        {"date": "2024-07-09", "home": "두산", "away": "LG", "home_score": 3, "away_score": 5, "winner": "LG"},
        {"date": "2024-07-09", "home": "삼성", "away": "SSG", "home_score": 7, "away_score": 2, "winner": "삼성"},
    ]
    pd.DataFrame(results).to_csv(os.path.join(data_dir, 'results.csv'), index=False)

def fetch_team_stats():
    # 팀별 최근 5경기 성적 등 크롤링 (예시)
    stats = [
        {"team": "두산", "recent": "3승 2패", "avg": 0.285, "era": 3.12},
        {"team": "LG", "recent": "4승 1패", "avg": 0.301, "era": 2.98},
        {"team": "삼성", "recent": "2승 3패", "avg": 0.265, "era": 3.55},
        {"team": "SSG", "recent": "1승 4패", "avg": 0.250, "era": 4.12},
    ]
    pd.DataFrame(stats).to_csv(os.path.join(data_dir, 'team_stats.csv'), index=False)

def main():
    fetch_kbo_results()
    fetch_team_stats()
    print("KBO 데이터 최신화 완료")

if __name__ == "__main__":
    main() 