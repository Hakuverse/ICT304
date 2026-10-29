# SARAH maintenance and recovery plan

## Purpose and status

This plan explains how the team will keep the local SARAH prototype working, review updates, and return to an earlier accepted version if an update fails. The reviewed [local deployment guide](deployment-guide.md) explains how to install, check, start and stop the application on Windows and macOS.

SARAH currently runs as a **local Streamlit prototype**. This document does not establish public hosting, continuous monitoring, a production service or support after the project.

**Recovery status:** The steps below are a written plan. No recovery drill is claimed by this document. A drill may be marked successful only after its date, operator, commit, steps and actual results have been recorded separately.

**Packaged-app work:** Follow the [application plan](app-deployment-plan.md) and
[current package guide](app-package-testing.md) for #112–#118. Keep each complete
package with its version, build-info and checksum; do not mix an executable or
_internal folder from different builds. Only return to an accepted tested package,
not the superseded candidates that had the Windows loading fault. A package
recovery drill and final release instructions remain follow-up work.

## Roles and support limits

| Person or role | Responsibility during the project |
|---|---|
| Any teammate or tester | Report a problem with enough detail to reproduce it. Use fictional inputs and keep real student information out of public issues and evidence. |
| Jackie | Own the #77 local deployment instructions and this #78 maintenance and recovery plan; clarify the documented setup and recovery steps. |
| Assigned issue owner | Investigate a specific bug and prepare its fix in a separate branch. The owner is assigned when that issue is reviewed; this plan does not assign every future fix to Jackie. |
| Reviewer other than the fixer | Check the proposed change, relevant tests, evidence and documentation before merge. |
| Anna | Own the #79 user guide and review changes that affect its user-facing instructions or explanations. |
| Benjamin | Coordinate the #80 teammate walkthrough and #82 Sprint 7 review and handover, including unresolved issues and their next owners. |

These roles reflect the current project allocation. They do not create an indefinite helpdesk commitment. Before final handover, the team must record who accepts any remaining issues, what support they will provide and when that support ends. No 24-hour response time or post-project support period has been agreed.

## Report, review and release an update

1. **Report:** Open a GitHub issue. Record the affected commit, OS, Python and relevant package versions, the form or CSV workflow, steps to reproduce, expected result and actual result. Attach only safe logs or screenshots with fictional student data. Do not post credentials or real student records.
2. **Triage:** The team reviews impact and priority, assigns a fix owner and decides whether the current local version should continue to be used. A prediction, model-loading or recommendation problem should be treated cautiously; do not rely on an unverified result to make a student decision.
3. **Fix in a branch:** The owner makes the change in a separate branch and opens a pull request linked to the issue. Do not modify the accepted version in place.
4. **Check:** Run the relevant targeted tests and the full automated suite. Repeat affected form, CSV and platform checks when behaviour changes. Record the tested commit, commands, environment and actual outcomes. A failing check must remain visible rather than being called a pass.
5. **Review:** A teammate other than the fixer reviews the change and its evidence. Update the deployment guide, user guide, model documentation or this plan when their instructions are affected.
6. **Merge and record:** Merge only after the team accepts the evidence and remaining limitations. Record the new commit and version set before asking another person to use it.

A package update also needs review: the requirements include minimum versions for several packages, so a later installation may resolve to different exact versions. Do not treat `pip install` completing as proof that an updated environment behaves identically.

## Model and recommendation changes

Normal prediction uses the committed saved models; **retraining is not part of routine installation or maintenance**. The three model files are:

- `project/models/early_warning_model.joblib`
- `project/models/confirmatory_g1_model.joblib`
- `project/models/confirmatory_g1_g2_model.joblib`

If a model is deliberately retrained or replaced, review its dataset, evaluation method, false positives and false negatives, and relevant model and workflow tests before use. Record the new model files and the code commit together. Do not reuse earlier accuracy figures as results for a changed model.

If a recommendation rule or message changes, compare it with the [agreed recommendation rules](recommendation-rules.md), rerun the rule tests, and check the affected one-student and CSV outputs. Review the wording as a prompt for human discussion, not a proven cause of risk or a guarantee of benefit. An application that starts successfully has not, by that fact alone, passed model or recommendation review.

## Keep a known-working version set

For each version the team accepts for use, keep a record of these items **together**:

| Item | What to record |
|---|---|
| Code | Full Git commit SHA, date, reviewer and link to the accepted PR or decision. |
| Models | The three saved `.joblib` files from that same commit. Do not mix model files from another version. |
| Requirements | `project/code/requirements.txt` from the same commit; it pins `scikit-learn==1.8.0` for the saved models. |
| Environment | OS, Python version and the exact installed package versions from a successful check. Keep a version record, not a copied `.venv`. |
| Verification | Links to `pip check`, automated tests, sample prediction, relevant form/CSV checks and any platform or walkthrough results. |
| Limitations | Known failures, untested areas and any reason the version should not be used for a particular purpose. |

The deployment guide identifies Sprint 7 handover commit `914f808` after PR #107. The video at `847d460` shows the same code and models, with 110 tests reported by Anna. Earlier handovers include `fe9685a` without the warning and `2dfcdf3` before the CSV readability change. Keep historical records; returning to an older version can remove fixes. This review does not establish a recovery drill or a new macOS installation run.

The earlier [Sprint 6 functional evidence](sprint6-review.md) records Windows and macOS checks at `9dc7132`. That is a historical tested baseline, but it predates later usability changes. The [response-time evidence](evidence/issue67/2026-10-20-6395d82/results.md) is from `6395d82` on one reference Mac. Keep these original tested commits attached to their evidence; do not relabel the old runs as tests of `fe9685a`.

Before calling a newer commit the **known-working recovery version**, the team should record its own successful installation and checks. Keep the preceding accepted version available until the replacement is accepted.

## Recover from a failed update

The following is the procedure to follow **if** an update breaks the local application. It is not a record that these steps have already been performed.

1. **Stop and record the failure.** Stop the affected Streamlit process with **Ctrl+C**. Record the failing commit, symptom, OS, Python and package versions, and safe error output. Do not overwrite earlier evidence.
2. **Choose the recovery version.** Look up the latest version set that the team actually accepted. Confirm its commit, models, requirements, package versions, test evidence and known limitations. Do not assume that the newest commit is safe.
3. **Prepare a separate copy.** Obtain the exact recovery commit using the ZIP or clone method in the [deployment guide](deployment-guide.md). Put it in a separate folder. Do not overwrite or delete the broken copy while investigating it.
4. **Recreate the environment.** Make a fresh `.venv` in the recovery folder and follow the deployment guide’s commands for that platform. Run `pip check`, the full automated suite, dataset verification and the fictional sample CSV prediction. Compare the environment with the version record; if exact package versions differ, record that difference instead of claiming an identical restoration.
5. **Check the local workflow.** Start Streamlit and check a representative one-student prediction, a fictional CSV upload, visible results and a normal stop with **Ctrl+C**. Repeat any check related to the reported failure. If a check fails, stop and report it; do not declare recovery successful.
6. **Communicate and retain evidence.** Tell the team which commit is now being used and what limitations it has. Record the date, operator, original failure, recovered commit, checks and actual outcomes. Keep the faulty update linked to its issue until its fix has been reviewed.

An older version can restore operation while also restoring its old limitations. The team must explicitly review that trade-off before selecting it. Recovery means returning to an accepted local version; it does not mean silently discarding the broken version or its evidence.

## Demo data, exports and privacy

Use fictional student IDs and data in public fixtures, screenshots, demonstrations and test exports. Never put real student records, credentials, private forms or local `.venv` files in the public repository.

Temporary downloaded CSV results on a tester’s computer should be removed when no longer needed. Check the exact files first. Do **not** remove fictional exports deliberately retained and linked as project test evidence. Any handling of real student records would require a separately agreed privacy and operating process; this prototype plan does not authorise using them.

## Evidence, limits and next review

The [system test plan](system-test-plan.md) and [Sprint 6 review](sprint6-review.md) identify what was tested, on which commits, and what remains limited. In particular, the recorded timing is from one reference Mac and is not a performance guarantee on other computers. Software checks do not establish model accuracy for every population, calibrated probabilities, intervention benefit or safe automatic decisions.

The #80 walkthrough and corrections are merged in #108, with later guide and CSV warning updates in #109/#110. The Windows Python fallback is documented in the deployment guide. See the [Sprint 7 review](sprint7-review.md) for the handover and remaining limits. If the team performs a recovery rehearsal, add a separate dated record with its operator, exact commit, environment, steps, observed results and evidence link. Until that record exists, describe recovery as **planned, not tested**.
