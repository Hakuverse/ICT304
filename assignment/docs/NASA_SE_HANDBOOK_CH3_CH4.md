# NASA SE Handbook Chapters 3 and 4 — application to SARAH

This document connects the project life cycle and system design processes to
SARAH. References use the handbook's printed page numbers. Source: the official
NASA/SP-2016-6105 Rev2 PDF at
https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf.

## Full reference

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

## Relationship to the assignment

The stakeholder expectations and technical requirements in the report apply the
Chapter 4 processes to SARAH. The phase mapping above describes the course-level
adaptation, with prototype work in the assignment and later integration in the
project stage. The final report contains the corresponding in-text citations.
