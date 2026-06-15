import streamlit as st
import pandas as pd

st.set_page_config(page_title="문화재 훼손 예측")

st.title("문화재 훼손 현황")
st.divider()

# 데이터 불러오기
df = pd.read_csv("data/yc_heritage_detail_enriched.csv")

# 원본 데이터
st.subheader("원본 데이터")
st.dataframe(df)

# 컬럼 확인
st.subheader("데이터 컬럼")
st.write(df.columns.tolist())

# 국가유산종목별 시각화
if "국가유산종목" in df.columns:

    st.subheader("국가유산종목별 분포")

    heritage_count = (
        df["국가유산종목"]
        .value_counts()
        .reset_index()
    )

    heritage_count.columns = ["국가유산종목", "건수"]

    st.dataframe(heritage_count)

    # 막대그래프
    st.bar_chart(
        heritage_count.set_index("국가유산종목")
    )

    # 원형 차트용 데이터
    st.subheader("종목별 비율")

    st.dataframe(
        heritage_count.style.format({"건수": "{:,}"})
    )

else:
    st.error("'국가유산종목' 컬럼을 찾을 수 없습니다.")
