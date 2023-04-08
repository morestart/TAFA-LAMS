import os
from typing import Dict

import pandas as pd


def to_excel(dfs: Dict, save_path: str, save_name: str):
    writer = pd.ExcelWriter(os.path.join(save_path, save_name))
    for k, v in dfs.items():
        v.to_excel(writer, k)

    writer.save()
