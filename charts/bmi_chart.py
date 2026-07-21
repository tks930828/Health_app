import streamlit as st

from models import Profile

def create_bmi(
    session,
    df_weights,
):
    #プロフィール情報を取得
    profile = session.query(Profile).first()

    #プロフィール情報がない場合
    if profile is None:
        st.info("プロフィールを登録してください。")
        return

    if df_weights.empty:
        st.info("体重を登録してください。")
        return
    
    #身長取得
    height = profile.height

    #体重取得
    current_weight = df_weights["weight"].iloc[-1]

    height_m = height / 100

    bmi = current_weight / (height_m ** 2)

    if bmi < 18.5:
        result = "低体重"

    elif bmi < 25:
        result = "普通体重"

    elif bmi < 30:
        result = "肥満（1度）"

    elif bmi < 35:
        result = "肥満（2度）"

    elif bmi < 40:
        result = "肥満（3度）"

    else:
        result = "肥満（4度）"

    st.metric(
        "BMI",
        f"{bmi:.1f}"
    )

    st.success(result)