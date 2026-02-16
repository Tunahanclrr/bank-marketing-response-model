## evaulate py 
import numpy as np
from sklearn.metrics import (
    classification_report,
    roc_auc_score,
    precision_recall_curve,
    f1_score,
    auc
)

def evaluate_model(pipe, X_train, y_train, X_test, y_test):
    """
    Pipeline üzerinden tahmin yapar ve PR-AUC + F1 sonuçlarını gösterir.
    """
    # Tahmin olasılıkları
    y_prob_train = pipe.predict_proba(X_train)[:, 1]
    y_prob_test = pipe.predict_proba(X_test)[:, 1]

    # Train PR Curve + PR AUC
    precision_train, recall_train, thresholds_train = precision_recall_curve(
        y_train, y_prob_train
    )
    pr_auc_train = auc(recall_train, precision_train)

    # F1'e göre en iyi threshold
    f1_scores = 2 * (precision_train[:-1] * recall_train[:-1]) / (
        precision_train[:-1] + recall_train[:-1] + 1e-8
    )
    best_idx = np.argmax(f1_scores)
    best_threshold = thresholds_train[best_idx]

    print(f"Optimal threshold for F1: {best_threshold:.3f}")
    print(f"Best F1 score on train: {f1_scores[best_idx]:.3f}")

    # Test PR AUC
    precision_test, recall_test, _ = precision_recall_curve(
        y_test, y_prob_test
    )
    pr_auc_test = auc(recall_test, precision_test)

    # Yeni threshold ile sınıflandır
    y_pred_train_opt = (y_prob_train >= best_threshold).astype(int)
    y_pred_test_opt = (y_prob_test >= best_threshold).astype(int)

    # Sonuçları yazdır
    print("\n--- EĞİTİM (TRAIN) SONUÇLARI ---")
    print(classification_report(y_train, y_pred_train_opt))
    print("Train ROC AUC:", roc_auc_score(y_train, y_prob_train))
    print("Train PR AUC:", pr_auc_train)
    print("Train F1:", f1_score(y_train, y_pred_train_opt))

    print("\n" + "="*40 + "\n")

    print("--- TEST SONUÇLARI ---")
    print(classification_report(y_test, y_pred_test_opt))
    print("Test ROC AUC:", roc_auc_score(y_test, y_prob_test))
    print("Test PR AUC:", pr_auc_test)
    print("Test F1:", f1_score(y_test, y_pred_test_opt))

    return {
        "best_threshold": best_threshold,
        "pr_auc_train": pr_auc_train,
        "pr_auc_test": pr_auc_test,
        "f1_train": f1_score(y_train, y_pred_train_opt),
        "f1_test": f1_score(y_test, y_pred_test_opt)
    }

