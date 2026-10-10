# DCH L2: Real-model composite-memory development calibration

**Date:** 2026-10-09 America/Chicago. **Study type:** development-only model instrumentation, not an efficacy result about human dyads.

## Model and fixture

The runner is integration_v2.py. It uses the fixed Qwen/Qwen2.5-0.5B-Instruct model with greedy decoding, up to 120 new tokens, on eight of twelve generated synthetic trajectories. Each trajectory has initial and amended authorized records for permission, commitment status, due turn, and priority, plus one explicitly unauthorized distractor.

The action follows an ordered rule: revoked permission -> WITHHOLD; else cancelled commitment -> DECLINE; else current turn before due turn -> SCHEDULE; otherwise FULFILL_<PRIORITY>. The answer key and required source IDs are isolated in dev_EVALUATOR_ONLY.json and read only after raw model generations. All other history is synthetic investigator-authored data.

## Conditions and mandatory controls

The expert-auto condition retains the latest authorized record per key. The human-coded proxy deliberately retains *exactly the same records and text*; this is a deterministic exact-input replay control and is not an observation of a human partner. The stale condition provides the initial records before correction, the cold condition provides no archive, and oracle supplies all authorized entries without a record budget. Thus oracle is an information ceiling, not an equal-token competitor. No actual live incumbent or replacement partner is present.

Measure exact action accuracy, JSON parse rate, proper source citations, and completeness of the four required event IDs. Preserve raw text, input hashes, model identifier, source authorization and token counts. A passing experiment execution requires 40 model responses and hash-identical human-coded/expert inputs. No particular correctness score is required for successful engineering execution.

## Scientific limitation and follow-up gates

Weak model accuracy is evidence of instrument sensitivity limits, not a DCH null. An incumbent advantage is not testable here because the continuing-partner trajectory and live-yoked newcomer arms have not been run. This fixture covers one composite-decision construct, not all four outcomes of behavioral profile, autobiography, value stability and relationship obligations. Neither this run nor exact-input equivalence is a demonstration of dyadic constitution.

The prior six go/no-go gates remain in force, including source authorization, blended human rater calibration, budget parity, independent trajectories and actual live-vs-replay comparisons. Real humans and personal conversation logs must not be introduced before independent consent and a preregistered protocol.
