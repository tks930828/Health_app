import pandas as pd
import streamlit as st
import plotly.express as px

#関数分割
from charts.kpi_chart import create_kpi
from charts.pfc_chart import create_pfc_summary
from charts.pfc_chart import create_pfc_chart
from charts.meal_chart import create_meal_type_chart
from charts.meal_chart import create_monthly_chart
from charts.meal_chart import create_daily_chart
from charts.weight_chart import create_weight_chart
from charts.weight_chart import create_scatter_chart
from charts.goal_chart import create_goal_progress
from charts.bmi_chart import create_bmi

def analysis_page(
        session,
        df_meals,
        df_weights,
):
    tab1, tab2, tab3 = st.tabs(
    ["サマリー", "食事分析", "体重分析"]
)
    with tab1:

        create_kpi(
            session,
            df_meals,
            df_weights
        )

        col1, col2 = st.columns(2)

        with col1:
            create_goal_progress(
                session,
                df_weights
            )

        with col2:
            create_bmi(
                session,
                df_weights
            )

        create_pfc_summary(
            df_meals
        )

        create_pfc_chart(
            df_meals
        )

    with tab2:

        col1, col2 = st.columns(2)

        with col1:
            create_meal_type_chart(
                df_meals
            )

        with col2:
            create_monthly_chart(
                df_meals
            )

        create_daily_chart(
            df_meals
        )

    with tab3:

        col1, col2 = st.columns(2)

        with col1:
            create_weight_chart(
                df_weights
            )

        with col2:
            create_scatter_chart(
                df_meals,
                df_weights
            )