import streamlit as st


with st.form('eat_form'):
    date = st.datetime_input("日付を入力してください")
    meal = st.text_area("食事名を入力してください")
    


