import itertools
import sys

import minineedle
import miniseq as ms

ch_offset = 96


def transform_line_order_to_sequence(line_numbers):
    sequence = ''
    for number in line_numbers:
        if number <= 0 or number >= 27:
            #raise Exception('number outside of scope: ' + str(number))
            print('Ignore match in line ' + str(number) + ' as it breaks the algorithm.')
            continue

        letter = chr(number + ch_offset)
        sequence += letter

        #print('transformed number ' + str(number) + ' to ' + letter)

    return sequence


def nwalign_and_compute_nw_score_naive(line_numbers_model, line_numbers_gaze):
    if not line_numbers_model:
        return 0

    model = transform_line_order_to_sequence(line_numbers_model)
    gaze = transform_line_order_to_sequence(line_numbers_gaze)

    seq_model = ms.Sequence('Model', model)
    seq_gaze = ms.Sequence('Actual', gaze)

    alignment = minineedle.NeedlemanWunsch(seq_model, seq_gaze)
    alignment.change_matrix(minineedle.ScoreMatrix(match=3, miss=-3, gap=-2))

    try:
        alignment.align()
        #print(alignment)

        score = alignment.get_score()
        #print('score: ', str(score))
    except ZeroDivisionError as e:
        print('ZeroDivisionError when comparing the following numbers')
        print('repeated ', line_numbers_model)
        print('gaze     ', line_numbers_gaze)

        score = 0

    return score


def nwalign_and_compute_nw_score_dynamic(line_numbers_model, line_numbers_gaze):
    if not line_numbers_model:
        return [0, 0]

    length_gaze = len(line_numbers_gaze)

    high_score = None
    repetitions = None

    multiplicator = 1

    while True:
        model = list(itertools.chain.from_iterable(itertools.repeat(line_numbers_model, multiplicator)))
        length_model = len(model)

        score = nwalign_and_compute_nw_score_naive(model, line_numbers_gaze)

        if not high_score or score > high_score:
            high_score = score
            repetitions = multiplicator

        multiplicator += 1

        if length_model > length_gaze:
            break

    #print('best score is ' + str(score) + ' with repetitions: ' + str(repetitions))

    return [repetitions, high_score]


#result = nwalign_and_compute_nw_score_dynamic([1, 2, 3, 4], [1, 2, 3, 1, 2, 3, 2, 3, 1, 2, 1, 3, 4, 3, 2])
#result = nwalign_and_compute_nw_score_naive([1, 2, 3, 4], [1, 2, 3, 1, 2, 3, 2, 3, 1, 2, 1, 3, 4, 3, 2])