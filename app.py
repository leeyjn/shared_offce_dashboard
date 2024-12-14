import streamlit as st
import os
import json
import firebase_admin
from firebase_admin import credentials, db
import qrcode

# Firebase 초기화
firebase_key = os.getenv("FIREBASE_CONFIG")  # 환경 변수에서 키를 가져옴
if not firebase_key:
    st.error("Firebase 환경 변수가 설정되지 않았습니다!")
    st.stop()

# JSON 키를 환경 변수에서 로드
firebase_config = json.loads(firebase_key)
cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://shareoffice-dashboard-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# QR 코드 생성 함수
def generate_qr(link, file_name="feedback_qr.png"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_name)

# QR 코드 생성
generate_qr("https://sharedofficedashboard.streamlit.app/pages/survey", "feedback_qr.png")

# Streamlit 시작
st.set_page_config(page_title="공유 오피스 대시보드", layout="wide")
st.sidebar.image("feedback_qr.png", caption="QR 코드를 스캔하여 설문에 참여하세요!")

st.title("공유 오피스 대시보드")
st.write("왼쪽 QR 코드를 스캔하여 설문을 진행하세요.")
st.write("실시간 설문 결과는 대시보드에서 확인할 수 있습니다.")
