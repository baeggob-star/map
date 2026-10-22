import streamlit as st
import pandas as pd
import folium
import math
from streamlit_folium import st_folium

# 앱 제목 설정
st.title("부산 지하철 역별 이용객 지도 분석")

# 1. CSV 파일 업로드 받기
uploaded_file = st.file_uploader("busan_subway.csv 파일을 업로드해주세요", type=['csv'])

if uploaded_file is not None:
    # CSV 파일을 데이터프레임으로 읽기
    df = pd.read_csv(uploaded_file)

    # [호선 필터] 데이터에 있는 호선 목록을 가져와서 다중 선택 메뉴 만들기
    line_list = df['호선'].unique()
    selected_lines = st.multiselect("지도에 표시할 호선을 선택하세요", line_list, default=line_list)

    # 선택한 호선에 해당하는 데이터만 남기기 (필터링)
    filtered_df = df[df['호선'].isin(selected_lines)]

    # [표] 이용객 상위 5개 역 추출 및 표시
    st.subheader("🏆 이용객 상위 5개 역")
    # 이용객수를 기준으로 내림차순 정렬 후 위에서 5개만 가져오기
    top5_df = filtered_df.sort_values(by='이용객수', ascending=False).head(5)
    st.dataframe(top5_df)

    # [색상] 호선별 색상 지정용 딕셔너리 만들기
    colors = {
        '1호선': 'orange',
        '2호선': 'green',
        '3호선': 'brown',
        '4호선': 'blue'
    }

    # folium 지도 생성 (초기 위치는 부산 중심부)
    m = folium.Map(location=[35.1795543, 129.0756416], zoom_start=11)

    # 필터링된 데이터(filtered_df)의 각 줄(역)마다 반복하며 마커 추가하기
    for i, row in filtered_df.iterrows():
        # 원의 면적이 이용객 수에 비례하도록 반지름 계산
        radius_size = math.sqrt(row['이용객수']) / 5

        # 해당 역의 호선에 맞는 색상 가져오기 (딕셔너리에 없으면 gray 지정)
        line_color = colors.get(row['호선'], 'gray')

        # CircleMarker로 지도에 원 그리기
        folium.CircleMarker(
            location=[row['위도'], row['경도']],
            radius=radius_size,
            color=line_color,  # 테두리 색상 지정
            fill=True,
            fill_color=line_color,  # 원 안쪽 색상 지정
            tooltip=row['역명'],
            popup=f"{row['호선']} 이용객: {row['이용객수']}명"
        ).add_to(m)

    # 생성한 지도를 Streamlit 화면에 출력
    st.subheader("🗺️ 이용객 분포 지도")
    st_folium(m, width=720, height=500)