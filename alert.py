"""
=========================================================
Project : Log Quality Evaluation and Governance

File    : alert.py

Description :

    日志质量预警模块

    根据质量评分变化趋势，
    检测异常下降窗口

Output:

    alert.csv

=========================================================
"""


import os

import pandas as pd

import config




class AlertGenerator:


    def __init__(self):


        self.score_file = config.SCORE_FILE


        self.output_file = config.ALERT_FILE


        self.threshold = config.ALERT_THRESHOLD



    # =====================================================
    # 读取评分数据
    # =====================================================

    def load_score(self):


        return pd.read_csv(

            self.score_file

        )



    # =====================================================
    # 预警计算
    # =====================================================

    def generate(self, df):


        score = df["score"]


        alert=[]



        for i,value in enumerate(score):


            # 第一个窗口没有变化

            if i==0:

                alert.append(
                    "Normal"
                )

                continue



            decrease = score[i-1]-value



            if decrease >= self.threshold:


                alert.append(
                    "Warning"
                )


            else:


                alert.append(
                    "Normal"
                )



        result=pd.DataFrame({


            "Window":

                df["window"],



            "Score":

                df["score"],



            "Alert":

                alert



        })


        return result



    # =====================================================
    # 保存
    # =====================================================

    def save(self,df):


        df.to_csv(

            self.output_file,

            index=False,

            encoding="utf-8-sig"

        )


        print(

            "预警结果保存:",

            self.output_file

        )



    # =====================================================
    # 统计
    # =====================================================

    def summary(self,df):


        print()

        print(
            "========== 预警统计 =========="
        )


        print(

            df["Alert"].value_counts()

        )


        print()



    # =====================================================
    # Run
    # =====================================================

    def run(self):


        print(

            "开始日志质量预警分析"

        )


        df=self.load_score()


        result=self.generate(df)


        self.save(result)


        self.summary(result)


        return result





if __name__=="__main__":


    model=AlertGenerator()


    model.run()