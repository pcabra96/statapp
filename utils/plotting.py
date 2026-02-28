"""
utils/plotting.py
-----------------
Shared plotting utilities.

Why render to a buffer instead of saving to disk?
  Streamlit can display images from an in-memory BytesIO buffer directly.
  Saving to disk would require managing temporary files and cleaning them up —
  especially tricky inside Docker where the filesystem may be read-only or
  epehemeral. In-memory is simpler and more portable.
"""

import io

import matplotlib.pyplot as plt
import streamlit as st


# Global style applied to every figure in the app.
# Change this once here rather than repeating it in every section.
plt.rcParams.update(
    {
        "figure.facecolor": "white",
        "axes.facecolor": "#f8f9fa",
        "axes.grid": True,
        "grid.color": "white",
        "grid.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.size": 11,
    }
)

PRIMARY_COLOR = "steelblue"
ACCENT_COLOR = "crimson"


def fig_to_streamlit(fig: plt.Figure) -> None:
    """
    Render a matplotlib Figure into the Streamlit UI, then close it.

    Closing the figure after rendering is important: matplotlib keeps
    figures in memory until explicitly closed. In a long session with
    many variables, unclosed figures would slowly leak memory.
    """
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=120)
    buf.seek(0)
    st.image(buf)
    plt.close(fig)  # free memory — do not skip this
