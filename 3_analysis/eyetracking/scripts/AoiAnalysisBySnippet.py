import _pickle as pickle
# sys.stdout = open('output/LoggingOutput.md', 'w')
import itertools

import numpy
import pandas

import config
from scripts.analyses import NWAlgorithm

pandas.set_option('display.max_columns', 500)
pandas.set_option('display.expand_frame_repr', False)

from scripts import OverlayAoiOnSnippet

resolutions = ['1050', '1080', '1200']
HORIZONTAL_AOI_DEVIATION_THRESHOLD = 100


def get_linearity_category(snippet):
    if snippet in ['MoneyClass', 'SumArray']:
        return 1
    elif snippet in ['Calculation', 'CheckIfLettersOnly']:
        return 2
    elif snippet in ['InsertSort', 'Vehicle']:
        return 3
    elif snippet in ['SignChecker', 'Student']:
        return 4
    else:
        return 5


def is_error_snippet(expert, snippet, scrambled):
    if scrambled and snippet in ['SignChecker', 'Street']:
        return True
    else:
        return False


def run_calculations(preprocessed_data, group, scrambled, results_for_anova):
    expert = group == 'Experts'

    for i, snippet in enumerate(config.SNIPPETS_UNIQUE):
        print('\n\nComputing snippet: ', snippet)

        fixations = {
            "1050": [],
            "1080": [],
            "1200": []
        }

        saccades_by_participant = {}
        matched_fixations_by_participant = {}

        snippet_name = snippet
        if scrambled:
            snippet_name += '_scrambled'

        # get all fixations from snippet
        for participant in preprocessed_data:
            matched_fixations_by_participant[participant['id_short']] = []
            saccades_by_participant[participant['id_short']] = []

            for fixation in participant['fixations']:
                if fixation['Snippet'] == snippet_name:
                    fixation['Participant'] = participant['id_short']
                    fixations[str(participant['screen_resolution'])].append(fixation)

            for saccade in participant['saccades']:
                if saccade['Snippet'] == snippet_name:
                    saccade['Participant'] = participant['id_short']
                    saccades_by_participant[participant['id_short']].append(saccade)

        overall_fixations = len(fixations['1050']) + len(fixations['1080']) + len(fixations['1200'])
        print('-> Number of fixations ', overall_fixations)

        # match AOIs for each fixation
        for resolution in resolutions:
            # get AOI information
            [AOIs, story_order, execution_order] = OverlayAoiOnSnippet.compute_aois(resolution, snippet, scrambled)

            for fixation in fixations[resolution]:
                # check whether fixation is in an AOI
                # get coordinates
                x = fixation['AveragePositionX']
                y = fixation['AveragePositionY']

                aoi_line_hit = None
                aoi_block_hit = None
                is_answer_hit = None

                # go through each AOI and check whether there is a hit
                for nr_line, aoi_line in enumerate(AOIs['lines']):
                    if aoi_line['start_x'] <= x < (aoi_line['end_x'] + HORIZONTAL_AOI_DEVIATION_THRESHOLD):
                        if aoi_line['start_y'] <= y < aoi_line['end_y']:
                            aoi_line_hit = nr_line + 1
                            break

                for nr_block, aoi_block in enumerate(AOIs['blocks']):
                    if aoi_block['start_x'] <= x < aoi_block['end_x']:
                        if aoi_block['start_y'] <= y < aoi_block['end_y']:
                            aoi_block_hit = nr_block + 1
                            break

                if AOIs['answer']['start_x'] <= x < AOIs['answer']['end_x']:
                    if AOIs['answer']['start_y'] <= y < AOIs['answer']['end_y']:
                        is_answer_hit = True

                matched_fixations_by_participant[fixation['Participant']].append({
                    'line': aoi_line_hit,
                    'block': aoi_block_hit,
                    'is_answer': is_answer_hit,
                    'fixation': fixation
                })

        # calculate metrics
        if overall_fixations != 0:
            for participant in matched_fixations_by_participant:
                vertical_next = []
                vertical_later = []
                regression = []
                horizontal_later = []
                line_regression = []

                fixations_part = matched_fixations_by_participant[participant]
                fixations_aoi_cleaned_line = list(filter(lambda elem: elem['line'], fixations_part))
                reading_order_line_without_unmatched = [fixation['line'] for fixation in fixations_aoi_cleaned_line]

                fixations_aoi_cleaned_block = list(filter(lambda elem: elem['block'], matched_fixations_by_participant[participant]))
                reading_order_block_without_unmatched = [fixation['block'] for fixation in fixations_aoi_cleaned_block]

                fixations_aoi_cleaned_answer = list(filter(lambda elem: elem['is_answer'], matched_fixations_by_participant[participant]))
                reading_order_answer = [fixation['is_answer'] for fixation in fixations_aoi_cleaned_answer]

                if not fixations_aoi_cleaned_line:
                    #print('seems like there are no fixations for ' + participant + ' for snippet ' + snippet)
                    continue

                for current_fixation, next_fixation in zip(fixations_aoi_cleaned_line, fixations_aoi_cleaned_line[1:]):
                    # for current_fixation, next_fixation in zip(matched_fixations, matched_fixations[1:]):
                    # only compute when both fixations have matched lines
                    if not next_fixation['line'] or not current_fixation['line']:
                        # print('Ignored a saccade with jump from ' + str(current_fixation['line']) + ' to ' + (next_fixation['line']))
                        continue

                    # Horizontal Later Text: check whether a saccade (between two fixations) is forward on a line
                    if current_fixation['line'] == next_fixation['line']:
                        # check whether it moved to the right
                        if next_fixation['fixation']['AveragePositionX'] >= current_fixation['fixation']['AveragePositionX']:
                            horizontal_later.append(next_fixation)
                        else:
                            line_regression.append(next_fixation)
                    else:
                        # check whether it's an up or down movement
                        if current_fixation['line'] <= next_fixation['line'] <= (1 + current_fixation['line']):
                            vertical_next.append(next_fixation)

                        if next_fixation['line'] >= current_fixation['line']:
                            vertical_later.append(next_fixation)
                        else:
                            regression.append(next_fixation)

                reading_order_line_without_unmatched_participant = [fixation['line'] for fixation in fixations_aoi_cleaned_line]
                reading_order_line_without_unmatched_no_duplicates_participant = [x[0] for x in itertools.groupby(reading_order_line_without_unmatched_participant)]

                nw_score_story_naive = NWAlgorithm.nwalign_and_compute_nw_score_naive(story_order, reading_order_line_without_unmatched_no_duplicates_participant)
                [nw_score_story_dynamic_repetitions, nw_score_story_dynamic_score] = NWAlgorithm.nwalign_and_compute_nw_score_dynamic(story_order, reading_order_line_without_unmatched_no_duplicates_participant)

                nw_score_exec_naive = NWAlgorithm.nwalign_and_compute_nw_score_naive(execution_order, reading_order_line_without_unmatched_no_duplicates_participant)
                [nw_score_exec_dynamic_repetitions, nw_score_exec_dynamic_score] = NWAlgorithm.nwalign_and_compute_nw_score_dynamic(execution_order, reading_order_line_without_unmatched_no_duplicates_participant)

                result_for_participant = {
                    'Participant': participant,
                    'Expert': expert,
                    'Snippet': snippet,
                    'Linearity': get_linearity_category(snippet),
                    'HasError': is_error_snippet(expert, snippet, scrambled),
                    'Scrambled': scrambled,

                    'HitsLine': len(reading_order_line_without_unmatched) / len(fixations_part),
                    'HitsBlocks': len(reading_order_block_without_unmatched) / len(fixations_part),
                    'HitsAnswer': len(reading_order_answer) / len(fixations_part),

                    'VerticalNext': len(vertical_next) / len(fixations_aoi_cleaned_line),
                    'VerticalLater': len(vertical_later) / len(fixations_aoi_cleaned_line),
                    'Regression': len(regression) / len(fixations_aoi_cleaned_line),
                    'HorizontalLater': len(horizontal_later) / len(fixations_aoi_cleaned_line),
                    'LineRegression': len(line_regression) / len(fixations_aoi_cleaned_line),
                    'SaccadeLength': numpy.mean([saccade['Distance'] for saccade in saccades_by_participant[participant]]),

                    'StoryOrder_Naive_Score': nw_score_story_naive,
                    'StoryOrder_Dynamic_Score': nw_score_story_dynamic_score,
                    'StoryOrder_Dynamic_Repetitions': nw_score_story_dynamic_repetitions,

                    'ExecOrder_Naive_Score': nw_score_exec_naive,
                    'ExecOrder_Dynamic_Score': nw_score_exec_dynamic_score,
                    'ExecOrder_Dynamic_Repetitions': nw_score_exec_dynamic_repetitions
                }

                results_for_anova = results_for_anova.append(result_for_participant, ignore_index=True)

    return results_for_anova


if __name__ == "__main__":
    print('should not call this python file directly anymore.')
