# 🔒 Real-Time Risk Scoring System Based on Login Data (Deep Learning)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Enabled-brightgreen?logo=streamlit)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?logo=tensorflow)

---

## 🚀 Project Overview
This project aims to develop a deep learning-based system that calculates a real-time risk score for user logins, based on behavioral and contextual login data. The model compares each login attempt with the user's historical patterns and outputs a risk score between 0 and 100.

---

## 📁 Project Structure
```
risk_skorlama_projesi/
│
├── data/                # Mock/generated datasets
├── src/                 # Source code modules
│   ├── data_generation.py   # Mock data generation
│   ├── labeling.py          # Risk labeling & scoring
│   ├── model.py             # Model training & evaluation
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
├── main.py              # Main pipeline script
└── app.py               # Streamlit web app
```

---

## ✨ Features
- **Realistic Mock Data Generation:** Simulates user login behavior with configurable randomness.
- **Flexible Risk Labeling:** Rule-based and statistical risk scoring for each login event.
- **Deep Learning Model:** Predicts risk scores using a neural network (TensorFlow/Keras).
- **Interactive Web UI:** Modern Streamlit interface for real-time scoring and data exploration.
- **Modular & Reusable:** Clean, well-documented, and easy to extend.

---

## 🖥️ Quick Start
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the main pipeline:**
   ```bash
   python main.py
   ```
3. **Launch the web app:**
   ```bash
   streamlit run app.py
   ```

---

## 📊 Screenshots

![git1](https://github.com/user-attachments/assets/6f488c6f-e1db-48ae-9efe-b0f013387314)

![git2](https://github.com/user-attachments/assets/9c48ae27-ae27-4da9-970c-957d07b736cc)

---

## ⚙️ How It Works
- **Data Generation:** Produces mock login data with realistic user patterns and anomalies.
- **Risk Labeling:** Assigns a risk score (0-100) to each login based on time, IP, MFA, device, and behavioral deviations.
- **Model Training:** Trains a deep learning model to predict risk scores from login features.
- **Web Interface:** Allows users to simulate logins, get instant risk scores, and explore the dataset interactively.

---

## 📚 Technologies Used
- Python, Pandas, NumPy
- TensorFlow & Keras
- Scikit-learn
- Streamlit
- Faker (for data generation)

---


## 🙋‍♂️ Author & Contact
- Developed by Yusuf Uzun
- yusfuzn@hotmail.com

Feel free to contribute, open issues, or suggest improvements!
