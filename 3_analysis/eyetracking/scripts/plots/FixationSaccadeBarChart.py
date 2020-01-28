import matplotlib.pyplot as plt
import numpy


def plot_bar_chart_participant(results_novice, results_expert, property):
    # plot in a bar chart
    plt.clf()
    participant_nov_strings = []
    participant_exp_strings = []
    for i in range(len(results_novice[property])):
        participant_nov_strings.append('Novice ' + str(i + 1))
    for i in range(len(results_expert[property])):
        participant_exp_strings.append('Expert ' + str(i + 1))

    y_pos_novice = numpy.arange(len(results_novice['FixationsPerSecond']))
    y_pos_expert = numpy.arange(start=len(y_pos_novice), stop=len(y_pos_novice) + len(results_expert['FixationsPerSecond']))

    plt.bar(y_pos_novice, results_novice[property], color='blue', width=0.5, alpha=0.5)
    plt.bar(y_pos_expert, results_expert[property], color='red', width=0.5, alpha=0.5)

    plt.ylabel(property)
    xticks_pos = numpy.concatenate((y_pos_novice, y_pos_expert))
    xticks_label = numpy.concatenate((participant_nov_strings, participant_exp_strings))
    plt.xticks(xticks_pos, xticks_label, rotation='vertical')

    plt.tight_layout()
    plt.savefig('output/GroupPlot_' + property + '.png', dpi=300)
    plt.close()


def plot_bar_chart_snippet(participant_dfs_novice, participant_dfs_expert, snippet, property):
    # filter data
    novices = []
    experts = []

    for novice in participant_dfs_novice:
        if not novice['gaze_data'].loc[novice['gaze_data']['Snippet'] == snippet].empty:
            novices.append(novice['results']['BySnippet'][snippet][property])

    for expert in participant_dfs_expert:
        if not expert['gaze_data'].loc[expert['gaze_data']['Snippet'] == snippet].empty:
            experts.append(expert['results']['BySnippet'][snippet][property])

    # plot in a bar chart
    plt.clf()
    plt.figure(figsize=(20, 8))

    participant_nov_strings = []
    participant_exp_strings = []
    for i in range(len(novices)):
        participant_nov_strings.append('Novice ' + str(i + 1))
    for i in range(len(experts)):
        participant_exp_strings.append('Expert ' + str(i + 1))

    y_pos_novice = numpy.arange(len(novices))
    y_pos_expert = numpy.arange(start=len(y_pos_novice), stop=len(y_pos_novice) + len(experts))

    plt.bar(y_pos_novice, novices, color='blue', width=0.5, alpha=0.5)
    plt.bar(y_pos_expert, experts, color='red', width=0.5, alpha=0.5)

    plt.ylabel(property)
    xticks_pos = numpy.concatenate((y_pos_novice, y_pos_expert))
    xticks_label = numpy.concatenate((participant_nov_strings, participant_exp_strings))
    plt.xticks(xticks_pos, xticks_label, rotation='vertical')

    plt.tight_layout()
    plt.savefig('output/BySnippet/GroupPlot_Snippet_' + snippet + '_' + property + '.png', dpi=300)
    plt.close()


def plot_bar_chart_scramble(participant_dfs_novice, participant_dfs_expert, property):
    # filter data
    novices = []
    experts = []
    novices_scrambled = []
    experts_scrambled = []

    for novice in participant_dfs_novice:
        novices.append(novice['results']['ByScrambled']['normal'][property])
        novices_scrambled.append(novice['results']['ByScrambled']['scrambled'][property])

    for expert in participant_dfs_expert:
        experts.append(expert['results']['ByScrambled']['normal'][property])
        experts_scrambled.append(expert['results']['ByScrambled']['scrambled'][property])

    participant_nov_strings = []
    participant_exp_strings = []
    for i in range(len(novices)):
        participant_nov_strings.append('Novice ' + str(i + 1))
    for i in range(len(experts)):
        participant_exp_strings.append('Expert ' + str(i + 1))

    y_pos_novice = numpy.arange(len(novices))
    y_pos_expert = numpy.arange(start=len(y_pos_novice), stop=len(y_pos_novice) + len(experts))

    # plot in twp bar charts
    plt.clf()
    plt.figure(figsize=(20, 8))

    # todo: unify the y-labels across both subplots
    # bar chart 1: normal code
    plt.subplot(2, 1, 1)
    plt.bar(y_pos_novice, novices, color='blue', width=0.5, alpha=0.5)
    plt.bar(y_pos_expert, experts, color='red', width=0.5, alpha=0.5)

    plt.ylabel('Normal: ' + property)
    xticks_pos = numpy.concatenate((y_pos_novice, y_pos_expert))
    xticks_label = numpy.concatenate((participant_nov_strings, participant_exp_strings))
    plt.xticks(xticks_pos, xticks_label, rotation='vertical')

    # bar chart 2: scrambled code
    plt.subplot(2, 1, 2)
    plt.bar(y_pos_novice, novices_scrambled, color='blue', width=0.5, alpha=0.5)
    plt.bar(y_pos_expert, experts_scrambled, color='red', width=0.5, alpha=0.5)

    plt.ylabel('Scrambled: ' + property)
    xticks_pos = numpy.concatenate((y_pos_novice, y_pos_expert))
    xticks_label = numpy.concatenate((participant_nov_strings, participant_exp_strings))
    plt.xticks(xticks_pos, xticks_label, rotation='vertical')

    plt.tight_layout()
    plt.savefig('output/ByScrambled/GroupPlot_Scrambled_' + property + '.png', dpi=300)
    plt.close()
