import streamlit as st
from streamlit_option_menu import option_menu

# 멀티 페이지 설정
st.set_page_config(page_title="공유 오피스 설문/대시보드", layout="wide")

# 사이드바 네비게이션
selected = option_menu(
    menu_title="Navigation",
    options=["설문 양식", "대시보드"],
    icons=["pencil", "bar-chart"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# 각 페이지 불러오기
if selected == "설문 양식":
    import survey
elif selected == "대시보드":
    import dashboard
