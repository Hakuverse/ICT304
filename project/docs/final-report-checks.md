# Final report checks — 2 November 2026

Benjamin leads final report editing; Anna and Jackie review. The local Word report
remains separate from the public repository. AI prompt content was excluded from
this review. PR #126 is the selected final-change branch and is not yet merged.

## Second review

Corrected in the revised report: purpose subtitle, most spelling corrections,
depth-6 recall 0.395, test commit 9dc7132, main-body headings 7.4/11.3, obsolete
assignment paragraphs removed, Appendix G reference replaced, release screenshot
added and supporting evidence links expanded.

Remaining report edits:
- Update the contents again: cached entries still show 7.3/11.2 for renamed
  subsections. Confirm all headings/bookmarks/page numbers in the final export.
- Use PR #126's current candidate SHA during review; after merge replace cover,
  version table, repository reference and evidence links with the actual merge SHA.
  Keep historical test dates/commits and ab4a604 binary identity unchanged.
- Section 7.4: replace “the attendance and estimate” with “the attendance estimate,
  and”; prefer “unresolved” to “unsolved” methodological limitations.
- Section 8.2: add launcher/packaging verification to the coverage table.
- Section 10.4: remove repeated public-download/hash sentence and “; At publication”.
- Section 10.3: identify Anna as Windows acceptance tester and Jackie as Mac tester.
- Section 11.1: use the agreed assessment-period support statement.
- Section 12: replace draft/TODO text with operating instructions, reproduction
  procedure, version distinction and actual manifest/check status.
- Section 13: equal one-third contribution and confirmed signing; add external-work
  acknowledgment without changing the unfinished AI prompt record.
- Appendix A: “TN: LR...” should be “Note: LR...”; TN already means true negative.
- Appendix B E9: remove editorial advice copied into the cell. E11 must describe
  merged PR #127 and pin its file link to the selected PR #126 snapshot.
- Appendix C: add source download/root-folder step and identify training versus
  comparison-report regeneration. Point app users to the release guide.
- Recheck large blank areas, small labels and table/heading pagination in Word.

No final archive test, rehearsal completion, upload or tutor-device/recovery test
is inferred from editing this report. See [package checks](submission-package-checks.md),
[contributions](contribution-checks.md), [presentation](presentation-notes.md) and
[maintenance](maintenance-plan.md) for current evidence and decisions.

## Repository validation — 2 November

- 110 application tests and 18 packaging tests passed in the existing local
  Windows Python 3.12 environment under normal permissions. Restricted attempts
  encountered temporary-folder permission errors/stalling before the successful runs.
- 945 local Markdown file targets in project/ resolved; git diff --check passed.
- Compared with main after PR #127, the training-script AST is unchanged after
  excluding its module documentation and the corrected generated reference text.
- No datasets, saved models or AI prompt records changed. Published binaries
  were not rebuilt. These development checks do not substitute for Benjamin's
  upcoming clean-extracted submission-package verification.
- The revised report's read-only Word PDF export has 45 pages and no detected
  bookmark-error text; the contents still needs its renamed subsection labels refreshed.
