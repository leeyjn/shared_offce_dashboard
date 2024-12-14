import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image
import qrcode
import plotly.graph_objects as go

# SQLite 연결
conn = sqlite3.connect("feedback.db")
c = conn.cursor()

# 데이터베이스 테이블 확인 및 생성
c.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY,
        site_id INTEGER,
        satisfaction INTEGER,
        day INTEGER
    )
''')
conn.commit()

# QR 코드 생성 함수
def generate_qr(link):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

# Streamlit 앱 구성
st.title("공유 오피스 대시보드")
st.sidebar.title("QR 코드 안내")

# QR 코드 생성 및 표시
survey_link = "https://sharedofficedashboard-qgz4njnzvj7hcgvo2lsibq.streamlit.app/survey"
qr_img = generate_qr(survey_link)
st.sidebar.image(qr_img, caption="QR 코드를 스캔하여 설문에 참여하세요!")

# 데이터 로드
def load_feedback():
    query = "SELECT site_id, satisfaction, day FROM feedback"
    df = pd.read_sql(query, conn)
    return df

feedback_data = load_feedback()

# 데이터가 있을 때만 시각화
if not feedback_data.empty:
    st.subheader("지점별 평균 만족도")
    site_avg = feedback_data.groupby("site_id")["satisfaction"].mean().reset_index()
    st.bar_chart(site_avg.set_index("site_id"))

    st.subheader("체험 일차별 평균 만족도")
    day_avg = feedback_data.groupby("day")["satisfaction"].mean().reset_index()
    st.line_chart(day_avg.set_index("day"))

    st.subheader("실시간 데이터")
    st.write(feedback_data)

# 변동성 강조 (Plotly)
st.subheader("만족도 변동성 시각화")
if not feedback_data.empty:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=feedback_data["day"], 
        y=feedback_data["satisfaction"],
        mode="lines+markers",
        name="만족도"
    ))
    st.plotly_chart(fig)
