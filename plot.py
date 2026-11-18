"""
=========================================================
Project : Log Quality Evaluation and Governance
File    : plot.py

Description :
    论文实验结果可视化模块

    图3-14 指标变化趋势
    图3-15 Baseline方法对比
    图3-16 消融实验
    图3-17 ARIMA预测
    图3-18 日志质量趋势
    图3-19 日志质量预警

Author : ChatGPT
=========================================================
"""

import warnings
warnings.filterwarnings("ignore")

import os

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib

import config

matplotlib.rcParams["font.family"] = config.FONT_FAMILY
matplotlib.rcParams["axes.unicode_minus"] = False

# ---------------------------------------------------------
# Chinese legend labels.  Keys are the ORIGINAL English
# strings, which are also CSV column names / data keys.
# Only the text shown in the legend is translated.
# ---------------------------------------------------------
LEGEND_CN = {
    "Parse Failure Rate": "解析失败率",
    "Duplicate Rate": "重复率",
    "Drift Rate": "漂移率",
    "Disorder Rate": "乱序率",
    "Single Indicator": "单指标法",
    "Equal Weight": "等权重法",
    "Manual Weight": "人工赋权法",
    "Proposed": "本文方法（FAHP）",
    "Full Model": "完整模型",
    "w/o FAHP": "去除 FAHP",
    "w/o Multi-Metric": "去除多指标",
    "w/o Score Fusion": "去除分数融合",
    "Real Score": "真实得分",
    "ARIMA Prediction": "ARIMA 预测值",
    "Train/Test Split": "训练/测试分界",
    "Quality Score": "质量评分",
    "Average": "平均值",
    "Good Threshold": "良好阈值",
    "Warning Threshold": "预警阈值",
    "Warning Window": "预警窗口",
}


plt.rcParams["font.size"] = 12


class PlotExperiment:
    """
    论文实验绘图
    """

    def __init__(self):

        print(config.LINE)
        print("Loading experiment results...")
        print(config.LINE)

        self.result_dir = config.RESULT_DIR
        self.figure_dir = config.FIGURE_DIR

        os.makedirs(
            self.figure_dir,
            exist_ok=True
        )

        self.metrics = self.load_csv("metrics.csv")
        self.score = self.load_csv("score.csv")
        self.baseline = self.load_csv("baseline.csv")
        self.ablation = self.load_csv("ablation.csv")
        self.predict = self.load_csv("arima_prediction.csv")
        self.error = self.load_csv("arima_error.csv")
        self.alert = self.load_csv("alert.csv")

        print(config.LINE)
        print("Experiment data loaded.")
        print(config.LINE)

    # =====================================================
    # CSV读取
    # =====================================================

    def load_csv(self, filename):

        path = os.path.join(
            self.result_dir,
            filename
        )

        if not os.path.exists(path):

            print(f"[Missing] {filename}")

            return pd.DataFrame()

        df = pd.read_csv(path)

        print(
            f"{filename:<25} {df.shape}"
        )

        return df

    # =====================================================
    # 保存图片
    # =====================================================

    def save_fig(self, filename):

        save_path = os.path.join(
            self.figure_dir,
            filename
        )

        plt.tight_layout()

        plt.savefig(
            save_path,
            dpi=config.DPI,
            bbox_inches="tight"
        )

        plt.close()

        print(
            f"Saved -> {save_path}"
        )

    # =====================================================
    # 获取窗口
    # =====================================================

    def get_window(self, df):

        if "Window" in df.columns:
            return df["Window"]

        if "window" in df.columns:
            return df["window"]

        return np.arange(
            1,
            len(df) + 1
        )

    # =====================================================
    # 统一绘图格式
    # =====================================================

    def init_figure(self):

        plt.figure(
            figsize=config.FIG_SIZE
        )

    def finish_figure(
            self,
            xlabel,
            ylabel,
            title
    ):

        plt.xlabel(xlabel)

        plt.ylabel(ylabel)

        plt.title(title)

        plt.grid(
            linestyle="--",
            alpha=config.GRID_ALPHA
        )

        plt.legend()

    # =====================================================
    # 图3-14
    # 指标变化趋势
    # =====================================================

    def plot_metric(self):

        if self.metrics.empty:
            return

        self.init_figure()

        x = self.get_window(self.metrics)

        cols = [
            "parse_rate",
            "duplicate_rate",
            "drift_rate",
            "disorder_rate"
        ]

        labels = [
            "Parse Failure Rate",
            "Duplicate Rate",
            "Drift Rate",
            "Disorder Rate"
        ]

        for col, label in zip(cols, labels):

            if col not in self.metrics.columns:
                continue

            y = (
                self.metrics[col]
                .rolling(
                    window=10,
                    center=True
                )
                .mean()
            )

            plt.plot(
                x,
                y,
                linewidth=2,
                label=LEGEND_CN.get(label, label)
            )

        plt.xlabel("窗口")

        plt.ylabel("错误率")

        plt.title(
            "日志质量指标变化趋势"
        )

        plt.grid(
            linestyle="--",
            alpha=0.25
        )

        plt.legend(
            frameon=False
        )

        plt.ylim(
            0,
            self.metrics[cols].max().max() * 1.15
        )

        self.save_fig(
            "Fig3-14_Metric.png"
        )

    # =====================================================
    # 图3-15 Baseline方法对比
    # =====================================================

    def plot_baseline(self):

        if self.baseline.empty:
            return

        self.init_figure()

        x = self.get_window(self.baseline)

        models = [
            "Single Indicator",
            "Equal Weight",
            "Manual Weight",
            "Proposed"
        ]

        # 论文图3-2：四条原始评分曲线，不做平滑
        for model in models:

            if model not in self.baseline.columns:
                continue

            lw = 3 if model == "Proposed" else 1.8

            plt.plot(
                x,
                self.baseline[model],
                linewidth=lw,
                label=LEGEND_CN.get(model, model)
            )

        plt.xlabel("窗口")
        plt.ylabel("综合质量评分")
        plt.title("不同评价方法综合评分对比")
        plt.grid(linestyle="--", alpha=0.25)
        plt.legend(frameon=False, loc="upper right")
        plt.ylim(58, 102)

        self.save_fig("Fig3-15_Baseline.png")

    # =====================================================
    # 图3-16 消融实验
    # =====================================================

    def plot_ablation(self):

        if self.ablation.empty:
            return

        x = self.get_window(self.ablation)

        # 论文图3-3：2x2 四个子图，前三组模型 + 第四组独立指标分数
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        axs = axes.ravel()

        panels = [
            ("Full Model",        "完整模型"),
            ("w/o FAHP",          "去除FAHP：等权重"),
            ("w/o Multi-Metric",  "去除多指标融合")
        ]

        for ax, (col, title) in zip(axs[:3], panels):

            if col in self.ablation.columns:
                ax.plot(x, self.ablation[col], linewidth=1.4, color="#4C72B0")

            ax.set_title(title, fontsize=12)
            ax.set_xlabel("窗口")
            ax.set_ylabel("评分")
            ax.grid(linestyle="--", alpha=0.3)

        ax4 = axs[3]
        rate_cols = [
            "parse_rate",
            "duplicate_rate",
            "drift_rate",
            "disorder_rate"
        ]
        rate_labels = [
            "解析失败率",
            "重复率",
            "漂移率",
            "乱序率"
        ]

        # 不做评分融合时，四项独立指标的质量分数 = 100*(1-指标率)
        if not self.metrics.empty:
            mx = self.get_window(self.metrics)
            for col, label in zip(rate_cols, rate_labels):
                if col in self.metrics.columns:
                    ax4.plot(
                        mx,
                        100 * (1 - self.metrics[col]),
                        linewidth=1.0,
                        label=label
                    )
            ax4.legend(fontsize=9, loc="lower left")

        ax4.set_title("去除评分融合：独立指标", fontsize=12)
        ax4.set_xlabel("窗口")
        ax4.set_ylabel("评分")
        ax4.grid(linestyle="--", alpha=0.3)

        fig.suptitle("消融实验结果", fontsize=14)
        fig.tight_layout()

        save_path = os.path.join(self.figure_dir, "Fig3-16_Ablation.png")
        fig.savefig(save_path, dpi=config.DPI, bbox_inches="tight")
        plt.close(fig)
        print("Saved -> %s" % save_path)

    # =====================================================
    # 图3-17
    # ARIMA预测
    # =====================================================

    def plot_arima(self):

        if self.predict.empty:
            return

        self.init_figure()

        x = self.get_window(self.predict)

        if "Real Score" in self.predict.columns:
            real = self.predict["Real Score"]
        elif "True" in self.predict.columns:
            real = self.predict["True"]
        else:
            real = None

        # 论文图3-4：只展示留出法的 60 个测试窗口
        split = int(len(x) * 0.7)
        x_test = x.iloc[split:]

        if real is not None:
            plt.plot(
                x_test, real.iloc[split:],
                linewidth=1.5,
                label=LEGEND_CN["Real Score"]
            )

        if "Prediction" in self.predict.columns:
            pred = self.predict["Prediction"]
        elif "Predict" in self.predict.columns:
            pred = self.predict["Predict"]
        else:
            pred = None

        if pred is not None:
            plt.plot(
                x_test, pred.iloc[split:],
                linewidth=3.0,
                linestyle="-",
                label=LEGEND_CN["ARIMA Prediction"]
            )

        plt.axvline(
            x.iloc[split],
            linestyle="--",
            linewidth=1.5,
            alpha=0.6,
            label=LEGEND_CN["Train/Test Split"]
        )

        plt.xlim(x.iloc[split] - 1, x.max())

        self.finish_figure(
            "窗口",
            "综合质量评分",
            "ARIMA质量评分预测结果"
        )

        self.save_fig("Fig3-17_ARIMA.png")

        # =====================================================
        # 图3-18
        # 日志质量趋势
        # =====================================================

    def plot_quality(self):

        print("绘制日志质量趋势图")

        df = pd.read_csv(config.SCORE_FILE)

        window = df["window"]
        score = df["score"]

        plt.figure(figsize=(10, 5))

        # 论文图3-5：只保留一条综合评分曲线，无参考线与图例
        plt.plot(window, score, linewidth=1.6, color="#4C72B0")

        plt.xlabel("窗口")
        plt.ylabel("综合质量评分")
        plt.title("日志质量综合评分变化趋势")
        plt.grid(linestyle="--", alpha=0.3)
        plt.ylim(65, 101)
        plt.tight_layout()

        plt.savefig(
            os.path.join(config.FIGURE_DIR, "Fig3-18_Quality.png"),
            dpi=300,
            bbox_inches="tight"
        )
        plt.close()

    # =====================================================
    # 图3-19
    # 日志质量预警
    # =====================================================

    def plot_alert(self):

            if self.alert.empty:
                return

            self.init_figure()

            # ===============================
            # Window
            # ===============================

            x = self.get_window(
                self.alert
            )

            # ===============================
            # Score
            # ===============================

            if "Score" in self.alert.columns:

                score = self.alert["Score"]


            elif "score" in self.alert.columns:

                score = self.alert["score"]


            else:

                return

            # ===============================
            # 质量趋势曲线
            # ===============================

            plt.plot(
                x,
                score,
                linewidth=1.8,
                color="#4C72B0",
                label=LEGEND_CN["Quality Score"]
            )

            # ===============================
            # Alert字段
            # ===============================

            if "Alert" in self.alert.columns:

                alert = self.alert["Alert"]


            elif "alert" in self.alert.columns:

                alert = self.alert["alert"]


            else:

                alert = pd.Series(

                    ["Normal"] * len(self.alert)

                )

            # ===============================
            # 找Warning窗口
            # ===============================

            if alert.dtype == "object":

                warning_mask = (

                    alert

                    .astype(str)

                    .str.contains(

                        "Warning",

                        case=False

                    )

                )


            else:

                warning_mask = (

                        alert > 0

                )

            warning_windows = x[warning_mask]

            # ===============================
            # 绘制预警标记
            # ===============================

            warning_label = True

            # ===============================
            # 红色预警点标记
            # ===============================

            warning_scores = score[warning_mask]

            plt.scatter(

                warning_windows,

                warning_scores,

                s=55,

                marker="x",

                color="#C00000",

                linewidths=2,

                label=LEGEND_CN["Warning Window"],

                zorder=5

            )

            # ===============================
            # legend去重
            # ===============================

            handles, labels = plt.gca().get_legend_handles_labels()

            new_handles = []

            new_labels = []

            for h, l in zip(handles, labels):

                if l is not None and l not in new_labels:
                    new_handles.append(h)

                    new_labels.append(l)

            plt.legend(

                new_handles,

                new_labels

            )

            # ===============================
            # 保存
            # ===============================

            self.finish_figure(

                "窗口",

                "质量评分",

                "日志质量预警结果"

            )

            self.save_fig(

                "Fig3-19_Alert.png"

            )

        # =====================================================
        # 一键运行
        # =====================================================

    def run(self):

        print(config.LINE)
        print("Generating figures...")
        print(config.LINE)

        self.plot_metric()

        self.plot_baseline()

        self.plot_ablation()

        self.plot_arima()

        self.plot_quality()

        self.plot_alert()

        print(config.LINE)
        print("All figures generated.")
        print(config.LINE)

    # =========================================================
    # Main
    # =========================================================

if __name__ == "__main__":
    plotter = PlotExperiment()

    plotter.run()