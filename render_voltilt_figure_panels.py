"""Render the illustrative chart panels used in the VolTilt Method figures.

Layout, type, palette, and export conventions follow figures4papers'
scientific-figure-making skill. Dimensions and type sizes are set at final
LNCS print size so TikZ can place each PDF without further scaling.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator

OUT = Path(__file__).resolve().parent / "voltilt_figure_panels"
PALETTE = {
    "ink": "#172C3D",
    "blue": "#0F4D92",
    "medium": "#3775BA",
    "light": "#A6C5E6",
    "exclusion": "#B64342",
    "neutral": "#CFCECE",
}
ASSET_COLORS = [PALETTE[key] for key in ("blue", "medium", "light", "neutral")]
RETURNS = np.array([
    -.273, .954, -1.499, 2.044, -.954, .477, -2.180, 1.499, 2.521, -1.703,
    -.477, 1.703, -2.521, .273, 2.180, -2.044, .954, -.954, 1.499, -1.499,
])


def apply_publication_style():
    plt.rcParams.update({
        "font.family": "sans-serif",
        # Use a TrueType Helvetica-compatible face for reliable PDF embedding.
        "font.sans-serif": ["Liberation Sans", "Arial", "DejaVu Sans"],
        "font.size": 7.2,
        "text.color": PALETTE["ink"],
        "axes.labelcolor": PALETTE["ink"],
        "xtick.color": PALETTE["ink"],
        "ytick.color": PALETTE["ink"],
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": .55,
        "legend.frameon": False,
        "mathtext.fontset": "stix",
        "pdf.fonttype": 42,
        "svg.fonttype": "none",
    })


def finalize_figure(fig, basename):
    # Preserve the exact panel dimensions required by the layout.
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / f"{basename}.pdf", transparent=True, dpi=300)
    plt.close(fig)


def render_returns(*, large):
    width, height = (77.6, 20.5) if large else (40.5, 19.3)
    fig = plt.figure(figsize=(width / 25.4, height / 25.4))
    ax = fig.add_axes([.105, .24, .885, .73] if large else [.19, .025, .805, .95])
    ax.spines[["bottom", "left"]].set_visible(False)
    ax.axhline(0, lw=.5, color="#8B99A2", zorder=1)
    positions = np.arange(20)
    colors = [PALETTE["medium"]] * 20
    if large:
        colors[8] = PALETTE["blue"]
        colors[-1] = PALETTE["blue"]
    ax.bar(positions, RETURNS, width=.62, color=colors, linewidth=0, zorder=2)
    ax.set_ylim(-3.05, 3.18)
    ax.set_xlim(-1.95 if large else -.7, 19.65)
    ax.yaxis.set_major_locator(FixedLocator([-2, 0, 2]))
    ax.set_yticklabels(["−2%", "0", "+2%"], fontsize=6.1)
    ax.tick_params(axis="y", length=0, pad=1.8)
    ax.tick_params(axis="x", length=0, pad=1.8)
    if large:
        ax.bar(-1, -1.6, width=.62, facecolor="none", edgecolor=PALETTE["exclusion"],
               linewidth=.7, linestyle="--", zorder=2)
        ax.axvline(-.5, color="#8B99A2", linewidth=.5, linestyle=":")
        ax.xaxis.set_major_locator(FixedLocator([-1, 8, 19]))
        ax.set_xticklabels([r"$t-20$", r"$s$", r"$t$"])
        ax.plot([-.4, -.4, 19.4, 19.4], [-2.67, -2.95, -2.95, -2.67],
                color=PALETTE["blue"], linewidth=.6)
        ax.annotate(r"$t-19$", xy=(0, -2.95), xytext=(15, -4),
                    textcoords="offset points", ha="left", va="top", fontsize=6.7,
                    arrowprops={"arrowstyle": "-", "color": PALETTE["ink"], "lw": .45})
        ax.text(8, RETURNS[8] + .14, r"$\tilde{r}_s$", ha="center", va="bottom",
                color=PALETTE["blue"], fontsize=7.4)
    else:
        ax.set_xticks([])
    finalize_figure(fig, "returns_window" if large else "returns_overview")


def render_capital(name, relative_weights, *, width=52.9, height=6.5, labels=True):
    assert np.isclose(sum(relative_weights), 1)
    invested = 0.8
    amounts = [*(invested * np.asarray(relative_weights)), 1 - invested]
    assert np.isclose(sum(amounts), 1)
    fig = plt.figure(figsize=(width / 25.4, height / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    left = 0.0
    for asset, value, color in zip(("A", "B", "C", "Cash"), amounts, ASSET_COLORS):
        ax.barh(0, value, left=left, height=1, color=color)
        if left > 0:
            ax.axvline(left, color="white", linewidth=.55)
        if labels:
            percent = f"{value:.1%}".replace(".0%", "%")
            ax.text(left + value / 2, 0, f"{asset}\n{percent}", ha="center", va="center",
                    color="white" if asset in ("A", "B") else PALETTE["ink"],
                    weight="bold", fontsize=6.6 if value < .15 else 7.2,
                    linespacing=.95)
        left += value
    ax.set(xlim=(0, 1), ylim=(-.5, .5))
    ax.set_axis_off()
    finalize_figure(fig, name)


if __name__ == "__main__":
    assert len(RETURNS) == 20 and np.isclose(RETURNS.std() * np.sqrt(252), 25, atol=.001)
    apply_publication_style()
    render_returns(large=False)
    render_returns(large=True)
    render_capital("capital_overview", [.5, 1 / 3, 1 / 6], width=36.2, height=4.1, labels=False)
    render_capital("capital_equal", [1 / 3] * 3)
    render_capital("capital_tilted", [.5, 1 / 3, 1 / 6])
