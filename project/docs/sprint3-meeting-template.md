# SARAH Sprint 3 planning meeting

Prepared 20 September 2026 from GitHub main `abd33806ef54416e0296541289f3f8fbbb414246`, live issues, and the local assignment brief. Planning template; two-mode approval and the meeting routine were confirmed by Benjamin during this review. Other proposals remain for team agreement.

**Sprint:** Tuesday 22-Tuesday 29 September 2026 | **Milestone:** [Sprint 3](https://github.com/Hakuverse/ICT304/milestone/3)

**Meeting:** Tuesday 22 September 2026, after class; tutor review first, then team-only planning.

**Time/location/link:** ____ | **Facilitator:** ____ | **Notes:** ____

**Attendees:** Benjamin / Anna / Jackie / ____ | **Absent:** ____

**Proposed goal:** Implement SARAH's approved two-mode contract and agree subsystem interfaces, evaluation protocol and test plan, and prepare a reproducible handoff for the AI prototype due on 3 October.

## 1. Preparation

- [ ] Bring the current report/Colab link: ____ (work outside GitHub was not reviewed).
- [ ] Bring evidence for #9 and record the approved two-mode decision in the project decision log.
- [ ] Each member estimates available hours and names one reviewer.
- [ ] Read [the repository review](sprint3-repo-review-and-issue-drafts.md) beside this file.
- [ ] Confirm any tutor changes to the published assignment brief and the LMS deadline/time zone.

| Member | Available hours | Main responsibility this sprint | Reviewer |
|---|---:|---|---|
| Benjamin | ____ | ____ | ____ |
| Anna | ____ | ____ | ____ |
| Jackie | ____ | ____ | ____ |

## 2. Tuesday meeting sequence

**First: tutor/stakeholder review (5-10 minutes).** Use section 7 below before team planning; capture feedback and constraints. Two modes are already approved, so show the implementation plan and raise only unresolved details.

**Then: team-only planning (45 minutes), all three members present.**

| Minutes | Discussion | Required output |
|---|---|---|
| 0-5 | Sprint 2 closeout | Accept #9 evidence or name remaining action; record approved modes |
| 5-15 | Mode implementation and architecture | Signed-off input table, prediction timing and three-subsystem boundary |
| 15-23 | Evaluation and tests | Agree metric, folds, tuning separation and test-plan owner |
| 23-35 | Backlog and capacity | Owners, reviewers, sizes, due dates and committed/deferred work |
| 35-42 | 3 October readiness | Prototype owner, report location, submission checklist and contingency |
| 42-45 | Read decisions aloud | Confirm actions and questions for tutor |

## 3. Sprint 2 closeout

Live snapshot: 7/8 issues closed. [#9](https://github.com/Hakuverse/ICT304/issues/9) is open, assigned to Benjamin, with a 19 September comment saying the draft is done. Check the report paragraph and review evidence before closing.

| Item | Evidence / remaining gap | Decision | Owner / date |
|---|---|---|---|
| #9 subsystem reasoning | Report section/link: ____ | Close / finish / carry over | ____ |
| #8 and #16 mode lists | Closed, but main documents only one four-feature list | Follow-up under #26 | ____ |
| #10 G3 exclusion | Documentation closed; automated tests absent from main | Tests under #26 | ____ |
| #15 distributions | Current plotting code pools classes; issue requested risk-separated distributions | Add small follow-up under #21 or linked task | ____ |

## 4. Decisions to settle

| Decision | Proposed starting point | Final decision / evidence |
|---|---|---|
| Early-Warning inputs | `attendance_pct`, `study_hours`, `failures` | Two-mode approach approved; record exact contract |
| Confirmatory inputs | Same three plus `previous_score` | ____ |
| Availability | Confirmatory requires both G1 and G2 for the current average; define the early prediction cutoff | ____ |
| Approval | Benjamin confirms two modes are approved | Proceed to implementation/testing; add approval evidence link: ____ |
| Architecture | Prediction; Recommendation/Intervention; Batch Roster Processor + Dashboard. Show preprocessing as a component | ____ |
| Attendance meaning | Current 0-100 value is a capped absence proxy, not a measured attendance percentage | ____ |
| Primary metric | Proposed High-Risk F1, with recall/precision and missed-student counts explicitly discussed | ____ |
| Validation | Fixed seeded stratified folds shared across comparisons; learned preprocessing fitted within folds | ____ |
| Tuning | Inner validation/nested CV if tuning; do not report tuning-selection scores as independent final performance | ____ |
| Recommendation meaning | Rule-selected support factor; do not call global importance a per-student explanation | ____ |
| Source of truth | Canonical report link, code path and assignment packaging approach | ____ |

Proposed workflow: teacher form/CSV -> validate mode-specific input -> matching preprocessing/model -> risk output -> recommendation rules -> roster display. Separate offline training and G3-derived labels from live prediction.

## 5. Sprint backlog and ownership

Sprint 3 issues #17-#21 and #26-#28 are open. Owners and reviewers remain for the team to assign. Sizes below are provisional: S <= half day, M around one day; resize for your actual capacity.

| Issue | Deliverable / acceptance evidence | Size | Owner | Reviewer | Target |
|---|---|---|---|---|---|
| [#17](https://github.com/Hakuverse/ICT304/issues/17) Architecture | Three named subsystems, offline/online paths, inputs/outputs, mode handling | S | ____ | ____ | 24 Sep |
| [#18](https://github.com/Hakuverse/ICT304/issues/18) Split + CV | Fold/seed policy, leakage controls, metrics, tuning and confusion-matrix plan | M | ____ | ____ | 24 Sep |
| [#19](https://github.com/Hakuverse/ICT304/issues/19) Class weights | Eight configurations: 2 modes x 2 models x 2 weight settings; same splits | S | ____ | ____ | 24 Sep |
| [#20](https://github.com/Hakuverse/ICT304/issues/20) NASA citations | Ch.3 lifecycle and Ch.4 design processes correctly separated and checked | S | ____ | ____ | 25 Sep |
| [#21](https://github.com/Hakuverse/ICT304/issues/21) System Design | Architecture, contracts, timing limitations and reconciled feature documentation | M | ____ | ____ | 27 Sep |
| [#26](https://github.com/Hakuverse/ICT304/issues/26) | Implement approved modes, explicit feature selection and tests | M | ____ | ____ | 25 Sep |
| [#27](https://github.com/Hakuverse/ICT304/issues/27) | Requirement-to-test matrix across every subsystem | S | ____ | ____ | 26 Sep |
| [#28](https://github.com/Hakuverse/ICT304/issues/28) | Assignment readiness and reproducible prototype handoff | S | ____ | ____ | 27 Sep |

**Capacity check:** This is eight candidate issues, above the local Scrum template's suggested 3-6. Keep #20 as a checklist within #21 and #19 within #18 if helpful; preserve traceability rather than losing their work. Agree commitments when assigning the eight issues now listed in the milestone.

**Committed:** ____ | **Deferred:** ____ | **Reason:** ____

## 6. Exit criteria and Sprint 4 handoff

- [ ] Two-mode approval, exact input contract and any implementation questions recorded.
- [ ] Diagram, interfaces and test matrix linked from the report.
- [ ] Mode tests pass; inference does not require G3 or unavailable prior grades.
- [ ] Dataset scope and input semantics are explicit.
- [ ] Evaluation plan ready for LR/Decision Tree implementation.
- [ ] Clean-environment setup command and tested dependency versions recorded.
- [ ] Prototype/training owner and initial-results date confirmed; target an initial run by 27-28 September if capacity allows.
- [ ] Report sections have owners; declaration form and AI prompt evidence have owners.

**Proposed buffer:** 29 Sep integrate design/prototype; 30 Sep-1 Oct complete comparisons/report; 2 Oct teammate reproduces package and checks submission; 3 Oct final deadline. Confirm exact LMS cutoff.

## 7. Tutor review (5-10 minutes)

1. Goal: hit / partial / missed, with evidence: ____
2. Show: diagram, both input schemas, test plan, preprocessing output, any prototype results.
3. Confirm remaining detail: with the two modes approved, what prediction time can we credibly claim?
4. Confirm: attendance proxy and dataset limitations are acceptable for this prototype.
5. Report: remaining blockers, owner and resolution date; bring feedback into the following team meeting.
6. Next goal: complete and reproduce the AI subsystem prototype and initial results for 3 October.

**Tutor feedback and changes:** ____

## 8. Decisions, actions and retrospective

| Decision/action | Owner | Due | Evidence link | Status |
|---|---|---|---|---|
| ____ | ____ | ____ | ____ | ____ |
| ____ | ____ | ____ | ____ | ____ |
| ____ | ____ | ____ | ____ | ____ |

| Keep | Stop | Try |
|---|---|---|
| ____ | ____ | ____ |

**One improvement to act on:** ____ | **Owner:** ____

Definition of Done: peer-reviewed PR merged, relevant documentation updated, and code reproduced by another member; for documents, reviewer checks them against the brief and the agreed design. Link evidence before closing issues.

