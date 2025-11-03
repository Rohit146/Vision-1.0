import pandas as pd

def load_excel(file):
    """Load Excel file and return dict of DataFrames"""
    try:
        return pd.read_excel(file, sheet_name=None)
    except Exception as e:
        raise ValueError(f"Error reading Excel file: {e}")

def summarize_dataframe(df: pd.DataFrame):
    """Create a readable summary of a dataframe"""
    summary = []
    summary.append(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    summary.append("Columns:")
    for col in df.columns:
        dtype = df[col].dtype
        sample = df[col].dropna().unique()[:3]
        summary.append(f" - {col} ({dtype}) → sample: {sample}")
    return "\n".join(summary)

def generate_data_profile(excel_dict):
    """Generate combined sheet summaries"""
    profiles = []
    for name, df in excel_dict.items():
        profiles.append(f"📄 Sheet: {name}")
        profiles.append(summarize_dataframe(df))
        profiles.append("-" * 40)
    return "\n".join(profiles)
