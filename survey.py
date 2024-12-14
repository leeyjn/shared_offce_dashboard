import streamlit as st
import sqlite3

# SQLite 연결
conn = sqlite3.connect("feedback.db")
c = conn.cursor()

# 데이터베이스 테이블 생성
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
st.title("공유 오피스 설문")
st.write("설문에 참여해주셔서 감사합니다!")

# 설문 데이터 입력
site_id = st.selectbox("지점을 선택하세요", [1, 2, 3])
satisfaction = st.slider("만족도를 입력하세요 (1~10)", 1, 10, 5)
day = st.number_input("체험 일차를 입력하세요 (1~3)", min_value=1, max_value=3, step=1)

# 제출 버튼
if st.button("제출"):
    c.execute('INSERT INTO feedback (site_id, satisfaction, day) VALUES (?, ?, ?)',
              (site_id, satisfaction, day))
    conn.commit()
    st.success("설문 데이터가 저장되었습니다!")
