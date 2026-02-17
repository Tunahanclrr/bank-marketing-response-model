from src.data_loader import load_data
from src.preprocess import preprocess_data, build_preprocessor
from src.trainer import train_model
from src.evaluate import evaluate_model
import joblib
import os


def main():
    df = load_data()
    print(df.head())    
    print("Shape:", df.shape)
    X_train, X_test, y_train, y_test = preprocess_data(df)
    preprocessor, X_train_processed = build_preprocessor(X_train)
    pipe = train_model(X_train, y_train, preprocessor)
    results = evaluate_model(pipe, X_train, y_train, X_test, y_test)
    print("Evaluation completed.")
    print("Best Threshold:", results["best_threshold"])
    print("Train PR AUC:", results["pr_auc_train"])
    print("Test PR AUC:", results["pr_auc_test"])
    print("Train F1:", results["f1_train"])
    print("Test F1:", results["f1_test"])
    print("All steps completed successfully.")
    print("All steps completed successfully.")
    
    ## modeli kaydet
    os.makedirs("models", exist_ok=True)

    joblib.dump({
        "model": pipe,
        "threshold": results["best_threshold"]
    }, "models/lgbm_pipeline.pkl")

    print("Model models/lgbm_pipeline.pkl olarak kaydedildi ✅")
    print("All steps completed successfully.")
if __name__ == "__main__":
    main()
