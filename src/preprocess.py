
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

df = pd.read_parquet(
    ROOT / "data/raw/cve_sample.parquet"
)

print("Before cleaning:", len(df))


df["cve_id"] = df["cve_id"].astype("string").str.strip()

df["severity"] = (
    df["severity"]
    .astype("string")
    .str.strip()
    .str.upper()
)


df["description"] = (
    df["description"]
    .astype("string")
    .fillna("")
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)


valid_labels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

df = df[df["severity"].isin(valid_labels)]

df = df[
    df["cve_id"].notna()
    & df["description"].ne("")
]


df = df.drop_duplicates(subset=["cve_id"])


output = ROOT / "data/processed/cve_clean.parquet"
output.parent.mkdir(parents=True, exist_ok=True)

df.to_parquet(output, index=False)

print("After cleaning:", len(df))
print("\nSeverity distribution:")
print(df["severity"].value_counts())
print("\nMissing values:")
print(df[["cve_id", "severity", "description"]].isna().sum())
