# Submission package checks

## Final handover plan — 4 November 2026

Benjamin uploads **two ZIPs to separate LMS submissions** by 7 November:

1. Final project: selected repository source, final report, signed declaration,
   guides, dataset/models/samples, evidence, retrospective meeting log and AI records.
2. Presentation/product demo: final slide deck and both MP4 demonstration videos.

Any app ZIPs included in the project submission retain their original release
filenames and checksums. Include them explicitly in the private manifest.
Benjamin is the sole uploader; no backup is agreed. The exact cutoff time has
not been supplied here, so Benjamin must use the time shown in LMS.

The final source version is the actual approved **PR #126 merge commit**.
Obtain it from the merged PR after review, record it in the private manifest
and report, and download that commit's source ZIP. A branch head or temporary
test-merge SHA is not the approved final merge. Recording this after merge does
not require a new repository PR.

The published app remains v0.1.0-preview / ab4a604, distinct from later source
documentation. See [release notes](app-release-notes.md).

## Evidence and completion status

| Check | Status |
|---|---|
| Candidate source f9c9d12 | Checks reported in Section 12.5 of the supplied report and confirmed by Benjamin; detailed original artifacts/date were not provided for this update |
| Repository verification on 4 November | 110 application and 18 packaging tests passed in the existing Windows Python 3.12.10 environment; not a final archive run |
| Declaration | Equal thirds and all three signatures/confirmations reported; private form |
| Slides | Reviewed by all three; merged PR #127 |
| Rehearsal | Completed 3 November, all three, 30-minute session, all good per Benjamin |
| Public app downloads | All 11 assets verified on 31 October; unchanged published ZIPs |
| Final report | Anna and Jackie approved for submission; confirmed by Benjamin on 4 November |
| Final merged-source ZIP and two assembled LMS ZIPs | Must be identified, extracted and checked after final merge; results belong in the private manifest and #97 |
| LMS upload and receipts | Not yet reported; Benjamin records these privately and updates #98 after upload |

The later candidate-source check does not establish acceptance of the final
assembled report/media ZIPs. Keep that distinction in the final report.

## Package checklist

Use a new empty folder at a short path, such as `D:\sarah`, separate from the
working repository. If Windows extraction reports a path-length error, resolve
it and extract a complete copy before testing. The source root
must contain project/ and assignment/ where the documented relative paths expect
them. Include tracked repository content; exclude .git, .venv, caches, local
temporary/build folders, credentials and unrelated personal material. Required
private declarations belong in the private LMS package, not public GitHub.

- Record candidate or final status, exact source SHA, ZIP filename, date and tester.
- Extract the ZIP using Windows Extract All or the platform's normal tool.
- Confirm report, signed declaration, guide, repository evidence, data, three
      models, fictional samples, both MP4 files and presentation deck are present.
- If app ZIPs are included, keep their original filenames/bytes and checksums.
- Run the source checks below from the extracted repository root.
- Start the dashboard; check all three model routes, mixed CSV, export and
      warnings. Use fictional data and record errors without changing results.
- Check the packaged app separately if distributing its ZIP: extraction,
      allowed security approval, Ready/browser, prediction, CSV, Quit and reopen.
- Open the report and guide; check contents links, figures, evidence links and
      final version wording. Do not count a Word bookmark error as acceptable.
- Play both videos fully with intended audio; open the slides in presentation mode.
- Record exact environment, commands, counts, screenshots/logs and failures.
- Obtain teammate review; after merge confirm the final source SHA/ZIP.
- Upload each ZIP to its correct LMS submission, download each uploaded copy if possible,
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

## Private submission manifest fields

- Candidate/final status, source SHA, each ZIP filename and SHA-256.
- Tester, date, OS, browser and Python.
- pip check, application tests, packaging tests and dataset verification outcomes.
- Three routes, mixed CSV/skipped reasons, export and study-hours warning outcomes.
- Source shutdown and packaged launch/Quit/reopen if checked.
- Report/guide/evidence links, both complete video playbacks and slide opening.
- Declaration included, teammate reviewer and review date.
- Any failure, assistance or unresolved issue and its resolution.

Do not post personal file paths, signatures or real student data in public evidence.
