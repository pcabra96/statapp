"""
app.py — StatApp entry point
============================
This file is intentionally thin. Its only job is to:
  1. Configure the Streamlit page
  2. Call each section in order
  3. Pass data between sections

All real logic lives in sections/ and utils/.

To add a new section:
  1. Create sections/my_section.py with a render(df, num_cols) function
  2. Import it here
  3. Add a st.divider() and call sections.my_section.render(df, num_cols)

Run locally:
  streamlit run app.py
"""

import warnings

import streamlit as st

import sections.upload as upload
import sections.univariate as univariateßß
import sections.bivariate as bivariate
import sections.regression as regression

warnings.filterwarnings("ignore")  # suppress noisy statsmodels output in the UI

# ---------------------------------------------------------------------------
# Page configuration — must be the very first Streamlit call in the script
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="StatApp",
    page_icon="📊",
    layout="wide",
)

st.title("📊 StatApp")
st.caption("Upload data · Explore · Regress")

# ---------------------------------------------------------------------------
# Section 1: Upload
# df and num_cols are None if no file has been uploaded yet.
# Each section below guards against that and returns early if needed.
# ---------------------------------------------------------------------------
st.divider()
df, num_cols = upload.render()

if df is None:
    st.stop()  # nothing else to show until the user uploads a file

# ---------------------------------------------------------------------------
# Section 2: Univariate EDA
# ---------------------------------------------------------------------------
st.divider()
univariate.render(df, num_cols)

# ---------------------------------------------------------------------------
# Section 3: Bivariate EDA
# Returns the selected Y so we can pre-fill the regression formula.
# ---------------------------------------------------------------------------
st.divider()
selected_y = bivariate.render(df, num_cols)

# ---------------------------------------------------------------------------
# Section 4: OLS Regression
# ---------------------------------------------------------------------------
st.divider()
regression.render(df, num_cols, default_y=selected_y)
