# app.py
import streamlit as st
from supabase import create_client, Client

# Supabase 설정
url = "https://<project_id>.supabase.co"
anon_key = "<anon_key>"
supabase: Client = create_client(url, anon_key)

# Streamlit 대시보드
st.title("공유 오피스 대시보드")
st.sidebar.header("설문 데이터")

# Supabase 데이터 가져오기
data = supabase.table("feedback").select("*").execute().data

if data:
    st.write("실시간 설문 데이터:")
    st.write(data)
    
    # 평균 만족도 계산
    import pandas as pd
    df = pd.DataFrame(data)
    avg_satisfaction = df.groupby("site_id")["satisfaction"].mean().reset_index()
    
    st.subheader("지점별 평균 만족도")
    st.bar_chart(avg_satisfaction.set_index("site_id"))
else:
    st.write("아직 설문 데이터가 없습니다.")
