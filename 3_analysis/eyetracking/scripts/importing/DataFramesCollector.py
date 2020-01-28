import os
import pandas as pd

import config


class DataFramesCollector:
    def __init__(self):
        pass

    @staticmethod
    def get_all_files_from_directory(path):
        f = []
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                f.append(os.path.join(dirpath, filename))
            for dirname in dirnames:
                f.extend(DataFramesCollector.get_all_files_from_directory(os.path.join(dirpath, dirname)))
            break
        return f

    @staticmethod
    def get_gaze_files(path_of_directory):
        files = DataFramesCollector.get_all_files_from_directory(path_of_directory)
        return [f for f in files if os.path.basename(f).startswith("GazeData")]

    @staticmethod
    def get_gaze_data_frames(path_of_directory):
        files = DataFramesCollector.get_gaze_files(path_of_directory)

        dfs = []
        for f in files:
            df = DataFramesCollector.load_dataframe_from_csv(f)
            if df is not None:
                dfs.append(df)

        return dfs

    @staticmethod
    def load_dataframe_from_csv(csv_file):
        df = pd.read_csv(csv_file, engine="python", sep=";")

        if df.shape[0] == 0:
            print('Gaze frame is empty: some kind of problem with this participant or file. Ignoring data set: ', csv_file)
            return None

        if df.shape[0] < 3600:
            print('Gaze frame has less than a minute of data. Ignoring data set: ', csv_file)
            #return df
            return None

        print('Gaze frame looks good: ', csv_file)
        return df

    @staticmethod
    def load_gazeframes(group):
        if group == 'Novices':
            return DataFramesCollector.get_gaze_data_frames(config.PATH_DATA_RAW_NOVICES)
        elif group == 'Experts':
            return DataFramesCollector.get_gaze_data_frames(config.PATH_DATA_RAW_EXPERTS)
        else:
            raise Exception('Do not have data for this participant group.')
