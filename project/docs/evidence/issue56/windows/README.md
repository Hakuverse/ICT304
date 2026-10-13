# Issue #56 - Windows test evidence

Tester: Benjamin. Date: 12 October 2026.
Tested commit: `2bbb083074e265bb8931b053bd262bbf47d29b19`.

See the [completed checklist](../../../prototype-test-checklist.md) for inputs,
actual results and links to each screenshot. These checks cover software
behaviour, not model accuracy or the effectiveness of recommendations.

Benjamin reported all P1-P16 checks passed. The screenshots show 89 automated
tests passing and a separate run of all 11 recommendation tests passing.
The recommendation tests are already part of the 89; they are not 11 extra tests.

## Evidence notes

- The replacement [study-hours 40 screenshot](p7-study-40.png) shows the
  accepted boundary value and a Low Risk result (0.284) with routine guidance.
- The [all-invalid CSV screenshot](p10-all-invalid.png) shows Confirmatory mode,
  4 rows, 0 predicted and 4 skipped, with a reason for each skipped row.
- Both earlier screenshot gaps were resolved in PR #76.
- P13 shows the downloaded result opened in Excel. The downloaded CSV itself
  is not included in this evidence folder.
- The [duplicate-ID input](../../../../data/issue56-duplicate-and-invalid.csv)
  contains fictional students and reproduces P12/P16.
- This is a Windows record. macOS testing and the tutor demo are separate work.

## Screenshot index

- [p1-environment00.png](p1-environment00.png)
- [p1-environment01.png](p1-environment01.png)
- [p1-tests.png](p1-tests.png)
- [p10-all-invalid.png](p10-all-invalid.png)
- [p10-empty.png](p10-empty.png)
- [p10-header-only.png](p10-header-only.png)
- [p10-missing-column.png](p10-missing-column.png)
- [p11-extra-comma.png](p11-extra-comma.png)
- [p11-no-ids.png](p11-no-ids.png)
- [p12-duplicate-results.png](p12-duplicate-results.png)
- [p13-export.png](p13-export.png)
- [p14-after-input-change.png](p14-after-input-change.png)
- [p14-after-mode-change.png](p14-after-mode-change.png)
- [p14-before-change.png](p14-before-change.png)
- [p15-rule-tests.png](p15-rule-tests.png)
- [p16-failures-options.png](p16-failures-options.png)
- [p16-invalid-failures.png](p16-invalid-failures.png)
- [p2-early-warning.png](p2-early-warning.png)
- [p3-g1-only.png](p3-g1-only.png)
- [p4-g2-zero.png](p4-g2-zero.png)
- [p5-low-risk.png](p5-low-risk.png)
- [p6-cli-comparison.png](p6-cli-comparison.png)
- [p7-attendance-150-error.png](p7-attendance-150-error.png)
- [p7-study-0.png](p7-study-0.png)
- [p7-study-40.png](p7-study-40.png)
- [p7-study-41-error.png](p7-study-41-error.png)
- [p8-g2-NA-error.png](p8-g2-NA-error.png)
- [p8-missing-g1.png](p8-missing-g1.png)
- [p9-results.png](p9-results.png)
- [p9-skipped.png](p9-skipped.png)
