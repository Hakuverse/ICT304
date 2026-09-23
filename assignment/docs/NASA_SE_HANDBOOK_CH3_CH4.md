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

**How this applies to SARAH:** our team's own project brief already maps itself onto this
framework — the Assignment and the Final Project are, in effect, our own Pre-Phase A/Phase A and
Phase B. Concretely:

- **Pre-Phase A / Phase A (Concept Studies, Concept and Technology Development)** ≈ our project
  proposal stage: pitching the SARAH idea, identifying the problem (students flagged too late),
  and getting tutor approval before committing development time — the same "prove the concept is
  worth funding/committing to before building it" logic NASA applies at Pre-Phase A (NASA, 2016,
  §3.3, p. 21).
- **Phase B (Preliminary Design and Technology Completion)** ≈ this Assignment: our data
  pipeline, EDA, feature selection, and the working Logistic Regression / Decision Tree prototype
  are exactly "preliminary design and technology completion" — proving the chosen approach works
  before committing to the full build (NASA, 2016, §3.5, p. 25).
- **Phase C/D (Final Design, Integration and Test)** ≈ our Final Project: turning the prototype
  into the finished dashboard, testing it end-to-end, and delivering the demo video (NASA, 2016,
  §3.6–§3.7, pp. 27–29).

We are a small student prototype, not a NASA spaceflight program, so we don't have formal Key
Decision Point reviews or Phase E/F (operations, decommissioning) — those stages are outside this
unit's scope. The value of citing Chapter 3 is structural: it's the justification for why our
report is organised as "Assignment = early life-cycle phases, Final Project = later phases,"
which is exactly the framing the project brief already uses.

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
  `src/data_processing.py` and `src/train_models.py`.

Citing §4.1 and §4.2 by name and page also strengthens the report's methodology section: it shows
the team didn't just build a classifier and call it "system engineering" — the actual
requirements-gathering step (stakeholder → requirement) followed the process the unit teaches.

## In-text citation examples (ready to paste into the report)

Use these forms — page numbers for anything closely paraphrasing a specific process description,
section numbers alone when referring to the phase/process in general:

- "We follow the System Engineering Product Life Cycle described in the NASA Systems Engineering
  Handbook (NASA, 2016), specifically the Formulation phases — Pre-Phase A through Phase B
  (NASA, 2016, §3.3–§3.5, pp. 21–27) — for this Assignment, and the Implementation phases —
  Phase C and D (NASA, 2016, §3.6–§3.7, pp. 27–29) — for the Final Project."
- "Our Stakeholder Expectation and Technical Requirement sections follow the Stakeholder
  Expectations Definition Process and Technical Requirements Definition Process described in the
  NASA Systems Engineering Handbook (NASA, 2016, §4.1, p. 45; §4.2, p. 54)."

## Checklist status (issue #20)

- [x] Read Chapter 3 for the system engineering life-cycle phases.
- [x] Read Chapter 4 for stakeholder expectations and technical requirements.
- [x] Write a short explanation of how each applies to SARAH (above).
- [x] Add separate in-text citations and the full handbook reference, with section/page details
      (above). Page numbers verified against the handbook's own table of contents, not guessed.

**File/report link for the issue's "Finished when" field:** `docs/NASA_SE_HANDBOOK_CH3_CH4.md`
(this file) — once pushed, paste that path (or the GitHub blob URL) into the issue.

## Where this replaces/upgrades existing report content

`report_template/generate.js` Section 2 ("System Engineering Process Overview") currently cites
the handbook only in general terms ("Chapter 3 of the NASA Systems Engineering Handbook," no
section/page). Swap its intro paragraph and the "Evidence" column of the phase table for the
section/page-cited versions above — the phase-mapping table in that file already lines up almost
exactly with the Chapter 3/4 structure above, it just needs the specific citations added.
