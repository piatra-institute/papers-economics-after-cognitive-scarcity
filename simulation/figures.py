"""Figures for *Economics After Cognitive Scarcity*."""
from __future__ import annotations

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

INK, GRID = "#1a1a1a", "#d9d9d9"
AMBER, GREEN, BLUE, GRAY, RED = "#b45309", "#15803d", "#2563eb", "#57534e", "#b3202c"


def _style(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(INK)
    ax.tick_params(colors=INK, labelsize=8.5)
    ax.set_axisbelow(True)
    ax.grid(True, color=GRID, lw=0.6)


def plot_allocation(res, path):
    A, R = res["allocation"], res["remainder"]
    fig, axes = plt.subplots(1, 3, figsize=(12.2, 3.6))

    ax = axes[0]
    labels = ["no pooling", "half pooled", "fully pooled"]
    top = [r["consumption_top"] for r in A["rows"]]
    rest = [r["consumption_rest"] for r in A["rows"]]
    x = np.arange(3)
    ax.bar(x - 0.18, top, width=0.34, color=AMBER, label="each of the ten owners")
    ax.bar(x + 0.18, rest, width=0.34, color=BLUE, label="each of the other ninety")
    for xi, r in enumerate(A["rows"]):
        ax.text(xi, max(top[xi], rest[xi]) + 0.35, f"{r['ratio']:.0f}:1",
                ha="center", fontsize=8.4, color=INK)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8.4)
    ax.set_ylabel("consumption per person", fontsize=8.5)
    ax.set_ylim(0, 10.6)
    ax.set_title("a. identical intelligence, three distributions", fontsize=9.5,
                 color=INK, loc="left")
    ax.legend(fontsize=7.2, frameon=False, loc="upper right")
    _style(ax)

    ax = axes[1]
    years = np.arange(len(R["paths"]["sweep_0.2"])) / 12.0
    for key, colour, label in (("sweep_0.1", GREEN, "capability passes a task in 10 years"),
                               ("sweep_0.2", BLUE, "in 5 years"),
                               ("sweep_1", AMBER, "in 1 year")):
        ax.plot(years, R["paths"][key], color=colour, lw=1.9, label=label)
    ax.plot(years, R["paths"]["noncognitive_0.10"], color=RED, lw=1.9, ls="--",
            label="in 1 year, but a tenth of new tasks\nneed more than reasoning")
    ax.set_xlim(0, 120)
    ax.set_xlabel("years", fontsize=9)
    ax.set_ylabel("share of tasks held by people", fontsize=8.5)
    ax.set_ylim(0, 1.02)
    ax.set_title("b. an always-nonempty frontier, a vanishing share",
                 fontsize=9.5, color=INK, loc="left")
    ax.legend(fontsize=6.8, frameon=False, loc="upper right")
    _style(ax)

    ax = axes[2]
    for arrival, colour, marker in zip(R["arrivals"], (GRAY, BLUE, AMBER),
                                       ("o", "s", "^")):
        ax.scatter([arrival["arrival_rate"]], [arrival["final_share"]],
                   color=colour, s=64, marker=marker,
                   label=f"{arrival['arrival_rate']:g} new tasks a year")
    ax.axhline(R["share_at_turnover_5_sweep_20"], color=RED, lw=1.2, ls="--")
    ax.text(1.4, R["share_at_turnover_5_sweep_20"] + 0.012,
            "the limit, $\\delta/(a+\\delta)$", fontsize=8, color=RED)
    ax.set_xscale("log")
    ax.set_xlim(0.5, 250)
    ax.set_ylim(0.15, 0.25)
    ax.set_xlabel("rate at which new tasks appear", fontsize=9)
    ax.set_ylabel("share of tasks held by people", fontsize=8.5)
    ax.set_title("c. more new work changes nothing", fontsize=9.5, color=INK,
                 loc="left")
    ax.legend(fontsize=7.2, frameon=False, loc="lower right")
    _style(ax)

    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def plot_fallback(res, path):
    F = res["fallback"]
    fig, axes = plt.subplots(1, 3, figsize=(12.2, 3.6),
                             gridspec_kw={"width_ratios": [1.15, 1.0, 1.0]})

    ax = axes[0]
    names = ["human", "second system", "safe state"]
    colours = [BLUE, AMBER, GRAY]
    codes = np.array([[names.index(cell) for cell in row] for row in F["surface"]])
    ax.imshow(codes, origin="lower", aspect="auto", interpolation="nearest",
              cmap=ListedColormap(colours), vmin=0, vmax=2,
              extent=[F["dependence_grid"][0], F["dependence_grid"][-1],
                      F["capability_grid"][0], F["capability_grid"][-1]])
    ax.set_xlabel("share of the primary's failures the second system also fails on",
                  fontsize=8)
    ax.set_ylabel("capability of the second system", fontsize=8.5)
    ax.set_title("a. which fallback is right", fontsize=9.5, color=INK, loc="left")
    ax.legend(handles=[Patch(color=c, label=n) for c, n in zip(colours, names)],
              fontsize=7.2, frameon=False, loc="lower left")
    ax.grid(False)

    ax = axes[1]
    shares = [d["routine_automated"] for d in F["decay"]]
    ax.plot(shares, [d["human_conditional"] for d in F["decay"]], color=BLUE,
            lw=2.0, marker="o", ms=4.6, label="a responder who has stopped practising")
    ax.axhline(F["safe_state"], color=GRAY, lw=1.6, ls="--",
               label="containment, no diagnosis")
    cross = F["routine_share_at_which_a_person_loses_to_containment"]
    ax.axvline(cross, color=RED, lw=1.0, ls=":")
    ax.text(cross + 0.02, 0.68, f"crosses at {cross:.0%}\nof routine incidents\nautomated",
            fontsize=7.4, color=RED)
    ax.set_xlabel("share of routine incidents handled automatically", fontsize=8.6)
    ax.set_ylabel("success given the primary failed", fontsize=8.5)
    ax.set_ylim(0.40, 0.72)
    ax.set_title("b. where Bainbridge's irony bites", fontsize=9.5, color=INK,
                 loc="left")
    ax.legend(fontsize=7.2, frameon=False, loc="lower left")
    _style(ax)

    ax = axes[2]
    sel = [s["rise_over_baseline"] for s in F["selection"]]
    deg = [d["rise_over_baseline"] for d in F["degradation"]]
    ax.plot(shares, sel, color=AMBER, lw=2.0, marker="o", ms=4.6,
            label="harder cases, competence unchanged")
    ax.plot(shares, deg, color=RED, lw=2.0, ls="--", marker="s", ms=4.2,
            label="same cases, competence degraded")
    ax.annotate(f"{F['selection_share_of_observed_rise']:.0%} of the rise\nis case mix",
                xy=(0.75, F["selection_rise_at_75"]), xytext=(0.30, 2.05),
                fontsize=7.6, color=AMBER,
                arrowprops=dict(arrowstyle="->", color=AMBER, lw=0.9))
    ax.set_xlabel("share of routine incidents handled automatically", fontsize=8.6)
    ax.set_ylabel("mean time to resolve, relative to baseline", fontsize=8.5)
    ax.set_ylim(0.9, 2.6)
    ax.set_title("c. two explanations of the same measurement", fontsize=9.5,
                 color=INK, loc="left")
    ax.legend(fontsize=7.2, frameon=False, loc="upper left")
    _style(ax)

    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)
