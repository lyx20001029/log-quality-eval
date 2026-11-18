# 日志数据质量评估与量化模型实验（log-quality-eval）

本仓库为「日志数据质量评估与量化模型」论文实验的完整可复现代码与数据集，包含日志数据集、质量指标计算、FAHP 权重、综合评分、Baseline 对比、消融实验、ARIMA 趋势预测、模型评价与质量预警的全流程实现，以及论文所需的图表与表格产出。

## 数据集

| 项目 | 说明 |
| --- | --- |
| 文件 | `data/raw_log.csv` |
| 规模 | 10,000 条日志，200 个窗口，每窗口 50 条 |
| 字段 | `log_id`、`window`、`timestamp`、`host`、`level`、`event`、`parse_fail`、`duplicate`、`disorder`、`drift` |
| 缺陷标记 | `parse_fail`（解析失败）、`duplicate`（重复）、`disorder`（乱序）、`drift`（时钟/内容漂移），取值 0/1 |
| 生成方式 | 由 `generator.py` 以 `RANDOM_SEED = 2026` 生成，缺陷注入比例在 0%～30% 区间按窗口递增，用于构造不同质量水平的分段 |
| 编码 | UTF-8，逗号分隔，首行为表头 |

样本（前 3 行）：

```csv
log_id,window,timestamp,host,level,event,parse_fail,duplicate,disorder,drift
1,1,2026-01-01 00:02:01,server-01,INFO,Heartbeat,0,0,0,0
2,1,2026-01-01 00:03:48,server-04,WARN,Gateway,0,0,0,0
```

> 数据集为实验用合成日志，不含任何真实业务数据或个人信息。

## 目录结构

```
log-quality-eval/
├── main.py                  # 一键运行全流程（Step1–Step11）
├── config.py                # 全局配置：路径、随机种子、窗口参数、缺陷比例、FAHP 判断矩阵
├── generator.py             # Step1  日志生成
├── metrics.py               # Step2  质量指标计算（解析失败率/重复率/漂移率/乱序率）
├── fahp.py                  # Step3  FAHP 权重计算与一致性检验
├── score.py                 # Step4  综合评分、趋势、滑动平均、质量阶段划分
├── baseline.py              # Step5  Baseline 对比实验
├── ablation.py              # Step6  消融实验
├── arima_predict.py         # Step7  ARIMA 趋势预测
├── evaluation.py            # Step8  模型性能评价
├── alert.py                 # Step9  质量预警
├── plot.py                  # Step10 论文图片生成
├── export.py                # Step11 结果整理（CSV / Tables / Figures / Report）
├── plot_ablation_single.py  # 消融单图单独绘制（可选）
├── generate_report.py       # 实验报告生成（可选）
├── verify_figures.py        # 图表标签核查（可选）
├── data/raw_log.csv         # 数据集
├── result/                  # 各步骤指标、评分、对比实验结果 CSV
├── res_new/                 # 论文插图（Fig3-14 ~ Fig3-19）
└── result/experiment_result/ # 归档整理后的 CSV / Figures / Tables / Report
```

## 环境要求

- Python 3.8+
- 依赖见 `requirements.txt`：numpy、pandas、matplotlib、statsmodels

```bash
pip install -r requirements.txt
```

## 运行方式

```bash
python main.py
```

程序按 Step1→Step11 顺序执行，全部产出写入 `result/` 与 `res_new/`。

说明：Step1 会用 `config.RANDOM_SEED` 重新生成 `data/raw_log.csv`；若只想复现已有结果、不覆盖数据集，可跳过 Step1，从 Step2 开始执行（注释掉 `main()` 中的 `step1_generate()`）。

## 复现性说明

- 固定随机种子 `2026`，同一环境下多次运行结果一致。
- 窗口参数：`LOG_NUM = 10000`、`WINDOW_NUM = 200`、`WINDOW_SIZE = 10`。
- FAHP 判断矩阵与一致性随机指标均定义在 `config.py` 中。

## 引用

如使用本仓库代码或数据集，请注明来源：

```
日志数据质量评估与量化模型实验 (log-quality-eval)
https://github.com/<owner>/log-quality-eval
```
