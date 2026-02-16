import pandas as pd

def load_data():
    df = pd.read_csv("./data/train.csv")
    print("Data loaded successfully.")
    return df
