# Benjamin's preliminary Windows launch check

Date: 28 October 2026. Tester: Benjamin.

This records a preliminary launch check on Benjamin's development computer.
It does not replace Anna's full Windows checklist or Jackie's macOS checks.

## Package and environment

- Reported OS: Windows 11 Home 25H2. Exact OS build was not recorded for this check.
- Browser: Opera GX, identified from the original supplied screenshot. Version not recorded.
- Package: `SARAH-0.1.0-preview-windows-x64-ab4a604.zip`.
- Source: `ab4a604a71ecef9f0585a137a014e7dd6fb861e2` (PR test-merge build).
- [Actions run](https://github.com/Hakuverse/ICT304/actions/runs/40556703379),
  [Windows artifact SARAH-windows-x64-4](https://github.com/Hakuverse/ICT304/actions/runs/40556703379/artifacts/12757642322).
- [Build details](build-info.json). The outer and inner build-info files matched;
  only one copy is included. The build machine listed there is not the test computer.
- [Package checksum](package.sha256). The local ZIP matched the supplied SHA-256.
  The extracted executable also matched the executable hash in build-info.json.
- [Automated extracted-package checks](extracted-check.json) are build evidence,
  separate from Benjamin's manual observations. Their timings are not GUI startup times.

## Observations

| Step | Actual observation | Evidence |
|---|---|---|
| First launch | Windows displayed "Windows protected your PC" and blocked initial startup. | [Warning screenshot](01-smartscreen-warning.png) |
| More info | The expanded warning showed SARAH.exe, Unknown publisher and Run anyway. | [Expanded warning](02-smartscreen-more-info.png) |
| Continue | Benjamin reported selecting Run anyway, after which the mini launcher and browser dashboard opened and worked. | Tester confirmation and [loaded dashboard](03-dashboard-loaded.png), showing the page and input controls. |

Outcome: **launch passed with an unsigned-application warning** on this device.
The included dashboard screenshot was supplied by Benjamin without the browser
tabs and bookmarks. It shows the loaded form, not a completed prediction or startup
duration. The original screenshot containing personal information remains local.
No separate screenshot of the mini launcher was supplied.

Startup duration, offline operation, repeated launch, quit/restart, detailed
prediction checks and CSV export were not recorded in this preliminary check.
No complete W01-W09 pass is claimed. Anna's [Windows results](../results.md)
were subsequently completed and reviewed in merged PR #121; #114/#115 are closed. This preliminary record remains a separate, limited check.

An unsigned-app warning remains a deployment limitation. This successful launch
does not establish that a managed university computer will permit the same action.
