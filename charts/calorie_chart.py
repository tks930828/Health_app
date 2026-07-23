import streamlit as st

from models import Profile


def create_calorie_info(
    session,
    df_weights,
):
    #プロフィール情報を取得
    profile = session.query(Profile).first()

    #体重取得
    weight = df_weights["weight"].iloc[-1]

    if profile.sex == "男性":

        bmr = (
            10 * weight
            + 6.25 * profile.height
            - 5 * profile.age
            + 5
        )

    else:

        bmr = (
            10 * weight
            + 6.25 * profile.height
            - 5 * profile.age
            - 161
        )