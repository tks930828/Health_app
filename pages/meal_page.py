import pandas as pd
import streamlit as st

from models import Meal

def meal_page(session):

    st.header("食事記録")

        #食事入力フォーム
    with st.form('eat_form'):
        meal_date = st.date_input("日付を入力してください")
        meal_type = st.selectbox("食事区分を選択してください",
                                 ["朝食","昼食","夕食","間食"]
        )
        meal = st.text_input("食事名を入力してください")
        calories = st.number_input(
        "カロリー(kcal)を入力してください",
        min_value=0,
        step=1
        )
        protein = st.number_input("タンパク質(g)を入力してください")
        fat = st.number_input("脂質(g)を入力してください")
        carb = st.number_input("炭水化物(g)を入力してください")

        #送信ボタン
        meal_submitted = st.form_submit_button("送信")
        if meal_submitted:

            #食事入力フォームのデータ作成
            new_meal = Meal(
                date = meal_date,
                meal_name = meal,
                meal_type = meal_type,
                calories = calories,
                protein = protein,#単位
                fat = fat,#単位
                carb = carb#単位
            )

            #insert実行準備
            session.add(new_meal)
            #SQL実行(insert)
            session.commit()
            st.success("食事を登録しました")

    st.header("食事記録一覧")

    #DBからmealのデータを全件取得（select * from meals)
    meals = session.query(Meal).all()

    #dataframe用のリスト取得
    meal_data = []

    #for文で1件ずつ取得
    for meal in meals:

        meal_data.append({
            "date":meal.date,
            "meal_type":meal.meal_type,
            "meal_name":meal.meal_name,
            "calories":meal.calories,
            "protein":meal.protein,
            "fat":meal.fat,
            "carb":meal.carb
        })
    #meal_dataをdataframe化
    df = pd.DataFrame(meal_data)

    #日別集計
    if not df.empty:#データが空でなければ

        daily_calories = (
            df.groupby("date")["calories"] #日付でgroupby
            .sum() #合計
            .reset_index() #dataframe化
        )

    else:#データが空であれば
        st.info("食事データがありません")

    #pandas_dataframe（2次元データ）
    df_meals = pd.DataFrame(meal_data)

    #streamlit表示
    st.dataframe(df_meals)

    # 食事データからID一覧を取得
    meal_ids = [meal.id for meal in meals]

    if meal_ids:

        #編集するIDを選択
        selected_id = st.selectbox(
            "編集する食事",
            meal_ids,
            key = "meal_update_id"
        )

        #DBから対象データを取得
        meal = session.query(Meal).filter(
                    Meal.id == selected_id
                ).first()
        
        if meal:

            new_date = st.date_input(
                "日付",
                value=meal.date
            )

            new_meal_type = st.selectbox(
                "食事区分",
                ["朝食", "昼食", "夕食", "間食"],
                index=["朝食", "昼食", "夕食", "間食"].index(meal.meal_type)
            )

            new_meal_name = st.text_input(
                "食事名",
                value=meal.meal_name
            )

            new_calories = st.number_input(
                "カロリー",
                value=int(meal.calories)
            )
            
            new_protein = st.number_input(
                "プロテイン(g)",
                value=float(meal.protein)
            )

            new_fat = st.number_input(
                "脂肪(g)",
                value=float(meal.fat)
            )

            new_carb = st.number_input(
                "炭水化物",
                value=float(meal.carb)
            )

        else:
            st.error("対象データが見つかりません")

        #更新ボタン
        if st.button(
            "更新",
            key = "meal_update_button"
        ):
        
            #値を更新
            meal.date = new_date
            meal.meal_type = new_meal_type
            meal.meal_name = new_meal_name
            meal.calories = new_calories
            meal.protein = new_protein
            meal.fat = new_fat
            meal.carb = new_carb

            #commit
            session.commit()
            st.success("更新しました")
            st.rerun()

    else:
        st.info("編集できるデータがありません")

    #食事記録の削除
    st.subheader("削除")

    # 食事データからID一覧を取得
    meal_ids = [meal.id for meal in meals]

    if meal_ids:

     #削除するIDを選択
        selected_id = st.selectbox(
            "削除するID",
            meal_ids,
            key = "meal_delete_id"
        )

        #削除ボタンが押された場合に削除を実行する
        if st.button(
            "削除",
            key="meal_delete_button"
        ):
        
            meal = session.query(Meal).filter(
                Meal.id == selected_id
            ).first()

            if meal:

                #レコード削除
                session.delete(meal)
                #DBに反映
                session.commit()

                st.success("削除しました")
                st.rerun()
        
            else:
                st.error("データが存在しません")
        
    else:
         st.info("削除できるデータがありません")
    
    return df_meals