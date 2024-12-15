import qrcode

def generate_qr(link: str, file_name: str = "feedback_qr.png"):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_name)

# Typeform 링크에 대한 QR 코드 생성
typeform_link = "https://nwdkhtkycyq.typeform.com/to/kPCn5Xgy"
generate_qr(typeform_link)
