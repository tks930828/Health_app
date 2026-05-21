from sqlalchemy import Column, Integer, String, Float, Date
from database import Base

class Meal(Base):
    __tablename__="meals"

    id = Column(Integer,primary_key=True)
    date = Column(Date)
    meal_name = Column(String)
    calories = Column(Integer)
    protein = Column(Float)
    fat = Column(Float)
    carb = Column(Float)

