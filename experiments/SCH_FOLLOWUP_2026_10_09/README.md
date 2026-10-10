# SCH Follow-up Studies: A2 and B1

**Prepared:** October 9, 2026 (America/Chicago)  
**Status:** Preregistered exploratory computational follow-ups. Neither fixture is confirmatory or peer-reviewed.  
**Parent hypothesis:** [The Synthematic Cue Hypothesis](../../papers/synthematic-cue-hypothesis/PAPER.md), version 0.2.1  
**Original retained result:** [Experiment A pilot 001](../EXP-A_ZERO_SHOT_SYNTHEMATA/PILOT_ANALYSIS.md)

## Objectives

**A2, corrected zero-shot steering:** Re-test P1 following pilot 001's 88-token truncation and metalinguistic instruction problem. All conditions use independent contexts. Four neutral scene prompts are each paired with five cue arms (familiar emoji, related ordinary word, neutral word, nonce identifier, and concise explicit-language instruction) in two target discourse regimes. A2 records actual model tokens, complete texts, completion limits, literal cue echo, and a narrowly defined lexical marker proxy. The directional expectation is familiar cues above neutral/nonce for register markers, and explicit instruction as a cost-conscious strong comparator. Genre registers are not specific personas.

The lexical measure is explicitly *exploratory* and not a validated semantic style grader. Marker words present in a cue are excluded from lexical scoring; potential meta-statements about tags are independently flagged. The stronger intended outcome is human-blinded evaluation of full responses, still outstanding. This design improves over pilot 001 but **does not** fix the lack of blind qualitative evaluation or limited task sample.

**B1, within-context symbolic binding:** Test whether arbitrary tags acquire local predictive meaning through exposure. VORNA and KELVO are counterbalanced synthetic labels for two policies: SHARE iff consent=yes, and SHARE iff public_audit=yes. Their rules are not given in the stable or swapped arms. Each arm presents the **same number of demonstrations** representing all four possible combinations of consent and audit, for both tags. The cue-label mapping is flipped in the swapped arm. The unpaired arm retains both tags and outputs but scrambles the reliable tag-to-rule association. The explicit arm states the two rules compactly and avoids demonstrations. The fresh arm contains no training information.

Responses must be exactly SHARE or REDACT. A held-out query is constructed for each consent/audit combination and each tag (8 test situations per arm, 40 calls). The primary B1 observable is agreement with the mapping induced by the visible examples. Critically, **swapped cases should match the reversed mapping** if the model is learning an association, rather than matching the fixed investigator-preferred labels. On the two diagnostic conflict cases (consent=yes/audit=no or consent=no/audit=yes), the outcome should flip when the training mapping flips. The other two cases check basic rule execution but cannot discriminate the two rules. Scoring reports induced-target accuracy, canonical-target accuracy, and the diagnostic reversal rate. Do not call this persistent identity or demonstrate biological learning.

Cost comparison is to the explicit arm and includes *all* prompt+output tokens, including every demonstration. Marginal cue spelling alone is not an efficiency result.

## Control caveats

A2 and B1 use the same frozen instruction-tuned architecture but different tasks. B1 is an instruction-following association experiment, not a model of rich autobiographical continuity. The unpaired arm is a noisy-label control and cannot be expected to yield a specific label. Any outcome on its forced response may be arbitrary. B1's eight demonstrations are training data *within the context window*; model weights are not updated. Zero-shot fresh cue testing is a calibration, not persistence.

These are low-powered exploratory pilots. Even with two different model sizes in the same Qwen family, apparent agreement is not independent cross-family replication. Greedy decoding yields deterministic outputs, so the 8 situations per arm are different items, not stochastic repeats. Any result must be interpreted at this scope.

## Execution

Fixture: [conditions.json](conditions.json). Runner: [run.py](run.py). GitHub Actions: [sch-followups.yml](../../.github/workflows/sch-followups.yml). Each matrix job writes its own folder under \`results/<model-slug>-<run-id>/\` and uploads a separate artifact. The GitHub Actions job then commits provenance, raw generations, token counts, and summaries. Failed or partial runs must remain labeled partial.

To validate without generating: \`python experiments/SCH_FOLLOWUP_2026_10_09/run.py --validate-only\`.

To execute: \`python experiments/SCH_FOLLOWUP_2026_10_09/run.py --model Qwen/Qwen2.5-0.5B-Instruct --output experiments/SCH_FOLLOWUP_2026_10_09/results/local\`.

The paper is not amended to claim positive confirmation merely because a workflow completes. Interpret all pilot outcomes including zero effects, rule failures, and control failures.

## Completed runs and outcome log

The [running evidence report](RESULTS_STATUS.md) documents completed A2, B1, and B0 model tests with archived raw generations, cost counts, control anomalies, and unresolved limitations. The B0 capacity-control protocol is in [B0_CALIBRATION.md](B0_CALIBRATION.md). The raw [Qwen0.5 A2/B1](results/qwen25-05b-38014716712/), [SmolLM2 A2/B1](results/smollm2-360m-38014802469/), [Qwen0.5 B0](results/b0-qwen25-05b-38015425441/), [Qwen1.5 B0](results/b0-qwen25-15b-38015425441/), and [SmolLM2 B0](results/b0-smollm2-360m-38015425441/) artifacts are saved on main. The separate Qwen1.5 A2/B1 job is not included in these completed records until verified.

The current strongest narrow positive result is reversible arbitrary cue-to-codename association on the Qwen models in B0. A2 discourse induction and B1 rule integration have not established corresponding robust symbolic effects. Neither construct demonstrates across-session identity persistence. The explicit B0 comparator is much shorter than the repeatedly demonstrated mapping and achieves comparable performance, so no efficiency advantage is established.

