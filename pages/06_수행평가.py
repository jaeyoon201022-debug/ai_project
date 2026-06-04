import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="혼자 가기 좋은 서울 맛집",
    page_icon="🍜",
    layout="wide"
)

st.title("🍜 혼자 가기 좋은 서울 맛집 추천")
st.write("지역을 선택한 후 혼밥하기 좋은 맛집을 찾아보세요!")

# -----------------------------
# 맛집 데이터
# -----------------------------
data = [

    # 홍대
    ["홍대","옥동식","서울 마포구 양화로7길 44-10"],
    ["홍대","오레노라멘","서울 마포구 동막로8길 16"],
    ["홍대","윤씨밀방","서울 마포구 독막로15길 3-14"],
    ["홍대","또보겠지떡볶이집","서울 마포구 양화로19길 22-25"],
    ["홍대","우동카덴","서울 마포구 양화로7안길 2-1"],
    ["홍대","홍대부대찌개","서울 마포구 홍익로5안길 34"],
    ["홍대","신미경홍대닭갈비","서울 마포구 와우산로21길 31-10"],
    ["홍대","새마을식당 홍대서교점","서울 마포구 어울마당로 144"],
    ["홍대","돈수백 홍대점","서울 마포구 홍익로 15"],
    ["홍대","강남돼지상회 홍대점","서울 마포구 홍익로5안길 28"],

    # 성수
    ["성수","성수다락","서울 성동구 뚝섬로9길 20"],
    ["성수","스케줄 성수","서울 성동구 아차산로 104"],
    ["성수","브라이비트","서울 성동구 성수동1가 13-191"],
    ["성수","쵸리상경","서울 성동구 연무장길 33"],
    ["성수","난포 성수점","서울 성동구 서울숲4길 18"],
    ["성수","다운타우너 성수점","서울 성동구 연무장길 31"],
    ["성수","제스티살룬 성수점","서울 성동구 성수이로 18"],
    ["성수","어니언 성수","서울 성동구 아차산로9길 8"],
    ["성수","대림창고","서울 성동구 성수이로 78"],
    ["성수","소문난성수감자탕","서울 성동구 연무장길 45"],

    # 명동
    ["명동","왕비집 본점","서울 중구 명동8가길 26"],
    ["명동","명동식당 더식당","서울 중구 명동10길 36"],
    ["명동","COW&PIG 명동점","서울 중구 명동8길 38-14"],
    ["명동","명동교자 본점","서울 중구 명동10길 29"],
    ["명동","하동관 명동본점","서울 중구 명동9길 12"],
    ["명동","유가네 명동점","서울 중구 명동8나길 6"],
    ["명동","오다리집","서울 중구 명동8나길 28"],
    ["명동","만족오향족발 시청점","서울 중구 서소문로 134"],
    ["명동","명동돈가스","서울 중구 명동3길 8"],
    ["명동","유천냉면 명동점","서울 중구 명동길 26"]
]

df = pd.DataFrame(
    data,
    columns=["지역", "음식점명", "주소"]
)

# -----------------------------
# 지역 좌표
# -----------------------------
coords = {
    "홍대": [37.5563, 126.9220],
    "성수": [37.5446, 127.0557],
    "명동": [37.5636, 126.9827]
}

# -----------------------------
# 지역 선택
# -----------------------------
selected_area = st.selectbox(
    "📍 지역 선택",
    ["홍대", "성수", "명동"]
)

# 선택한 지역 데이터
filtered_df = df[df["지역"] == selected_area]

# -----------------------------
# 지도 생성
# -----------------------------
m = folium.Map(
    location=coords[selected_area],
    zoom_start=14
)

# 마커 표시
for i, row in filtered_df.iterrows():

    lat = coords[selected_area][0] + ((i % 10) * 0.001)
    lon = coords[selected_area][1] + ((i % 10) * 0.001)

    folium.Marker(
        location=[lat, lon],
        tooltip=row["음식점명"],
        popup=row["음식점명"],
        icon=folium.Icon(
            color="blue",
            icon="cutlery",
            prefix="fa"
        )
    ).add_to(m)

# 지도 출력
st.subheader(f"🗺️ {selected_area} 혼밥 맛집 지도")

st_folium(
    m,
    width=900,
    height=550
)

# -----------------------------
# 맛집 목록
# -----------------------------
st.subheader("🍴 선택 가능한 맛집")

st.dataframe(
    filtered_df[["음식점명"]],
    use_container_width=True
)

# -----------------------------
# 맛집 선택
# -----------------------------
restaurant = st.selectbox(
    "🍜 맛집 선택",
    filtered_df["음식점명"].tolist()
)

info = filtered_df[
    filtered_df["음식점명"] == restaurant
].iloc[0]

# -----------------------------
# 상세 정보
# -----------------------------
st.markdown("## 📋 맛집 상세 정보")

st.write(f"🍽️ 음식점명 : {info['음식점명']}")
st.write(f"📍 지역 : {info['지역']}")
st.write(f"🏠 주소 : {info['주소']}")

st.success("혼자 방문하기 좋은 맛집으로 추천됩니다!")
import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="혼자 가기 좋은 서울 맛집",
    page_icon="🍜",
    layout="wide"
)

st.title("🍜 혼자 가기 좋은 서울 맛집 추천 서비스")

# CSV 불러오기
df = pd.read_csv("food.csv")

# -----------------------
# 지역별 맛집 수 그래프
# -----------------------

st.subheader("📊 지역별 맛집 개수")

area_count = (
    df["지역"]
    .value_counts()
    .reset_index()
)

area_count.columns = ["지역", "맛집 수"]

fig = px.bar(
    area_count,
    x="지역",
    y="맛집 수",
    text="맛집 수",
    title="지역별 혼밥 맛집 개수",
    hover_data=["맛집 수"]
)

fig.update_layout(
    title_x=0.5,
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------
# 지역 선택
# -----------------------

st.subheader("📍 지역 선택")

selected_area = st.selectbox(
    "지역을 선택하세요",
    ["전체"] + sorted(df["지역"].unique())
)

if selected_area == "전체":
    filtered_df = df
else:
    filtered_df = df[df["지역"] == selected_area]

# -----------------------
# 지역별 맛집 그래프
# -----------------------

st.subheader("🍽️ 맛집 목록")

fig2 = px.bar(
    filtered_df,
    x="음식점명",
    title=f"{selected_area} 맛집 목록",
    hover_data=[
        "대표메뉴",
        "가격대",
        "혼밥추천이유"
    ]
)

fig2.update_layout(
    xaxis_title="음식점",
    yaxis_visible=False,
    title_x=0.5,
    height=600
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# -----------------------
# 맛집 선택
# -----------------------

restaurant = st.selectbox(
    "🍜 맛집 선택",
    filtered_df["음식점명"].tolist()
)

info = filtered_df[
    filtered_df["음식점명"] == restaurant
].iloc[0]

# -----------------------
# 상세 정보
# -----------------------

st.markdown("---")
st.subheader("📋 맛집 상세 정보")

col1, col2 = st.columns(2)

with col1:
    st.write(f"**🍽️ 음식점명** : {info['음식점명']}")
    st.write(f"**📍 지역** : {info['지역']}")
    st.write(f"**🏠 주소** : {info['주소']}")
    st.write(f"**🍜 대표 메뉴** : {info['대표메뉴']}")

with col2:
    st.write(f"**💰 가격대** : {info['가격대']}")
    st.write(f"**👤 혼밥 추천 이유** : {info['혼밥추천이유']}")
    st.write(f"**🎈 주변 놀거리** : {info['주변놀거리']}")

st.info(info["설명"])

# -----------------------
# 데이터 테이블
# -----------------------

st.subheader("📄 전체 데이터")

st.dataframe(
    filtered_df,
    use_container_width=True
)
