"""
Model eğitimi ve değerlendirme modülü
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow.keras import layers

def prepare_data(df):
    df = df.copy()
    df['Hour'] = pd.to_datetime(df['CreatedAt']).dt.hour
    for col in ["UserId", "MFAMethod", "ClientIP", "Application", "Browser", "OS", "Unit", "Title"]:
        df[col] = LabelEncoder().fit_transform(df[col])
    X = df[["UserId", "MFAMethod", "ClientIP", "Application", "Browser", "OS", "Unit", "Title", "Hour"]]
    y = df["RiskScore"]
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train, y_train, X_val, y_val):
    model = tf.keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        layers.Dense(32, activation='relu'),
        layers.Dense(1, activation='linear')
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_val, y_val), verbose=2)
    return model

def evaluate_model(model, X_test, y_test):
    loss, mae = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test MAE: {mae:.2f}")
    return mae