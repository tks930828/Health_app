import pandas as pd
import streamlit as st

from models import Profile

def profile_page(session):

    st.subheader("プロフィール")

    profile = session.query(Profile).first()

    if profile:
        default_height = profile.height
    else:
        default_height = 170.0
    
    height = st.number_input(
        "身長(cm)",
        min_value=100.0,
        max_value=250.0,
        value=default_height,
        step=0.1
    )

    if st.button("プロフィール保存"):

        if profile:
            profile.height = height

        else:
            profile = Profile(height=height)
            session.add(profile)

        session.commit()

        st.success("プロフィールを保存しました")

        st.rerun()