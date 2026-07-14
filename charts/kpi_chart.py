import streamlit as st

from models import Goal

#kpi
def create_kpi(
        session,
        df_meals,
        df_weights,
):
    
    # 総摂取カロリー
    total_calories = df_meals["calories"].sum()

    # 平均体重
    average_weight = (
        df_weights["weight"].mean()
        if not df_weights.empty
        else None
    )

    # 記録日数
    record_days = len(df_weights)

    # 体重変化
    end_weight = None
    weight_change = None

    if not df_weights.empty:
        start_weight = df_weights["weight"].iloc[0]
        end_weight = df_weights["weight"].iloc[-1]
        weight_change = end_weight - start_weight
    
    #目標体重
    goal = session.query(Goal).first()
    remaining = None

    if goal and not df_weights.empty:
        current_weight = df_weights["weight"].iloc[-1]
        remaining = current_weight - goal.target_weight

    st.subheader("健康サマリー")

    col1, col2, col3, col4 ,col5 = st.columns(5)

    with col1:
        st.metric(
            "総摂取カロリー",
            f"{total_calories:.0f} kcal"
        )

    with col2:
        st.metric(
            "平均体重",
            f"{average_weight:.1f} kg"
            if average_weight is not None
            else "-"
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
            if end_weight is not None
            else "-",
            delta=(
                f"{weight_change:+.1f} kg"
                if weight_change is not None
                else "-"
            )
        )
    
    with col5:
        st.metric(
        "目標まで",
        f"{remaining:.1f} kg"
        if remaining is not None
        else "-"
    )