"""
sections/regression.py
----------------------
Section 4: OLS Regression via statsmodels.

What gets shown:
  - Model fit: R², Adj. R², F-statistic, AIC, BIC, observation count
  - Coefficient table: estimate, std. error, t-stat, p-value, 95% CI
    (p < 0.05 highlighted in green for quick visual scanning)
  - Residuals vs Fitted plot  → checks linearity & homoscedasticity
  - Q-Q plot of residuals     → checks normality assumption

Patsy formula syntax (same as R):
  "y ~ x1 + x2"         additive model
  "y ~ x1 + x2 + x1:x2" with interaction
  "y ~ np.log(x1)"      transformation applied on the fly
  "y ~ C(group)"         treat 'group' as categorical (dummy-coded)
  "y ~ Q('my col')"      column name with spaces

Common failure points:
  - Column name typo → Patsy raises a PatsyError with a helpful message.
  - Column with spaces: wrap in Q('col name').
  - Perfect multicollinearity: statsmodels drops the redundant column and warns.
  - All-missing column: statsmodels raises a ValueError; check the data first.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import statsmodels.formula.api as smf
import streamlit as st

from utils.plotting import ACCENT_COLOR, PRIMARY_COLOR, fig_to_streamlit


def render(df: pd.DataFrame, num_cols: list[str], default_y: str | None = None) -> None:
    """Render the OLS Regression section."""

    st.header("4 · OLS Regression")
    st.markdown(
        "Type your model formula using **Patsy notation** (same as R). Examples:\n"
        "- `salary ~ age + experience`\n"
        "- `price ~ np.log(area) + bedrooms + C(city)` — `C()` makes a variable categorical\n"
        "- `y ~ x1 + x2 + x1:x2` — `:` is an interaction term\n"
        "- `Q('col name') ~ x` — wrap column names that contain spaces in `Q()`"
    )

    # Show available columns so the user knows what to type
    with st.expander("Available columns"):
        st.write(list(df.columns))

    # Pre-fill a sensible default formula using the Y from Section 3
    y_default = default_y if default_y else (num_cols[0] if num_cols else "y")
    xs_default = [c for c in num_cols if c != y_default][:3]
    formula_default = f"{y_default} ~ " + " + ".join(xs_default) if xs_default else y_default

    formula = st.text_input(
        "Formula",
        value=formula_default,
        help="Patsy formula. Hit 'Fit model' to run.",
    )

    if not st.button("Fit model", type="primary"):
        return  # nothing to do until the user clicks

    _fit_and_display(df, formula)


def _fit_and_display(df: pd.DataFrame, formula: str) -> None:
    """Fit the model and render all output tables and plots."""

    try:
        model = smf.ols(formula=formula, data=df).fit()
    except Exception as exc:
        # Surface the error in the UI with context — don't just crash silently
        st.error(f"**Model failed:** {exc}")
        st.info(
            "Common causes: typo in column name, column name with spaces "
            "(use Q('col name')), or a column that is all-missing."
        )
        return

    _show_fit_metrics(model)
    _show_coef_table(model)
    _show_diagnostics(model)

    with st.expander("Full statsmodels summary (text)"):
        st.text(model.summary().as_text())


def _show_fit_metrics(model) -> None:
    """Display a compact model-fit table."""
    st.subheader("Model fit")

    metrics = {
        "R²": f"{model.rsquared:.4f}",
        "Adjusted R²": f"{model.rsquared_adj:.4f}",
        "F-statistic": f"{model.fvalue:.4f}",
        "Prob (F-statistic)": f"{model.f_pvalue:.4e}",
        "AIC": f"{model.aic:.2f}",
        "BIC": f"{model.bic:.2f}",
        "Observations": f"{int(model.nobs):,}",
        "Df Residuals": f"{int(model.df_resid):,}",
    }
    st.table(pd.DataFrame.from_dict(metrics, orient="index", columns=["Value"]))


def _show_coef_table(model) -> None:
    """Display the coefficient table with p < 0.05 highlighted."""
    st.subheader("Coefficients")

    coef_df = model.summary2().tables[1].rename(
        columns={
            "Coef.": "Estimate",
            "Std.Err.": "Std. Error",
            "t": "t-stat",
            "P>|t|": "p-value",
            "[0.025": "CI 2.5%",
            "0.975]": "CI 97.5%",
        }
    )

    def _highlight_sig(val):
        # Green background for statistically significant p-values
        try:
            return "background-color: #d4edda" if float(val) < 0.05 else ""
        except (ValueError, TypeError):
            return ""

    st.dataframe(
        coef_df.style.format("{:.4f}").applymap(_highlight_sig, subset=["p-value"]),
        use_container_width=True,
    )


def _show_diagnostics(model) -> None:
    """Render the Residuals vs Fitted and Q-Q plots side by side."""
    st.subheader("Diagnostics")

    residuals = model.resid
    fitted = model.fittedvalues

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # --- Residuals vs Fitted ---
    # A random scatter around the horizontal zero line is what we want.
    # Patterns (funnel shape, curve) indicate heteroscedasticity or non-linearity.
    axes[0].scatter(fitted, residuals, alpha=0.4, s=15, color=PRIMARY_COLOR)
    axes[0].axhline(0, color=ACCENT_COLOR, linewidth=1.2, linestyle="--")
    axes[0].set_xlabel("Fitted values")
    axes[0].set_ylabel("Residuals")
    axes[0].set_title("Residuals vs Fitted")

    # --- Q-Q Plot ---
    # Points should follow the diagonal line if residuals are roughly normal.
    # Heavy tails or S-curves suggest non-normality.
    (osm, osr), (slope, intercept, _) = stats.probplot(residuals, dist="norm")
    axes[1].scatter(osm, osr, alpha=0.4, s=15, color=PRIMARY_COLOR)
    axes[1].plot(
        osm,
        slope * np.array(osm) + intercept,
        color=ACCENT_COLOR,
        linewidth=1.2,
    )
    axes[1].set_xlabel("Theoretical quantiles")
    axes[1].set_ylabel("Sample quantiles")
    axes[1].set_title("Q-Q Plot (residuals)")

    fig.tight_layout()
    fig_to_streamlit(fig)
