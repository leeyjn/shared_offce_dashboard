import streamlit as st
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials

# Firebase 초기화
cred = credentials.Certificate("C:\Users\pc\Python_Projects\shared_office_dashboard\serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# 설문 양식 UI
st.title("공유 오피스 설문 양식")
st.write("QR 코드를 스캔한 후 설문을 완료해주세요.")

site_id = st.selectbox("지점을 선택하세요", [1, 2, 3])
satisfaction = st.slider("만족도를 입력하세요 (1~10)", 1, 10, 5)
day = st.number_input("체험 일차 (1~3)", min_value=1, max_value=3, step=1)

if st.button("제출"):
    # 데이터 Firestore에 추가
    data = {
        "site_id": site_id,
        "satisfaction": satisfaction,
        "day": day
    }
    db.collection("feedback").add(data)
    st.success("감사합니다! 설문이 저장되었습니다.")
