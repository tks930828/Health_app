import streamlit as st

from database import engine
from database import SessionLocal

from models import Base

from pages.profile_page import profile_page
from pages.meal_page import meal_page
from pages.weight_page import weight_page
from pages.analysis_page import analysis_page

#テーブル作成
Base.metadata.create_all(bind=engine)

#DB構築
session = SessionLocal()

#tabの作成
tab1, tab2, tab3 ,tab4 = st.tabs(
    ["プロフィール","食事", "体重","分析"]
    )
with tab1:
    df_profile = profile_page(session)
    
with tab2:
    df_meals = meal_page(session)

with tab3:
    df_weights = weight_page(session)

with tab4:
    analysis_page(
        session,
        df_meals,
        df_weights
    )