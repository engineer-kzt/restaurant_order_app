import streamlit as st


# セッション状態
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# =====画面構成====
# 画面構成【1】-Home
if st.session_state["page"] == "home":
    st.title("FOOD-MENU")
