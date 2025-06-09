import streamlit as st
import pandas as pd
import numpy as np
from src.data_generation import generate_mock_data
from src.labeling import label_risk_scores
from src.model import prepare_data, train_model
import os

# Sayfa ayarları
st.set_page_config(
    page_title="🔒 Anlık Risk Skorlama Sistemi",
    layout="wide",
    page_icon="🔒"
)

# Stil
st.markdown("""
    <style>
        .stApp {
            background-color: #1e1e1e;
            color: white;
        }
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #00CED1;
        }
        .subtitle {
            font-size: 20px;
            margin-bottom: 20px;
            color: #B0C4DE;
        }
        .metric-box {
            background: #2a2a2a;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0px 0px 10px #00000050;
        }
        .stButton>button {
            background-color: #00CED1;
            color: black;
            font-weight: bold;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# Başlık
st.markdown('<div class="title">🔒 Anlık Risk Skorlama Sistemi</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Kullanıcı giriş verilerine dayalı anlık risk skoru tahmini ve analiz platformu.</div>', unsafe_allow_html=True)

# Veri ve model
@st.cache_data
def get_data_and_model():
    data_path = "data/mock_login_data_with_risk.csv"
    if not os.path.exists(data_path):
        df = generate_mock_data(user_count=1000, log_per_user=3)
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
st.sidebar.title("🛡️ Giriş Simülasyonu")

user_id = st.sidebar.selectbox("👤 Kullanıcı ID", df["UserId"].unique())
mfa_method = st.sidebar.selectbox("🔐 MFA Yöntemi", df["MFAMethod"].unique())
created_at = st.sidebar.text_input("📅 Oluşturulma Zamanı", "2025-05-29 08:15:23")
client_ip = st.sidebar.text_input("🌐 IP Adresi", df["ClientIP"].unique()[0])
application = st.sidebar.selectbox("📱 Uygulama", df["Application"].unique())
browser = st.sidebar.selectbox("🌍 Tarayıcı", df["Browser"].unique())
os = st.sidebar.selectbox("💻 İşletim Sistemi", df["OS"].unique())
unit = st.sidebar.selectbox("🏢 Birim", df["Unit"].unique())
title = st.sidebar.selectbox("📌 Ünvan", df["Title"].unique())

# Skor hesaplama
if st.sidebar.button("🎯 Risk Skoru Hesapla"):
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
    temp_df = pd.concat([df, input_df], ignore_index=True)
    X_all, _, _, _ = prepare_data(temp_df)
    X_input = X_all.iloc[[-1]]
    risk_score = model.predict(X_input)[0][0]

    # Renk ve etiket
    if risk_score < 40:
        color = "#32CD32"  # Yeşil
        label = "Düşük Risk"
    elif risk_score < 70:
        color = "#FFA500"  # Turuncu
        label = "Orta Risk"
    else:
        color = "#FF4500"  # Kırmızı
        label = "Yüksek Risk"

    st.markdown(f"""
        <div class="metric-box">
            <h3>🔎 Tahmini Risk Skoru: 
            <span style="color:{color};">{risk_score:.2f}</span> / 100</h3>
            <p><b>⚠️ Risk Seviyesi:</b> <span style="color:{color};">{label}</span></p>
        </div>
    """, unsafe_allow_html=True)

# Metrikler
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="metric-box">', unsafe_allow_html=True)
    st.metric("👥 Toplam Kullanıcı", df["UserId"].nunique())
    st.metric("🔁 Toplam Giriş", len(df))
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-box">', unsafe_allow_html=True)
    st.metric("📊 Ortalama Risk Skoru", f"{df['RiskScore'].mean():.2f}")
    st.metric("⚠️ En Yüksek Risk Skoru", f"{df['RiskScore'].max():.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

# Veri ve grafik
st.markdown("---")
st.subheader("📊 Mock Veri Seti (İlk 100 Satır)")
page_size = st.selectbox("Kayıt sayısı (sayfa başı)", [10, 20, 50, 100], index=1)
total_rows = len(df)
total_pages = (total_rows - 1) // page_size + 1
page = st.number_input("Sayfa numarası", min_value=1, max_value=total_pages, value=1, step=1)

start_idx = (page - 1) * page_size
end_idx = start_idx + page_size
st.dataframe(df.iloc[start_idx:end_idx], use_container_width=True)
st.caption(f"Sayfa {page} / {total_pages} ({total_rows} kayıt)")

st.markdown("---")
st.subheader("📈 Risk Skoru Dağılımı")
st.bar_chart(df["RiskScore"])
