"""
=========================================================
Project : Log Quality Evaluation and Governance
File    : metrics.py
Author  : ChatGPT
Description : 服务器日志质量指标计算（论文最终版）
=========================================================
"""

import os
import numpy as np
import pandas as pd

import config


class MetricsCalculator:

    def __init__(self):

        self.raw_file = config.RAW_LOG_FILE

        self.output_file = config.METRIC_FILE

        self.df = None

    # ======================================================
    # 读取日志
    # ======================================================

    def load_data(self):

        if not os.path.exists(self.raw_file):

            raise FileNotFoundError(
                "raw_log.csv不存在，请先运行generator.py"
            )

        self.df = pd.read_csv(self.raw_file)

        return self.df

    # ======================================================
    # 四项指标
    # ======================================================

    def calc_parse_rate(self, window_df):

        return window_df["parse_fail"].sum() / len(window_df)

    def calc_duplicate_rate(self, window_df):

        return window_df["duplicate"].sum() / len(window_df)

    def calc_drift_rate(self, window_df):

        return window_df["drift"].sum() / len(window_df)

    def calc_disorder_rate(self, window_df):

        return window_df["disorder"].sum() / len(window_df)

    # ======================================================
    # 证据索引
    # ======================================================

    def build_evidence(self, window_df):

        evidence = {}

        evidence["parse_logs"] = window_df[
            window_df["parse_fail"] == 1
        ]["log_id"].tolist()

        evidence["duplicate_logs"] = window_df[
            window_df["duplicate"] == 1
        ]["log_id"].tolist()

        evidence["drift_logs"] = window_df[
            window_df["drift"] == 1
        ]["log_id"].tolist()

        evidence["disorder_logs"] = window_df[
            window_df["disorder"] == 1
        ]["log_id"].tolist()

        return evidence

    # ======================================================
    # 质量等级
    # ======================================================

    def quality_level(self, score):

        for threshold, level in config.GRADE_RULE:

            if score >= threshold:

                return level

        return "危险"

    # ======================================================
    # 窗口统计
    # ======================================================

    def calculate_metrics(self):

        windows = sorted(self.df["window"].unique())

        result = []

        for window in windows:

            temp = self.df[self.df["window"] == window]

            parse_rate = self.calc_parse_rate(temp)

            duplicate_rate = self.calc_duplicate_rate(temp)

            drift_rate = self.calc_drift_rate(temp)

            disorder_rate = self.calc_disorder_rate(temp)

            evidence = self.build_evidence(temp)

            parse_num = int(temp["parse_fail"].sum())

            duplicate_num = int(temp["duplicate"].sum())

            drift_num = int(temp["drift"].sum())

            disorder_num = int(temp["disorder"].sum())

            result.append({

                "window": window,

                "log_num": len(temp),

                "parse_num": parse_num,

                "duplicate_num": duplicate_num,

                "drift_num": drift_num,

                "disorder_num": disorder_num,

                "parse_rate": round(parse_rate, 4),

                "duplicate_rate": round(duplicate_rate, 4),

                "drift_rate": round(drift_rate, 4),

                "disorder_rate": round(disorder_rate, 4),

                "parse_logs": ",".join(map(str, evidence["parse_logs"])),

                "duplicate_logs": ",".join(map(str, evidence["duplicate_logs"])),

                "drift_logs": ",".join(map(str, evidence["drift_logs"])),

                "disorder_logs": ",".join(map(str, evidence["disorder_logs"]))

            })

        metric_df = pd.DataFrame(result)

        return metric_df

        # ======================================================
        # 保存指标结果
        # ======================================================

    def save_result(self, metric_df):

        metric_df.to_csv(
            self.output_file,
            index=False,
            encoding="utf-8-sig"
        )

        print(config.LINE)
        print("窗口质量指标计算完成")
        print("结果保存：")
        print(self.output_file)
        print(config.LINE)

    # ======================================================
    # 输出统计信息
    # ======================================================

    def summary(self, metric_df):

        print()

        print("================== 指标统计 ==================")

        print("窗口数量：", len(metric_df))

        print("总日志数：", metric_df["log_num"].sum())

        print()

        print("平均解析失败率：",
                round(metric_df["parse_rate"].mean(), 4))

        print("平均重复率：",
                round(metric_df["duplicate_rate"].mean(), 4))

        print("平均漂移率：",
                round(metric_df["drift_rate"].mean(), 4))

        print("平均乱序率：",
                round(metric_df["disorder_rate"].mean(), 4))

        print()

        print("解析失败日志：",
                metric_df["parse_num"].sum())

        print("重复日志：",
                metric_df["duplicate_num"].sum())

        print("漂移日志：",
                metric_df["drift_num"].sum())

        print("乱序日志：",
                metric_df["disorder_num"].sum())

        print("==============================================")

    # ======================================================
    # 缺陷统计
    # ======================================================

    def defect_statistics(self, metric_df):

        stat = pd.DataFrame({

            "Metric": [

                "Parse Failure",

                "Duplicate",

                "Drift",

                "Disorder"

            ],

            "Average": [

                metric_df["parse_rate"].mean(),

                metric_df["duplicate_rate"].mean(),

                metric_df["drift_rate"].mean(),

                metric_df["disorder_rate"].mean()

                ],

            "Maximum": [

                metric_df["parse_rate"].max(),

                metric_df["duplicate_rate"].max(),

                metric_df["drift_rate"].max(),

                metric_df["disorder_rate"].max()

            ],

            "Minimum": [

                metric_df["parse_rate"].min(),

                metric_df["duplicate_rate"].min(),

                metric_df["drift_rate"].min(),

                metric_df["disorder_rate"].min()

            ]

        })

        stat_file = os.path.join(

            config.RESULT_DIR,

            "metric_statistics.csv"

        )

        stat.to_csv(

            stat_file,

            index=False,

            encoding="utf-8-sig"

        )

        print("指标统计保存：")

        print(stat_file)

    # ======================================================
    # 数据合法性检查
    # ======================================================

    def check(self, metric_df):

        for col in [

            "parse_rate",

            "duplicate_rate",

            "drift_rate",

            "disorder_rate"

        ]:

            if metric_df[col].max() > 1:
                raise ValueError(col + " 大于1")

            if metric_df[col].min() < 0:
                raise ValueError(col + " 小于0")

    print("指标检查通过。")

    # ======================================================
    # 主程序
    # ======================================================

    def run(self):

        self.load_data()

        metric_df = self.calculate_metrics()

        self.check(metric_df)

        self.save_result(metric_df)

        self.summary(metric_df)

        self.defect_statistics(metric_df)

        return metric_df

# ======================================================
# Main
# ======================================================
if __name__ == "__main__":
    calculator = MetricsCalculator()

    calculator.run()