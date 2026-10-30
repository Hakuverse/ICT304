# Issue 116 packaged workflow evidence

Status at 30 October 2026: ready for team review, with macOS D01 still outstanding.

| Coverage | Windows - Anna | macOS - Jackie |
|---|---|---|
| A01-A05 | Earlier #114 evidence reused | Earlier #115 evidence reused |
| B01-B09 | Passed, 30 October | Passed as reported, 29 October |
| C01-C08 | Passed, 30 October | Passed as reported, 29 October |
| D01 occupied port | Passed; original image reviewed locally | Not tested |
| Team approval | Pending | Pending |

- [Windows results and evidence](windows/results.md)
- [macOS results and remaining D01 steps](macos/results.md)
- [Shared run sheet](../../../app-workflow-testing.md)
- [Source reference outputs](source-reference.json)
- [Evidence file hashes](evidence-manifest.json)

Both platforms used their ab4a604 packages from Actions run 40556703379, with bundled Python 3.12.10. These records do not claim a new build, a clean machine or a tutor-device test.

The four supplied C05/C06 exports match the source reference in every field. Jackie's seven input files match the shared CSV fixtures. Source-reference values remain expected outputs; actual evidence comes from the testers' records, screenshots and exports.

The PR includes focused screenshots and all four exports. Additional Mac context captures remain in the local evidence folder. One Mac image was renamed from G1=21 to G1=-1 to match its contents. Anna's D01 screenshot was withheld from the public repository because it contains a personal computer username; her recorded ports and outcome are retained. No screenshot content was changed.

Before completing #116, add Jackie's D01 result and have a teammate review the records in PR #122. The later #117 walkthrough remains separate from these functional tests.
