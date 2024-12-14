import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go

# 데이터베이스 연결
conn = sqlite3.connect("feedback.db")
c = conn.cursor()

# 데이터 로드
c.execute('SELECT site_id, satisfaction, day FROM feedback')
feedback_data = pd.DataFrame(c.fetchall(), columns=["site_id", "satisfaction", "day"])

# 가중치 적용 함수
def apply_weighted_satisfaction(data):
    weights = {1: 0.7, 2: 1.0, 3: 1.3}
    data["weighted_satisfaction"] = data.apply(
        lambda row: row["satisfaction"] * weights.get(row["day"], 1.0), axis=1)
    return data

if not feedback_data.empty:
    feedback_data = apply_weighted_satisfaction(feedback_data)

# 대시보드 UI
st.title("공유 오피스 대시보드")

# 지점별 평균 만족도
st.subheader("지점별 평균 만족도")
if not feedback_data.empty:
    site_avg = feedback_data.groupby("site_id")["satisfaction"].mean().reset_index()
    fig = go.Figure(data=[
        go.Bar(x=site_avg["site_id"], y=site_avg["satisfaction"], name="지점별 평균 만족도")
    ])
    st.plotly_chart(fig)

# 체험 일차별 만족도 변화
st.subheader("체험 일차별 만족도 변화")
if not feedback_data.empty:
    day_avg = feedback_data.groupby("day")["satisfaction"].mean().reset_index()
    fig = go.Figure(data=[
        go.Scatter(x=day_avg["day"], y=day_avg["satisfaction"], mode="lines+markers", name="체험 일차별 만족도")
    ])
    st.plotly_chart(fig)

# 실시간 집계 데이터
st.subheader("실시간 집계 데이터")
st.write(feedback_data)
