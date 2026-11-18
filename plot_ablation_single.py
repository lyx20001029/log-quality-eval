"""重绘消融实验图：由 2x2 四子图改为单图四曲线对比。

- 数据源：result/ablation.csv（真实实验结果）
- 中文标题、中文坐标轴、中文图例
- 图例中标注各组均值 +/- 标准差（样本标准差，与原 Table3-12 口径一致）
- 固定 figsize，不使用 bbox_inches='tight'，保证比例稳定便于等比替换论文图片
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.abspath(__file__))
RESULT = os.path.join(ROOT, "result")
FIGURE = os.path.join(ROOT, "res_new")

plt.rcParams["font.family"] = "SimHei"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.size"] = 14

df = pd.read_csv(os.path.join(RESULT, "ablation.csv"))
x = df["Window"].values

# (列名, 中文图例, 颜色)
series = [
    ("Full Model",       "完整模型",       "#2F5597"),
    ("w/o FAHP",         "去除FAHP权重",   "#C00000"),
    ("w/o Multi-Metric", "去除多指标融合", "#548235"),
    ("w/o Score Fusion", "去除评分融合",   "#BF8F00"),
]

fig, ax = plt.subplots(figsize=(12, 8), dpi=200)

for col, label, color in series:
    vals = df[col].values.astype(float)
    mean = float(np.mean(vals))
    std = float(np.std(vals, ddof=1))
    ax.plot(x, vals, color=color, linewidth=2.0, alpha=0.92,
            label="%s（%0.2f±%0.2f）" % (label, mean, std))

ax.set_title("消融实验结果", fontsize=22, pad=18, fontweight="bold")
ax.set_xlabel("窗口序号", fontsize=17)
ax.set_ylabel("综合质量评分", fontsize=17)
ax.tick_params(axis="both", labelsize=13)
ax.grid(linestyle="--", alpha=0.35)
ax.set_axisbelow(True)
ax.legend(loc="lower left", fontsize=14, framealpha=0.92, ncol=2)

for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)

fig.subplots_adjust(left=0.09, right=0.97, top=0.92, bottom=0.11)

out = os.path.join(FIGURE, "Fig3-16_Ablation_single.png")
fig.savefig(out, dpi=200, facecolor="white")
plt.close(fig)

im = plt.imread(out)
print("saved:", out, "size:", im.shape[1], "x", im.shape[0],
      "ratio: %.4f" % (im.shape[1] / im.shape[0]))
for col, label, _ in series:
    v = df[col].values.astype(float)
    print("  %-16s mean=%.3f std=%.3f" % (label, np.mean(v), np.std(v, ddof=1)))
