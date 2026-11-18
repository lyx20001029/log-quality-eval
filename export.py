"""
=========================================================
Project : Log Quality Evaluation and Governance
File    : export.py

Description :
    实验结果统一整理模块

Function:

    1. 整理实验CSV
    2. 整理论文统计表
    3. 整理论文图片
    4. 生成实验说明

Output:

    experiment_result/

=========================================================
"""


import os
import shutil

import config



class ExperimentExporter:


    def __init__(self):


        self.data_dir = os.path.dirname(

            config.SCORE_FILE

        )


        self.output_dir=os.path.join(

            self.data_dir,

            "experiment_result"

        )


        self.csv_dir=os.path.join(

            self.output_dir,

            "CSV"

        )


        self.table_dir=os.path.join(

            self.output_dir,

            "Tables"

        )


        self.figure_dir=os.path.join(

            self.output_dir,

            "Figures"

        )


        self.create_folder()



    # =====================================================
    # 创建目录
    # =====================================================

    def create_folder(self):


        folders=[

            self.output_dir,

            self.csv_dir,

            self.table_dir,

            self.figure_dir

        ]


        for folder in folders:


            os.makedirs(

                folder,

                exist_ok=True

            )



    # =====================================================
    # 文件复制
    # =====================================================

    def copy_file(

            self,

            filename,

            target_dir

    ):


        src=os.path.join(

            self.data_dir,

            filename

        )


        if os.path.exists(src):


            shutil.copy(

                src,

                target_dir

            )


            print(

                "复制成功:",

                filename

            )


        else:


            print(

                "文件不存在:",

                filename

            )



    # =====================================================
    # CSV实验数据
    # =====================================================

    def export_csv(self):


        files=[


            # baseline

            "baseline.csv",

            "baseline_sample.csv",

            "baseline_mean.csv",


            # ablation

            "ablation.csv",

            "ablation_sample.csv",

            "ablation_mean.csv",


            # arima

            "arima_prediction.csv",

            "arima_test_result.csv",

            "arima_error.csv"


        ]


        for file in files:


            self.copy_file(

                file,

                self.csv_dir

            )



    # =====================================================
    # 论文统计表
    # =====================================================

    def export_tables(self):


        files=[


            "Table3-11_Baseline.csv",


            "Table3-12_Ablation.csv"


        ]


        for file in files:


            self.copy_file(

                file,

                self.table_dir

            )



    # =====================================================
    # 图片
    # =====================================================

    def export_figures(self):


        source=os.path.join(

            self.data_dir,

            "figures"

        )


        files=[


            "Fig3-15_Baseline.png",


            "Fig3-16_Ablation.png",


            "Fig3-17_ARIMA.png",


            "Fig3-18_Quality.png",


            "Fig3-19_Alert.png"


        ]



        for file in files:


            src=os.path.join(

                source,

                file

            )


            if os.path.exists(src):


                shutil.copy(

                    src,

                    self.figure_dir

                )


                print(

                    "图片复制:",

                    file

                )


            else:


                print(

                    "图片不存在:",

                    file

                )



    # =====================================================
    # README
    # =====================================================

    def create_readme(self):


        content="""

日志数据质量评估与量化模型实验结果

======================================


一、CSV目录

保存实验原始数据。


1. Baseline实验

baseline.csv

baseline_sample.csv



2. Ablation实验

ablation.csv

ablation_sample.csv



3. ARIMA预测实验

arima_prediction.csv

arima_test_result.csv

arima_error.csv



======================================


二、Tables目录


论文实验统计结果：


Table3-11_Baseline.csv


Table3-12_Ablation.csv



======================================


三、Figures目录


论文实验图片：


Fig3-15 Baseline方法比较


Fig3-16 消融实验


Fig3-17 ARIMA预测


Fig3-18 日志质量趋势


Fig3-19 质量预警



======================================


论文：

《日志数据质量评估与量化模型的研究》


"""


        with open(

            os.path.join(

                self.output_dir,

                "README.txt"

            ),

            "w",

            encoding="utf-8"

        ) as f:


            f.write(content)



    # =====================================================
    # run
    # =====================================================

    def run(self):


        print("="*60)


        print(

            "开始整理实验结果"

        )


        self.export_csv()


        self.export_tables()


        self.export_figures()


        self.create_readme()



        print(

            "实验结果整理完成"

        )


        print(

            "输出目录:",

            self.output_dir

        )


        print("="*60)




if __name__=="__main__":


    exporter=ExperimentExporter()


    exporter.run()