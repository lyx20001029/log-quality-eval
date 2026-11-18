"""
=========================================================
Project : Log Quality Evaluation and Governance
File    : arima_predict.py

Description :
    基于ARIMA的日志质量趋势预测

    对应论文:
    日志质量预测与预警实验

Output:

    arima_prediction.csv
    arima_test_result.csv
    arima_error.csv

=========================================================
"""


import os
import warnings

import numpy as np
import pandas as pd


from statsmodels.tsa.arima.model import ARIMA


import config



warnings.filterwarnings(
    "ignore"
)




class ARIMAPredictor:



    def __init__(self):


        self.score_file=config.SCORE_FILE



        self.output_dir=os.path.dirname(

            self.score_file

        )



        self.predict_file=os.path.join(

            self.output_dir,

            "arima_prediction.csv"

        )


        self.test_file=os.path.join(

            self.output_dir,

            "arima_test_result.csv"

        )


        self.error_file=os.path.join(

            self.output_dir,

            "arima_error.csv"

        )


        # 论文采用ARIMA(1,1,1)

        self.order=(

            1,

            1,

            1

        )



        # 训练比例

        self.train_ratio=0.7




    # =====================================================
    # 数据读取
    # =====================================================

    def load_score(self):


        return pd.read_csv(

            self.score_file

        )




    # =====================================================
    # ARIMA训练
    # =====================================================

    def train(
            self,
            data
    ):


        model=ARIMA(

            data,

            order=self.order,

            enforce_stationarity=False,

            enforce_invertibility=False

        )


        result=model.fit()



        return result




    # =====================================================
    # 预测
    # =====================================================

    def predict(
            self,
            history
    ):
        model = self.train(
            history
        )

        pred = model.forecast(
            steps=1
        )

        return float(
            pred.iloc[0]
            if hasattr(pred, "iloc")
            else pred[0]
        )




    # =====================================================
    # 误差
    # =====================================================

    def error(
            self,
            real,
            pred
    ):


        return np.abs(

            real-pred

        )




    # =====================================================
    # 保存
    # =====================================================

    def save(
            self,
            df,
            path
    ):


        df.to_csv(

            path,

            index=False,

            encoding="utf-8-sig"

        )



        print(

            "保存:",

            path

        )





    # =====================================================
    # 主流程
    # =====================================================

    def run(self):


        print(

            "="*60

        )


        print(

            "开始ARIMA预测实验"

        )


        df=self.load_score()



        score=df["score"].values



        window=df["window"].values



        length=len(score)



        train_size=int(

            length*self.train_ratio

        )



        train=score[:train_size]


        test=score[train_size:]



        test_window=window[train_size:]




        # -----------------------
        # 测试预测
        # -----------------------

        # -----------------------
        # 滚动一步预测
        # -----------------------

        pred = []

        history = list(train)

        for i in range(len(test)):
            yhat = self.predict(

                history

            )

            pred.append(

                yhat

            )

            # 更新历史数据

            history.append(

                test[i]

            )

        pred = np.array(

            pred

        )




        error=self.error(

            test,

            pred

        )





        # -----------------------
        # 完整结果
        # -----------------------


        result=pd.DataFrame({


            "Window":window,


            "Real Score":score,


            "Prediction":

                np.concatenate(

                    [

                        np.full(

                            train_size,

                            np.nan

                        ),

                        pred

                    ]

                ),



            "Type":

                [

                    "Train"

                ]*train_size+

                [

                    "Prediction"

                ]*len(test)

        })



        self.save(

            result,

            self.predict_file

        )





        # -----------------------
        # 测试结果
        # -----------------------


        test_result=pd.DataFrame({


            "Window":test_window,


            "Real Score":test,


            "Prediction":pred


        })


        self.save(

            test_result,

            self.test_file

        )




        error_df=pd.DataFrame({


            "Window":test_window,


            "Error":error


        })


        self.save(

            error_df,

            self.error_file

        )



        print(

            "ARIMA预测完成"

        )


        print(

            "="*60

        )





if __name__=="__main__":


    model=ARIMAPredictor()


    model.run()