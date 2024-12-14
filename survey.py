import streamlit as st
import sqlite3

# SQLite 데이터베이스 설정
conn = sqlite3.connect("feedback.db")
c = conn.cursor()

# 설문 데이터베이스 테이블 생성
c.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY,
        site_id INTEGER,
        satisfaction INTEGER,
        day INTEGER
    )
''')
conn.commit()

# 설문 양식 UI
st.title("공유 오피스 설문 양식")
st.write("QR 코드를 스캔한 후 설문을 완료해주세요.")

site_id = st.selectbox("지점을 선택하세요", [1, 2, 3])
satisfaction = st.slider("만족도를 입력하세요 (1~10)", 1, 10, 5)
day = st.number_input("체험 일차 (1~3)", min_value=1, max_value=3, step=1)

if st.button("제출"):
    # 데이터 삽입
    c.execute('INSERT INTO feedback (site_id, satisfaction, day) VALUES (?, ?, ?)', 
              (site_id, satisfaction, day))
    conn.commit()
    st.success("감사합니다! 설문이 저장되었습니다.")
