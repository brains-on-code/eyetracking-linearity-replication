from os import path

import pandas

from scripts import ParticipantSummary, AoiAnalysisBySnippet, AnovaAnalysis
#from scripts.export import Ogama, ImageExporterGroup, ImageExporterIndividual
import config

# STEP 1. look for config files and sanity-check whether everything is there
OVERRIDE_PREPROCESSED_DATA = False

# STEP 2: look for raw data and preprocess it
for group in config.PARTICIPANT_GROUPS:
    if not path.isfile(path.join(config.PATH_DATA_RAW, "PreprocessedData" + group + ".pkl")) or OVERRIDE_PREPROCESSED_DATA:
        print("Reading and preprocessing raw data for ", group)
        ParticipantSummary.preprocess_raw_data(group)
    else:
        print("Using existing preprocessed data for ", group)


# STEP 3: load preprocessed data
data_preprocessed = {}
for group in config.PARTICIPANT_GROUPS:
    data_preprocessed[group] = ParticipantSummary.load_preprocessed(group)

    print(data_preprocessed[group][0]['gaze_data'].head(5))

# STEP 4: visualize preprocessed data
if config.RUN_EXPORT_OGAMA:
    for group in config.PARTICIPANT_GROUPS:
        Ogama.export_data(data_preprocessed[group], group)

# STEP 5A: analyse data for general metrics (fixation times, saccade rate, ...)
data_analyzed = {}
data_results = {}
data_aoi = pandas.DataFrame(columns=['Participant', 'Expert', 'Snippet', 'Linearity', 'HasError', 'Scrambled', 'HitsLine', 'HitsBlocks', 'HitsAnswer', 'VerticalNext', 'VerticalLater',
                                     'Regression', 'HorizontalLater', 'LineRegression', 'SaccadeLength', 'StoryOrder_Naive_Score', 'StoryOrder_Dynamic_Score',
                                     'StoryOrder_Dynamic_Repetitions', 'ExecOrder_Naive_Score', 'ExecOrder_Dynamic_Score', 'ExecOrder_Dynamic_Repetitions'])

for group in config.PARTICIPANT_GROUPS:
    data_analyzed[group], data_results[group] = ParticipantSummary.run_analysis_pipeline(data_preprocessed[group])
    pass

# STEP 5B: analyse data AOIs
for group in config.PARTICIPANT_GROUPS:
    data_aoi = AoiAnalysisBySnippet.run_calculations(data_preprocessed[group], group, False, data_aoi)
    data_aoi = AoiAnalysisBySnippet.run_calculations(data_preprocessed[group], group, True, data_aoi)

# STEP 6: visualize analyzed data
if config.RUN_EXPORT_PNG:
    for group in config.PARTICIPANT_GROUPS:
        ImageExporterIndividual.export_individual_data(data_preprocessed[group], True)
        ImageExporterGroup.export_group_data(data_preprocessed[group], True)

# STEP 7. statistical analysis
print(data_aoi.head(5))
data_aoi.to_csv('output/AOI/Metrics_Data_for_Anova.csv', index=False)

# todo continue statistical analysis in R with above .csv file





