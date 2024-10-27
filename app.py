import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title='교육과정 찾기',page_icon='🥘')

curri_url = st.secrets["gsheets"]["curri_url"]
idea_url = st.secrets["gsheets"]["idea_url"]
conn = st.connection("gsheets", type=GSheetsConnection)
curri = conn.read(spreadsheet=curri_url, usecols=[0,1,2,3,4,5,6,7]) 
# st.write(curri.head())

idea = conn.read(spreadsheet=idea_url, usecols=[0,1]) 
# st.write(idea.head())

# 파일 읽기
# curri = pd.read_csv("data/수학과 교육과정 정리 - 교육과정합본.csv")
# idea = pd.read_csv("data/수학과 교육과정 정리 - 2022핵심아이디어.csv")

# 타이틀 설정
st.title("🥘 교육과정 찾기")
st.info("**curricurri**에 오신 것을 환영합니다. 과목별 2015개정교육과정, 2022개정교육과정을 쉽게 찾고 비교해보세요. 현재는 수학만 지원됩니다. 성취기준 상의 오류 제보 등은 여기로 해주세요! :email: sbhath17@gmail.com")

# 검색 필터 추가
st.markdown("### 교육과정 성취기준 필터링", help='개정 일시와 영역, 학교급, 과목을 선택해보세요. 선택하지 않은 경우 전체 선택으로 인식됩니다.')
revision_options = curri['개정일시'].dropna().unique().tolist()
level_options = curri['학교급'].dropna().unique().tolist()
area_options = curri['영역'].dropna().unique().tolist()
subject_options = curri['과목'].dropna().unique().tolist()

col1, col2 = st.columns(2)
with col1:
    selected_revisions = st.multiselect("개정 일시 선택", revision_options)
    selected_levels = st.multiselect("학교급 선택", level_options)
with col2:
    selected_areas = st.multiselect("영역 선택", area_options)
    selected_subjects = st.multiselect("과목 선택", subject_options)

# 키워드 검색 필드 강조
st.markdown("### 성취기준 키워드 검색", help='혹은 성취기준에 들어간 단어 위주로 검색해보세요. 해당 키워드를 가진 성취기준이 모두 검색됩니다. ')
keyword = st.text_input("키워드 검색", placeholder="검색할 키워드를 입력하세요...", key="keyword_input", max_chars=50)

# 필터 적용
st.markdown("### 성취기준 결과")

filtered_curri = curri
if selected_revisions:
    filtered_curri = filtered_curri[filtered_curri['개정일시'].isin(selected_revisions)]
if selected_levels:
    filtered_curri = filtered_curri[filtered_curri['학교급'].isin(selected_levels)]
if selected_areas:
    filtered_curri = filtered_curri[filtered_curri['영역'].isin(selected_areas)]
if selected_subjects:
    filtered_curri = filtered_curri[filtered_curri['과목'].isin(selected_subjects)]
if keyword:
    filtered_curri = filtered_curri[filtered_curri.apply(lambda row: row.astype(str).str.contains(keyword).any(), axis=1)]

# 색상 지정 함수
def color_rows(row):
    if row['개정일시'] == '2015개정':
        return ['background-color: #E9DFC8'] * len(row)  # 위의 색상
    elif row['개정일시'] == '2022개정':
        return ['background-color: #DAB6B1'] * len(row)  # 아래의 색상
    else:
        return [''] * len(row)

if "2022개정" in filtered_curri["개정일시"].unique():
    dom = filtered_curri.과목.unique()
    f_idea = idea[idea.영역.isin(dom)]

with st.expander("💡관련된 핵심아이디어 살펴보기"):
    st.dataframe(f_idea)

    

# 데이터프레임 스타일링 적용
styled_curri = filtered_curri[['개정일시', '성취기준', '학교급', '교육과정', '과목', '영역']].style.apply(lambda x: pd.Series(color_rows(x), index=x.index), axis=1)

# 메시지 출력
if filtered_curri.empty:
    st.error("조건에 맞는 교육과정이 없습니다.")
else:
    st.info(f"총 {len(filtered_curri)}개의 교육과정이 검색되었습니다. 표에 마우스를 올리면 해당 표를 다운로드, 표에서 검색, 혹은 확대해서 전체 창으로 볼 수 있습니다. ")

# 스타일링된 데이터프레임 출력
st.dataframe(styled_curri)


# 저작권 정보 추가
st.markdown("""
---
<div style="text-align: right;">
    © 2024 curricurri. All rights reserved.
    <span style="color: #1E90FF; font-weight: bold; font-size: 16px;">made by 반포고 황수빈</span>
    <a href="https://github.com/Surihub">
        <img src="https://img.shields.io/badge/github-181717?style=flat&logo=github&logoColor=white" alt="GitHub">
    </a>
</div>
""", unsafe_allow_html=True)