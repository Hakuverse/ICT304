# Submission package checks

## Confirmed plan — 2 November 2026

Benjamin will upload **one ZIP** containing the repository files, report, full
guide/evidence, signed group declaration, both video files and presentation deck.
All three declaration signatures/confirmations and equal contributions are
reported in [contribution checks](contribution-checks.md).
Rehearsal is scheduled for 3 November, not completed.

The final source version is the **eventual approved merge commit of PR #126**.
PR #126 remains open at Benjamin's instruction. Its head can be tested as a
candidate, but neither that head nor GitHub's temporary test-merge SHA should be
labelled the final merged submission version. Record the actual merge SHA after
merge, build the final source archive from it and verify the extracted copy.

Published app packages remain v0.1.0-preview, source ab4a604. Documentation
changes do not rebuild the ZIPs or change model results. Their separate
identities/hashes are in [release notes](app-release-notes.md).

## Actual completion status

| Check | Status |
|---|---|
| Final source basis | Eventual approved PR #126 merge selected; merge SHA not yet available |
| Final archive filename and checksum | Not yet recorded |
| All three declaration signatures/confirmations | Confirmed by Benjamin; private form not independently inspected |
| Slides | Reviewed by all three; merged PR #127 |
| Rehearsal | Scheduled 3 November; not yet performed |
| Public app download hashes | All 11 assets verified on 31 October; historical record |
| Later public-release launch | Anna's short Windows clip, confirmed by Benjamin; not a full suite or timing rerun |
| Final source archive clean extraction and tests | Not yet performed/reported |
| Final archive report/media/guide/evidence playback and links | Not yet performed/reported |
| Uploader | Benjamin |
| Backup uploader / exact LMS cutoff / upload receipt | Not yet recorded |

## Package checklist

Use a new empty folder, separate from the working repository. The source root
must contain project/ and assignment/ where the documented relative paths expect
them. Include tracked repository content; exclude .git, .venv, caches, local
temporary/build folders, credentials and unrelated personal material. Required
private declarations belong in the private LMS package, not public GitHub.

- [ ] Record candidate or final status, exact source SHA, ZIP filename, date and tester.
- [ ] Extract the ZIP using Windows Extract All or the platform's normal tool.
- [ ] Confirm report, signed declaration, guide, repository evidence, data, three
      models, fictional samples, both MP4 files and presentation deck are present.
- [ ] If app ZIPs are included, keep their original filenames/bytes and checksums.
- [ ] Run the source checks below from the extracted repository root.
- [ ] Start the dashboard; check all three model routes, mixed CSV, export and
      warnings. Use fictional data and record errors without changing results.
- [ ] Check the packaged app separately if distributing its ZIP: extraction,
      allowed security approval, Ready/browser, prediction, CSV, Quit and reopen.
- [ ] Open the report and guide; check contents links, figures, evidence links and
      final version wording. Do not count a Word bookmark error as acceptable.
- [ ] Play both videos fully with intended audio; open the slides in presentation mode.
- [ ] Record exact environment, commands, counts, screenshots/logs and failures.
- [ ] Obtain teammate review; after merge confirm the final source SHA/ZIP.
- [ ] Upload the single ZIP to LMS, download the uploaded copy if possible,
      compare SHA-256, check extraction and retain the receipt privately.

### Windows source checks

From the extracted repository root with Python 3.12 installed:

~~~powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe --version
.venv\Scripts\python.exe -m pip install -r project/code/requirements.txt
.venv\Scripts\python.exe -m pip check
.venv\Scripts\python.exe -m pip freeze
.venv\Scripts\python.exe -m unittest discover -s project/code -v
.venv\Scripts\python.exe -m unittest discover -s project/packaging -v
.venv\Scripts\python.exe project/code/verify_dataset.py
.venv\Scripts\python.exe project/code/predict.py --mode confirmatory --csv project/data/sample_roster.csv
.venv\Scripts\python.exe -m streamlit run project/code/dashboard.py
~~~

Historical suites contain 110 application tests and 18 packaging tests; report
the actual output, not an assumed pass count. Dataset verification should report
395 Mathematics records, 130 High Risk and 265 Low Risk. The sample roster
predicts A/B and skips C/D with reasons. Stop source Streamlit using Ctrl+C.

For an easy manual routing check, use attendance 80, study hours 4, failures 0,
G1 12, with G2 blank, then 0, then 14: expected retained-model High-Risk
probabilities are approximately 9.2%, 99.6% and 0.3% respectively. For Early-Warning,
attendance 40, study hours 4, failures 0 gives High Risk, approximately 85.9%.
For study-hours warning, use attendance 80, study hours 40, failures 0, G1 12,
G2 blank: approximately 66.1% High Risk with warning. Results are fictional
functional checks, not new predictive evaluation.

Do not retrain models as an ordinary installation check. Deliberate model
reproduction overwrites generated artifacts and belongs in a separate copy.

## Return this record to the team

- Candidate/final; source SHA; ZIP filename and SHA-256:
- Tester, date, OS, browser and Python:
- pip check; application tests; packaging tests; dataset verification:
- Three routes; mixed CSV/skipped reasons; export; study-hours warning:
- Source shutdown; packaged launch/Quit/reopen if checked:
- Report/guide/evidence links; both full video playbacks; slides:
- Declaration included; teammate reviewer/date:
- Any failure, assistance or unresolved issue:

Do not post personal file paths, signatures or real student data in public evidence.
