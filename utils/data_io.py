"""
utils/data_io.py
----------------
Data loading helpers shared across all sections.

Why a separate module?
  Multiple sections need to know which columns are numeric, or might
  need to reload data. Keeping that logic here avoids copy-paste and
  makes it easy to add new file formats later (e.g. Parquet, SPSS).
"""

import pandas as pd
import streamlit as st


def load_data(uploaded_file) -> pd.DataFrame:
    """
    Read a CSV or Excel file from a Streamlit UploadedFile object.

    We detect format from the filename extension, not the MIME type,
    because browsers sometimes report the wrong MIME type for .xls files.

    Failure point: files saved with unusual encodings (e.g. from old Excel
    or non-Western locales) may fail UTF-8 decoding. The latin-1 fallback
    covers most Western European characters. If you see garbled characters,
    try re-saving the file as UTF-8 from Excel first.
    """
    name = uploaded_file.name.lower()

    if name.endswith(".csv"):
        try:
            return pd.read_csv(uploaded_file, encoding="utf-8")
        except UnicodeDecodeError:
            uploaded_file.seek(0)  # reset pointer before second read attempt
            return pd.read_csv(uploaded_file, encoding="latin-1")

    elif name.endswith((".xlsx", ".xls")):
        # openpyxl is required for .xlsx; xlrd would be needed for old .xls
        return pd.read_excel(uploaded_file, engine="openpyxl")

    else:
        st.error("Unsupported file type. Please upload a .csv or .xlsx file.")
        st.stop()


def numeric_cols(df: pd.DataFrame) -> list[str]:
    """
    Return only the names of numeric columns.

    We restrict analysis to numeric columns because summary statistics,
    correlations, and regression all require numeric inputs.
    Categorical variables can still be used in regression via C() in the formula.
    """
    return df.select_dtypes(include="number").columns.tolist()
