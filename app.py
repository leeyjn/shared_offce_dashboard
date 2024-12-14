import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import plotly.express as px

# Firebase 설정
cred = credentials.Certificate(st.secrets["FIREBASE_CONFIG"])  # secrets에서 Firebase 설정 가져오기
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://shareoffice-dashboard-default-rtdb.asia-southeast1.firebasedatabase.app/'  # 본인의 Firebase Realtime Database URL
})

# Streamlit 페이지 설정
st.set_page_config(page_title="공유 오피스 대시보드", layout="wide")

st.title("공유 오피스 대시보드")
st.write("실시간 설문 데이터를 시각화합니다.")

# 데이터베이스에서 데이터 가져오기
ref = db.reference('feedback')
data = ref.get()

# 데이터 처리 및 시각화
if data:
    feedback_data = [{"site_id": key, **value} for key, value in data.items()]
    st.write("실시간 설문 데이터:")
    st.write(feedback_data)

    # 데이터 프레임 생성
    df = pd.DataFrame(feedback_data)

    # 지점별 평균 만족도
    st.subheader("지점별 평균 만족도")
    avg_satisfaction = df.groupby("site_id")["satisfaction"].mean().reset_index()
    if not avg_satisfaction.empty:
        fig = px.bar(avg_satisfaction, x="site_id", y="satisfaction", title="지점별 평균 만족도")
        st.plotly_chart(fig)
    else:
        st.write("설문 데이터가 없습니다.")
else:
    st.write("설문 데이터가 없습니다.")

# QR 코드 표시
try:
    st.sidebar.image("feedback_qr.png", caption="QR 코드를 스캔하여 설문에 참여하세요!")
except FileNotFoundError:
    st.sidebar.write("QR 코드 이미지 파일을 찾을 수 없습니다.")
