import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Firebase 설정
firebase_config = st.secrets["FIREBASE_CONFIG"]  # secrets에서 Firebase 설정 가져오기
if not firebase_admin._apps:  # 중복 초기화 방지
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://shareoffice-dashboard-default-rtdb.asia-southeast1.firebasedatabase.app/'
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

    # 데이터 시각화
    st.subheader("지점별 평균 만족도")
    import pandas as pd

    df = pd.DataFrame(feedback_data)
    avg_satisfaction = df.groupby("site_id")["satisfaction"].mean().reset_index()
    st.bar_chart(avg_satisfaction.set_index("site_id"))
else:
    st.write("설문 데이터가 없습니다.")

# QR 코드 표시
st.sidebar.image("feedback_qr.png", caption="QR 코드를 스캔하여 설문에 참여하세요!")
