# Warning follow-up - 24 October 2026

Separate from Benjamin's 23 October walkthrough. On the review branch, all 109
project tests passed in 11.377 seconds on Windows with Python 3.12.10 and
scikit-learn 1.8.0. The three added tests exercise form warnings and clearance,
CSV warning alignment/export including Low-Risk rows, and the unchanged 0–40
contract in all three setups. Subcases run inside these three tests.

The original walkthrough remains a 106-test record. No new manual macOS run,
independent-user study or model evaluation is claimed. Reviewers should check
the new warning visually before merging. The existing example remains 0.661;
adding a warning does not improve its accuracy.

Tested source SHA-256 values:

- `project/code/predict.py`: `a2061bf26a3e66f238e08608b2f17f4f254119c68a16c035b59964b9a3ebef27`
- `project/code/dashboard.py`: `3d57e44ac8736b4a984a01fb391b12205bbbe6379e996ac10ca35a746076a889`
- `project/code/test_predict.py`: `ac4341155152074824173720edf0690a3c79fe599441171561bb2557640a6bcc`
- `project/code/test_study_hours_warning.py`: `037d72790ca11016ff14e68c5af0b6f0b006cbaff982e2a873c5c9b99bb66283`
