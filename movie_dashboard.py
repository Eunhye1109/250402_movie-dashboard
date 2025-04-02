import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# ✅ 한글 폰트 설정
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 기본 설정
plt.rcParams['axes.unicode_minus'] = False

try:
    # 한글 폰트 시도 (로컬용)
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.plot()  # 폰트 적용 테스트
    _ = fm.FontProperties(fname='Malgun Gothic')  # 강제 시도
    use_korean = True
except:
    # 안 되면 안전한 영어 웹 폰트로 대체
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'sans-serif']
    use_korean = False


# ✅ 데이터 불러오기
movie = np.genfromtxt('ratings.dat', delimiter='::', dtype=np.int64)
df = pd.DataFrame(movie, columns=['user_id', 'movie_id', 'rating', 'timestamp'])

# ✅ 제목
st.title("🎬 MovieLens 영화 평점 대시보드")

# ✅ 영화 ID 선택 드롭다운
movie_ids = np.unique(df['movie_id'])
selected_id = st.number_input("🎞️ 영화 ID를 입력하세요", min_value=int(df['movie_id'].min()), max_value=int(df['movie_id'].max()), step=1)


# ✅ 해당 영화의 평점 데이터 필터링
filtered = df[df['movie_id'] == selected_id]

# ✅ 평균 평점 출력
if len(filtered) > 0:
    selected_avg = filtered['rating'].mean()
    overall_avg = df['rating'].mean()

    st.subheader("⚖️ 전체 평균 vs 선택한 영화 평균 비교")

    fig2, ax2 = plt.subplots(figsize=(6, 4))

    # x축 위치를 명확히 나눔
    x_labels = ['전체 평균', '선택한 영화']
    x_pos = [0, 1]
    y_vals = [overall_avg, selected_avg]
    colors = ['blue', 'red']

    ax2.scatter(x_pos, y_vals, s=200, color=colors)

    # y축 범위 고정
    ax2.set_ylim(0, 5)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(x_labels)
    ax2.set_ylabel("평점")
    ax2.set_title("전체 평균 평점 vs 선택한 영화 평균 평점")

    # 값 표시
    for i, val in enumerate(y_vals):
        ax2.text(x_pos[i], val + 0.1, f"{val:.2f}", ha='center', fontsize=12)

    st.pyplot(fig2)

# ✅ 평점 테이블 출력
st.subheader("📋 평점 데이터 테이블")
st.dataframe(filtered)

#cmd에 cd 경로 >> streamlit run movie_dashboard.py 붙여넣기
