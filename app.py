import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(
    page_title="문화재 훼손 위험도 분석",
    layout="wide"
)

st.title("문화재 훼손 위험도 분석 시스템")
st.divider()

# =========================
# 데이터 불러오기
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("data/yc_heritage_detail_enriched.csv")

df = load_data()

# =========================
# 원본 데이터 출력
# =========================
st.subheader("원본 데이터")
st.dataframe(df, use_container_width=True)

# =========================
# 컬럼 확인
# =========================
st.subheader("데이터 컬럼")
st.write(df.columns.tolist())

# =========================
# 위험도 계산 함수
# =========================
def calculate_risk_score(row):

    score = 0

    # -------------------------
    # 1. 훼손 정도 기반 점수
    # -------------------------
    if "훼손정도" in row.index:

        damage = str(row["훼손정도"])

        if "심각" in damage:
            score += 50

        elif "중간" in damage:
            score += 30

        elif "경미" in damage:
            score += 10

    # -------------------------
    # 2. 경과 연수 기반 점수
    # -------------------------
    if "건립년도" in row.index:

        try:
            current_year = pd.Timestamp.now().year
            built_year = int(row["건립년도"])

            age = current_year - built_year

            # 오래될수록 위험 증가
            score += min(age / 5, 30)

        except:
            pass

    # -------------------------
    # 3. 재질 기반 점수
    # -------------------------
    if "재질" in row.index:

        material = str(row["재질"])

        if "목조" in material:
            score += 20

        elif "석조" in material:
            score += 10

        elif "금속" in material:
            score += 5

    # -------------------------
    # 4. 관리상태 기반 점수
    # -------------------------
    if "관리상태" in row.index:

        condition = str(row["관리상태"])

        if "불량" in condition:
            score += 30

        elif "보통" in condition:
            score += 15

        elif "양호" in condition:
            score += 5

    return round(score, 1)

# =========================
# 위험도 계산
# =========================
st.subheader("문화재 위험도 계산")

df["위험점수"] = df.apply(calculate_risk_score, axis=1)

# 위험등급 분류
def classify_risk(score):

    if score >= 80:
        return "매우 위험"

    elif score >= 50:
        return "위험"

    elif score >= 30:
        return "주의"

    else:
        return "양호"

df["위험등급"] = df["위험점수"].apply(classify_risk)

# =========================
# 결과 출력
# =========================
st.subheader("위험도 분석 결과")

result_cols = []

for col in [
    "국가유산명",
    "국가유산종목",
    "위험점수",
    "위험등급"
]:
    if col in df.columns:
        result_cols.append(col)

st.dataframe(
    df[result_cols].sort_values(
        by="위험점수",
        ascending=False
    ),
    use_container_width=True
)

# =========================
# 위험등급 분포
# =========================
st.subheader("위험등급 분포")

risk_count = (
    df["위험등급"]
    .value_counts()
    .reset_index()
)

risk_count.columns = ["위험등급", "건수"]

chart = alt.Chart(risk_count).mark_bar().encode(
    x=alt.X("위험등급", sort=None),
    y="건수",
    tooltip=["위험등급", "건수"]
).properties(
    width=700,
    height=400
)

st.altair_chart(chart, use_container_width=True)

# =========================
# 국가유산종목별 분포
# =========================
if "국가유산종목" in df.columns:

    st.subheader("국가유산종목별 분포")

    heritage_count = (
        df["국가유산종목"]
        .value_counts()
        .reset_index()
    )

    heritage_count.columns = ["국가유산종목", "건수"]

    st.dataframe(
        heritage_count,
        use_container_width=True
    )

    st.bar_chart(
        heritage_count.set_index("국가유산종목")
    )

# =========================
# 위험도 TOP 10
# =========================
st.subheader("위험도 TOP 10 문화재")

top10 = df.sort_values(
    by="위험점수",
    ascending=False
).head(10)

show_cols = []

for col in [
    "국가유산명",
    "국가유산종목",
    "위험점수",
    "위험등급"
]:
    if col in top10.columns:
        show_cols.append(col)

st.dataframe(
    top10[show_cols],
    use_container_width=True
)

# =========================
# 평균 위험도
# =========================
st.subheader("전체 평균 위험도")

avg_score = round(df["위험점수"].mean(), 2)

st.metric(
    label="평균 위험 점수",
    value=avg_score
)
