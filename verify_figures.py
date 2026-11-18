"""
=========================================================
Project : Log Quality Evaluation and Governance
File    : verify_figures.py

Description :
    Optional helper: regenerate the six figures and check
    that they exist.  Titles, axis labels and legends are
    all Chinese; curves, colours, thresholds and data stay
    exactly as before.

    You can also simply run main.py - plotting is Step10.

Run:
    python verify_figures.py
=========================================================
"""

import os

import config
from plot import PlotExperiment


# Chinese labels used by plot.py (titles / axes only).
FIGURE_LABELS = [
    ("Fig3-14_Metric.png",   "日志质量指标变化趋势",     "窗口", "错误率"),
    ("Fig3-15_Baseline.png", "不同评价方法综合评分对比", "窗口", "综合质量评分"),
    ("Fig3-16_Ablation.png", "消融实验结果(2x2子图)",   "窗口", "评分"),
    ("Fig3-17_ARIMA.png",    "ARIMA质量评分预测结果",    "窗口", "综合质量评分"),
    ("Fig3-18_Quality.png",  "日志质量综合评分变化趋势", "窗口", "综合质量评分"),
    ("Fig3-19_Alert.png",    "日志质量预警结果",         "窗口", "质量评分"),
]


def main():

    PlotExperiment().run()

    print("=" * 70)
    print("Figure labels | title / x-axis / y-axis / legend = Chinese")
    print("=" * 70)

    missing = []
    for name, title, xlabel, ylabel in FIGURE_LABELS:
        path = os.path.join(config.FIGURE_DIR, name)
        ok = os.path.isfile(path) and os.path.getsize(path) > 0
        if not ok:
            missing.append(name)
        print(
            "%-24s %s  %-16s x=%-4s y=%-6s" %
            (name, "OK" if ok else "MISSING", title, xlabel, ylabel)
        )

    print("-" * 70)
    print("Missing files : %s" % (", ".join(missing) if missing else "None"))
    print("RESULT: %s" % ("OK" if not missing else "CHECK THE LIST ABOVE"))
    print("Figure directory: %s" % config.FIGURE_DIR)
    print("=" * 70)

    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
