"""
=========================================================
Project : Log Quality Evaluation and Governance

File    : config.py

Author  : ChatGPT

Description :
    全局配置文件（论文最终版）

    数据:
        result/

    图片:
        res_new/

=========================================================
"""


import os
import numpy as np



# ==========================================================
# 工程目录
# ==========================================================

ROOT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# 数据目录

DATA_DIR = os.path.join(
    ROOT_DIR,
    "data"
)


# 实验结果 CSV

RESULT_DIR = os.path.join(
    ROOT_DIR,
    "result"
)


# 论文图片目录

FIGURE_DIR = os.path.join(
    ROOT_DIR,
    "res_new"
)



# 创建目录

for path in [

    DATA_DIR,

    RESULT_DIR,

    FIGURE_DIR

]:

    os.makedirs(
        path,
        exist_ok=True
    )





# ==========================================================
# 随机种子
# ==========================================================

RANDOM_SEED = 2026


np.random.seed(
    RANDOM_SEED
)





# ==========================================================
# 数据集参数
# ==========================================================


LOG_NUM = 10000


WINDOW_SIZE = 10


WINDOW_NUM = 200


LOG_PER_WINDOW = (
    LOG_NUM //
    WINDOW_NUM
)





# ==========================================================
# 缺陷注入比例
# ==========================================================


DEFECT_LEVELS = [

    0.00,

    0.05,

    0.10,

    0.15,

    0.20,

    0.25,

    0.30

]





# ==========================================================
# 质量指标
# ==========================================================


METRICS = [

    "parse_rate",

    "duplicate_rate",

    "drift_rate",

    "disorder_rate"

]



METRIC_NAME_CN = {


    "parse_rate":
        "解析失败率",


    "duplicate_rate":
        "重复率",


    "drift_rate":
        "漂移率",


    "disorder_rate":
        "乱序率"

}





# ==========================================================
# FAHP判断矩阵
# ==========================================================


FAHP_MATRIX = np.array([


    [1.0, 2.0, 2.0, 3.0],


    [0.5, 1.0, 1.0, 2.0],


    [0.5, 1.0, 1.0, 2.0],


    [0.3333,0.5,0.5,1.0]


])





# ==========================================================
# 一致性随机指标
# ==========================================================


RI = {


    1:0,

    2:0,

    3:0.58,

    4:0.90,

    5:1.12,

    6:1.24,

    7:1.32,

    8:1.41,

    9:1.45,

    10:1.49

}





# ==========================================================
# 综合评分
# ==========================================================


FULL_SCORE = 100


MIN_SCORE = 0





# ==========================================================
# 等级划分
# ==========================================================


GRADE_RULE = [

    (90,"优秀"),

    (80,"良好"),

    (70,"中等"),

    (60,"较差"),

    (0,"危险")

]





# ==========================================================
# Baseline实验
# ==========================================================


BASELINE_MODELS = [

    "Single Indicator",

    "Equal Weight",

    "Manual Weight",

    "Proposed"

]





# ==========================================================
# 消融实验
# ==========================================================


ABLATION_MODELS = [

    "Full Model",

    "w/o FAHP",

    "w/o Multi-Metric",

    "w/o Score Fusion"

]





# ==========================================================
# ARIMA参数
# ==========================================================


ARIMA_ORDER = (

    1,

    1,

    1

)



TRAIN_RATIO = 0.80


TEST_RATIO = 0.20


FORECAST_STEP = 1





# ==========================================================
# 预警参数
# ==========================================================


ALERT_THRESHOLD = 5





# ==========================================================
# CSV文件路径
# ==========================================================


RAW_LOG_FILE = os.path.join(

    DATA_DIR,

    "raw_log.csv"

)



METRIC_FILE = os.path.join(

    RESULT_DIR,

    "metrics.csv"

)



WEIGHT_FILE = os.path.join(

    RESULT_DIR,

    "weight.csv"

)



SCORE_FILE = os.path.join(

    RESULT_DIR,

    "score.csv"

)



BASELINE_FILE = os.path.join(

    RESULT_DIR,

    "baseline.csv"

)



ABLATION_FILE = os.path.join(

    RESULT_DIR,

    "ablation.csv"

)



ARIMA_FILE = os.path.join(

    RESULT_DIR,

    "arima.csv"

)



# ARIMA预测结果

ARIMA_PREDICT_FILE = os.path.join(

    RESULT_DIR,

    "arima_prediction.csv"

)



# ARIMA误差

ARIMA_ERROR_FILE = os.path.join(

    RESULT_DIR,

    "arima_error.csv"

)



# 预警结果

ALERT_FILE = os.path.join(

    RESULT_DIR,

    "alert.csv"

)



EVALUATION_FILE = os.path.join(

    RESULT_DIR,

    "evaluation.csv"

)





# ==========================================================
# 图片路径
# ==========================================================


FIG314 = os.path.join(

    FIGURE_DIR,

    "Fig3-14_metric.png"

)



FIG315 = os.path.join(

    FIGURE_DIR,

    "Fig3-15_baseline.png"

)



FIG316 = os.path.join(

    FIGURE_DIR,

    "Fig3-16_ablation.png"

)



FIG317 = os.path.join(

    FIGURE_DIR,

    "Fig3-17_ARIMA.png"

)



FIG318 = os.path.join(

    FIGURE_DIR,

    "Fig3-18_score.png"

)



FIG319 = os.path.join(

    FIGURE_DIR,

    "Fig3-19_alert.png"

)





# ==========================================================
# 表格
# ==========================================================


TABLE310 = os.path.join(

    RESULT_DIR,

    "Table3-10.csv"

)


TABLE311 = os.path.join(

    RESULT_DIR,

    "Table3-11.csv"

)


TABLE312 = os.path.join(

    RESULT_DIR,

    "Table3-12.csv"

)


TABLE313 = os.path.join(

    RESULT_DIR,

    "Table3-13.csv"

)


TABLE315 = os.path.join(

    RESULT_DIR,

    "Table3-15.csv"

)





# ==========================================================
# matplotlib配置
# ==========================================================


FONT_FAMILY = "SimHei"



DPI = 600



FIG_SIZE = (

    8,

    5

)



LINE_WIDTH = 2



GRID_ALPHA = 0.4





# ==========================================================
# 控制信息
# ==========================================================


LINE = "=" * 70



PROJECT_NAME = (

    "服务器日志数据质量评估与量化模型实验平台"

)



VERSION = "V1.0"



AUTHOR = "Li Yuxuan"





# ==========================================================
# 调试
# ==========================================================


DEBUG = True


VERBOSE = True