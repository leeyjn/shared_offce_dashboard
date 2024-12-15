# generate_qr.py
import qrcode

def generate_qr(link, file_name="survey_qr.png"):
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

if __name__ == "__main__":
    # Typeform 설문 링크
    survey_link = "https://typeform.com/to/<form_id>"
    generate_qr(survey_link)
    print(f"QR 코드가 {survey_link} 링크로 생성되었습니다.")
