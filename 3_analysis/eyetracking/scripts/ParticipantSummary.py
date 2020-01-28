import _pickle as pickle
# sys.stdout = open('output/LoggingOutput.md', 'w')
import pprint
from os import path

import numpy
import pandas as pd

import config
from scripts.analyses import ParticipantFixationSaccade
from scripts.importing.DataFramesCollector import DataFramesCollector
from scripts.importing.GazeDataCleaner import GazeDataCleaner
from scripts.preprocessing.GazeDataClassifier import GazeDataClassifier
from scripts.preprocessing.GazeDataPreprocessing import GazeDataPreprocessing
from scripts.plots import FixationSaccadeBarChart


# todo: consider different screen resolutions: the fixation/saccade detection algorithms relies on velocity in pixe/second -> leads to different results when participants use different screens
# todo: clean data: separate tasks, since instructions are not tracked (todo: verify this!) -> transition between those is messing up analysis. Alternatively, deal with missing data better.
def preprocess_raw_data(group):
    print('\n### Preprocessing Pipeline from Raw Data')
    print('-> Reading data...')
    gaze_frames = DataFramesCollector.load_gazeframes(group)

    print('\n-> Cleaning data...')
    gaze_frames_cleaned = GazeDataCleaner.clean_gaze_data_frames(gaze_frames)

    print('\nReading general info data...')
    general_data = pd.read_csv(path.join('studies', config.CURRENT_STUDY, 'GeneralInfo_' + group + '.csv'), delimiter=';')

    print('\nPreprocessing data...')
    gaze_frames_preprocessed = GazeDataPreprocessing.preprocess_data_frames(gaze_frames_cleaned, general_data)

    print('\nClassify data...')
    participant_dicts = GazeDataClassifier.prepare_participant_dfs(gaze_frames_preprocessed, general_data)
    participant_dicts = GazeDataClassifier.classify_data_frames(participant_dicts)

    participant_dicts = GazeDataClassifier.reduce_gaze_dataframes(participant_dicts)

    with open(path.join(config.PATH_DATA_RAW, "PreprocessedData" + group + ".pkl"), 'wb') as output:
        pickle.dump(participant_dicts, output)


def load_preprocessed(group='Novice'):
    print('\n### Preprocessing Pipeline from Raw Data')
    if group == 'Novices':
        print('Reading novice data...')
        with open(path.join(config.PATH_DATA_RAW, "PreprocessedDataNovices.pkl"), 'rb') as input:
            preprocessed_data_novice = pickle.load(input)
            return preprocessed_data_novice

    else:
        print('Reading expert data...')
        with open(path.join(config.PATH_DATA_RAW, "PreprocessedDataExperts.pkl"), 'rb') as input:
            preprocessed_data_expert = pickle.load(input)
        return preprocessed_data_expert


def run_analysis_pipeline(participant_dfs):
    print('\nAnalyzing data...')

    for participant_df in participant_dfs:
        participant_df = ParticipantFixationSaccade.participant_fixation_saccades(participant_df)
        participant_df = ParticipantFixationSaccade.participant_fixation_saccades_task(participant_df)
        participant_df = ParticipantFixationSaccade.participant_fixation_saccades_scramble(participant_df)

    # todo prepare more experiment-level contrasts for novice vs expert: fixations/saccade on (non)scrambled level, task level, behavioral data
    results = {
        'FixationsPerSecond': [],
        'FixationLength': [],
        'SaccadesPerSecond': [],
        'SaccadeDistance': [],
    }

    for participant_df in participant_dfs:
        results['FixationsPerSecond'].append(participant_df['results']['FixationsPerSecond'])
        results['FixationLength'].append(participant_df['results']['FixationLength'])
        results['SaccadesPerSecond'].append(participant_df['results']['SaccadesPerSecond'])
        results['SaccadeDistance'].append(participant_df['results']['SaccadeDistance'])

    return participant_dfs, results


def run_plots_pipeline(participant_dfs_novice, participant_dfs_expert):
    #for participant_df in participant_dfs_novice:
    #    GazeXYVelocityPlot.xy_velocity_plot(participant_df)

    #for participant_df in participant_dfs_expert:
    #    GazeXYVelocityPlot.xy_velocity_plot(participant_df)

    for snippet in config.SNIPPETS_ALL:
        print('\nExporting bar charts for snippet: ', snippet)
        FixationSaccadeBarChart.plot_bar_chart_snippet(participant_dfs_novice, participant_dfs_expert, snippet, 'FixationsPerSecond')
        FixationSaccadeBarChart.plot_bar_chart_snippet(participant_dfs_novice, participant_dfs_expert, snippet, 'FixationLength')
        FixationSaccadeBarChart.plot_bar_chart_snippet(participant_dfs_novice, participant_dfs_expert, snippet, 'SaccadesPerSecond')
        FixationSaccadeBarChart.plot_bar_chart_snippet(participant_dfs_novice, participant_dfs_expert, snippet, 'SaccadeDistance')

    FixationSaccadeBarChart.plot_bar_chart_scramble(participant_dfs_novice, participant_dfs_expert, 'FixationsPerSecond')
    FixationSaccadeBarChart.plot_bar_chart_scramble(participant_dfs_novice, participant_dfs_expert, 'FixationLength')
    FixationSaccadeBarChart.plot_bar_chart_scramble(participant_dfs_novice, participant_dfs_expert, 'SaccadesPerSecond')
    FixationSaccadeBarChart.plot_bar_chart_scramble(participant_dfs_novice, participant_dfs_expert, 'SaccadeDistance')


def run_comparison_pipeline(results_novice, results_expert):
    print('\n## GROUP LEVEL ANALYSIS: Novices')
    print('Average fixations per second: ', round(numpy.mean(results_novice['FixationsPerSecond']), 1))
    print('Average fixations length in msec: ', round(numpy.mean(results_novice['FixationLength']), 1))
    print('Average saccades per second: ', round(numpy.mean(results_novice['SaccadesPerSecond']), 1))
    print('Average saccades distance in pixel ', round(numpy.mean(results_novice['SaccadeDistance']), 1))

    print('\n## GROUP LEVEL ANALYSIS: Experts')
    print('Average fixations per second: ', round(numpy.mean(results_expert['FixationsPerSecond']), 1))
    print('Average fixations length in msec: ', round(numpy.mean(results_expert['FixationLength']), 1))
    print('Average saccades per second: ', round(numpy.mean(results_expert['SaccadesPerSecond']), 1))
    print('Average saccades distance in pixel ', round(numpy.mean(results_expert['SaccadeDistance']), 1))

    FixationSaccadeBarChart.plot_bar_chart_participant(results_novice, results_expert, 'FixationsPerSecond')
    FixationSaccadeBarChart.plot_bar_chart_participant(results_novice, results_expert, 'FixationLength')
    FixationSaccadeBarChart.plot_bar_chart_participant(results_novice, results_expert, 'SaccadesPerSecond')
    FixationSaccadeBarChart.plot_bar_chart_participant(results_novice, results_expert, 'SaccadeDistance')


if __name__ == "__main__":
    print('should not call this python file directly anymore.')
