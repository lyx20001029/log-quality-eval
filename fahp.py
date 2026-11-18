"""
=========================================================
Project : Log Quality Evaluation and Governance
File    : fahp.py
Author  : ChatGPT
Description : FAHP权重计算（论文最终版）
=========================================================
"""

import numpy as np
import pandas as pd
import config


class FAHP:

    def __init__(self):

        self.matrix = np.array(config.FAHP_MATRIX, dtype=float)

        self.metric_names = [
            "Parse Failure",
            "Duplicate",
            "Drift",
            "Disorder"
        ]

        self.weight_file = config.WEIGHT_FILE

    # ======================================================
    # 一致性检验
    # ======================================================

    def consistency_test(self, eigenvalue):

        n = self.matrix.shape[0]

        ci = (eigenvalue - n) / (n - 1)

        ri = config.RI[n]

        if ri == 0:
            cr = 0
        else:
            cr = ci / ri

        return ci, cr

    # ======================================================
    # 特征值法计算权重
    # ======================================================

    def calculate_weight(self):

        eigenvalues, eigenvectors = np.linalg.eig(self.matrix)

        max_index = np.argmax(eigenvalues.real)

        lambda_max = eigenvalues.real[max_index]

        weight = eigenvectors[:, max_index].real

        weight = weight / np.sum(weight)

        return lambda_max, weight

    # ======================================================
    # 保存CSV
    # ======================================================

    def save_weight(self, weight):

        df = pd.DataFrame({

            "Metric": self.metric_names,

            "Weight": np.round(weight, 6)

        })

        df.to_csv(

            self.weight_file,

            index=False,

            encoding="utf-8-sig"

        )

        print()

        print("权重已保存：")

        print(self.weight_file)

        return df

    # ======================================================
    # 输出结果
    # ======================================================

    def show(self, df, lambda_max, ci, cr):

        print(config.LINE)

        print("FAHP 权重计算结果")

        print(config.LINE)

        print(df)

        print()

        print("λmax = {:.6f}".format(lambda_max))

        print("CI    = {:.6f}".format(ci))

        print("CR    = {:.6f}".format(cr))

        if cr < 0.10:

            print()

            print("一致性检验：通过 √")

        else:

            print()

            print("一致性检验：未通过 ×")

    # ======================================================
    # 主程序
    # ======================================================

    def run(self):

        lambda_max, weight = self.calculate_weight()

        ci, cr = self.consistency_test(lambda_max)

        df = self.save_weight(weight)

        self.show(df, lambda_max, ci, cr)

        return df


if __name__ == "__main__":

    fahp = FAHP()

    fahp.run()