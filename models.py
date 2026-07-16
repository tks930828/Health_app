from sqlalchemy import Column, Integer, String, Float, Date
from database import Base

#Mealのテーブル定義
class Meal(Base):
    __tablename__="meals"

    id = Column(Integer,primary_key=True)
    date = Column(Date)
    meal_name = Column(String)
    meal_type = Column(String) #朝食・昼食・夕食・間食
    calories = Column(Integer)
    protein = Column(Float)
    fat = Column(Float)
    carb = Column(Float)

#weightlogのテーブル定義
class Weightlog(Base):
    __tablename__= "weight_logs"

    id = Column(Integer,primary_key=True)
    date = Column(Date)
    weight = Column(Float)

#目標体重管理のテーブル定義
class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True)
    target_weight = Column(Float, nullable=False)
    target_date = Column(Date, nullable=False)

#プロフィール情報のテーブル定義
class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)

    height = Column(Float)
    age = Column(Integer)
    sex = Column(String)
    activity_level = Column(String)