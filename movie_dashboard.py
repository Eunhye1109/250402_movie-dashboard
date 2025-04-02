import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# ✅ 영문 폰트 설정
plt.rcParams['axes.unicode_minus'] = False

    # Streamlit Cloud에서 쓸 수 있는 기본 폰트 목록 중 하나로 설정
    # 예: DejaVu Sans, Arial, sans-serif 등
plt.rcParams['font.family'] = 'Arial'

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
    x_labels = ['Total Average', 'Selected Movie']
    x_pos = [0, 1]
    y_vals = [overall_avg, selected_avg]
    colors = ['blue', 'red']

    ax2.scatter(x_pos, y_vals, s=200, color=colors)

    # y축 범위 고정
    ax2.set_ylim(0, 5)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(x_labels)
    ax2.set_ylabel("Score")
    ax2.set_title("Total Average Score vs Selected Movie Score")

    # 값 표시
    for i, val in enumerate(y_vals):
        ax2.text(x_pos[i], val + 0.1, f"{val:.2f}", ha='center', fontsize=12)

    st.pyplot(fig2)

# ✅ 평점 테이블 출력
st.subheader("📋 Score Data Table")
st.dataframe(filtered)

#cmd에 cd 경로 >> streamlit run movie_dashboard.py 붙여넣기
