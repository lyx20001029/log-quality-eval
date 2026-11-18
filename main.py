"""
=========================================================
Project : Log Quality Evaluation and Governance
File    : main.py

Description :

    日志数据质量评估与量化模型实验主程序


Pipeline:

    Step1   日志生成
    Step2   指标计算
    Step3   FAHP权重计算
    Step4   综合评分
    Step5   Baseline实验
    Step6   消融实验
    Step7   ARIMA预测实验
    Step8   模型评价
    Step9   质量预警实验
    Step10  论文图片生成
    Step11  实验结果整理


Run:

    python main.py

=========================================================
"""


import os
import warnings


warnings.filterwarnings(
    "ignore"
)



# =====================================================
# 导入模块
# =====================================================


import config


from generator import LogGenerator

from metrics import MetricsCalculator

from fahp import FAHP

from score import ScoreCalculator


from baseline import BaselineExperiment

from ablation import AblationExperiment

from arima_predict import ARIMAPredictor


from evaluation import Evaluator


from alert import AlertGenerator


from plot import PlotExperiment


from export import ExperimentExporter





# =====================================================
# 创建目录
# =====================================================


def create_dirs():


    dirs=[

        config.DATA_DIR,

        config.RESULT_DIR,

        config.FIGURE_DIR

    ]


    for d in dirs:

        if not os.path.exists(d):

            os.makedirs(d)





# =====================================================
# Step1
# 日志生成
# =====================================================


def step1_generate():


    print("="*60)

    print("Step1 生成窗口日志")

    print("="*60)


    model=LogGenerator()

    model.run()


    print()





# =====================================================
# Step2
# 指标计算
# =====================================================


def step2_metrics():


    print("="*60)

    print("Step2 计算日志质量指标")

    print("="*60)


    model=MetricsCalculator()

    model.run()


    print()





# =====================================================
# Step3
# FAHP权重计算
# =====================================================


def step3_fahp():


    print("="*60)

    print("Step3 FAHP权重计算")

    print("="*60)


    model=FAHP()

    model.run()


    print()





# =====================================================
# Step4
# 综合评分
# =====================================================


def step4_score():


    print("="*60)

    print("Step4 日志质量综合评分")

    print("="*60)


    model=ScoreCalculator()

    model.run()


    print()





# =====================================================
# Step5
# Baseline实验
# =====================================================


def step5_baseline():


    print("="*60)

    print("Step5 Baseline对比实验")

    print("="*60)


    model=BaselineExperiment()

    model.run()


    print()





# =====================================================
# Step6
# 消融实验
# =====================================================


def step6_ablation():


    print("="*60)

    print("Step6 消融实验")

    print("="*60)


    model=AblationExperiment()

    model.run()


    print()





# =====================================================
# Step7
# ARIMA预测实验
# =====================================================


def step7_arima():


    print("="*60)

    print("Step7 ARIMA趋势预测实验")

    print("="*60)


    model=ARIMAPredictor()

    model.run()


    print()





# =====================================================
# Step8
# 模型评价
# =====================================================


def step8_evaluation():


    print("="*60)

    print("Step8 模型性能评价")

    print("="*60)


    model=Evaluator()

    model.run()


    print()





# =====================================================
# Step9
# 质量预警
# =====================================================


def step9_alert():


    print("="*60)

    print("Step9 日志质量预警实验")

    print("="*60)


    model=AlertGenerator()

    model.run()


    print()





# =====================================================
# Step10
# 绘制论文图片
# =====================================================


def step10_plot():


    print("="*60)

    print("Step10 生成论文实验图片")

    print("="*60)


    model=PlotExperiment()

    model.run()


    print()





# =====================================================
# Step11
# 实验结果整理
# =====================================================


def step11_export():


    print("="*60)

    print("Step11 整理实验结果")

    print("="*60)


    model=ExperimentExporter()

    model.run()


    print()





# =====================================================
# Main
# =====================================================


def main():


    print()

    print("="*70)

    print(
        "日志数据质量评估与量化模型实验系统"
    )

    print(
        "Log Quality Evaluation Experiment"
    )

    print("="*70)

    print()



    # 创建目录

    create_dirs()



    # ==========================
    # 实验流程
    # ==========================


    step1_generate()


    step2_metrics()


    step3_fahp()


    step4_score()


    step5_baseline()


    step6_ablation()


    step7_arima()


    step8_evaluation()


    step9_alert()


    step10_plot()


    step11_export()



    print()


    print("="*70)

    print(
        "全部实验流程执行完成！"
    )

    print()


    print(
        "实验结果目录:"
    )

    print(
        config.RESULT_DIR
    )


    print()


    print(
        "图片目录:"
    )

    print(
        config.FIGURE_DIR
    )


    print("="*70)





# =====================================================
# 程序入口
# =====================================================


if __name__=="__main__":


    main()