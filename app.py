import streamlit as st
from supabase import create_client, Client
import pandas as pd

# Supabase 클라이언트 초기화
supabase_url = st.secrets["supabase"]["url"]
supabase_anon_key = st.secrets["supabase"]["anon_key"]

supabase: Client = create_client(supabase_url, supabase_anon_key)

# Supabase 연결 확인
try:
    supabase.table("feedback").select("*").limit(1).execute()
except Exception as e:
    st.error(f"Supabase에 연결할 수 없습니다: {e}")
    st.stop()

# Streamlit 설정
st.title("공유 오피스 대시보드")
st.write("실시간 데이터를 확인하세요!")

# Supabase 데이터 가져오기
try:
    data = supabase.table("feedback").select("*").execute().data

    if data:
        # 데이터를 Pandas DataFrame으로 변환
        df = pd.DataFrame(data)

        # 데이터 표시
        st.write("데이터:")
        st.write(df)

        # 지점별 평균 만족도 시각화
        if "site_id" in df.columns and "satisfaction" in df.columns:
            avg_satisfaction = df.groupby("site_id")["satisfaction"].mean().reset_index()
            st.subheader("지점별 평균 만족도")
            st.bar_chart(avg_satisfaction.set_index("site_id"))
        else:
            st.warning("데이터에 'site_id' 또는 'satisfaction' 컬럼이 없습니다.")
    else:
        st.write("데이터가 없습니다.")
except Exception as e:
    st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")
