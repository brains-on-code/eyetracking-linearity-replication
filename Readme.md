# Replication Package for "What Drives the Reading Order of Programmers?"

This repository contains all stimuli and source code snippets necessary to replicate our study. In addition, we provide acquired raw data, eye-tracking analysis scripts, and the statistical analysis.

## Paper Abstract

**Background:** The way how programmers comprehend source code depends on several factors, some depend on the source code itself, others on the programmer. Recent studies showed that novice programmers tend to read source code more like natural language text, whereas experts tend to follow the program execution flow. But, it is unknown how the linearity of source code and the comprehension strategy influence programmers' linearity of reading order.

**Objective:** Our overall objective is to replicate two previous studies with the aim to additionally provide empirical evidence on the influencing effects of linearity of source code and programmers' comprehension strategy on linearity of reading order.

**Methods:** To understand the effects of linearity of source code on reading order, we conducted a non-exact replication of studies by Busjahn et al. and Peachock et al., which compared the reading order of novice and expert programmers. Like the original studies, we used an eye tracker to record the eye movements of participants (12 novice and 19 experienced programmers).

**Results:** In line with Busjahn et al., we found that expertise modulates the reading behavior of participants. However, the linearity of source code has an even stronger effect on reading order than expertise, whereas the comprehension strategy has a minor effect.

**Implications:** Our results demonstrate that studies on the reading behavior of programmers must carefully select source code snippets to control the influence of confounding factors. Furthermore, we identify a need for further studies into how programmers should structure source code to align it with their natural reading behavior to ease program comprehension.

## Replication Package

### Stimuli Description

In `1_stimuli`, we provide everything necessary to replicate our study with the same source code snippets. 

### Raw Data

In `2_raw data`, we provide almost all acquired data separated by our two participant groups (novice and experienced programmers). We provide the behavioral, eye-tracking, and questionnaire data. In line with our privacy protection policy, we did not upload separately stored personal data (e.g., email addresses used for the chance to win a gift card).

Each folder contains a single participant dataset. The folder are always named `Trial_<ParticipantID>`. In each sub folder is a `.csv` file with the eye-tracking data and one `.csv` file with the behavioral data. 

Finally, for each group, we provide one `.csv` sheet with the questionnaire data.

### Analysis

In `3_analysis`, we provide everything necessary to analyze the raw data.

The behavioral data was interpreted and summarized with Microsoft Excel (`Analysis_Behavioral_Data.xlsx`). It contains our interpretation whether participants submitted *semantically* correct responses. Additionally, we summarize the behavioral data (e.g., average response time of novices).

The eye-tracking data was analyzed with Python 3.6. In `/3_analysis/eyetracking/`, we provide the full project. If you want to re-run our analysis, make sure to install all dependencies (`requirements.txt`). Next, run `RunPipelineData.py`. 

Please note that (1) it can take up to an hour to preprocess and analyze all data and (2) that we temporarily removed snippet images from `studies\linearity\images` as they may reveal our identities.

### Statistics

In `4_statistics`, we provide the subsequent statistical analysis done with R, including the [lme4](https://cran.r-project.org/package=lme4) (version 1.1.21) and [car](https://cran.r-project.org/package=car) (version 3.0.6) packages. The `EyetrackingLinearity.R` file contains a single regression model for one linearity measure. We provide the output for every linearity measure in `/4_statistics/output/`.



