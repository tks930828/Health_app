import streamlit as st

from database import engine
from database import SessionLocal
from models import Base
from models import Meal,Weightlog

#テーブル作成
Base.metadata.create_all(bind=engine)

#DB構築
session = SessionLocal()

#食事入力フォーム
with st.form('eat_form'):
    meal_date = st.date_input("日付を入力してください")
    meal = st.text_input("食事名を入力してください")
    calories = st.number_input(
    "カロリー(kcal)",
    min_value=0,
    step=1
    )
    protein = st.number_input("タンパク質を入力してください")
    fat = st.number_input("脂質を入力してください")
    carb = st.number_input("炭水化物を入力してください")

    #送信ボタン
    meal_submitted = st.form_submit_button("送信")
    if meal_submitted:

        #食事入力フォームのデータ作成
        new_meal = Meal(
            date = meal_date,
            meal_name = meal,
            calories = calories,
            protein = protein,
            fat = fat,
            carb = carb
        )

        #insert実行準備
        session.add(new_meal)
        #SQL実行(insert)
        session.commit()

        st.success("食事を登録しました")

#体重入力フォーム
with st.form('weight_form'):
    weight_date = st.date_input("日付を入力してください")
    weight = st.number_input(
    "体重(kg)を入力してください",
    min_value=0.0,
    step=0.1
)
    #送信ボタン
    weight_submitted = st.form_submit_button("送信")
    if weight_submitted:
        st.success("体重を登録しました")
