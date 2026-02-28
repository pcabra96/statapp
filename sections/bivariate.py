"""
sections/bivariate.py
---------------------
Section 3: Bivariate Exploratory Data Analysis.

For each (X, Y) pair the user sees:
  - Pearson correlation coefficient r and its p-value
  - A scatterplot with an OLS trend line and 95% confidence band

Why show the confidence band?
  The band narrows where data is dense and widens at the extremes.
  A very wide band at the edges signals that predictions there are
  unreliable — a common source of over-confident extrapolation.

Why Pearson r and not Spearman?
  Pearson r is the natural companion to OLS regression (it squares to R²
  in simple regression). If the scatterplot looks non-linear or has heavy
  outliers, adding Spearman would be a good extension.
"""

import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import streamlit as st

from utils.plotting import ACCENT_COLOR, fig_to_streamlit


def render(df: pd.DataFrame, num_cols: list[str]) -> str | None:
    """
    Render the Bivariate EDA section.

    Returns the selected Y variable name so app.py can pass it as a
    default to the regression section — avoids the user having to type it again.
    """
    st.header("3 · Bivariate EDA")
    st.markdown(
        "Choose a **Y** (outcome) and one or more **X** (predictors). "
        "Each scatterplot includes the Pearson correlation *r* and a linear trend line."
    )

    if len(num_cols) < 2:
        st.warning("Need at least 2 numeric columns for bivariate analysis.")
        return None

    y_col = st.selectbox("Y variable (outcome)", options=num_cols, index=0)
    x_options = [c for c in num_cols if c != y_col]
    x_cols = st.multiselect(
        "X variable(s) (predictors)",
        options=x_options,
        default=x_options[:1],
    )

    for x_col in x_cols:
        _render_pair(df, x_col, y_col)

    # Return y_col so the regression section can pre-fill the formula
    return y_col


def _render_pair(df: pd.DataFrame, x_col: str, y_col: str) -> None:
    """Render correlation stat + scatterplot for one (X, Y) pair."""

    pair = df[[x_col, y_col]].dropna()

    if len(pair) < 3:
        st.warning(f"Not enough non-missing data to correlate `{x_col}` and `{y_col}`.")
        return

    r, p_val = stats.pearsonr(pair[x_col], pair[y_col])

    st.subheader(f"`{x_col}` vs `{y_col}`")
    st.markdown(
        f"**Pearson r = {r:.3f}** &nbsp;|&nbsp; "
        f"p-value = {p_val:.4f} &nbsp;|&nbsp; "
        f"n = {len(pair):,}"
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.regplot(
        data=pair,
        x=x_col,
        y=y_col,
        ax=ax,
        scatter_kws={"alpha": 0.5, "s": 20},
        line_kws={"color": ACCENT_COLOR, "linewidth": 1.5},
    )
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(f"{y_col} ~ {x_col}  (r = {r:.3f})")
    fig_to_streamlit(fig)
