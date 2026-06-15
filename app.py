import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="문화재 훼손 예측")

st.title("문화재 훼손 현황")
st.divider()

# 데이터 불러오기
df = pd.read_csv("data/yc_heritage_detail_enriched.csv")

# 데이터 표시
st.subheader("원본 데이터")
st.dataframe(df)

# 국가유산종목별 개수 집계
heritage_count = (
    df["국가유산종목"]
    .value_counts()
    .reset_index()
)

heritage_count.columns = ["국가유산종목", "건수"]

# 시각화
st.subheader("국가유산종목별 분포")

fig = px.bar(
    heritage_count,
    x="국가유산종목",
    y="건수",
    color="건수",
    text="건수",
    title="국가유산종목별 문화재 수"
)

fig.update_layout(
    xaxis_title="국가유산종목",
    yaxis_title="건수",
    xaxis_tickangle=-45
)

st.plotly_chart(fig, use_container_width=True)
