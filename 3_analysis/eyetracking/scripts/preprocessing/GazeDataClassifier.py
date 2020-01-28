import math


class GazeDataClassifier:

    @staticmethod
    def prepare_participant_dfs(gaze_data_frames, general_data):
        participant_dicts = []

        for gaze_frame in gaze_data_frames:
            # todo merge in behavioral data
            participant_data = general_data.loc[general_data.SubjectID == gaze_frame['SubjectID'][0]]
            screen_height = participant_data['ActualScreenHeight'].item()

            participant_dict = {
                'id': gaze_frame['SubjectID'][0],
                'id_short': gaze_frame['SubjectID'][0][:8],
                'gaze_data': gaze_frame.drop('SubjectID', axis=1),
                'fixations': [],
                'saccades': [],
                'screen_resolution': screen_height,
                'results': {
                    'BySnippet': {},
                    'ByScrambled': {},
                }
            }

            participant_dict['gaze_frames'] = gaze_frame.shape[0]
            participant_dict['experiment_runtime'] = gaze_frame['ExperimentTime'].iloc[[0, -1]].diff().iloc[-1]

            print(participant_dict['gaze_data'].head(5))

            participant_dicts.append(participant_dict)

        return participant_dicts

    @staticmethod
    def classify_data_frames(participant_dfs):
        return [GazeDataClassifier.classify_data_frame(participant_df) for participant_df in participant_dfs]

    @staticmethod
    def classify_data_frame(participant_df):
        participant_df = GazeDataClassifier.compute_fixations_saccades(participant_df)

        return participant_df

    @staticmethod
    def compute_fixations_saccades(participant_df):
        # print out some statistics
        frames = participant_df['gaze_data'].shape[0]
        print('\n## Participant: ' + participant_df['id_short'])
        print('Amount of frames: ' + str(frames))
        print('-> This dataframe contains roughly ' + str(round(participant_df['gaze_data'].shape[0] / 60 / 60)) + ' minutes of eye gaze.')

        print('\nClassifying Fixation/Saccades')
        # todo: this seems really slow
        # go through event column data, whenever there is a switch, create new object
        events = participant_df['gaze_data']['Gaze_EventSmooth'].values

        fixations = []
        saccades = []
        current_event = None
        for i, event in enumerate(events):
            if (i % 2500) == 0:
                print("-> Reading event of gaze data: ", i)

            if current_event is None:
                current_event = {
                    'Type': event,
                    'Snippet': participant_df['gaze_data'].iloc[i]['Snippet'],
                    'Data': participant_df['gaze_data'].iloc[[i]]
                }
                continue

            if current_event['Type'] == event and current_event['Snippet'] == participant_df['gaze_data'].iloc[i]['Snippet']:
                current_event['Data'] = current_event['Data'].append(participant_df['gaze_data'].iloc[[i]], ignore_index=True)

            else:
                # final computations for current event
                if current_event['Type'] == 'Fixation':
                    current_event['AveragePositionX'] = current_event['Data'].loc[:, "GazePosX"].mean()
                    current_event['AveragePositionY'] = current_event['Data'].loc[:, "GazePosY"].mean()
                    current_event['Frames'] = current_event['Data'].shape[0]

                    time_first_and_last_row = current_event['Data']['ExperimentTime'].iloc[[0, -1]]
                    time_diff = time_first_and_last_row.diff().iloc[-1]
                    current_event['TimeLength'] = time_diff

                    fixations.append(current_event)
                elif current_event['Type'] == 'Saccade':
                    # compute for each saccade: x/y distance, length, average velocity
                    current_event['Frames'] = current_event['Data'].shape[0]
                    current_event['AverageVelocity'] = current_event['Data'].loc[:, "VelocitySmooth"].mean()

                    gaze_pos_first_and_last_row = current_event['Data'][['GazePosX', 'GazePosY', 'ExperimentTime']].iloc[[0, -1]]
                    gaze_pos_diff = gaze_pos_first_and_last_row.diff().iloc[-1]
                    current_event['TimeLength'] = gaze_pos_diff['ExperimentTime']
                    current_event['DistanceX'] = abs(gaze_pos_diff['GazePosX'])
                    current_event['DistanceY'] = abs(gaze_pos_diff['GazePosY'])
                    current_event['Distance'] = math.sqrt((gaze_pos_first_and_last_row.iloc[1]['GazePosX'] - gaze_pos_first_and_last_row.iloc[0]['GazePosX'])**2 + (gaze_pos_first_and_last_row.iloc[1]['GazePosY'] - gaze_pos_first_and_last_row.iloc[0]['GazePosY'])**2)

                    saccades.append(current_event)
                else:
                    print('unknown event type :(')

                # finally, create new event
                current_event = {
                    'Type': event,
                    'Snippet': participant_df['gaze_data'].iloc[i]['Snippet'],
                    'Data': participant_df['gaze_data'].iloc[[i]]
                }

        participant_df['fixations'] = fixations
        participant_df['saccades'] = saccades

        print('-> classifying fixation/saccades done')

        return participant_df

    @staticmethod
    def reduce_gaze_dataframes(participant_dicts):
        return [GazeDataClassifier.reduce_gaze_dataframe(participant_dict) for participant_dict in participant_dicts]

    @staticmethod
    def reduce_gaze_dataframe(participant_dict):
        participant_dict['gaze_data'] = participant_dict['gaze_data'].drop(participant_dict['gaze_data'].columns.difference(['Time', 'GazePosX', 'GazePosY', 'Velocity', 'Snippet', 'ExperimentTime', 'Gaze_Event', 'TrialNumber']), 1)
        participant_dict['gaze_data'] = participant_dict['gaze_data'].round({'GazePosX': 2, 'GazePosY':2, 'Velocity': 2})

        print('Reduced gaze_data dataframe:')
        print(participant_dict['gaze_data'].head(5))

        return participant_dict
