```python
import streamlit as st
import pandas as pd
import requests

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

st.set_page_config(
    page_title="AI 문화재 위험도 예측",
    layout="wide"
)

st.title("AI 기반 문화재 훼손 위험도 예측")
st.divider()

# =========================
# 데이터 불러오기
# =========================

df = pd.read_csv("data/yc_heritage_detail_enriched.csv")

st.subheader("원본 데이터")
st.dataframe(df)

# =========================
# 예시 학습 데이터 생성
# 실제론 과거 센서 데이터 사용
# =========================

# 예시:
# 온도 / 습도 / 풍속 -> 실제 훼손 점수

train_df = pd.DataFrame({

    "temp": [10, 15, 20, 25, 30, 35],
    "humidity": [30, 40, 50, 60, 70, 90],
    "wind": [1, 2, 3, 5, 7, 10],

    # 실제 과거 훼손도
    "damage_score": [10, 15, 20, 40, 70, 95]
})

# =========================
# 머신러닝 학습
# =========================

X = train_df[["temp", "humidity", "wind"]]
y = train_df["damage_score"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# =========================
# 실시간 날씨 데이터 가져오기
# =========================

API_KEY = "여기에_API_KEY"

CITY = "Andong"

url = f"""
https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric
"""

response = requests.get(url)

if response.status_code == 200:

    weather = response.json()

    temp = weather["main"]["temp"]
    humidity = weather["main"]["humidity"]
    wind = weather["wind"]["speed"]

    st.subheader("실시간 환경 데이터")

    col1, col2, col3 = st.columns(3)

    col1.metric("온도", f"{temp}°C")
    col2.metric("습도", f"{humidity}%")
    col3.metric("풍속", f"{wind}m/s")

    # =========================
    # AI 예측
    # =========================

    input_data = pd.DataFrame({
        "temp": [temp],
        "humidity": [humidity],
        "wind": [wind]
    })

    predicted_risk = model.predict(input_data)[0]

    predicted_risk = round(predicted_risk, 1)

    st.subheader("AI 위험도 예측")

    if predicted_risk >= 80:

        st.error(
            f"현재 환경은 문화재 훼손 위험이 매우 높습니다. (예측 위험도: {predicted_risk})"
        )

    elif predicted_risk >= 50:

        st.warning(
            f"현재 문화재 훼손 위험이 높습니다. (예측 위험도: {predicted_risk})"
        )

    else:

        st.success(
            f"현재 문화재 상태는 비교적 안정적입니다. (예측 위험도: {predicted_risk})"
        )

else:

    st.error("실시간 날씨 데이터를 가져오지 못했습니다.")
```
