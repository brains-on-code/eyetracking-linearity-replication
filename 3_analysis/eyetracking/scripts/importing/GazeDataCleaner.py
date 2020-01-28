class GazeDataCleaner:

    @staticmethod
    def clean_gaze_data_frames(gaze_data_frames):
        return [GazeDataCleaner.clean_gaze_data_frame(gdf) for gdf in gaze_data_frames]

    @staticmethod
    def clean_gaze_data_frame(gdf):
        gdf = GazeDataCleaner.drop_unnecessary_columns(gdf)
        gdf = GazeDataCleaner.drop_fixation_cross_rows(gdf)
        gdf = GazeDataCleaner.rename_columns(gdf)

        gdf['Time'] = gdf.Time.apply(lambda time: round(time) if isinstance(time, float) else round(float(time.replace(',', '.'))))
        gdf['GazePosX'] = gdf.GazePosX.apply(lambda x: round(x) if isinstance(x, float) else round(float(x.replace(',', '.')), 1))
        gdf['GazePosY'] = gdf.GazePosY.apply(lambda y: round(y) if isinstance(y, float) else round(float(y.replace(',', '.')), 1))

        basetime = gdf['Time'].values[0]
        gdf['ExperimentTime'] = gdf.Time.apply(lambda time: time - basetime)

        return gdf

    @staticmethod
    def drop_unnecessary_columns(gdf):
        return gdf.drop('Indentation', axis=1)

    @staticmethod
    def drop_fixation_cross_rows(gdf):
        original_size = gdf.shape[0]
        gdf = gdf[~gdf['Snippet'].str.contains("FixationCross")]
        reduced_size = gdf.shape[0]
        gdf.reset_index(inplace=True)

        print('Dropped some eye-gaze data from fixation-cross condition: ', str(original_size - reduced_size))

        return gdf

    @staticmethod
    def rename_columns(gdf):
        return gdf.rename(columns={
            'Gaze.X': 'GazePosX',
            'GazeY': 'GazePosY'
        })
