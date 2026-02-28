"""
sections/univariate.py
----------------------
Section 2: Univariate Exploratory Data Analysis.

For each selected variable the user sees:
  - A summary statistics table (mean, std, percentiles, skewness, kurtosis, missing count)
  - A histogram showing the distribution shape
  - A boxplot showing spread and potential outliers

Why skewness and kurtosis?
  They are the first things a statistician checks to decide whether normality
  holds before running parametric tests (t-tests, ANOVA, OLS). Both are
  missing from pandas describe() by default.

Why a side-by-side histogram + boxplot?
  The histogram shows where the bulk of the data sits; the boxplot
  efficiently flags outliers. Together they give the full picture faster
  than either alone.
"""

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from utils.plotting import PRIMARY_COLOR, fig_to_streamlit


def render(df: pd.DataFrame, num_cols: list[str]) -> None:
    """Render the Univariate EDA section."""

    st.header("2 · Univariate EDA")
    st.markdown(
        "Select one or more variables. For each you'll see summary statistics, "
        "a histogram (distribution shape), and a boxplot (spread + outliers)."
    )

    selected = st.multiselect(
        "Variables to explore",
        options=num_cols,
        default=num_cols[:1],  # pre-select first column as a sensible default
    )

    for col in selected:
        st.subheader(f"Variable: `{col}`")
        _render_variable(df, col)


def _render_variable(df: pd.DataFrame, col: str) -> None:
    """Render stats table + plots for a single variable."""

    series = df[col].dropna()
    n_missing = df[col].isna().sum()

    # Build a summary table with standard + extra stats
    desc = series.describe(percentiles=[0.05, 0.25, 0.5, 0.75, 0.95])
    extra = pd.Series(
        {
            "skewness": series.skew(),
            "kurtosis (excess)": series.kurt(),  # 0 = normal; >0 = heavy tails
            "missing": float(n_missing),
        }
    )
    summary = pd.concat([desc, extra]).rename("value").to_frame()
    summary.index.name = "statistic"

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.dataframe(
            summary.style.format({"value": "{:.4f}"}),
            use_container_width=True,
        )

    with col_right:
        fig = _histogram_boxplot(series, col)
        fig_to_streamlit(fig)


def _histogram_boxplot(series: pd.Series, label: str) -> plt.Figure:
    """
    Build a figure with a histogram (left) and boxplot (right) sharing the y-axis.

    Sharing the y-axis means the boxplot whiskers align with the histogram bars,
    making it easy to see exactly where outliers fall on the distribution.
    """
    fig = plt.figure(figsize=(8, 4))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1], wspace=0.05)

    ax_hist = fig.add_subplot(gs[0])
    ax_box = fig.add_subplot(gs[1], sharey=ax_hist)

    ax_hist.hist(
        series,
        bins="auto",  # numpy picks a sensible bin count
        color=PRIMARY_COLOR,
        edgecolor="white",
        linewidth=0.5,
    )
    ax_hist.set_xlabel(label)
    ax_hist.set_ylabel("Count")
    ax_hist.set_title("Histogram")

    ax_box.boxplot(
        series,
        vert=True,
        patch_artist=True,
        boxprops=dict(facecolor=PRIMARY_COLOR, alpha=0.6),
        medianprops=dict(color="white", linewidth=2),
    )
    ax_box.set_title("Boxplot")
    ax_box.tick_params(labelleft=False)  # y-labels already on the histogram side

    return fig
