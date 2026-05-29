# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np

# 페이지 설정
st.set_page_config(
    page_title="날짜별 기온분석",
    layout="wide"
)

# 제목
st.title("날짜별 기온분석")

# 데이터 불러오기
@st.cache_data
def load_data():

    df = pd.read_csv(
        "seoul.csv",
        encoding="cp949"
    )

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

# -----------------------------
# 월 / 일 선택
# -----------------------------
month = st.selectbox(
    "월 선택",
    sorted(df["월"].unique())
)

day = st.selectbox(
    "일 선택",
    sorted(
        df[df["월"] == month]["일"].unique()
    )
)

# -----------------------------
# 미래 연도 선택
# -----------------------------
future_year = st.number_input(
    "예측할 미래 연도를 입력하세요",
    min_value=int(df["연도"].max() + 1),
    max_value=3000,
    value=int(df["연도"].max() + 1)
)

# -----------------------------
# 선택된 날짜 데이터
# -----------------------------
filtered_df = df[
    (df["월"] == month) &
    (df["일"] == day)
]

filtered_df = filtered_df.sort_values("연도")

# -----------------------------
# 머신러닝 예측
# -----------------------------
X = filtered_df[["연도"]]

# 최고기온 모델
y_max = filtered_df["최고기온(℃)"]

max_model = LinearRegression()
max_model.fit(X, y_max)

pred_max = max_model.predict(
    [[future_year]]
)[0]

# 최저기온 모델
y_min = filtered_df["최저기온(℃)"]

min_model = LinearRegression()
min_model.fit(X, y_min)

pred_min = min_model.predict(
    [[future_year]]
)[0]

# -----------------------------
# 그래프 생성
# -----------------------------
fig = go.Figure()

# 최고기온
fig.add_trace(
    go.Scatter(
        x=filtered_df["연도"],
        y=filtered_df["최고기온(℃)"],
        mode="lines+markers",
        name="최고기온",
        line=dict(
            color="hotpink",
            width=3
        ),

        # 마우스 올렸을 때 표시
        hovertemplate=
        "연도: %{x}<br>" +
        "최고기온: %{y:.1f}℃<extra></extra>"
    )
)

# 최저기온
fig.add_trace(
    go.Scatter(
        x=filtered_df["연도"],
        y=filtered_df["최저기온(℃)"],
        mode="lines+markers",
        name="최저기온",
        line=dict(
            color="lightblue",
            width=3
        ),

        # 마우스 올렸을 때 표시
        hovertemplate=
        "연도: %{x}<br>" +
        "최저기온: %{y:.1f}℃<extra></extra>"
    )
)

# 예측 최고기온 점
fig.add_trace(
    go.Scatter(
        x=[future_year],
        y=[pred_max],
        mode="markers",
        name="예측 최고기온",
        marker=dict(
            color="red",
            size=12
        ),

        hovertemplate=
        "예측 연도: %{x}<br>" +
        "예측 최고기온: %{y:.1f}℃<extra></extra>"
    )
)

# 예측 최저기온 점
fig.add_trace(
    go.Scatter(
        x=[future_year],
        y=[pred_min],
        mode="markers",
        name="예측 최저기온",
        marker=dict(
            color="blue",
            size=12
        ),

        hovertemplate=
        "예측 연도: %{x}<br>" +
        "예측 최저기온: %{y:.1f}℃<extra></extra>"
    )
)

# -----------------------------
# 그래프 레이아웃
# -----------------------------
fig.update_layout(
    title="날짜별 기온분석",

    xaxis_title="연도",
    yaxis_title="온도(℃)",

    legend_title="범례",

    template="plotly_white",

    hovermode="x unified",

    height=650
)

# 그래프 출력
st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# 예측 결과 출력
# -----------------------------
st.subheader(f"{future_year}년 예측 결과")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "예측 최고기온",
        f"{pred_max:.1f}℃"
    )

with col2:
    st.metric(
        "예측 최저기온",
        f"{pred_min:.1f}℃"
    )

# -----------------------------
# 데이터 표 출력
# -----------------------------
st.subheader(
    f"{month}월 {day}일 실제 데이터"
)

st.dataframe(
    filtered_df[
        [
            "연도",
            "최고기온(℃)",
            "최저기온(℃)"
        ]
    ].reset_index(drop=True)
)
