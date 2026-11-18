"""
=========================================================
Project : Log Quality Evaluation and Governance
File    : baseline.py
Author  : ChatGPT

Description :
    Baseline对比实验优化版

    对应论文:
    3.6.8 Baseline对比实验

Output:
    baseline.csv
    baseline_sample.csv
    baseline_mean.csv
    Table3-11_Baseline.csv

=========================================================
"""


import os

import numpy as np
import pandas as pd

import config




class BaselineExperiment:



    def __init__(self):


        self.metric_file = config.METRIC_FILE

        self.score_file = config.SCORE_FILE


        self.output_file = config.BASELINE_FILE


        self.output_dir = os.path.dirname(

            self.output_file

        )


        os.makedirs(

            self.output_dir,

            exist_ok=True

        )


        # 人工经验权重

        self.manual_weight=np.array([

            0.40,

            0.20,

            0.25,

            0.15

        ])




    # =====================================================
    # 数据读取
    # =====================================================

    def load_metrics(self):


        return pd.read_csv(

            self.metric_file

        )



    def load_proposed(self):


        df=pd.read_csv(

            self.score_file

        )


        return df["score"].values




    # =====================================================
    # Single Indicator
    # =====================================================

    def single_indicator(
            self,
            metric
    ):


        return np.round(

            100*(1-metric["parse_rate"]),

            2

        )




    # =====================================================
    # Equal Weight
    # =====================================================

    def equal_weight(
            self,
            metric
    ):


        data=metric[[

            "parse_rate",

            "duplicate_rate",

            "drift_rate",

            "disorder_rate"

        ]].values



        score=100*(

            1-

            np.mean(

                data,

                axis=1

            )

        )


        return np.round(

            score,

            2

        )




    # =====================================================
    # Manual Weight
    # =====================================================

    def manual_weight_score(
            self,
            metric
    ):


        data=metric[[

            "parse_rate",

            "duplicate_rate",

            "drift_rate",

            "disorder_rate"

        ]].values



        score=100*(

            1-

            np.sum(

                data*self.manual_weight,

                axis=1

            )

        )


        return np.round(

            score,

            2

        )




    # =====================================================
    # 计算
    # =====================================================

    def calculate(self):


        metric=self.load_metrics()


        result=pd.DataFrame()



        result["Window"]=metric["window"]



        result["Single Indicator"]=self.single_indicator(metric)



        result["Equal Weight"]=self.equal_weight(metric)



        result["Manual Weight"]=self.manual_weight_score(metric)



        result["Proposed"]=self.load_proposed()



        return result




    # =====================================================
    # 保存完整结果
    # =====================================================

    def save_result(
            self,
            result
    ):


        result.to_csv(

            self.output_file,

            index=False,

            encoding="utf-8-sig"

        )


        print(

            "baseline.csv保存:",

            self.output_file

        )




    # =====================================================
    # 生成趋势采样数据
    # 用于论文图3-15
    # =====================================================

    def save_sample(
            self,
            result
    ):


        length=len(result)



        # 控制显示点数量

        step=max(

            length//20,

            1

        )


        sample=result.iloc[::step]



        sample.to_csv(

            os.path.join(

                self.output_dir,

                "baseline_sample.csv"

            ),

            index=False,

            encoding="utf-8-sig"

        )



        print(

            "baseline趋势采样完成"

        )




    # =====================================================
    # 平均统计
    # 用于柱状图
    # =====================================================

    def save_mean(
            self,
            result
    ):


        methods=[

            "Single Indicator",

            "Equal Weight",

            "Manual Weight",

            "Proposed"

        ]



        mean=pd.DataFrame({

            "Method":methods,


            "Mean Score":[

                result[x].mean()

                for x in methods

            ]

        })



        mean.to_csv(

            os.path.join(

                self.output_dir,

                "baseline_mean.csv"

            ),

            index=False,

            encoding="utf-8-sig"

        )




    # =====================================================
    # 表3-11
    # =====================================================

    def statistics(
            self,
            result
    ):


        methods=[

            "Single Indicator",

            "Equal Weight",

            "Manual Weight",

            "Proposed"

        ]


        table=[]



        for m in methods:


            table.append({

                "Method":m,

                "Mean":

                    round(

                        result[m].mean(),

                        4

                    ),


                "Std":

                    round(

                        result[m].std(),

                        4

                    ),


                "Max":

                    round(

                        result[m].max(),

                        4

                    ),


                "Min":

                    round(

                        result[m].min(),

                        4

                    )

            })


        df=pd.DataFrame(table)



        df.to_csv(

            os.path.join(

                self.output_dir,

                "Table3-11_Baseline.csv"

            ),

            index=False,

            encoding="utf-8-sig"

        )



    # =====================================================
    # run
    # =====================================================

    def run(self):


        print(

            "开始Baseline实验"

        )


        result=self.calculate()



        self.save_result(

            result

        )


        self.save_sample(

            result

        )


        self.save_mean(

            result

        )


        self.statistics(

            result

        )



        print(

            "Baseline实验完成"

        )





if __name__=="__main__":


    model=BaselineExperiment()


    model.run()