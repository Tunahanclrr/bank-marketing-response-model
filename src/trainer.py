import numpy as np
from sklearn.pipeline import Pipeline
from lightgbm import LGBMClassifier

def train_model(X_train, y_train, preprocessor):
    """
    Pipeline kurar ve modeli eğitir.
    """
    model = LGBMClassifier(
        n_estimators=1000,
        learning_rate=0.1,
        is_unbalance=True,      # dengesiz veri için
        max_depth=12,
        min_child_samples=20,
        colsample_bytree=0.8,
        n_jobs=-1,
        random_state=42
    )

    # Pipeline: önce preprocessing, sonra model
    pipe = Pipeline([
        ("preprocess", preprocessor),
        ("model", model)
    ])

    # Sadece TRAIN verisi ile fit
    pipe.fit(X_train, y_train)
    print("Model eğitildi.")

    return pipe