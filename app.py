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

    #体重入力フォーム
    with st.form('weight_form'):
        weight_date = st.date_input("日付を入力してください")
        weight = st.number_input(
        "体重(kg)を入力してください",
        min_value=0.0,
        step=0.1
    )
        #送信ボタン
        weight_submitted = st.form_submit_button("送信")
        if weight_submitted:

            #体重入力フォームのデータ作成
            new_weight = Weightlog(
                date = weight_date,
                weight = weight,
            )

            #insert実行準備
            session.add(new_weight)
            #SQL実行(insert)
            session.commit()

            st.success("体重を登録しました")

    st.header("体重記録一覧")

    #DBからweightのデータを全件取得（select * from weights)
    weights = session.query(Weightlog).all()

    #dataframe用のリスト取得
    weight_data = []

    #for文で1件ずつ取得
    for weight in weights:

        weight_data.append({
            "id":weight.id,
            "date":weight.date,
            "weight":weight.weight,
        })

    #pandas_dataframe（2次元データ）
    df_weights = pd.DataFrame(weight_data)

    #streamlit表示
    st.dataframe(df_weights)

    # 体重記録の削除
st.subheader("削除")

weight_ids = [weight.id for weight in weights]

if weight_ids:

    selected_id = st.selectbox(
        "削除するID",
        weight_ids
    )

    if st.button("削除"):

        weight = session.query(Weightlog).filter(
            Weightlog.id == selected_id
        ).first()

        if weight:

            session.delete(weight)
            session.commit()

            st.success("削除しました")
            st.rerun()

        else:
            st.error("データが存在しません")

else:
    st.info("削除できるデータがありません")


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