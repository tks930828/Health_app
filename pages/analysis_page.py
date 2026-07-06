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

def analysis_page(
        df_meals,
        df_weights,
):

    create_kpi(
        df_meals,
        df_weights
    )

    create_pfc_summary(
          df_meals,
    )

    create_pfc_chart(
        df_meals,
    )

    create_meal_type_chart(
        df_meals,
    )

    create_monthly_chart(
        df_meals,
    )

    create_daily_chart(
    df_meals,
    )

def create_weight_chart(
    df_weights,
    ):

    #体重推移グラフ（折れ線グラフ）の作成
    if not df_weights.empty:
            
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
    else:
        st.info("体重データがありません")

def create_scatter_chart(
    df_meals,
    df_weights,
    ):

    daily_calories = (
        df_meals.groupby("date")["calories"]
        .sum()
        .reset_index()
        )

    #カロリーと体重の関係分析
    merged_df = pd.merge(
        daily_calories,
        df_weights,
        on="date",
        how="inner"
    )

    #散布図
    fig = px.scatter(
        merged_df,
        x="calories",
        y="weight",
        title="摂取カロリーと体重"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

#関数
def analysis_page(
        df_meals,
        df_weights,
):
    tab1, tab2, tab3 = st.tabs(
        ["サマリー", "食事分析", "体重分析"]
    )

    with tab1:
        create_kpi(
            df_meals,
            df_weights
        )

        col1, col2 = st.columns(2)

        with col1:
            create_pfc_chart(
                df_meals
            )

        with col2:
            create_pfc_summary(
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