from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///health.db"

#DB接続エンジンの作成
engine = create_engine(DATABASE_URL)

#session生成
SessionLocal = sessionmaker(bind=engine)

#ORMモデル用のクラス作成
Base = declarative_base()