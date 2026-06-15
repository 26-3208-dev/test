import streamlit as st

st.set_page_config(
  page_title="문화재 훼손"
)

st.title("문화재 훼손 예측")
st.divider()

df = pd.read_csv("data/yc_heritage_detail_enriched.csv")
st.dataframe(df)
