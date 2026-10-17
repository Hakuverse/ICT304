# Usability check record (#68)

**Date:** 17 October 2026
**Run by:** Anna
**Tester:** Tester A (family member, non-team)
**Version tested:** `main` at commit 13d85f9
**Data:** fictional only (typed examples and `project/data/sample_roster.csv`)

## Earlier session with the tutor (13 October 2026)

Presented using the SARAH Progress Update slides (about 1 minute). The tutor tried
two single-student examples in Confirmatory mode with G1, and the predictions
worked. No specific feedback was given. This was an assisted demonstration, not
an independent usability check.

## Tasks

| # | Task | Expected result | Result | Alone or helped |
|---|---|---|---|---|
| 1 | Early-Warning: attendance 40, study 4, failures 0 | High Risk 0.859 + attendance suggestion | Correct | Helped: did not know where to choose Early-Warning mode or what attendance % means |
| 2 | Confirmatory: attendance 80, study 4, failures 0, G1 8, G2 blank | High Risk 0.818 + assessment review suggestion | Correct | Helped: did not know what G1 is or that G2 can be left blank |
| 3 | Confirmatory: upload `sample_roster.csv` | A and B predicted, C and D skipped | Correct | Alone |
| 4 | Explain why C and D were skipped | C: attendance over 100; D: G2 "NA" not a number | Correct after help | Helped: did not notice the skipped-row messages or the "NA" value; Anna pointed them out |

## Questions

| Question | Tester's answer |
|---|---|
| What does "High Risk" mean? | The student needs more attention from the teacher. (Understood) |
| What does 0.818 mean? | Did not understand without explanation; Anna then explained it as an estimated chance of High Risk. |
| Were the suggestions useful? (1–5) | No rating given; tester understood the meaning of the suggestions. |
| Was anything confusing? | Nothing reported. |
| Would you use SARAH alone to decide? | Yes, but only for teachers. |

## Findings

1. Tester needed help on tasks 1, 2 and 4: finding the mode choice, and the meaning
   of attendance %, G1 and a blank G2.
2. The probability number (e.g. 0.818) was not understood without explanation.
3. Tester said they would use SARAH alone to decide. The limitation (SARAH supports,
   not replaces, the teacher's judgement) was not clear.
4. In the CSV upload, the tester did not notice the skipped-row messages or the
   "NA" value until they were pointed out.

## Proposed changes for #69 (to be agreed by the team)

| Finding | Proposed change | Priority |
|---|---|---|
| 1 | Make the mode choice easier to find, and add short help text to fields (e.g. "G1 = first test grade, 0–20", "Leave G2 blank if there is no second test yet") | To agree |
| 2 | Show plain words next to the probability, e.g. "about 82% estimated chance of High Risk" | To agree |
| 3 | Add a visible note: "Support tool only. Confirm with your own judgement." | To agree |
| 4 | Make skipped rows stand out (e.g. a warning box near the top: "2 students skipped – see reasons below") | To agree |

## Limits of this check

- One tester only, and a family member of the team.
- Tasks 1, 2 and 4 were assisted, so they are not fully independent results.
- The tutor session on 13 October was very short and gave no specific feedback.
