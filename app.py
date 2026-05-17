import streamlit as st

#食事入力フォーム
with st.form('eat_form'):
    date = st.datetime_input("日付を入力してください")
    meal = st.text_area("食事名を入力してください")
    

    submitted = st.form_submit_button("送信")


