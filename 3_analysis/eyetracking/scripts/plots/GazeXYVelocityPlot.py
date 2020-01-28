import matplotlib.pyplot as plt


def xy_velocity_plot(participant_df):
    print('\nPlotting gaze data')
    plt.figure(figsize=(50, 8))

    gaze_data_time = participant_df['gaze_data']['ExperimentTime'].values

    plt.clf()
    plt.subplot(3, 1, 1)
    #plt.ylim(participant_df['gaze_data']['GazePosX'].max(), 0) # decreasing y axis
    plt.plot(gaze_data_time, participant_df['gaze_data']['GazePosX'].values, label='X', color='lightgray')
    plt.plot(gaze_data_time, participant_df['gaze_data']['GazePosXSmooth'].values, label='Y', color='dimgray', alpha=0.5)
    plt.legend()

    plt.subplot(3, 1, 2)
    #plt.ylim(participant_df['gaze_data']['GazePosY'].max(), 0)  # decreasing y axis
    plt.plot(gaze_data_time, participant_df['gaze_data']['GazePosY'].values, label='X', color='lightgray')
    plt.plot(gaze_data_time, participant_df['gaze_data']['GazePosYSmooth'].values, label='Y', color='dimgray', alpha=0.5)
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(gaze_data_time, participant_df['gaze_data']['Velocity'].values, label='Velocity', color='red')
    plt.plot(gaze_data_time, participant_df['gaze_data']['VelocitySmooth'].values, label='Velocity Smoothed', color='mistyrose')
    plt.legend()

    plt.tight_layout()
    plt.savefig('output/GazePlot_' + participant_df['id_short'] + '.png', dpi=300)

    print('-> plotting gaze data done')
