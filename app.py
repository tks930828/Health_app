import streamlit as st

from database import engine
from database import SessionLocal

from models import Base

from pages.meal_page import meal_page
from pages.weight_page import weight_page
from pages.analysis_page import analysis_page

#テーブル作成
Base.metadata.create_all(bind=engine)

#DB構築
session = SessionLocal()

#tabの作成
tab1, tab2 ,tab3 = st.tabs(
    ["食事", "体重","分析"]
    )

with tab1:
    df_meals = meal_page(session)

with tab2:
    df_weights = weight_page(session)

with tab3:
    analysis_page(
        df_meals,
        df_weights
    )