import streamlit as st

from models import Goal

def create_goal_progress(
        session,
        df_weights
):

    # 目標達成進捗バー
    goal = session.query(Goal).first()

    progress = None

    if goal and not df_weights.empty:

        start_weight = df_weights["weight"].iloc[0]
        current_weight = df_weights["weight"].iloc[-1]
        target_weight = goal.target_weight

    #進捗率の計算
    if start_weight != target_weight:

        progress = (
            (start_weight - current_weight)
            /
            (start_weight - target_weight)
        )

    progress = max(0, min(progress, 1))

    st.subheader("目標達成率")

    if progress is not None:

        st.progress(progress)

        st.write(f"{progress * 100:.1f}% 達成")

    else:

        st.info("目標体重を登録すると表示されます。")