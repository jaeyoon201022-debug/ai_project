import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="서울시 인구통계", layout="wide")

# 제목
st.title("서울시의 인구통계")

# CSV 파일 불러오기
df = pd.read_csv("POPULATION.csv", encoding="cp949")

# 숫자형 변환
age_columns = df.columns[1:]

for col in age_columns:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .astype(int)
    )

# 행정구 목록
districts = df["행정구역"].tolist()

# 선택 박스
selected_district = st.selectbox(
    "행정구를 선택하세요",
    districts
)

# 선택된 데이터
selected_data = df[df["행정구역"] == selected_district]

# 연령대 데이터 추출
ages = age_columns
population = selected_data.iloc[0, 1:].values

# Plotly 꺾은선 그래프
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=ages,
        y=population,
        mode="lines+markers",
        line=dict(color="red", width=3),
        marker=dict(size=8, color="red"),
        name="인구수"
    )
)

# 그래프 디자인
fig.update_layout(
    title="서울시의 인구통계",
    xaxis_title="연령대",
    yaxis_title="인구수",
    plot_bgcolor="#E6D6FF",   # 연한 보라색
    paper_bgcolor="#E6D6FF",
    font=dict(
        family="Malgun Gothic",
        size=14,
        color="black"
    ),
    title_font=dict(size=24),
    height=600
)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)
