import requests
import psycopg2
import os

API_KEY = os.getenv("TMDB_API_KEY")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "accept": "application/json"
}

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": 5432
}

def search_movie(query):
    url = 'https://api.themoviedb.org/3/search/movie'
    params = {
        'query': query,
        'language': 'ko-KR'
    }
    res = requests.get(url, params=params, headers=headers)
    res.raise_for_status()
    return res.json().get('results', [])

def save_movie_to_db(movie):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO movies (
            tmdb_id, title, original_title, overview, release_date,
            vote_average, vote_count, poster_path
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (tmdb_id) DO NOTHING;
    """, (
        movie["id"],
        movie["title"],
        movie["original_title"],
        movie["overview"],
        movie.get("release_date"),
        movie.get("vote_average"),
        movie.get("vote_count"),
        movie.get("poster_path")
    ))
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ '{movie['title']}' 저장 완료!")

def main():
    query = input("🎬 영화 제목을 입력하세요: ")
    results = search_movie(query)
    if not results:
        print("❌ 검색 결과가 없습니다.")
        return

    print(f"\n🔍 '{query}' 검색 결과:")
    for idx, movie in enumerate(results[:10], 1):
        print(f"{idx}. {movie['title']} ({movie.get('release_date', '미상')})")

    try:
        selection = int(input("\n저장할 영화 번호를 선택하세요: "))
        selected_movie = results[selection - 1]
    except (ValueError, IndexError):
        print("❌ 잘못된 선택입니다.")
        return

    save_movie_to_db(selected_movie)

if __name__ == '__main__':
    main()
