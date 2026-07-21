import pandas as pd
import streamlit as st

from datetime import date
from models import Goal
from models import Profile

from charts.goal_chart import create_goal_progress


def profile_page(session):

    st.subheader("プロフィール")

    profile = session.query(Profile).first()

    if profile:
        default_height = profile.height
    else:
        default_height = 170.0
    
    height = st.number_input(
        "身長(cm)",
        min_value=100.0,
        max_value=250.0,
        value=default_height,
        step=0.1
    )

    if st.button("プロフィール保存"):

        if profile:
            profile.height = height

        else:
            profile = Profile(height=height)
            session.add(profile)

        session.commit()

        st.success("プロフィールを保存しました")
        
#--------------------------------------
#目標体重
    st.subheader("目標体重")

    goal = session.query(Goal).first()

    if goal:
        default_weight = goal.target_weight
        default_date = goal.target_date
    else:
        default_weight = 60.0
        default_date = date.today()
        
    target_weight = st.number_input(
        "目標体重(kg)",
        min_value=30.0,
        max_value=200.0,
        value=default_weight,
        step=0.1
    )

    target_date = st.date_input(
        "目標日",
        value=default_date
    )

    if st.button("保存"):
        if goal:
            goal.target_weight = target_weight
            goal.target_date = target_date
        else:
            goal = Goal(
            target_weight=target_weight,
            target_date=target_date
            )
            session.add(goal)
    
        session.commit()
        st.success("目標を保存しました")
        st.rerun()

    if goal:
        st.info(
            f"""
            現在の目標
            目標体重：{goal.target_weight:.1f} kg
            目標日：{goal.target_date}
            """
        )