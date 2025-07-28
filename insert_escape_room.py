import psycopg2
import os

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": 5432
}

def input_escape_room_data():
    print("🔐 새로운 방탈출 테마 정보를 입력하세요:")
    theme_name = input("🎭 테마명: ")
    branch_name = input("🏢 방탈출카페 지점명: ")
    
    while True:
        try:
            difficulty = int(input("🧩 난이도 (1~5): "))
            if 1 <= difficulty <= 5:
                break
            print("❗ 1에서 5 사이 숫자를 입력하세요.")
        except ValueError:
            print("❗ 숫자를 입력하세요.")
    
    while True:
        try:
            horror_level = int(input("👻 공포도 (0~5): "))
            if 0 <= horror_level <= 5:
                break
            print("❗ 0에서 5 사이 숫자를 입력하세요.")
        except ValueError:
            print("❗ 숫자를 입력하세요.")

    location = input("📍 위치: ")
    poster_image_url = input("🖼 포스터 이미지 URL: ")

    while True:
        try:
            play_time = int(input("⏱ 플레이타임 (분): "))
            break
        except ValueError:
            print("❗ 숫자를 입력하세요.")

    synopsis = input("📝 시놉시스: ")

    return {
        "theme_name": theme_name,
        "branch_name": branch_name,
        "difficulty": difficulty,
        "horror_level": horror_level,
        "location": location,
        "poster_image_url": poster_image_url,
        "play_time": play_time,
        "synopsis": synopsis
    }

def save_escape_room_to_db(data):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO escape_rooms (
            theme_name, branch_name, difficulty, horror_level,
            location, poster_image_url, play_time, synopsis
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, (
        data["theme_name"],
        data["branch_name"],
        data["difficulty"],
        data["horror_level"],
        data["location"],
        data["poster_image_url"],
        data["play_time"],
        data["synopsis"]
    ))
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ '{data['theme_name']}' 테마가 저장되었습니다!")

def main():
    data = input_escape_room_data()
    save_escape_room_to_db(data)

if __name__ == "__main__":
    main()
