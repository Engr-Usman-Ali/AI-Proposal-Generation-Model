# src/data_preprocessing.py
import pandas as pd

def load_and_clean_data(file_path: str):
    """
    Load and clean client briefs dataset.
    CSV columns expected: id, text, service_type, budget, tone, features
    """
    df = pd.read_csv(file_path)
    df.dropna(subset=["text"], inplace=True)

    # Fill missing optional fields
    for col in ["service_type", "budget", "tone", "features"]:
        if col in df.columns:
            df[col].fillna("Unknown", inplace=True)
        else:
            df[col] = "Unknown"

    print(f"✅ Loaded {len(df)} client briefs.")
    return df
