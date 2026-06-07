import pandas as pd
import streamlit as st
import plotly.express as px

from database import engine
from database import SessionLocal
from models import Base
from models import Meal,Weightlog

#テーブル作成
Base.metadata.create_all(bind=engine)

#DB構築
session = SessionLocal()

#tabの作成
tab1, tab2 ,tab3 = st.tabs(["食事", "体重","分析"])

with tab1:
    st.header("食事記録")

with tab2:
    st.header("体重記録")

with tab3:
    st.header("分析")

    #日別カロリーグラフ（棒グラフ）の作成
    fig = px.bar(
        daily_calories,
        x = 'date',
        y = 'calories',
        title = '日別カロリー摂取量',
    )

    #x軸をカテゴリ軸として扱う
    fig.update_xaxes(type='category')

    #グラフの表示
    st.plotly_chart(fig)

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