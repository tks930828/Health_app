import streamlit as st

#食事入力フォーム
with st.form('eat_form'):
    date = st.datetime_input("日付を入力してください")
    meal = st.text_area("食事名を入力してください")
    calories = st.text_area("カロリーを入力してください")
    protein = st.text_area("タンパク質を入力してください")
    fat = st.text_area("脂質を入力してください")
    carb = st.text_area("炭水化物を入力してください")


    submitted = st.form_submit_button("送信")


