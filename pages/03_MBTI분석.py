import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="세계 MBTI 분석",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# 제목
# -----------------------------
st.title("🌍 국가별 MBTI 비율 분석")
st.markdown("국가를 선택하면 MBTI 비율을 인터랙티브하게 확인할 수 있습니다.")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# -----------------------------
# 국가 선택
# -----------------------------
countries = sorted(df["Country"].unique())

selected_country = st.selectbox(
    "국가를 선택하세요",
    countries
)

# -----------------------------
# 선택 국가 데이터
# -----------------------------
country_data = df[df["Country"] == selected_country]

# MBTI 컬럼만 추출
mbti_columns = [
    'INTJ', 'INTP', 'ENTJ', 'ENTP',
    'INFJ', 'INFP', 'ENFJ', 'ENFP',
    'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ',
    'ISTP', 'ISFP', 'ESTP', 'ESFP'
]

values = country_data[mbti_columns].iloc[0]

chart_df = pd.DataFrame({
    "MBTI": mbti_columns,
    "비율": values.values
})

# -----------------------------
# 1등 MBTI 찾기
# -----------------------------
top_mbti = chart_df.loc[chart_df["비율"].idxmax(), "MBTI"]

# 색상 설정
chart_df["색상"] = chart_df["MBTI"].apply(
    lambda x: "TOP" if x == top_mbti else "NORMAL"
)

# -----------------------------
# 그래프
# -----------------------------
fig = px.bar(
    chart_df,
    x="MBTI",
    y="비율",
    color="색상",
    text="비율",
    color_discrete_map={
        "TOP": "#ff0000",      # 빨간색
        "NORMAL": "#3b82f6"   # 파란색
    }
)

# 그래프 꾸미기
fig.update_traces(
    texttemplate='%{text:.2f}%',
    textposition='outside',
    marker_line_width=0
)

fig.update_layout(
    height=650,
    showlegend=False,
    template="plotly_white",
    title={
        "text": f"{selected_country} MBTI 비율",
        "x": 0.5,
        "xanchor": "center"
    },
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (%)",
    font=dict(
        family="Arial",
        size=15
    )
)

# 파란색 그라데이션 느낌 추가
fig.update_traces(
    marker=dict(
        line=dict(color='rgba(0,0,0,0)', width=0)
    )
)

# -----------------------------
# 그래프 출력
# -----------------------------
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# TOP MBTI 정보
# -----------------------------
st.subheader("🏆 가장 높은 MBTI")

top_value = chart_df["비율"].max()

st.success(
    f"{selected_country}에서 가장 높은 MBTI는 "
    f"'{top_mbti}' ({top_value:.2f}%) 입니다."
)

# -----------------------------
# 데이터 테이블
# -----------------------------
with st.expander("📊 데이터 보기"):
    st.dataframe(
        chart_df[["MBTI", "비율"]],
        use_container_width=True
    )
