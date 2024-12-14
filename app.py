import streamlit as st
import qrcode

# QR 코드 생성
def generate_qr(link, file_name="qr_code.png"):
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

# QR 코드 생성 및 표시
generate_qr("https://sharedofficedashboard-qgz4njnzvj7hcgvo2lsibq.streamlit.app/survey", "qr_code.png")

st.title("공유 오피스 대시보드")
st.sidebar.image("qr_code.png", caption="QR 코드를 스캔하여 설문에 참여하세요!")
st.write("대시보드를 보려면 왼쪽의 설문 QR 코드를 스캔하고 데이터를 입력하세요!")
