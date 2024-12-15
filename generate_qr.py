import qrcode

def generate_qr(link, file_name="survey_qr.png"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_name)
    print(f"QR 코드가 생성되었습니다: {file_name}")

# Typeform 설문 링크 (여기에 Typeform 설문 URL 넣기)
typeform_url = "https://nwdkhtkycyq.typeform.com/to/kPCn5Xgy"
generate_qr(typeform_url)
