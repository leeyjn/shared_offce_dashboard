import streamlit as st
import pandas as pd
from firebase_admin import db

st.title("공유 오피스 대시보드")
st.write("실시간 데이터를 확인하세요.")

# Firebase 데이터 가져오기
ref = db.reference("feedback")  # Firebase 경로
data = ref.get()

if data:
    feedback_data = pd.DataFrame(data.values())
    st.subheader("설문 데이터")
    st.dataframe(feedback_data)

    # 지점별 평균 만족도 계산
    st.subheader("지점별 평균 만족도")
    if "site_id" in feedback_data.columns:
        site_avg = feedback_data.groupby("site_id")["satisfaction"].mean().reset_index()
        st.bar_chart(site_avg.set_index("site_id"))

    # 체험 일차별 만족도 변화
    st.subheader("체험 일차별 만족도 변화")
    if "day" in feedback_data.columns:
        day_avg = feedback_data.groupby("day")["satisfaction"].mean().reset_index()
        st.line_chart(day_avg.set_index("day"))

else:
    st.write("아직 설문 데이터가 없습니다. 설문 결과를 기다리는 중입니다.")
