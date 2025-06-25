from sqlalchemy.orm import Session

from db import Base, engine, SessionLocal
from models import Movie, Tag

# DB 및 테이블 생성
Base.metadata.create_all(bind=engine)

# 세션 시작
db: Session = SessionLocal()

# 이미 데이터가 있다면 생략
if db.query(Movie).count() == 0:
    # 태그 생성
    tag_action = Tag(name="Action")
    tag_sf = Tag(name="SF")
    tag_adventure = Tag(name="Adventure")

    db.add_all([tag_action, tag_sf, tag_adventure])
    db.flush()  # 태그 id 할당을 위해 flush

    # 영화 데이터 생성
    movies = [
        Movie(
            title="Inception",
            description="A movie about dreams within dreams",
            rating=5,
            image="https://picsum.photos/600/400",
            tags=[tag_action, tag_sf, tag_adventure],
        ),
        Movie(
            title="The Matrix",
            description="A movie about a man who discovers that he is a computer program",
            rating=4,
            image="https://picsum.photos/600/400",
            tags=[tag_action, tag_sf, tag_adventure],
        ),
        Movie(
            title="Interstellar",
            description="A movie about a man who travels through time to save his family",
            rating=4,
            image="https://picsum.photos/600/400",
            tags=[tag_sf, tag_adventure],
        ),
    ]

    db.add_all(movies)
    db.commit()
    print("✅ 초기 영화 데이터가 성공적으로 삽입되었습니다.")
else:
    print("ℹ️ 이미 영화 데이터가 존재합니다. 삽입 생략.")

db.close()
