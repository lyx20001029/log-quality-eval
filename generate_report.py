"""
=========================================================
Project : Log Quality Evaluation and Governance
File    : generate_report.py

Description :

    自动生成论文第三章实验分析文本

Function:

    1. Baseline结果分析
    2. Ablation结果分析
    3. ARIMA预测误差分析

Output:

    Report/
        Chapter3_Experiment_Report.txt

=========================================================
"""


import os
import pandas as pd
import numpy as np

import config



class ExperimentReportGenerator:


    def __init__(self):


        self.data_dir = os.path.dirname(
            config.SCORE_FILE
        )


        self.result_dir = os.path.join(

            self.data_dir,

            "experiment_result"

        )


        self.table_dir=os.path.join(

            self.result_dir,

            "Tables"

        )


        self.csv_dir=os.path.join(

            self.result_dir,

            "CSV"

        )


        self.report_dir=os.path.join(

            self.result_dir,

            "Report"

        )


        os.makedirs(

            self.report_dir,

            exist_ok=True

        )



        self.output_file=os.path.join(

            self.report_dir,

            "Chapter3_Experiment_Report.txt"

        )



    # =====================================================
    # Baseline分析
    # =====================================================

    def baseline_analysis(self):


        file=os.path.join(

            self.table_dir,

            "Table3-11_Baseline.csv"

        )


        if not os.path.exists(file):

            return "Baseline实验数据不存在。\n"



        df=pd.read_csv(file)



        proposed=df[

            df["Method"]=="Proposed"

        ]["Mean"].values[0]



        manual=df[

            df["Method"]=="Manual Weight"

        ]["Mean"].values[0]



        equal=df[

            df["Method"]=="Equal Weight"

        ]["Mean"].values[0]



        improve_manual=(

            proposed-manual

        )/manual*100



        improve_equal=(

            proposed-equal

        )/equal*100



        text=f"""

3.6.1 Baseline方法对比分析

为了验证本文日志质量评估模型的有效性，
分别与Single Indicator、Equal Weight、
Manual Weight方法进行对比实验。


实验结果表明，本文提出的方法（Proposed）
平均质量评分达到 {proposed:.4f}。


相比Manual Weight方法，
平均评分提升 {improve_manual:.2f}%。


相比Equal Weight方法，
平均评分提升 {improve_equal:.2f}%。


说明基于FAHP的权重计算方法能够更加合理地
描述不同日志质量指标的重要程度，
提高综合质量评价结果的准确性。


"""


        return text



    # =====================================================
    # 消融分析
    # =====================================================

    def ablation_analysis(self):


        file=os.path.join(

            self.table_dir,

            "Table3-12_Ablation.csv"

        )


        if not os.path.exists(file):

            return "消融实验数据不存在。\n"



        df=pd.read_csv(file)



        full=df[

            df["Method"]=="Full Model"

        ]["Mean"].values[0]



        text="""

3.6.2 消融实验分析


为了进一步分析模型各组成模块的贡献，
分别移除FAHP权重模块、多指标融合模块以及评分融合模块。


"""


        for method in [

            "w/o FAHP",

            "w/o Multi-Metric",

            "w/o Score Fusion"

        ]:


            value=df[

                df["Method"]==method

            ]["Mean"].values[0]



            drop=(

                full-value

            )/full*100



            text+=f"""

去除{method}后，
模型平均评分下降至{value:.4f}，
相较完整模型下降{drop:.2f}%。


"""



        text+="""


实验结果说明：

FAHP权重计算、多维指标融合以及评分融合机制
均能够提升日志质量评价模型的稳定性和有效性。


"""


        return text



    # =====================================================
    # ARIMA分析
    # =====================================================

    def arima_analysis(self):


        file=os.path.join(

            self.csv_dir,

            "arima_error.csv"

        )


        if not os.path.exists(file):

            return "ARIMA实验数据不存在。\n"



        df=pd.read_csv(file)



        mae=df["Error"].mean()



        rmse=np.sqrt(

            np.mean(

                df["Error"]**2

            )

        )



        text=f"""

3.6.3 日志质量趋势预测分析


采用ARIMA模型对日志质量变化趋势进行预测。


实验结果显示：

测试阶段平均绝对误差（MAE）为：

{mae:.4f}


均方根误差（RMSE）为：

{rmse:.4f}


预测结果表明，
ARIMA模型能够较好地捕获日志质量变化趋势，
为后续质量异常预警提供有效的数据支持。


"""


        return text



    # =====================================================
    # 保存报告
    # =====================================================

    def save(self,text):


        with open(

            self.output_file,

            "w",

            encoding="utf-8"

        ) as f:


            f.write(text)



        print(

            "报告生成:",

            self.output_file

        )



    # =====================================================
    # run
    # =====================================================

    def run(self):


        print("="*60)

        print(

            "开始生成论文实验分析报告"

        )


        report="""

《日志数据质量评估与量化模型的研究》

第三章 实验结果分析辅助文本

======================================

"""


        report+=self.baseline_analysis()

        report+=self.ablation_analysis()

        report+=self.arima_analysis()



        self.save(

            report

        )


        print("="*60)





if __name__=="__main__":


    generator=ExperimentReportGenerator()


    generator.run()