from src.data_generation import generate_mock_data
from src.labeling import label_risk_scores
from src.model import prepare_data, train_model, evaluate_model

def main():
    print("Mock veri üretiliyor...")
    df = generate_mock_data(user_count=10, log_per_user=3, save_path="data/mock_login_data.csv")
    print(f"Veri seti boyutu: {df.shape}")

    print("Risk skorları hesaplanıyor...")
    df = label_risk_scores(df)
    df.to_csv("data/mock_login_data_with_risk.csv", index=False)
    print("Etiketli veri kaydedildi.")

    print("Model eğitimi başlıyor...")
    X_train, X_test, y_train, y_test = prepare_data(df)
    model = train_model(X_train, y_train, X_test, y_test)

    print("Model test verisi üzerinde değerlendiriliyor...")
    evaluate_model(model, X_test, y_test)
    print("Tüm akış tamamlandı.")

if __name__ == "__main__":
    main()