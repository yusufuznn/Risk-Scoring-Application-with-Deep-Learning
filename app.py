import streamlit as st
import pandas as pd
import numpy as np
from src.data_generation import generate_mock_data
from src.labeling import label_risk_scores
from src.model import prepare_data, train_model
import os

st.set_page_config(
    page_title="Anlık Risk Skorlama Sistemi",
    layout="wide",
    page_icon="🔒"
)

# Başlık
st.markdown(
    """
    <style>
    .main {background-color: #18191A;}
    .stApp {background-color: #23272F;}
    .big-font {font-size:32px !important; color: #00BFFF;}
    .metric-box {background: #222; border-radius: 10px; padding: 20px; margin-bottom: 10px;}
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<div class="big-font">🔒 Anlık Risk Skorlama Sistemi</div>', unsafe_allow_html=True)
st.write("Kullanıcı giriş verilerine dayalı anlık risk skoru tahmini ve analiz platformu.")

# Model ve veri önbelleği
@st.cache_data
def get_data_and_model():
    data_path = "data/mock_login_data_with_risk.csv"
    if not os.path.exists(data_path):
        df = generate_mock_data(user_count=10, log_per_user=3)
        df = label_risk_scores(df)
        os.makedirs("data", exist_ok=True)
        df.to_csv(data_path, index=False)
    else:
        df = pd.read_csv(data_path)
    X_train, X_test, y_train, y_test = prepare_data(df)
    model = train_model(X_train, y_train, X_test, y_test)
    return df, model

df, model = get_data_and_model()

# Sidebar
st.sidebar.image("https://img.icons8.com/fluency/96/lock-2.png", width=80)
st.sidebar.header("Kullanıcı Girişi Simülasyonu")
user_id = st.sidebar.selectbox("UserId", df["UserId"].unique())
mfa_method = st.sidebar.selectbox("MFAMethod", df["MFAMethod"].unique())
created_at = st.sidebar.text_input("CreatedAt (YYYY-MM-DD HH:MM:SS)", "2025-05-29 08:15:23")
client_ip = st.sidebar.text_input("ClientIP", df["ClientIP"].unique()[0])
application = st.sidebar.selectbox("Application", df["Application"].unique())
browser = st.sidebar.selectbox("Browser", df["Browser"].unique())
os = st.sidebar.selectbox("OS", df["OS"].unique())
unit = st.sidebar.selectbox("Unit", df["Unit"].unique())
title = st.sidebar.selectbox("Title", df["Title"].unique())

if st.sidebar.button("Risk Skoru Hesapla"):
    input_df = pd.DataFrame.from_dict({
        "UserId": [user_id],
        "MFAMethod": [mfa_method],
        "CreatedAt": [created_at],
        "ClientIP": [client_ip],
        "Application": [application],
        "Browser": [browser],
        "OS": [os],
        "Unit": [unit],
        "Title": [title],
    })
    from src.model import prepare_data
    temp_df = pd.concat([df, input_df], ignore_index=True)
    X_all, _, _, _ = prepare_data(temp_df)
    X_input = X_all.iloc[[-1]]
    risk_score = model.predict(X_input)[0][0]
    st.markdown(
        f'<div class="metric-box"><h3>🔎 Tahmini Risk Skoru: <span style="color:#00BFFF;">{risk_score:.2f}</span> / 100</h3></div>',
        unsafe_allow_html=True
    )

# Ana sayfa metrikleri ve grafikler
col1, col2 = st.columns(2)
with col1:
    st.metric("Toplam Kullanıcı", df["UserId"].nunique())
    st.metric("Toplam Giriş", len(df))
with col2:
    st.metric("Ortalama Risk Skoru", f"{df['RiskScore'].mean():.2f}")
    st.metric("En Yüksek Risk Skoru", f"{df['RiskScore'].max():.2f}")

st.markdown("---")
st.subheader("📊 Mock Veri Seti (İlk 100 Satır)")
st.dataframe(df.head(100), use_container_width=True)

st.markdown("---")
st.subheader("📈 Risk Skoru Dağılımı")
st.bar_chart(df["RiskScore"])