from typing import List

import numpy as np
import pandas as pd


class ComponentAnalysis:
    def __init__(
            self,
            measure_mz: List[float],
            measure_intensity: List[float],
            tags: List[str],
            element_names: List[str],
            ratio: List[str]
    ):

        self.element_names = element_names
        self.df = pd.DataFrame(
            {
                'tags': tags,
                'ratio': ratio,
                'measureMZ': measure_mz,
                'measureIntensity': measure_intensity,
            }
        )

    def get_calculate_num(self):
        calculate_num = []
        data = self.df.values
        data = data.tolist()

        for i in range(len(data)):
            # 如果没有系数
            if data[i][1]:
                ratio = data[i][1]
                if ratio != 0:
                    calc_num = data[i][-1] - (data[i - 1][-1] * ratio)
                    calculate_num.append(calc_num)
            else:
                calculate_num.append(data[i][-1])
        self.df['calculate_num'] = calculate_num
        self.df['RA'] = [round((x / sum(calculate_num)) * 100, 2) for x in calculate_num]

    def add_weights_column_name_to_df(self):
        """
        添加行名
        :return:
        """
        for item in self.element_names:
            self.df[item] = [0] * len(self.df)

    def get_element_weights(self):
        # 得到计算值
        self.get_calculate_num()

        # 插入列名
        self.add_weights_column_name_to_df()
        tags = self.df['tags'].values
        calculate_num = self.df['calculate_num'].values

        for i in range(len(self.df)):
            tags_split = tags[i].split('/')
            for tag in tags_split:
                self.df.loc[i, tag] = self.df[tag][i] + calculate_num[i]

    def get_percent(self, tags):
        all_element = self.df.values[-1]
        sum_element = 0
        for item in all_element:
            if not np.isnan(item):
                sum_element += item
        cache = []
        keys_len = len(self.df.keys())

        for i in range(keys_len - len(tags)):
            cache.append(np.nan)

        # cache_elements = []
        # for item in all_element:
        #     if not np.isnan(item):
        #         cache_elements.append(item)

        for tag in tags:
            cache.append((self.df[tag].values[-1] / sum_element) * 100)

        cache = [round(x, 2) for x in cache]
        return cache

    def get_total_weights(self):
        # 计算出需要的数据
        self.get_element_weights()

        # 计算元素总含量
        tags = self.element_names
        keys_len = len(self.df.keys())
        total_data = []
        for i in range(keys_len - len(tags)):
            total_data.append(np.nan)
        for tag in tags:
            total_data.append(sum(self.df[tag].values))

        size = self.df.index.size
        self.df.loc[size] = total_data

        percent = self.get_percent(tags)
        size = self.df.index.size
        self.df.loc[size] = percent

        return self.df
