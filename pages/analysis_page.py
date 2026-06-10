import streamlit as st
import plotly.express as px

def analysis_page(
        df_meals,
        df_weights
):

    st.header("分析")

    #食事推移グラフの作成
    if not df_meals.empty:

        daily_calories = (
        df_meals.groupby("date")["calories"]
        .sum()
        .reset_index()
    )

        fig = px.bar(
            df_meals,
            x="date",
            y="calories",
            title="日別カロリー摂取量"
        )

        fig.update_xaxes(type="category")

        #グラフの表示
        st.plotly_chart(fig)

    else:
        st.info("食事データがありません")


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