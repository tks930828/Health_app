import pandas as pd
import streamlit as st
import plotly.express as px

from database import engine
from database import SessionLocal
from models import Base
from models import Meal,Weightlog

#テーブル作成
Base.metadata.create_all(bind=engine)

#DB構築
session = SessionLocal()

#tabの作成
tab1, tab2 = st.tabs(["食事", "体重"])

#食事入力フォーム
with st.form('eat_form'):
    meal_date = st.date_input("日付を入力してください")
    meal = st.text_input("食事名を入力してください")
    calories = st.number_input(
    "カロリー(kcal)を入力してください",
    min_value=0,
    step=1
    )
    protein = st.number_input("タンパク質(g)を入力してください")
    fat = st.number_input("脂質(g)を入力してください")
    carb = st.number_input("炭水化物(g)を入力してください")

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
        "date":meal.date,
        "meal_name":meal.meal_name,
        "calories":meal.calories,
        "protein":meal.protein,
        "fat":meal.fat,
        "carb":meal.carb
    })
#meal_dataをdataframe化
df = pd.DataFrame(meal_data)

#日別集計
daily_calories = (
    df.groupby("date")["calories"] #日付でgroupby
    .sum() #合計
    .reset_index() #dataframe化
)

#pandas_dataframe（2次元データ）
df_meals = pd.DataFrame(meal_data)

#streamlit表示
st.dataframe(df_meals)

st.header("体重記録一覧")

#DBからweightのデータを全件取得（select * from weights)
weights = session.query(Weightlog).all()

#dataframe用のリスト取得
weight_data = []

#for文で1件ずつ取得
for weight in weights:

    weight_data.append({
        "date":weight.date,
        "weight":weight.weight,
    })

#pandas_dataframe（2次元データ）
df_weights = pd.DataFrame(weight_data)

#streamlit表示
st.dataframe(df_weights)

#棒グラフの作成
fig = px.bar(
    daily_calories,
    x = 'date',
    y = 'calories',
    title = '日別カロリー摂取量',
)

#x軸をカテゴリ軸として扱う
fig.update_xaxes(type='category')

#グラフの表示
st.plotly_chart(fig)

#折れ線グラフの作成
fig = px.line(
    df_weights,
    x = 'date',
    y = 'weight',
    title = '体重推移',
    markers = True
)
#x軸をカテゴリ軸として扱う
fig.update_xaxes(type='category')

#グラフの表示
st.plotly_chart(fig)