"""
prepare.py — Raw data load panni train/test split save pannudu.
DVC Stage 1: prepare
"""
import json
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

RAW_DATA_PATH = os.path.join("data", "raw", "housing.csv")
TRAIN_PATH = os.path.join("data", "processed", "train.csv")
TEST_PATH = os.path.join("data", "processed", "test.csv")
PARAMS_PATH = "params.yaml"


def load_raw_data() -> pd.DataFrame:
    return pd.read_csv(RAW_DATA_PATH)


def split_and_save(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42):
    train_df, test_df = train_test_split(df, test_size=test_size, random_state=random_state)
    os.makedirs(os.path.dirname(TRAIN_PATH), exist_ok=True)
    train_df.to_csv(TRAIN_PATH, index=False)
    test_df.to_csv(TEST_PATH, index=False)
    print(f"Train size: {len(train_df)}, Test size: {len(test_df)}")


if __name__ == "__main__":
    df = load_raw_data()
    split_and_save(df)
    print("Data preparation done.")
