import streamlit as st
import sqlite3
import qrcode
from PIL import Image

# SQLite 연결
conn = sqlite3.connect("feedback.db")
c = conn.cursor()

# 데이터베이스 테이블 확인 및 생성
c.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY,
        site_id INTEGER,
        satisfaction INTEGER,
        day INTEGER
    )
''')
conn.commit()

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
    return img

# QR 코드 생성
survey_link = "https://sharedofficedashboard-qgz4njnzvj7hcgvo2lsibq.streamlit.app/survey"
qr_image = generate_qr(survey_link)

# Streamlit 앱 구성
st.title("공유 오피스 설문 및 대시보드")
st.sidebar.title("QR 코드 안내")

# QR 코드 표시
st.sidebar.image(qr_image, caption="QR 코드를 스캔하여 설문에 참여하세요!")

# 설문 데이터 로드 및 시각화
st.subheader("설문 데이터")
query = "SELECT site_id, satisfaction, day FROM feedback"
feedback_data = pd.read_sql(query, conn)

if not feedback_data.empty:
    st.write(feedback_data)
else:
    st.write("현재 저장된 설문 데이터가 없습니다.")
