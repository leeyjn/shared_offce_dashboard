import streamlit as st
from supabase import create_client, Client

# Supabase 클라이언트 초기화
supabase_url = st.secrets["supabase"]["url"]
supabase_anon_key = st.secrets["supabase"]["anon_key"]

supabase: Client = create_client(supabase_url, supabase_anon_key)

# Streamlit 설정
st.title("공유 오피스 대시보드")
st.write("실시간 데이터를 확인하세요!")

# Supabase 데이터 가져오기
data = supabase.table("feedback").select("*").execute().data

if data:
    st.write("데이터:")
    st.write(data)
else:
    st.write("데이터가 없습니다.")
