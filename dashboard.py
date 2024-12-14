import streamlit as st
import pandas as pd
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials

# Firebase 초기화
cred = credentials.Certificate("C:\Users\pc\Python_Projects\shared_office_dashboard\serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Firestore 데이터 로드
def load_feedback():
    docs = db.collection("feedback").stream()
    data = [{"site_id": doc.to_dict()["site_id"],
             "satisfaction": doc.to_dict()["satisfaction"],
             "day": doc.to_dict()["day"]} for doc in docs]
    return pd.DataFrame(data)

# 대시보드 구성
st.title("공유 오피스 대시보드")

feedback_data = load_feedback()

# 지점별 평균 만족도
if not feedback_data.empty:
    st.subheader("지점별 평균 만족도")
    site_avg = feedback_data.groupby("site_id")["satisfaction"].mean().reset_index()
    st.bar_chart(site_avg.set_index("site_id"))

# 체험 일차별 만족도
if not feedback_data.empty:
    st.subheader("체험 일차별 평균 만족도")
    day_avg = feedback_data.groupby("day")["satisfaction"].mean().reset_index()
    st.line_chart(day_avg.set_index("day"))

# 전체 데이터 표시
st.subheader("전체 설문 데이터")
st.write(feedback_data)
