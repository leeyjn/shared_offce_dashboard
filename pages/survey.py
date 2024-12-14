import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Firebase 설정
firebase_config = st.secrets["FIREBASE_CONFIG"]  # Streamlit secrets에서 Firebase 설정 읽기
cred = credentials.Certificate(firebase_config)  # secrets 내용을 직접 전달
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://shareoffice-dashboard-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# 설문 UI
st.title("공유 오피스 설문 양식")
site_id = st.selectbox("지점을 선택하세요", [1, 2, 3])
satisfaction = st.slider("만족도를 입력하세요 (1~10)", 1, 10, 5)
day = st.number_input("체험 일차 (1~3)", min_value=1, max_value=3, step=1)

if st.button("제출"):
    ref = db.reference("feedback")  # Firebase Realtime Database의 'feedback' 참조
    ref.push({
        "site_id": site_id,
        "satisfaction": satisfaction,
        "day": day
    })
    st.success("설문이 제출되었습니다. 감사합니다!")
