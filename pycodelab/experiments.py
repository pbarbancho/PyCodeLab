import pickle
import pathlib
import os
import datetime

import pandas as pd

def get_current_time():
    return int(datetime.datetime.now().timestamp()*1000)


class ExperimentLogger:

    def __init__(self, loc: str='.', name: str='results', reset: bool=False):
        self.loc = pathlib.Path(loc)
        self.name = name

        if not reset and os.path.exists(self.loc / f'{self.name}.pcl.log'):
            with open(self.loc / f'{self.name}.pcl.log', 'rb') as log_file:
                self.logs = pickle.load(log_file)
        else:
            self.logs = {
                'values': [],
                'series': [],
                'dataframes': [],
                '2dplots': [],
                '3dplots': []
            }


    def log_value(self, name: str, value: any) -> None:
        self.logs['values'].append(
            {
                'name': name,
                'content': value,
                'timestamp': get_current_time()
            }
        )

        self.save_log()

    
    def log_series(self, name: str, serie: pd.Series) -> None:
        self.logs['series'].append(
            {
                'name': name,
                'content': serie.to_dict(),
                'timestamp': get_current_time()
            }
        )

        self.save_log()

    def log_dataframe(self, name: str, dataframe: pd.DataFrame) -> None:
        self.logs['dataframes'].append(
            {
                'name': name,
                'content': dataframe.to_dict(),
                'timestamp': get_current_time()
            }
        )

        self.save_log()


    def log_2dplot(self, name: str, x: dict, y: dict) -> None:

        self.logs['2dplots'].append(
            {
                'name': name,
                'x': x,
                'y': y,
                'timestamp': get_current_time()
            }
        )

        self.save_log()


    def log_3dplot(self, name: str, x: dict, y: dict, z: dict) -> None:

        self.logs['3dplots'].append(
            {
                'name': name,
                'x': x,
                'y': y,
                'z': z,
                'timestamp': get_current_time()
            }
        )

        self.save_log()

    
    def save_log(self):
        with open(self.loc / f'{self.name}.pcl.log', 'wb') as log_file:
            pickle.dump(self.logs, log_file)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save_log()

    def __del__(self):
        self.save_log()