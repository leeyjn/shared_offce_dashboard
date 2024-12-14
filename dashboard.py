import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Firebase 초기화
cred = credentials.Certificate("C:/Users/pc/Python_Projects/shared_office_dashboard/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://shareoffice-dashboard-default-rtdb.asia-southeast1.firebasedatabase.app'
})

st.title("지점별 대시보드")
st.sidebar.image("feedback_qr.png", caption="QR 코드를 스캔하여 설문에 참여하세요!")

# 데이터베이스에서 데이터 가져오기
ref = db.reference('feedback')
data = ref.get()

if data:
    feedback_data = [{"site_id": key, **value} for key, value in data.items()]
    st.write("설문 데이터:")
    st.write(feedback_data)
    
    # 체험 일차별 만족도 시각화
    st.subheader("체험 일차별 만족도 변화")
    import pandas as pd
    df = pd.DataFrame(feedback_data)
    day_avg = df.groupby("day")["satisfaction"].mean().reset_index()
    st.line_chart(day_avg.set_index("day"))
else:
    st.write("설문 데이터가 없습니다.")
