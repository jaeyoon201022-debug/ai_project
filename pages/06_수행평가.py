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
st.write("지역을 선택하고 혼밥하기 좋은 맛집을 찾아보세요!")

# 데이터
restaurants = {
    "홍대": [
        ["옥동식", "서울 마포구 양화로7길 44-10", "합정역", "돼지곰탕", "바 테이블이 있어 혼밥하기 편함", "홍대 걷고싶은거리"],
        ["오레노라멘", "서울 마포구 동막로8길 16", "합정역", "돈코츠라멘", "혼자 방문하는 손님이 많음", "연남동 카페거리"],
        ["윤씨밀방", "서울 마포구 독막로15길 3-14", "상수역", "함박스테이크", "1인 손님 방문 많음", "홍대 버스킹 거리"]
    ],
    "성수": [
        ["성수다락", "서울 성동구 뚝섬로9길 20", "성수역", "오므라이스", "조용한 분위기", "서울숲"],
        ["난포 성수점", "서울 성동구 서울숲4길 18", "서울숲역", "강된장쌈밥", "혼밥 손님 많음", "서울숲"],
        ["어니언 성수", "서울 성동구 아차산로9길 8", "성수역", "베이커리", "혼자 카페 이용 가능", "성수 카페거리"]
    ],
    "명동": [
        ["명동교자", "서울 중구 명동10길 29", "명동역", "칼국수", "회전율이 높음", "명동 쇼핑거리"],
        ["하동관", "서울 중구 명동9길 12", "을지로입구역", "곰탕", "혼밥 손님 많음", "명동성당"],
        ["왕비집", "서울 중구 명동8가길 26", "명동역", "한우구이", "1인 식사 가능", "남산타워"]
    ]
}

# 지역 좌표
coords = {
    "홍대": [37.5563, 126.9220],
    "성수": [37.5446, 127.0557],
    "명동": [37.5636, 126.9827]
}

# 지역 선택
area = st.selectbox(
    "📍 지역 선택",
    ["홍대", "성수", "명동"]
)

# 데이터프레임
df = pd.DataFrame(
    restaurants[area],
    columns=[
        "음식점명",
        "주소",
        "가까운역",
        "대표메뉴",
        "혼밥추천이유",
        "주변놀거리"
    ]
)

# 지도 생성
m = folium.Map(
    location=coords[area],
    zoom_start=14
)

# 맛집 마커 표시
for i, row in df.iterrows():

    # 맛집마다 약간씩 위치 다르게
    lat = coords[area][0] + (i * 0.001)
    lon = coords[area][1] + (i * 0.001)

    folium.Marker(
        location=[lat, lon],
        popup=row["음식점명"],
        tooltip=row["음식점명"],
        icon=folium.Icon(color="blue")
    ).add_to(m)

st.subheader(f"🗺️ {area} 맛집 지도")

st_folium(
    m,
    width=900,
    height=500
)

# 맛집 선택
restaurant = st.selectbox(
    "🍽️ 맛집 선택",
    df["음식점명"].tolist()
)

selected = df[df["음식점명"] == restaurant].iloc[0]

st.markdown("---")
st.markdown(f"## 🍜 {selected['음식점명']}")

st.write(f"📍 주소 : {selected['주소']}")
st.write(f"🚇 가까운 역 : {selected['가까운역']}")
st.write(f"🍴 대표 메뉴 : {selected['대표메뉴']}")

st.info(selected["혼밥추천이유"])

st.success(f"🎈 주변 놀거리 : {selected['주변놀거리']}")
