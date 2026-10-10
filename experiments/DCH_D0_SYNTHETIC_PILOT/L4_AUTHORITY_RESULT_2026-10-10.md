# DCH L4: external authority gate, measured engineering result

**Date:** October 10, 2026. **Study classification:** deterministic instrument validation. No participant study. No claim that any human-AI dyad was constituted or that automated curators are superior.

**Code:** [l4_authority_gate.py](l4_authority_gate.py), [adversarial tests](tests/test_l4_authority_gate.py), [paired analysis](l4_compare.py).
**Executed run:** [GitHub Actions 38058117852](https://github.com/Azimn/Attractomancy/actions/runs/38058117852).
**Raw and scored outputs:** [run-unique archive](results/l4-authority-38058117852/). Source model data: frozen [64-response Qwen L3](results/qwen25-15b-l3-38028160714/).

## Implemented decision boundary

The authority gate, separate from the language renderer, validates subject-owned event identifiers, chronological updates, allow-listed source keys and values, and action preconditions. It rejects unauthorized or cross-subject source records, duplicate event IDs, same-key same-time conflicts (including those preceding a later valid revision), invalid time/type metadata, and unsupported values. It returns UNKNOWN with an explicit status when required evidence is missing. For valid inputs, it applies the documented ordered rule and produces the minimum source-event certificate needed to justify that branch. Every output carries an input checksum and source-selection trace.

The initial adversarial tests found a real issue: equal-time conflicts in superseded history could escape validation when only the current latest record was checked. This was fixed in commit eb5a2ff728b7ff5926d491ef429e05cca19201ab by tracking every (key, turn) pair before source selection. The corrected workflow passed its adversarial tests and end-to-end evaluation.

## Executed results

For 12 synthetic histories across four stages and two evidence arms (96 total), the deterministic gate matched **96/96 target actions**, **96/96 exact minimal source certificates**, and **96/96 source authorization checks**. The archived run also compares the overlapping 64 cases to actual L3 Qwen2.5-1.5B-Instruct generations.

In the real L3 model's eight-case *available-record* groups, strict correct counts were S1 0/8, S2 0/8, S3 4/8, S4 0/8; the external deterministic gate scored 8/8 in each. In cold controls, Qwen scored 0/8 S1 (plain-text UNKNOWN caused JSON-format invalidity), 8/8 S2, 8/8 S3, 0/8 S4, while the gate scored 8/8 per arm. The paired analysis is descriptive; inference budgets and available computational support are fundamentally different. The gate has the exact rule baked into code, whereas the model must interpret and execute instructions. This is **not an unbiased demonstration that a hybrid architecture outperforms an LLM**, because these are different computational tasks and the gate was intentionally engineered to produce the fixture's expected actions.

## Gate interpretation and next decision

The current work validates that the source authority and decision policy can be separated from natural-language generation and tested for provenance integrity. It **does not** test DCH, human-specific curation, partner continuity, archive sufficiency, continuing-versus-replacement partner effects, or a history-conditioned curator advantage. All those remain open.

The next causal design should freeze this shared gate across treatments and manipulate only the upstream history selection and intervention policy. A strong automated curator must have the same authorized information, memory budget, repair opportunities, and update rights as a human or simulated incumbent. Literal yoked identical-tape replay is a negative control; after a registered unexpected event, a live adaptive policy must be compared against its fixed replay. To test human specificity rather than merely dynamic curation, an actual consented human policy, its well-informed replacement, and competent automation must be compared on independent held-out episodes. The experiment must measure policy actions as well as downstream persona decisions, not scripted labels or self-reports.

**Decision:** L4 engineering gate passes, but DCH inferential G1–G6 remain NO-GO pending actual partner-policy work, blind outcome scoring, and causal controls.
