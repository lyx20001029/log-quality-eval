"""
=========================================================
Project : Log Quality Evaluation and Governance
File    : evaluation.py

Description :

    日志质量评估模型性能评价模块

Output:

    evaluation_result.csv

=========================================================
"""


import os

import numpy as np
import pandas as pd

import config




class Evaluator:


    def __init__(self):


        self.score_file = config.SCORE_FILE


        self.output_dir = config.RESULT_DIR


        os.makedirs(

            self.output_dir,

            exist_ok=True

        )


        self.output_file = os.path.join(

            self.output_dir,

            "evaluation_result.csv"

        )



    # =====================================================
    # 数据读取
    # =====================================================

    def load_score(self):


        df = pd.read_csv(

            self.score_file

        )


        return df




    # =====================================================
    # 执行评价
    # =====================================================

    def run(self):


        print(

            "开始模型性能评价"

        )


        df=self.load_score()



        score=df["score"].values



        result=pd.DataFrame({

            "Metric":[

                "Mean Score",

                "Std",

                "Max Score",

                "Min Score",

                "Average Variation"

            ],


            "Value":[


                round(

                    np.mean(score),

                    4

                ),



                round(

                    np.std(score),

                    4

                ),



                round(

                    np.max(score),

                    4

                ),



                round(

                    np.min(score),

                    4

                ),



                round(

                    np.mean(

                        np.abs(

                            np.diff(score)

                        )

                    ),

                    4

                )

            ]

        })



        result.to_csv(

            self.output_file,

            index=False,

            encoding="utf-8-sig"

        )



        print(

            "模型评价完成"

        )


        print(

            "结果保存:",

            self.output_file

        )