# Final project stage

The working assignment prototype is in [assignment/](../assignment/), for the
assignment due on 3 October 2026. This folder is reserved for the next stage;
its code, data, docs and demo folders are currently placeholders.

## Starting after submission

1. Preserve the exact assignment ZIP and Git commit submitted through LMS.
2. Copy the required assignment code, dataset, saved models and useful documents
   into the corresponding folders here. Keep tutorials separate.
3. Leave out virtual environments, caches, temporary outputs and private forms.
4. Update commands and any hard-coded assignment paths for the project copy.
   Most scripts resolve data/models relative to their location, but
   `issue33_comparison.py` explicitly uses an `assignment/` layout and must be
   reviewed before reuse. Its checks describe the assignment's fixed experiment.
5. Create a fresh environment and run the copied tests and sample predictions.
6. Continue dashboard, recommendation and integration work here. Preserve the
   submitted assignment snapshot; any later correction must be separately recorded.

## Evidence and submission records

The [assignment verification summary](../assignment/docs/submission-verification.md)
records the existing prototype checks. They do not establish that new project
features work. New results, user testing and demonstration evidence belong to
this stage and will need their own records.

The [project prompt appendix](report/appendix-ai-prompts.md) remains a placeholder.
The earlier shared prompt-log path is not present in this checkout. Actual
required declarations and prompt records are maintained by the team for each
submission. The assignment report and signed declaration are submitted separately
and are not reproduced in this public repository with personal details.
