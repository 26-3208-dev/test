import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(
    page_title="실시간 문화재 위험도 분석",
    layout="wide"
)

st.title("실시간 문화재 훼손 위험도 분석 시스템")
st.divider()

# =========================
# CSV 데이터 불러오기
# =========================
df = pd.read_csv("data/yc_heritage_detail_enriched.csv")

# =========================
# 실시간 환경 데이터 수집
# OpenWeather API 사용
# =========================

API_KEY = "여기에_본인_API_KEY_입력"

# 예시 지역 (안동)
CITY = "Andong"

url = f"""
https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric
"""

response = requests.get(url)

# API 성공 시
if response.status_code == 200:

    weather_data = response.json()

    temp = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    wind = weather_data["wind"]["speed"]
    weather = weather_data["weather"][0]["description"]

    st.subheader("실시간 환경 데이터")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("온도", f"{temp}°C")
    col2.metric("습도", f"{humidity}%")
    col3.metric("풍속", f"{wind}m/s")
    col4.metric("날씨", weather)

else:
    st.error("실시간 날씨 데이터를 가져오지 못했습니다.")

# =========================
# 실시간 위험도 계산
# =========================

def calculate_realtime_risk(row):

    score = 0

    # -------------------------
    # 온도 영향
    # -------------------------
    if temp >= 35:
        score += 30

    elif temp >= 30:
        score += 20

    # -------------------------
    # 습도 영향
    # -------------------------
    if humidity >= 80:
        score += 30

    elif humidity >= 60:
        score += 15

    # -------------------------
    # 풍속 영향
    # -------------------------
    if wind >= 10:
        score += 20

    elif wind >= 5:
        score += 10

    # -------------------------
    # 문화재 재질 영향
    # -------------------------
    if "재질" in row.index:

        material = str(row["재질"])

        if "목조" in material:
            score += 20

        elif "석조" in material:
            score += 10

    return score

# 위험도 계산
df["실시간위험점수"] = df.apply(calculate_realtime_risk, axis=1)

# 위험등급 분류
def classify(score):

    if score >= 70:
        return "매우 위험"

    elif score >= 40:
        return "위험"

    elif score >= 20:
        return "주의"

    else:
        return "양호"

df["위험등급"] = df["실시간위험점수"].apply(classify)

# =========================
# 현재 상태 요약
# =========================

avg_risk = round(df["실시간위험점수"].mean(), 1)

st.subheader("현재 문화재 상태")

if avg_risk >= 70:
    st.error(f"현재 문화재 위험도가 매우 높습니다. (평균 위험점수: {avg_risk})")

elif avg_risk >= 40:
    st.warning(f"현재 문화재 훼손 위험이 높습니다. (평균 위험점수: {avg_risk})")

else:
    st.success(f"현재 문화재 상태는 비교적 안정적입니다. (평균 위험점수: {avg_risk})")

# =========================
# 위험도 TOP 10
# =========================

st.subheader("실시간 위험도 TOP 10")

top10 = df.sort_values(
    by="실시간위험점수",
    ascending=False
).head(10)

show_cols = []

for col in [
    "국가유산명",
    "국가유산종목",
    "재질",
    "실시간위험점수",
    "위험등급"
]:
    if col in top10.columns:
        show_cols.append(col)

st.dataframe(
    top10[show_cols],
    use_container_width=True
)

# =========================
# 마지막 업데이트 시간
# =========================

st.caption(
    f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)
