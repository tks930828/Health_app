import pandas as pd
import streamlit as st
import plotly.express as px

def analysis_page(
        df_meals,
        df_weights,
):
    # 総摂取カロリー
    total_calories = df_meals["calories"].sum()
    # 平均体重
    average_weight = df_weights["weight"].mean()
    # 記録日数
    record_days = len(df_weights)
    # プロテイン
    total_protein = df_meals["protein"].sum()
    # 脂質
    total_fat = df_meals["fat"].sum()
    # 炭水化物
    total_carb = df_meals["carb"].sum()

     # 体重変化
    end_weight = None
    weight_change = None

    #体重変化KPI
    if not df_weights.empty:
        start_weight = df_weights["weight"].iloc[0]
        end_weight = df_weights["weight"].iloc[-1]
        weight_change = end_weight - start_weight

    st.subheader("健康サマリー")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "総摂取カロリー",
            f"{total_calories:.0f} kcal"
        )
    with col2:
        st.metric(
            "平均体重",
            f"{average_weight:.1f} kg"
        )
    with col3:
        st.metric(
            "記録日数",
            f"{record_days} 日"
        )
    with col4:
        st.metric(
            "体重変化",
            f"{end_weight:.1f} kg"
            if end_weight is not None else "-",
            delta=f"{weight_change:+.1f} kg"
            if weight_change is not None else "-"
        )
        
    st.header("分析")
    tab1, tab2, tab3 = st.tabs(
        ["サマリー", "食事分析", "体重分析"]
    )

    with tab1:

        col1, col2 = st.columns(2)

        with col1:
            #円グラフの作成
            if not df_meals.empty:

                st.metric(
                    "体重変化",
                    f"{end_weight:.1f} kg",
                    delta=f"{weight_change:.1f} kg"
                )

                df_pfc = pd.DataFrame({
                    "nutrient":["protein","fat","carb"],
                    "amount":[
                        total_protein,
                        total_fat,
                        total_carb
                    ]
                })

                fig = px.pie(
                    df_pfc,
                    names="nutrient",
                    values="amount",
                    title="栄養素バランス"
                )

                st.plotly_chart(
                    fig,
                    width="stretch"
                )

            else:
                st.info("食事データがありません")
        
        with col2:

            st.write("PFC集計")

            st.write(
                f"""
                Protein : {total_protein:.1f} g

                Fat : {total_fat:.1f} g

                Carb : {total_carb:.1f} g
                """
            )
   
    with tab2:

        col1, col2 = st.columns(2)

        with col1:

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
        
        with col2:
            
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

        #食事推移グラフの作成
        if not df_meals.empty:

            daily_calories = (
            df_meals.groupby("date")["calories"]
            .sum()
            .reset_index()
            )

            daily_calories = pd.DataFrame()

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

    with tab3:

        col1, col2 = st.columns(2)

        with col1:

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
    
        with col2:
            #カロリーと体重の関係分析
            #体重とカロリーを日付で結合
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
