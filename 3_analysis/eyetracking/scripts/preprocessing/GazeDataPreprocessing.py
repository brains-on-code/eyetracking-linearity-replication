import scipy.signal

import numpy as np
import pandas as pd

VELOCITY_THRESHOLD = 150  # pixel/100 msec


class GazeDataPreprocessing:
    @staticmethod
    def cartesian_velocity(x, y, t):
        dx, dy, dt = np.diff(x), np.diff(y), np.diff(t)
        vx = dx / dt
        vy = dy / dt

        dr = np.sqrt(vx * vx + vy * vy)
        return dr

    @staticmethod
    def preprocess_data_frames(gaze_data_frames, general_data):
        return [GazeDataPreprocessing.preprocess_data_frame(gdf, general_data) for gdf in gaze_data_frames]

    @staticmethod
    def preprocess_data_frame(gdf, general_data):
        gdf = GazeDataPreprocessing.scale_data(gdf, general_data)
        gdf = GazeDataPreprocessing.smooth_data(gdf)
        gdf = GazeDataPreprocessing.calculate_velocity(gdf)
        gdf = GazeDataPreprocessing.detect_gaze_events(gdf)

        return gdf

    @staticmethod
    def scale_data(gdf, general_data):
        subjectId = gdf.loc[0, 'SubjectID']
        participant_data = general_data.loc[general_data.SubjectID == subjectId]
        screen_height = participant_data['ActualScreenHeight'].item()
        eyex_height = participant_data['EyeXScreenHeight'].item()

        # scale eyex resolution to actual screen resolution, if necessary
        scale = 1.0
        if eyex_height != screen_height:
            scale = screen_height / eyex_height
            print('--> scale: ', scale)

            gdf['GazePosX'] = gdf['GazePosX'].apply(lambda x: x * scale)
            gdf['GazePosY'] = gdf['GazePosY'].apply(lambda y: y * scale)

        return gdf

    @staticmethod
    def smooth_data(gdf):
        gazeX = gdf['GazePosX'].dropna()
        gazeY = gdf['GazePosY'].dropna()
        gazeXSmooth = scipy.signal.savgol_filter(gazeX, 5, 3)
        gazeYSmooth = scipy.signal.savgol_filter(gazeY, 5, 3)
        gdf['GazePosXSmooth'] = pd.Series(gazeXSmooth)
        gdf['GazePosYSmooth'] = pd.Series(gazeYSmooth)
        return gdf

    @staticmethod
    def calculate_velocity(gdf):
        velocity = GazeDataPreprocessing.cartesian_velocity(gdf['GazePosX'].values, gdf['GazePosY'].values, gdf['ExperimentTime'].values)
        velocity = np.multiply(velocity, 100)
        gdf['Velocity'] = pd.Series(velocity)

        velocitySmooth = GazeDataPreprocessing.cartesian_velocity(gdf['GazePosXSmooth'].values, gdf['GazePosYSmooth'].values, gdf['ExperimentTime'].values)
        velocitySmooth = np.multiply(velocitySmooth, 100)
        gdf['VelocitySmooth'] = pd.Series(velocitySmooth)

        return gdf

    @staticmethod
    def detect_gaze_event_based_on_velocity(row, column):
        if row[column] > VELOCITY_THRESHOLD:
            return 'Saccade'
        else:
            return 'Fixation'

    @staticmethod
    def detect_gaze_events(gdf):
        gdf['Gaze_Event'] = gdf.apply(lambda row: GazeDataPreprocessing.detect_gaze_event_based_on_velocity(row, 'Velocity'), axis=1)
        gdf['Gaze_EventSmooth'] = gdf.apply(lambda row: GazeDataPreprocessing.detect_gaze_event_based_on_velocity(row, 'VelocitySmooth'), axis=1)
        return gdf

