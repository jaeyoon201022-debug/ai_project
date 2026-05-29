# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="날짜별 기온분석", layout="wide")

# 제목
st.title("날짜별 기온분석")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("seoul.csv", encoding="cp949")

    # 날짜 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"],
        errors="coerce"
    )

    # 날짜 오류 제거
    df = df.dropna(subset=["날짜"])

    # 연도, 월, 일 컬럼 생성
    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df

df = load_data()

# 월 선택
month = st.selectbox(
    "월을 선택하세요",
    sorted(df["월"].unique())
)

# 일 선택
day = st.selectbox(
    "일을 선택하세요",
    sorted(df[df["월"] == month]["일"].unique())
)

# 선택된 날짜 데이터
filtered_df = df[
    (df["월"] == month) &
    (df["일"] == day)
]

# 연도 기준 정렬
filtered_df = filtered_df.sort_values("연도")

# 그래프 생성
fig = go.Figure()

# 최고기온
fig.add_trace(
    go.Scatter(
        x=filtered_df["연도"],
        y=filtered_df["최고기온(℃)"],
        mode="lines+markers",
        name="최고기온",
        line=dict(color="hotpink", width=3)
    )
)

# 최저기온
fig.add_trace(
    go.Scatter(
        x=filtered_df["연도"],
        y=filtered_df["최저기온(℃)"],
        mode="lines+markers",
        name="최저기온",
        line=dict(color="lightblue", width=3)
    )
)

# 그래프 레이아웃
fig.update_layout(
    title="날짜별 기온분석",
    xaxis_title="연도",
    yaxis_title="온도(℃)",
    legend_title="범례",
    template="plotly_white",
    height=600
)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)

# 데이터 표 출력
st.subheader(f"{month}월 {day}일 기온 데이터")

st.dataframe(
    filtered_df[
        ["연도", "최고기온(℃)", "최저기온(℃)"]
    ].reset_index(drop=True)
)
