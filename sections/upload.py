"""
sections/upload.py
------------------
Section 1: File upload and initial data preview.

This module is responsible for:
  - Rendering the file uploader widget
  - Calling load_data() and caching the result
  - Showing a preview and basic shape info
  - Returning the loaded DataFrame to the caller (app.py)

Why return the DataFrame instead of storing it in a global?
  Globals are tricky in Streamlit because the entire script reruns on every
  user interaction. Passing data explicitly through function return values
  makes the data flow easier to follow and debug.
"""

import streamlit as st

from utils.data_io import load_data, numeric_cols


def render() -> tuple[object, list[str]] | tuple[None, None]:
    """
    Render the upload section.

    Returns
    -------
    df : pd.DataFrame | None
        The loaded data, or None if no file has been uploaded yet.
    num_cols : list[str] | None
        Names of numeric columns, or None if no data loaded.
    """
    st.header("1 · Upload your data")

    uploaded = st.file_uploader(
        "Drop a CSV or Excel file here",
        type=["csv", "xlsx", "xls"],
        help="Files are processed in memory — nothing is stored on the server.",
    )

    if uploaded is None:
        st.info("Upload a file above to get started.")
        return None, None

    # Load data — errors inside load_data() call st.stop() themselves
    df = load_data(uploaded)

    st.success(f"Loaded **{df.shape[0]:,} rows × {df.shape[1]} columns**")

    with st.expander("Preview data (first 10 rows)"):
        st.dataframe(df.head(10), use_container_width=True)

    cols = numeric_cols(df)
    if len(cols) == 0:
        st.error("No numeric columns found. StatApp needs at least one numeric column.")
        st.stop()

    return df, cols
