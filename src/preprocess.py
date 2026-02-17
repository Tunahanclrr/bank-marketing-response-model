import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder

def preprocess_data(df):
    # Gereksiz kolonları sil
    cols_to_drop = ['id', 'duration']
    df = df.drop(columns=cols_to_drop)
    print("Columns dropped successfully.")

    # Campaign <= 9 filtrele
    df = df[df['campaign'] <= 9]
    print("Campaign filtering applied successfully.")

    

    # X ve y ayrımı
    X = df.drop("y", axis=1)
    y = df["y"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print("Train-test split applied successfully.")
    print("Train size:", X_train.shape)
    print("Test size:", X_test.shape)

    return X_train, X_test, y_train, y_test

def build_preprocessor(X_train):
    # Ordinal sıralamalar
    education_order = ['unknown', 'primary', 'secondary', 'tertiary']
    month_order = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 
                   'sep', 'oct', 'nov', 'dec']

    # Sütun kategorileri
    onehot_cols = ['job', 'marital', 'contact', 'poutcome']
    num_cols = ['age', 'balance', 'day', 'campaign', 'pdays', 'previous']

    # Transformerlar
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    ## binary kolonlar 

    binary_cols = ['default', 'housing', 'loan']

    binary_transformer = OrdinalEncoder(
    categories=[['no', 'yes']] * len(binary_cols)
    )
    # ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('ord', OrdinalEncoder(categories=[education_order, month_order]), ['education', 'month']),
            ('cat', categorical_transformer, onehot_cols),
            ('num', numeric_transformer, num_cols),
            ('bin', binary_transformer, binary_cols)
        ],
        remainder='passthrough'  # Binary kolonlar direkt geçer
    )

    # Fit ve transform
    X_train_processed = preprocessor.fit_transform(X_train)
    print("Preprocessing applied successfully.")

    return preprocessor, X_train_processed
