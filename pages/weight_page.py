import pandas as pd
import streamlit as st

from models import Weightlog
from models import Goal
from datetime import date

def weight_page(session):

    #DBからweightのデータを全件取得（select * from weights)
    weights = session.query(
        Weightlog
        ).all()
    
    weight_ids = [
        weight.id for weight in weights
        ]

#-------------------------------------------------------
#体重記録

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
            "date":weight.date,
            "weight":weight.weight,
        })

    #pandas_dataframe（2次元データ）
    df_weights = pd.DataFrame(weight_data)

    st.dataframe(df_weights)

    #体重記録編集の折り畳み
    with st.expander("体重記録編集"):

        st.subheader("編集")

        # 食事データからID一覧を取得
        weight_ids = [weight.id for weight in weights]

        if weight_ids:

            #抽出したIDの情報を変換（日付｜区分｜名前）
            weight_options = {
                weight.id:
                f"{weight.date} | {weight.weight}"
                for weight in weights
            }

            #編集する体重を選択
            selected_id = st.selectbox(
            "編集する体重データ",
            options=list(weight_options.keys()),
            format_func=lambda x: weight_options[x],
            key="weight_update_id"
            )

            #DBから対象データを取得
            weight = session.query(Weightlog).filter(
                        weight.id == selected_id
                    ).first()
            
            if weight:

                new_date = st.date_input(
                    "日付",
                    value=weight.date,
                    key="weight_update_date"
                )

                new_weight = st.number_input(
                    "体重(kg)",
                    value=float(weight.weight),
                    key="weight_update_weight"
                )

            else:
                st.error("対象データが見つかりません")

            #更新ボタン
            if st.button(
                "更新",
                key = "weight_update_button"
            ):
                #値を更新
                weight.date = new_date
                weight.weight = new_weight

                #commit
                session.commit()
                st.success("更新しました")
                st.rerun()
        else:
            st.info("編集できるデータがありません")

    with st.expander("体重記録削除"):
        #体重記録の削除
        st.subheader("削除")

        # 食事データからID一覧を取得
        weight_ids = [weight.id for weight in weights]

        if weight_ids:
            
            #抽出したIDの情報を変換（日付｜区分｜名前）
            weight_options = {
            weight.id:
            f"{weight.date} | {weight.weight}"
            for weight in weights
            }

            #削除する食事を選択
            selected_id = st.selectbox(
            "削除する体重データ",
            options=list(weight_options.keys()),
            format_func=lambda x: weight_options[x],
            key="weight_delete_id"
            )

            #削除ボタンが押された場合に削除を実行する
            if st.button(
                "削除",
                key="wieght_delete_button"
            ):
            
                weight = session.query(Weightlog).filter(
                    weight.id == selected_id
                ).first()

                if weight:

                    #レコード削除
                    session.delete(weight)
                    #DBに反映
                    session.commit()

                    st.success("削除しました")
                    st.rerun()
            
                else:
                    st.error("データが存在しません")
            
        else:
            st.info("削除できるデータがありません")
        
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
    #作ったDataFrameを呼び出し元に返す
    return df_weights
