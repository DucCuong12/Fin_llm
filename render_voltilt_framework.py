"""Build the VolTilt mechanism diagram at LNCS text width in Matplotlib."""
from pathlib import Path

from render_voltilt_figure_panels import PALETTE, apply_publication_style

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
from matplotlib.path import Path as PlotPath

WIDTH_MM, HEIGHT_MM = 122, 56
INK = PALETTE["ink"]
BLUE = PALETTE["blue"]
NEWS = "#266D63"
MUTED = "#495D6D"
EDGE = "#ACBBC6"
OUT = Path(__file__).resolve().with_name("voltilt_framework_matplotlib.pdf")


def text(ax, x, y, value, *, size=7.7, color=INK, bold=False, ha="center"):
    ax.text(x, y, value, color=color, fontsize=size,
            fontweight="bold" if bold else "normal", ha=ha, va="center")


def rect(ax, x, y, width, height, *, fill, edge=EDGE, lw=.55):
    ax.add_patch(Rectangle((x, y), width, height, facecolor=fill,
                           edgecolor=edge, linewidth=lw))


def panel(ax, x, y, width, height, title, *, fill, accent):
    rect(ax, x, y, width, height, fill="white")
    rect(ax, x, y + height - 6.6, width, 6.6, fill=fill)
    text(ax, x + 2.65, y + height - 3.3, title,
         size=8.5, color=accent, bold=True, ha="left")


def arrow(ax, points, color=INK):
    """Use routed arrows for data dependencies, with no decorative endpoints."""
    route = PlotPath(points, [PlotPath.MOVETO] + [PlotPath.LINETO] * (len(points) - 1))
    ax.add_patch(FancyArrowPatch(path=route, color=color, arrowstyle="-|>",
                                mutation_scale=6.5, linewidth=.7, zorder=4))


def stage(ax, x, y, title, value, *, title_size=7.35, value_size=8.15, color=INK):
    text(ax, x, y, title, size=title_size, bold=True)
    text(ax, x, y - 4.6, value, size=value_size, color=color)


def news_path(ax):
    panel(ax, .8, 30.4, 90.7, 24.8, "Relative weights",
          fill="#EAF3F0", accent=NEWS)
    text(ax, 88.9, 51.9, r"Close $t$", size=7.1, color=MUTED, ha="right")
    stage(ax, 9.5, 41.4, "Dated news", r"$\mathcal{X}_{i,t}$", title_size=7.0)
    stage(ax, 26.4, 41.4, "LLM record", "Impact + metadata", value_size=6.4)
    text(ax, 44.7, 41.4, "Event gate", size=7.35, bold=True)
    text(ax, 44.7, 36.8, "Main subject", size=6.55, color=MUTED)
    text(ax, 44.7, 33.3, "Reported figures", size=6.55, color=MUTED)
    stage(ax, 63.3, 41.4, "Sum + EMA", r"$s_{i,t}$")
    stage(ax, 81.3, 41.4, "Bounded rank", r"$q_{i,t}=\tau_{i,t}/N_t$",
          title_size=7.15, value_size=7.8, color=NEWS)
    for start, end in ((16, 19.1), (33, 36.1), (52.9, 56.1), (70.1, 73.3)):
        arrow(ax, [(start, 39.25), (end, 39.25)], NEWS)


def risk_path(ax):
    panel(ax, .8, 1.1, 90.7, 25.8, "Volatility budget",
          fill="#EAF0F6", accent=BLUE)
    text(ax, 88.9, 23.6, r"History through $t$", size=7.1, color=MUTED, ha="right")

    rect(ax, 3.15, 12.1, 20.9, 5.7, fill="#F0F4F9", edge="#BCC9D3")
    rect(ax, 3.15, 4.35, 20.9, 5.7, fill="#EDF5F1", edge="#ACC5BD")
    text(ax, 4.5, 14.95, "Returns", size=6.95, ha="left")
    text(ax, 21.95, 14.95, r"$r^{\mathrm{obs}}_{i,s}$", size=7.7, ha="right")
    text(ax, 4.5, 7.2, "Prior tilts", size=6.95, ha="left")
    text(ax, 21.95, 7.2, r"$\tau_{i,s-1}$", size=7.7, color=NEWS, ha="right")

    arrow(ax, [(24.05, 14.95), (26, 14.95), (26, 11.08), (29.3, 11.08)], BLUE)
    ax.plot([24.05, 26, 26], [7.2, 7.2, 11.08],
            color=NEWS, linewidth=.7, zorder=4)
    stage(ax, 42.45, 14.6, r"Unscaled $\tilde r_s$",
          r"$\langle\tau_{i,s-1}r^{\mathrm{obs}}_{i,s}\rangle_{i\in\mathcal{B}_s}$",
          value_size=7.7)
    text(ax, 62.0, 14.6, "Volatility", size=7.35, bold=True)
    text(ax, 62.0, 10.0, r"$\hat{\sigma}_t$", size=8.15)
    text(ax, 62.0, 5.7, "20 dates", size=6.55, color=MUTED)
    stage(ax, 81.0, 14.6, "Invested fraction",
          r"$\lambda_t=\min(1,\sigma^\star/\hat{\sigma}_t)$",
          title_size=7.15, value_size=6.9, color=BLUE)
    arrow(ax, [(53.25, 13.0), (55.65, 13.0)], BLUE)
    arrow(ax, [(68.1, 13.0), (71.7, 13.0)], BLUE)


def portfolio(ax):
    panel(ax, 96.25, 1.1, 24.95, 54.1, "Portfolio",
          fill="#EAF0F6", accent=BLUE)
    ax.plot([91.55, 93.3, 93.3], [39.25, 39.25, 27.35], color=NEWS, linewidth=.7)
    ax.plot([91.55, 93.3, 93.3], [13.0, 13.0, 27.35], color=BLUE, linewidth=.7)
    arrow(ax, [(93.3, 27.35), (96.25, 27.35)])
    stage(ax, 108.73, 37.05, "Risky weights", r"$a_{i,t}=\lambda_t q_{i,t}$",
          title_size=7.65, value_size=9.35)
    ax.plot([99.2, 118.2], [23.4, 23.4], color=EDGE, linewidth=.55)
    stage(ax, 108.73, 17.8, "Cash", r"$1-\lambda_t$",
          title_size=7.65, value_size=9.1)


def main():
    apply_publication_style()
    fig = plt.figure(figsize=(WIDTH_MM / 25.4, HEIGHT_MM / 25.4), facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1], xlim=(0, WIDTH_MM), ylim=(0, HEIGHT_MM))
    ax.set_axis_off()
    news_path(ax)
    risk_path(ax)
    portfolio(ax)
    fig.savefig(OUT, dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
