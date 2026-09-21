# Sprint 2: Requirements and Data Exploration

**Dates:** 15-22 September 2026

**Goal:** Understand the data, choose suitable inputs and explain the main parts of SARAH.

This summary was written on 20 September from our issues and project notes. All eight Sprint 2 issues are marked closed on GitHub.

## Tasks completed

- [x] [Check relationships between the data fields](https://github.com/Hakuverse/ICT304/issues/6).
- [x] [Decide how to handle unusually high absences](https://github.com/Hakuverse/ICT304/issues/7).
- [x] [Choose the input features](https://github.com/Hakuverse/ICT304/issues/8).
- [x] [Draft why the system needs three parts and class uploads](https://github.com/Hakuverse/ICT304/issues/9).
- [x] [Document why G3 must not be a model input](https://github.com/Hakuverse/ICT304/issues/10).
- [x] [Set up the Python package list](https://github.com/Hakuverse/ICT304/issues/14).
- [x] [Create the first data charts](https://github.com/Hakuverse/ICT304/issues/15).
- [x] [Record the selected features](https://github.com/Hakuverse/ICT304/issues/16).

## Main findings and decisions

Previous assessment scores showed the strongest relationship with risk. Past failures also showed a relationship, while attendance and study time were weaker on their own. This helped us narrow the inputs instead of using every column in the dataset.

The current attendance value is an estimate made from absence counts. Counts of 30 or more give a value of zero; we kept the student records rather than removing them. Study hours are also estimates based on the dataset's study-time categories.

G3 is the final grade. We use it to decide the correct risk label for training and testing, but never give it to the model as an input.

The two modes have been approved:

| Mode | Inputs |
|---|---|
| Early-Warning | Attendance estimate, study-hours estimate and past failures |
| Confirmatory | The same three inputs, plus the previous assessment score |

The previous score is currently calculated from G1 and G2, so both grades need to be available for that calculation. Personal and family-background details are outside our chosen input list.

The three main parts are the risk prediction model, the recommendation engine and the class-upload/dashboard part. The idea is to help a teacher see who needs attention and what support could be offered.

## Files

- [Data preparation code](../code/data_processing.py)
- [Python packages](../code/requirements.txt)
- [Data exploration code](../code/eda.py)
- [Findings](eda_findings.md), [feature selection notes](feature_selection.md) and [charts](figures/)

## Follow-up in Sprint 3

The decisions are ahead of some of the code and documents. We still need to add and test the two modes in [#26](https://github.com/Hakuverse/ICT304/issues/26), then update the feature notes to match. The current distribution charts combine both risk groups; the separate High/Low Risk comparison requested in #15 still needs checking. We also need the system diagram and a simple testing plan.

[Sprint 1](sprint1-planning.md) | [Sprint 3](sprint3-planning.md)
