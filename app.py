import streamlit as st
import pandas as pd
import sqlite3
import qrcode
from sklearn.ensemble import GradientBoostingClassifier
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# SQLite 데이터베이스 설정
conn = sqlite3.connect("feedback.db")
c = conn.cursor()

# 데이터베이스 테이블 생성
c.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY,
        site_id INTEGER,
        satisfaction INTEGER,
        day INTEGER
    )
''')
conn.commit()

# 데이터 삽입 함수
def insert_feedback(site_id, satisfaction, day):
    c.execute('INSERT INTO feedback (site_id, satisfaction, day) VALUES (?, ?, ?)', 
              (site_id, satisfaction, day))
    conn.commit()

# 데이터 로드 함수
def load_feedback():
    c.execute('SELECT site_id, satisfaction, day FROM feedback')
    return c.fetchall()

# QR 코드 생성 함수
def generate_qr(link, file_name="qr_code.png"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_name)

# QR 코드 생성
generate_qr("http://example.com/feedback-form", "feedback_qr.png")

# Streamlit 시작
st.set_page_config(page_title="공유 오피스 대시보드", layout="wide")

# 피드백 입력 섹션
st.sidebar.title("만족도 입력")
site_id = st.sidebar.selectbox("지점을 선택하세요", [1, 2, 3])
satisfaction = st.sidebar.slider("만족도를 입력하세요 (1~10)", 1, 10, 5)
day = st.sidebar.number_input("체험 일차 (1~3)", min_value=1, max_value=3, step=1)
if st.sidebar.button("제출"):
    insert_feedback(site_id, satisfaction, day)
    st.sidebar.success("만족도가 저장되었습니다!")

# 데이터 로드
feedback_data = pd.DataFrame(load_feedback(), columns=["site_id", "satisfaction", "day"])

# 가중치 적용
def apply_weighted_satisfaction(data):
    weights = {1: 0.7, 2: 1.0, 3: 1.3}  # 체험 일차별 가중치 설정
    data["weighted_satisfaction"] = data.apply(
        lambda row: row["satisfaction"] * weights.get(row["day"], 1.0), axis=1)
    return data

if not feedback_data.empty:
    feedback_data = apply_weighted_satisfaction(feedback_data)

# 대시보드: 지점별 만족도 평균
st.title("공유 오피스 대시보드")
col1, col2 = st.columns(2)

with col1:
    st.subheader("지점별 평균 만족도")
    site_avg = feedback_data.groupby("site_id")["satisfaction"].mean().reset_index()
    st.bar_chart(site_avg.set_index("site_id"))

with col2:
    st.subheader("체험 일차별 만족도 변화")
    day_avg = feedback_data.groupby("day")["satisfaction"].mean().reset_index()
    st.line_chart(day_avg.set_index("day"))

# 실시간 집계 데이터
st.subheader("실시간 집계 데이터")
st.write(feedback_data)

# 유료 전환 예측 모델
if not feedback_data.empty:
    st.subheader("전환 가능성 예측")

    # 가상 예측 모델링 데이터 준비
    X = feedback_data[["site_id", "weighted_satisfaction", "day"]]
    y = (feedback_data["satisfaction"] > 7).astype(int)  # 가상 전환 여부 데이터 생성

    # 모델 학습
    model = GradientBoostingClassifier()
    model.fit(X, y)

    # 예측
    feedback_data["conversion_prob"] = model.predict_proba(X)[:, 1]

    # 결과 시각화
    st.write("예측된 전환 가능성")
    st.dataframe(feedback_data[["site_id", "satisfaction", "day", "weighted_satisfaction", "conversion_prob"]])

    # 변동성 강조 그래프
    st.subheader("만족도 변동성 시각화")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=feedback_data["day"], 
        y=feedback_data["weighted_satisfaction"],
        mode="lines+markers", 
        name="가중 만족도"))
    st.plotly_chart(fig)

# QR 코드 표시
st.sidebar.image("feedback_qr.png", caption="QR 코드를 스캔하여 피드백을 입력하세요!")
