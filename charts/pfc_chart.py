import pandas as pd
import streamlit as st
import plotly.express as px

#栄養素バランス
def create_pfc_summary(
        df_meals,
):

    total_protein = df_meals["protein"].sum()
    total_fat = df_meals["fat"].sum()
    total_carb = df_meals["carb"].sum()

    st.write("PFC集計")

    st.write(
        f"""
        Protein : {total_protein:.1f} g

        Fat : {total_fat:.1f} g

        Carb : {total_carb:.1f} g
        """
    )


def create_pfc_chart(
        df_meals,
):

    if df_meals.empty:
        st.info("食事データがありません")
        return

    total_protein = df_meals["protein"].sum()
    total_fat = df_meals["fat"].sum()
    total_carb = df_meals["carb"].sum()

    df_pfc = pd.DataFrame(
        {
            "nutrient": [
                "Protein",
                "Fat",
                "Carb"
            ],
            "amount": [
                total_protein,
                total_fat,
                total_carb
            ]
        }
    )

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