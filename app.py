import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Firebase 초기화
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["FIREBASE_CONFIG"])
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://shareoffice-dashboard-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# Streamlit 대시보드 시작
st.set_page_config(page_title="공유 오피스 대시보드", layout="wide")

st.title("공유 오피스 대시보드")
st.write("QR 코드를 사용하여 설문을 제출하고, 결과를 실시간으로 확인하세요.")

# 데이터베이스에서 데이터 가져오기
ref = db.reference('feedback')
data = ref.get()

if data:
    feedback_data = [{"site_id": key, **value} for key, value in data.items()]
else:
    feedback_data = []

st.write("실시간 설문 데이터:")
st.write(feedback_data)

# 데이터 시각화
st.subheader("지점별 평균 만족도")
if feedback_data:
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.DataFrame(feedback_data)
    avg_satisfaction = df.groupby("site_id")["satisfaction"].mean().reset_index()
    st.bar_chart(avg_satisfaction.set_index("site_id"))
else:
    st.write("설문 데이터가 없습니다.")

st.sidebar.image("feedback_qr.png", caption="QR 코드를 스캔하여 설문에 참여하세요!")
