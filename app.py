import pandas as pd
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
            protein = protein,#単位
            fat = fat,#単位
            carb = carb#単位
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

        #体重入力フォームのデータ作成
        new_weight = Weightlog(
            date = weight_date,
            weight = weight,
        )

        #insert実行準備
        session.add(new_weight)
        #SQL実行(insert)
        session.commit()

        st.success("体重を登録しました")


st.header("食事記録一覧")

#DBからmealのデータを全件取得（select * from meals)
meals = session.query(Meal).all()

#dataframe用のリスト取得
meal_data = []

#for文で1件ずつ取得
for meal in meals:

    meal_data.append({
        "日付":meal.date,
        "食事名":meal.meal_name,
        "カロリー":meal.calories,
        "タンパク質":meal.protein,
        "脂肪":meal.fat,
        "炭水化物":meal.carb
    })

df_meals = pd.DataFrame(meal_data)

st.dataframe(df_meals)
