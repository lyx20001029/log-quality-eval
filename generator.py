"""
=========================================================
Project : Log Quality Evaluation and Governance
File    : generator.py
Author  : ChatGPT
=========================================================
"""

import os
import random
import datetime
import numpy as np
import pandas as pd

import config


class LogGenerator:

    def __init__(self):

        random.seed(config.RANDOM_SEED)
        np.random.seed(config.RANDOM_SEED)

        self.window_num = config.WINDOW_NUM

        self.window_size = config.WINDOW_SIZE

        self.log_num = config.LOG_NUM

    # -------------------------------------------------
    # 随机日志级别
    # -------------------------------------------------

    def random_level(self):

        levels = [
            "INFO",
            "WARN",
            "ERROR",
            "DEBUG"
        ]

        p = [0.70,0.15,0.10,0.05]

        return np.random.choice(levels,p=p)

    # -------------------------------------------------
    # 主机
    # -------------------------------------------------

    def random_host(self):

        hosts = [

            "server-01",

            "server-02",

            "server-03",

            "server-04"

        ]

        return random.choice(hosts)

    # -------------------------------------------------
    # 正常事件
    # -------------------------------------------------

    def random_event(self):

        events = [

            "Login",

            "Logout",

            "Request",

            "Upload",

            "Download",

            "Heartbeat",

            "Database",

            "Redis",

            "Gateway"

        ]

        return random.choice(events)

    # -------------------------------------------------
    # 缺陷注入
    # -------------------------------------------------

    def inject_defect(self,index):

        """
        每30个窗口提升一次缺陷比例

        与论文保持一致

        0%

        5%

        10%

        ...

        30%
        """

        stage = index // 30

        stage = min(stage,len(config.DEFECT_LEVELS)-1)

        return config.DEFECT_LEVELS[stage]

    # -------------------------------------------------
    # 生成窗口
    # -------------------------------------------------

    def generate(self):

        rows = []

        start = datetime.datetime(

            2026,

            1,

            1,

            0,

            0,

            0

        )

        log_id = 1

        for w in range(self.window_num):

            defect = self.inject_defect(w)

            begin = start + datetime.timedelta(

                minutes=w*self.window_size

            )

            for i in range(

                self.log_num//self.window_num

            ):

                timestamp = begin + datetime.timedelta(

                    seconds=random.randint(

                        0,

                        self.window_size*60-1

                    )

                )

                parse_fail = np.random.rand()<defect

                duplicate = np.random.rand()<defect*0.8

                disorder = np.random.rand()<defect*0.6

                drift = np.random.rand()<defect*0.7

                event = self.random_event()

                if drift:

                    event = random.choice([

                        "Unknown",

                        "Template_New",

                        "Version_Update"

                    ])

                rows.append({

                    "log_id":log_id,

                    "window":w+1,

                    "timestamp":timestamp,

                    "host":self.random_host(),

                    "level":self.random_level(),

                    "event":event,

                    "parse_fail":int(parse_fail),

                    "duplicate":int(duplicate),

                    "disorder":int(disorder),

                    "drift":int(drift)

                })

                log_id+=1

        return pd.DataFrame(rows)

    # -------------------------------------------------
    # 保存
    # -------------------------------------------------

    def save(self,df):

        file = os.path.join(

            config.DATA_DIR,

            "raw_log.csv"

        )

        df.to_csv(

            file,

            index=False,

            encoding="utf-8-sig"

        )

        print("原始日志已保存：")

        print(file)

        print(df.head())

    # -------------------------------------------------

    def run(self):

        df=self.generate()

        self.save(df)


if __name__=="__main__":

    LogGenerator().run()