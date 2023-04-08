from __future__ import annotations

import os
from typing import Dict
from typing import List

import numpy as np
import pandas as pd

from .get_element_weight import ComponentAnalysis
from .get_mz_and_intensity import MZMLAnalysis


def to_excel(dfs: Dict, save_path: str, save_name: str):
    writer = pd.ExcelWriter(os.path.join(save_path, save_name))
    for k, v in dfs.items():
        v.to_excel(writer, k)

    writer.save()


def get_one_file_result(params):
    # 遍历第一组配置
    for param in params:
        all_df: Dict[str: List[pd.DataFrame]] = {}
        mza = MZMLAnalysis(mzml_filepath=param.get('filePath'))
        # 遍历时间节点
        for bg_start_time, bg_end_time, need_start_time, need_end_time in param.get('timePoints'):
            mz, intensity, suffix = mza.get_final_mz_and_indensity(
                all_need_mz=param.get('mz'),
                bg_start_time=bg_start_time,
                bg_end_time=bg_end_time,
                need_start_time=need_start_time,
                need_end_time=need_end_time,
                loss=param.get('loss')
            )
            df = pd.DataFrame(
                {
                    '质荷比': mz,
                    '丰度': intensity
                }
            )

            df.loc[-1] = [np.NAN, suffix]
            ca = ComponentAnalysis(measure_mz=mz, measure_intensity=intensity,
                                   tags=param.get('tags'), element_names=param.get('elementNames'),
                                   ratio=param.get('ratios'))
            data_df = ca.get_total_weights()
            all_df[f'{bg_start_time}-{bg_end_time}-{need_start_time}-{need_start_time} mz-intensity'] = df
            all_df[
                f'{bg_start_time}-{bg_end_time}-{need_start_time}-{need_start_time} weightPercent'] = data_df

        write_file.to_excel(all_df, param.get('savePath'), param.get('saveName'))
        all_df.clear()
