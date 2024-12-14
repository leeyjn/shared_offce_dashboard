import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Firebase 초기화
if not firebase_admin._apps:
    cred = credentials.Certificate("C:/Users/pc/Python_Projects/shared_office_dashboard/serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://shareoffice-dashboard-default-rtdb.asia-southeast1.firebasedatabase.app'
    })

st.title("공유 오피스 설문 양식")
st.write("QR 코드를 스캔한 후 설문을 완료해주세요.")

site_id = st.selectbox("지점을 선택하세요", [1, 2, 3])
satisfaction = st.slider("만족도를 입력하세요 (1~10)", 1, 10, 5)
day = st.number_input("체험 일차 (1~3)", min_value=1, max_value=3, step=1)

if st.button("제출"):
    # 데이터베이스에 데이터 추가
    ref = db.reference('feedback')
    new_feedback = {
        "site_id": site_id,
        "satisfaction": satisfaction,
        "day": day
    }
    ref.push(new_feedback)
    st.success("감사합니다! 설문이 저장되었습니다.")
