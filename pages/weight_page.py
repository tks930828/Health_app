import pandas as pd
import streamlit as st

from models import Weightlog

def weight_page(session):

    #DBからweightのデータを全件取得（select * from weights)
    weights = session.query(
        Weightlog
        ).all()
    
    weight_ids = [
        weight.id for weight in weights
        ]

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

    st.dataframe(df_weights)

    # 体重記録の削除
    st.subheader("削除")

    if weight_ids:

        selected_id = st.selectbox(
            "削除するID",
            weight_ids,
            key = "weight_delete_id"
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

    return df_weights