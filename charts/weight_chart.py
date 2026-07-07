import pandas as pd
import streamlit as st
import plotly.express as px

#体重変化
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