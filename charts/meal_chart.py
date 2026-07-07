import pandas as pd
import streamlit as st
import plotly.express as px

#食事分析
def create_meal_type_chart(
        df_meals,
    ):

    # 食事区分別カロリー推移
    meal_type_calories = (
        df_meals.groupby("meal_type")["calories"]
        .sum()
        .reset_index()
    )

    fig  = px.bar(
        meal_type_calories,
        x="meal_type",
        y="calories",
        title="食事区分別カロリー"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

def create_monthly_chart(
        df_meals,
    ):
            
    #月別カロリー推移
    if not df_meals.empty:

        df_month = df_meals.copy()

        df_month["month"] = (
                pd.to_datetime(df_month["date"])
                .dt.strftime("%Y-%m")
            )

    monthly_calories = (
        df_month
        .groupby("month")["calories"]
        .sum()
        .reset_index()
    )
                
    fig = px.line(
            monthly_calories,
            x="month",
            y="calories",
            title="月別カロリー推移",
            markers=True
        )

    st.plotly_chart(
        fig,
        width="stretch"
    )

def create_daily_chart(
    df_meals,
    ):

    #食事推移グラフの作成
    if not df_meals.empty:

        daily_calories = (
            df_meals.groupby("date")["calories"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            daily_calories,
            x="date",
            y="calories",
            title="日別カロリー摂取量"
        )

        fig.update_xaxes(type="category")

        #グラフの表示
        st.plotly_chart(fig)

    else:
        st.info("食事データがありません")