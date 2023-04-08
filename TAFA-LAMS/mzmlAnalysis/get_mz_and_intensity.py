import numpy as np
from pyteomics import mzml
from pyteomics.mzml import MzML
from rich.progress import track
from loguru import logger

class MZMLAnalysis:

    def __init__(self, mzml_filepath: str):
        self.process_time: list = []
        self.mz: list = []
        self.intensity: list = []
        self.data: MzML = self.read_mzml_file(mzml_filepath)
        self.save_name = mzml_filepath.split('.')[0] + '.xlsx'
        self.get_all_mz_and_intensity()

    @staticmethod
    def read_mzml_file(file_path: str) -> MzML:
        """
        get file data
        :param file_path: mzml file path
        :return: MzML object
        """
        if not file_path.endswith('mzML'):
            raise TypeError(
                f'file must be .mzML, your name is {file_path}'
            )
        # use_index必须指定为True 如果不指定m/z array 和 intensity array得到的都是None
        data = mzml.read(file_path, use_index=True)
        return data

    def get_all_mz_and_intensity(self) -> None:
        """
        质谱仪数据提取 采集时间 质荷比 丰度

        :return:
        """

        for spectrum in mzml.read(self.data, use_index=True):
            # print(spectrum.get('centroid spectrum'))
            self.process_time.append(spectrum.get('scanList').get('scan')[0].get('scan start time'))
            self.mz.append(spectrum.get('m/z array'))
            self.intensity.append(spectrum.get('intensity array'))

    def cut_time(self, starttime: float, endtime: float) -> list:
        """
        剪切数据时间段

        :param starttime: 起始时间
        :param endtime: 终止时间
        :return: 时间索引列表
        """
        time_interval = []
        for index, one_time in track(enumerate(self.process_time),
                                     description='剪切数据:',
                                     total=len(self.process_time)):
            if starttime <= one_time <= endtime:
                time_interval.append(index)
        return time_interval

    def get_cut_time_mz_and_intensity(self, starttime: float, endtime: float):
        if starttime >= endtime:
            raise ValueError(
                f'start time must < end time, your tims is: {starttime}-{endtime}'
            )

        time_interval = self.cut_time(starttime, endtime)
        if time_interval[-1] > len(time_interval):
            logger.error(f'时间段超出数据范围, 请重新输入时间段, 数据范围为: {self.process_time[0]}-{self.process_time[-1]}')
        need_intensity = self.intensity[time_interval[0]: time_interval[-1]]
        need_mz = self.mz[time_interval[0]: time_interval[-1]]
        return need_intensity, need_mz

    def use_mz_get_indensity(self, all_need_mz: list, starttime: float, endtime: float, loss: float = 0):
        intensity, mz = self.get_cut_time_mz_and_intensity(starttime, endtime)
        cache = {
            'mz': [],
            'intensity': []
        }

        cache_mean = {
            'mz': [],
            'intensity': []
        }
        for need_mz in track(all_need_mz, description='查找质荷比对应丰度:'):
            for mz_list, intensity_list in zip(mz, intensity):
                for one_mz, one_intensity in zip(mz_list, intensity_list):
                    if one_mz - loss <= need_mz <= one_mz + loss:
                        cache.get('mz').append(one_mz)
                        cache.get('intensity').append(one_intensity)

            # 求平均 每个需要的质荷比对应的质谱数据的均值
            cache_mean.get('mz').append(np.round(np.mean(np.array(cache.get('mz'))), 2))
            cache_mean.get('intensity').append(np.round(np.mean(np.array(cache.get('intensity'))), 2))
            cache.get('mz').clear()
            cache.get('intensity').clear()
        # self.to_excel(cache_mean.get('mz'), cache_mean.get('intensity'), save_path)
        return cache_mean

    def get_final_mz_and_indensity(
            self,
            bg_start_time: float,
            bg_end_time: float,
            all_need_mz: list,
            need_start_time: float,
            need_end_time: float,
            loss: float = 0.3,
    ):
        bg_result = self.use_mz_get_indensity(all_need_mz, bg_start_time, bg_end_time, loss)
        need_result = self.use_mz_get_indensity(all_need_mz, need_start_time, need_end_time, loss)

        intensity = np.array(need_result.get('intensity')) - np.array(bg_result.get('intensity')).tolist()

        suffix = f'bg_start_time={bg_start_time}-bg_end_time={bg_end_time}-' \
                 f'need_start_time={need_start_time}-need_end_time={need_end_time}-loss={loss}'

        return need_result.get('mz'), intensity, suffix

    # def to_excel(self, need_mz: list, need_intensity: list, save_path: str, suffix: str):
    #     df = pd.DataFrame(
    #         {
    #             '质荷比': need_mz,
    #             '丰度': need_intensity
    #         }
    #     )
    #
    #     df.loc[-1] = [np.NAN, suffix]
    #
    #     df.to_excel(os.path.join(save_path, self.save_name))
