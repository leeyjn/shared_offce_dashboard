import streamlit as st
import sqlite3
import qrcode
from PIL import Image
import io

# SQLite 연결
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
    
    # QR 이미지를 바이트 데이터로 변환
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

# QR 코드 생성
survey_link = "https://sharedofficedashboard-qgz4njnzvj7hcgvo2lsibq.streamlit.app/survey"
qr_image = generate_qr(survey_link)

# Streamlit 앱 구성
st.title("공유 오피스 설문 및 대시보드")
st.sidebar.title("QR 코드 안내")

# QR 코드 표시
st.sidebar.image(qr_image, caption="QR 코드를 스캔하여 설문에 참여하세요!")

# 설문 결과 데이터 로드
def load_feedback():
    c.execute('SELECT site_id, satisfaction, day FROM feedback')
    return c.fetchall()

# 설문 데이터 로드
feedback_data = load_feedback()

if feedback_data:
    import pandas as pd
    import plotly.graph_objects as go

    feedback_df = pd.DataFrame(feedback_data, columns=["site_id", "satisfaction", "day"])

    # 가중치 적용
    def apply_weighted_satisfaction(data):
        weights = {1: 0.7, 2: 1.0, 3: 1.3}  # 체험 일차별 가중치 설정
        data["weighted_satisfaction"] = data.apply(
            lambda row: row["satisfaction"] * weights.get(row["day"], 1.0), axis=1)
        return data

    feedback_df = apply_weighted_satisfaction(feedback_df)

    # 대시보드: 지점별 만족도 평균
    st.subheader("지점별 평균 만족도")
    site_avg = feedback_df.groupby("site_id")["satisfaction"].mean().reset_index()
    st.bar_chart(site_avg.set_index("site_id"))

    # 체험 일차별 만족도 변화
    st.subheader("체험 일차별 만족도 변화")
    day_avg = feedback_df.groupby("day")["satisfaction"].mean().reset_index()
    st.line_chart(day_avg.set_index("day"))

    # 유료 전환 예측 모델
    st.subheader("전환 가능성 예측")

    from sklearn.ensemble import GradientBoostingClassifier

    # 가상 예측 모델링 데이터 준비
    X = feedback_df[["site_id", "weighted_satisfaction", "day"]]
    y = (feedback_df["satisfaction"] > 7).astype(int)  # 가상 전환 여부 데이터 생성

    # 모델 학습
    model = GradientBoostingClassifier()
    model.fit(X, y)

    # 예측
    feedback_df["conversion_prob"] = model.predict_proba(X)[:, 1]

    # 결과 시각화
    st.write("예측된 전환 가능성")
    st.dataframe(feedback_df[["site_id", "satisfaction", "day", "weighted_satisfaction", "conversion_prob"]])

    # 변동성 강조 그래프
    st.subheader("만족도 변동성 시각화")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=feedback_df["day"], 
        y=feedback_df["weighted_satisfaction"],
        mode="lines+markers", 
        name="가중 만족도"))
    st.plotly_chart(fig)
else:
    st.write("현재 설문 데이터가 없습니다.")
