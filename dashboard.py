import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Firebase 초기화
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["FIREBASE_CONFIG"])
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://shareoffice-dashboard-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

st.title("공유 오피스 대시보드")

# 데이터베이스에서 데이터 가져오기
ref = db.reference('feedback')
data = ref.get()

if data:
    feedback_data = [{"site_id": key, **value} for key, value in data.items()]
else:
    feedback_data = []

# 실시간 데이터 표시
st.write("실시간 설문 데이터:")
st.write(feedback_data)

# 데이터 시각화
if feedback_data:
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.DataFrame(feedback_data)

    # 지점별 평균 만족도
    avg_satisfaction = df.groupby("site_id")["satisfaction"].mean().reset_index()
    st.subheader("지점별 평균 만족도")
    st.bar_chart(avg_satisfaction.set_index("site_id"))

    # 체험 일차별 만족도 변화
    st.subheader("체험 일차별 만족도 변화")
    day_avg = df.groupby("day")["satisfaction"].mean().reset_index()
    st.line_chart(day_avg.set_index("day"))
else:
    st.write("설문 데이터가 없습니다.")
