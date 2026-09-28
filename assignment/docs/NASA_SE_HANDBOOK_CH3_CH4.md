# NASA SE Handbook Ch3,4 — how it applies to SARAH (Sprint backlog: ICT304 #20)

Covers the issue's checklist: read Ch.3 and Ch.4 of the NASA Systems Engineering Handbook,
explain how each applies to SARAH, and add proper in-text citations + full reference with
section/page detail. Source: the official PDF at
https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf
(NASA/SP-2016-6105 Rev2).

## Full reference (APA 7th — use exactly this in the report's References section)

National Aeronautics and Space Administration. (2016). *NASA systems engineering handbook*
(NASA/SP-2016-6105 Rev2). NASA. https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf

## Chapter 3 — "NASA Program/Project Life Cycle" (pp. 17–35)

Chapter 3 lays out NASA's seven-phase project life cycle, split into two halves:

- **Formulation** — Pre-Phase A: Concept Studies (§3.3, p. 21), Phase A: Concept and Technology
  Development (§3.4, p. 23), Phase B: Preliminary Design and Technology Completion (§3.5, p. 25).
- **Implementation** — Phase C: Final Design and Fabrication (§3.6, p. 27), Phase D: System
  Assembly, Integration and Test, Launch (§3.7, p. 29), Phase E: Operations and Sustainment
  (§3.8, p. 31), Phase F: Closeout (§3.9, p. 31).

Each phase ends in a Key Decision Point where the project either proceeds, is redirected, or is
cancelled — the whole chapter is essentially "what work happens, in what order, before you're
allowed to move to the next stage."

## SARAH phase mapping

We adapt Pre-Phase A through Phase F to a student project. The assignment due on 3 October covers the early design work and a classifier prototype. Later phases describe the complete project due on 7 November; they are not claims of a live university deployment.

| Phase | Application to SARAH | Evidence / next output |
|---|---|---|
| Pre-Phase A: Concept studies | Identify the problem and intended users; discuss the idea with the tutor. | Problem statement and tutor feedback. |
| Phase A: Concept and technology development | Explore the data, choose inputs and compare possible approaches. | Dataset checks, EDA and feature selection. |
| Phase B: Preliminary design and technology completion | Define the two modes, system parts and tests; investigate the classifier prototype. | Requirements, diagram, model comparison and assignment report. |
| Phase C: Final design and fabrication | Complete the dashboard and recommendation rules. | Working components and updated design. |
| Phase D: Integration and testing | Connect the components and test the complete tutor workflow. | Integration tests, fixes and tutor feedback. |
| Phase E: Operations and sustainment | Prepare deployment and maintenance plans, the user guide and a demo video. | Deployment/maintenance plan, user guide and demo video. |
| Phase F: Closeout | Polish the work, rehearse the presentation and submit the documents and project files. | Final report, tested code, slides, signed declaration and submission backup. |

The Phase E/F activities are our course-level adaptation. Weekly tutor reviews guide changes; we do not claim to follow NASA's formal approval process. Sprint 4 finishes the assignment prototype and report. A sprint number is not a NASA phase number.

## Chapter 4 — "System Design Processes" (pp. 43–76)

Chapter 4 covers the four processes that turn a vague need into a validated design. The two the
brief specifically asks about:

- **§4.1 Stakeholder Expectations Definition Process** (pp. 45–53) — the process of identifying
  who the stakeholders are and eliciting what they actually need, in their own language, before
  any technical translation happens. Output: a documented, agreed statement of expectations
  (NASA, 2016, §4.1, p. 45).
- **§4.2 Technical Requirements Definition Process** (pp. 54–62) — the process of translating
  those stakeholder expectations into specific, measurable, verifiable technical requirements
  that a design can actually be built and tested against (NASA, 2016, §4.2, p. 54).

**How this applies to SARAH:** this is a direct match to our own project structure — the project
proposal literally uses NASA's own terms, "Stakeholder Expectation" and "Technical Requirement,"
as section headings:

- **Stakeholder Expectation (§4.1):** "The university/lecturer wants to identify students who
  are at risk of failing early, so that support or intervention can be provided before it is too
  late." This is exactly a §4.1-style output — the stakeholder (the tutor/university) is
  identified, and their need is stated in plain language, not yet as a technical spec.
- **Technical Requirement (§4.2):** "The system should accept student information such as
  attendance, study hours, and assessment scores, then use an AI model to predict whether the
  student is High Risk or Low Risk." This is the §4.2 translation step — the vague stakeholder
  want ("identify at-risk students early") becomes a concrete, testable requirement (specific
  inputs, a binary classification output), which is what actually got built in
  `assignment/code/data_processing.py` and `assignment/code/train_models.py`.

Citing §4.1 and §4.2 by name and page also strengthens the report's methodology section: it shows
the team didn't just build a classifier and call it "system engineering" — the actual
requirements-gathering step (stakeholder → requirement) followed the process the unit teaches.

## In-text citation examples (ready to paste into the report)

Use these forms — page numbers for anything closely paraphrasing a specific process description,
section numbers alone when referring to the phase/process in general:

- "We follow the System Engineering Product Life Cycle described in the NASA Systems Engineering
  Handbook (NASA, 2016), specifically the Formulation phases — Pre-Phase A through Phase B
  (NASA, 2016, §3.3–§3.5, pp. 21–27) — for this Assignment, and the Implementation phases —
  Phase C through F (NASA, 2016, §3.6–§3.9) — for the Final Project."
- "Our Stakeholder Expectation and Technical Requirement sections follow the Stakeholder
  Expectations Definition Process and Technical Requirements Definition Process described in the
  NASA Systems Engineering Handbook (NASA, 2016, §4.1, p. 45; §4.2, p. 54)."

## Checklist status (issue #20)

- [x] Read Chapter 3 for the system engineering life-cycle phases.
- [x] Read Chapter 4 for stakeholder expectations and technical requirements.
- [x] Write a short explanation of how each applies to SARAH (above).
- [x] Add separate in-text citations and the full handbook reference, with section/page details
      (above). Page numbers verified against the handbook's own table of contents, not guessed.

**File/report link for the issue's "Finished when" field:** `assignment/docs/NASA_SE_HANDBOOK_CH3_CH4.md`
(this file) — once pushed, paste that path (or the GitHub blob URL) into the issue.
