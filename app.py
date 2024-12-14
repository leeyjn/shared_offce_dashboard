import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import qrcode
from PIL import Image

# Firebase 설정
firebase_config = st.secrets["FIREBASE_CONFIG"]  # secrets에서 Firebase 설정 가져오기
cred = credentials.Certificate(firebase_config)  # JSON 문자열을 직접 전달
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
    return file_name

# Streamlit 페이지 설정
st.set_page_config(page_title="공유 오피스 대시보드", layout="wide")

# 설문 페이지 URL로 QR 코드 생성
survey_link = "https://sharedofficedashboard-5rh9g5yyyfpszwi4cvbxax.streamlit.app/survey"
qr_file = generate_qr(survey_link)

# 대시보드 제목
st.title("공유 오피스 대시보드")
st.write("실시간 설문 데이터를 확인하세요!")

# 데이터베이스에서 데이터 가져오기
ref = db.reference('feedback')
data = ref.get()

if data:
    import pandas as pd
    st.write("실시간 설문 데이터:")
    feedback_data = [{"site_id": key, **value} for key, value in data.items()]
    st.write(feedback_data)

    # 지점별 평균 만족도 시각화
    st.subheader("지점별 평균 만족도")
    df = pd.DataFrame(feedback_data)
    avg_satisfaction = df.groupby("site_id")["satisfaction"].mean().reset_index()
    st.bar_chart(avg_satisfaction.set_index("site_id"))
else:
    st.write("설문 데이터가 없습니다.")

# QR 코드 표시
st.sidebar.image(qr_file, caption="QR 코드를 스캔하여 설문에 참여하세요!", use_column_width=True)
