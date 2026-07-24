import streamlit as st

from models import Profile


def create_calorie_info(
    session,
    df_weights,
):

    profile = session.query(Profile).first()

    if profile is None:
        st.info("プロフィールを登録してください。")
        return

    if df_weights.empty:
        st.info("体重を登録してください。")
        return

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

    activity = {
        "低い": 1.2,
        "普通": 1.55,
        "高い": 1.725,
    }

    activity_factor = activity.get(
        profile.activity_level,
        1.2
    )

    recommended = (
        bmr
        * activity_factor
    )

    st.metric(
        "基礎代謝",
        f"{bmr:.0f} kcal"
    )

    st.metric(
        "推奨摂取カロリー",
        f"{recommended:.0f} kcal"
    )

    st.caption(
    "※ 推奨摂取カロリーは活動レベルを考慮して計算しています。"
    )