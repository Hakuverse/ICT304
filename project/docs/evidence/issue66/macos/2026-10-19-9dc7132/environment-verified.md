# Supplementary environment verification

Recorded during evidence preparation on 19 October 2026, after Jackie's manual run.
This is a review-time check of the original test checkout, not a reconstructed original terminal transcript.

- Test checkout: `ICT304-issue66-check`.
- `git rev-parse HEAD`: `9dc7132dc0a1a735b508447b99f49b70afb84f6d`.
- Review-time status: `main...origin/main`; only untracked `.DS_Store` reported. Initial clean status is from the guided setup record, not this later check.
- `sw_vers`: macOS 26.6.2, build 25G83.
- `.venv/bin/python --version`: Python 3.13.9.
- `pip show`: scikit-learn 1.8.0; pandas 3.0.6; numpy 2.5.4; joblib 1.6.0; streamlit 1.66.0.
- `pip check`: No broken requirements found. The review sandbox disabled the pip cache because its directory was not writable; no package installation or dependency change was performed.
- Original package/version screenshot: [S6-1.png](screenshots/S6-1.png).
- Browser/version, viewport, screen resolution and zoom: not recorded for this run.
- Evidence checkout base: `2bba2c159716d3903ab0c16e6de96f1e425280a1`, on `66NNest-s6-run-complete-workflow-checks-on-windows-and-macos`. This is the submission base, not a new test run.
