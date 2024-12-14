import streamlit as st
from firebase_admin import credentials, db
import firebase_admin
import uuid  # 고유 ID 생성을 위한 라이브러리

# Firebase 초기화 (중복 초기화를 방지)
if not firebase_admin._apps:
    cred = credentials.Certificate("C:/Users/pc/Python_Projects/shared_office_dashboard/serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://shareoffice-dashboard-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# Streamlit 페이지 설정
st.title("공유 오피스 설문 양식")
st.write("QR 코드를 통해 설문 페이지에 접속하셨습니다. 아래 질문에 응답해주세요!")

# 설문 양식
site_id = st.selectbox("지점을 선택하세요", [1, 2, 3])
satisfaction = st.slider("만족도를 입력하세요 (1~10)", 1, 10, 5)
day = st.number_input("체험 일차 (1~3)", min_value=1, max_value=3, step=1)

# 설문 데이터 제출
if st.button("제출"):
    try:
        # 고유 ID 생성 및 데이터베이스에 저장
        unique_id = str(uuid.uuid4())
        ref = db.reference(f'feedback/{unique_id}')
        ref.set({
            "site_id": site_id,
            "satisfaction": satisfaction,
            "day": day
        })
        st.success("설문이 저장되었습니다. 감사합니다!")
    except Exception as e:
        st.error(f"데이터 저장 중 오류가 발생했습니다: {e}")
