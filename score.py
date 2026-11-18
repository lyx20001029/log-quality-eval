"""
=========================================================
Project : Log Quality Evaluation and Governance
File    : score.py
Author  : ChatGPT
Description : 综合评分计算（论文最终版）

新增：
    1. 质量趋势分析
    2. 滑动平均曲线
    3. 质量阶段划分

=========================================================
"""

import numpy as np
import pandas as pd

import config


class ScoreCalculator:

    def __init__(self):

        self.metric_file = config.METRIC_FILE

        self.weight_file = config.WEIGHT_FILE

        self.output_file = config.SCORE_FILE


    # =====================================================
    # 读取数据
    # =====================================================

    def load_metrics(self):

        return pd.read_csv(
            self.metric_file
        )


    def load_weights(self):

        weight_df = pd.read_csv(
            self.weight_file
        )

        return weight_df["Weight"].values



    # =====================================================
    # 综合评分
    #
    # Score = 100 × (1 - Σ(wi × xi))
    # =====================================================

    def calculate_score(
            self,
            metrics,
            weight
    ):


        score = []

        contribution = []


        for _, row in metrics.iterrows():


            indicator = np.array([

                row["parse_rate"],

                row["duplicate_rate"],

                row["drift_rate"],

                row["disorder_rate"]

            ])


            defect = np.sum(

                weight * indicator

            )


            s = config.FULL_SCORE * (

                1 - defect

            )


            s = max(

                config.MIN_SCORE,

                s

            )


            score.append(

                round(s, 2)

            )


            contribution.append(

                weight * indicator

            )


        metrics["score"] = score


        metrics["grade"] = (

            metrics["score"]

            .apply(self.grade)

        )



        metrics["parse_contribution"] = [

            round(c[0],4)

            for c in contribution

        ]


        metrics["duplicate_contribution"] = [

            round(c[1],4)

            for c in contribution

        ]


        metrics["drift_contribution"] = [

            round(c[2],4)

            for c in contribution

        ]


        metrics["disorder_contribution"] = [

            round(c[3],4)

            for c in contribution

        ]


        return metrics




    # =====================================================
    # 等级划分
    # =====================================================

    def grade(
            self,
            score
    ):


        for threshold, level in config.GRADE_RULE:


            if score >= threshold:

                return level


        return "危险"




    # =====================================================
    # 主导缺陷分析
    # =====================================================

    def analyse_defect(
            self,
            df
    ):


        dominant = []


        for _, row in df.iterrows():


            value = {


                "解析失败率":
                    row["parse_contribution"],


                "重复率":
                    row["duplicate_contribution"],


                "漂移率":
                    row["drift_contribution"],


                "乱序率":
                    row["disorder_contribution"]

            }


            dominant.append(

                max(

                    value,

                    key=value.get

                )

            )


        df["dominant_defect"] = dominant


        return df




    # =====================================================
    # 质量趋势分析
    #
    # 用于 Fig3-18
    # =====================================================

    def analyse_trend(
            self,
            df
    ):


        # -----------------------------
        # 滑动平均
        # -----------------------------

        df["smooth_score"] = (

            df["score"]

            .rolling(

                window=10,

                min_periods=1

            )

            .mean()

            .round(2)

        )



        # -----------------------------
        # 质量阶段划分
        # -----------------------------

        def stage(score):


            if score >= 90:

                return "稳定阶段"


            elif score >= 80:

                return "下降阶段"


            elif score >= 70:

                return "波动阶段"


            else:

                return "风险阶段"



        df["quality_stage"] = (

            df["score"]

            .apply(stage)

        )


        return df





    # =====================================================
    # 保存
    # =====================================================

    def save(
            self,
            df
    ):


        df.to_csv(

            self.output_file,

            index=False,

            encoding="utf-8-sig"

        )


        print()

        print(config.LINE)

        print("综合评分计算完成")

        print(self.output_file)

        print(config.LINE)




    # =====================================================
    # 输出统计
    # =====================================================

    def summary(
            self,
            df
    ):


        print()

        print("========== 综合评分统计 ==========")


        print(

            "窗口数：",

            len(df)

        )


        print()


        print(

            "平均得分：",

            round(

                df["score"].mean(),

                2

            )

        )


        print(

            "最高得分：",

            round(

                df["score"].max(),

                2

            )

        )


        print(

            "最低得分：",

            round(

                df["score"].min(),

                2

            )

        )


        print()


        print("等级统计：")


        print(

            df["grade"]

            .value_counts()

        )


        print()


        print("主导缺陷统计：")


        print(

            df["dominant_defect"]

            .value_counts()

        )


        print()




    # =====================================================
    # 导出论文表3-10
    # =====================================================

    def export_table(
            self,
            df
    ):


        table = df[[


            "window",

            "parse_rate",

            "duplicate_rate",

            "drift_rate",

            "disorder_rate",

            "score",

            "grade"


        ]]


        table.to_csv(

            config.TABLE310,

            index=False,

            encoding="utf-8-sig"

        )





    # =====================================================
    # Run
    # =====================================================

    def run(self):


        metric = self.load_metrics()


        weight = self.load_weights()



        # 评分

        result = self.calculate_score(

            metric,

            weight

        )



        # 缺陷分析

        result = self.analyse_defect(

            result

        )



        # 趋势分析（新增）

        result = self.analyse_trend(

            result

        )



        # 保存

        self.save(

            result

        )



        self.summary(

            result

        )



        self.export_table(

            result

        )


        return result




if __name__ == "__main__":


    ScoreCalculator().run()