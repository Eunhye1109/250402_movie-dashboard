import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 로드
@st.cache_data
def load_data():
    # 현재 실행 중인 스크립트 기준으로 경로 설정
    base_path = os.path.dirname(os.path.abspath(__file__))

    df_2015 = pd.read_csv(os.path.join(base_path, "2015.csv"), encoding='utf-8')
    df_2016 = pd.read_csv(os.path.join(base_path, "2016.csv"), encoding='utf-8')
    df_2017 = pd.read_csv(os.path.join(base_path, "2017.csv"), encoding='utf-8')

    df_2015['연도'] = 2015
    df_2016['연도'] = 2016
    df_2017['연도'] = 2017
    df_all = pd.concat([df_2015, df_2016, df_2017], ignore_index=True)
    df_all['구분'] = df_all['구분'].str.strip()  # 공백 제거
    df_incident = df_all[df_all['구분'].str.contains('발생건수', na=False)]
    df_incident['총범죄'] = df_incident[['살인', '강도', '강간·강제추행', '절도', '폭력']].sum(axis=1)

    return df_incident

# 로드한 데이터 준비
df = load_data()

# 사이드바 생성
st.sidebar.title('범죄 통계 대시보드')
year = st.sidebar.selectbox('연도 선택', df['연도'].unique())
selected_df = df[df['연도'] == year]

# 연간 총범죄
total_crime_by_year = df.groupby('연도')['총범죄'].sum()

# 범죄 유형별 발생 추이
crime_trend = df.groupby('연도')[['살인', '강도', '강간·강제추행', '절도', '폭력']].sum()

# 시각화 자료 
st.title('대한민국 범죄 통계 (2015-2017)')
st.subheader('연도별 총 범죄 발생 건수')
st.bar_chart(total_crime_by_year)

st.subheader('범죄별 연도별 발생 추이')
selected_crimes = st.multiselect('보고 싶은 범죄 항목을 선택하세요', crime_trend.columns.tolist(), default=crime_trend.columns.tolist())
st.line_chart(crime_trend[selected_crimes])

st.subheader(f'{year}년 지역별 범죄 발생 비율')
selected_row = selected_df[['관서명', '살인', '강도', '강간·강제추행', '절도', '폭력']].set_index('관서명')
st.dataframe(selected_row)

# 파이 차트
st.subheader(f'{year}년 범죄 항목별 비율')

# 범죄 항목별 합계 계산 (한글 기준 먼저 정의)
total_by_type = selected_df[['살인', '강도', '강간·강제추행', '절도', '폭력']].sum()

# 한글 → 영어 매핑
labels_kor_to_eng = {
    '살인': 'Murder',
    '강도': 'Robbery',
    '강간·강제추행': 'Sexual Assault',
    '절도': 'Theft',
    '폭력': 'Violence'
}

# 영어 인덱스로 변경
total_by_type_english = total_by_type.rename(index=labels_kor_to_eng)

# 파이 차트 출력
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(
    total_by_type_english,
    autopct='%1.1f%%',
    startangle=90
)
ax.axis('equal')
ax.legend(wedges, total_by_type_english.index, title='Crime Type', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))
st.pyplot(fig)


# 로우 데이터
if st.checkbox('원본 데이터 보기'):
    st.dataframe(df)
