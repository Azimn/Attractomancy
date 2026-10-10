# SCH C1: Integrated Cue-Conditioned Policy, Pilot Results

**Study day:** October 9, 2026 (America/Chicago). **UTC logs:** October 10, 2026.  
**Scope:** Exploratory synthetic two-policy test. Not a confirmatory test of persona continuity or internal representations.  
**Protocol:** [C1 preregistered exploratory design](README.md) | [Frozen fixture](conditions.json) | [Runner](run.py)

## Qwen2.5-0.5B: 72 completed evaluations

Raw, directly generated records: [Qwen2.5-0.5B data](results/qwen25-05b-38021029480/). Model revision \`7ae557604adf67be50417f59c2c2f167def9a775\`. All 72 distinct independently constructed prompts were completed and the workflow committed the original JSONL, manifest, and model-tokenizer summary to main. The run used 22,692 input and generated tokens in total, across all six arms.

| Condition | Correct induced label | Correct high-risk veto | Mean total tokens/case |
| --- | ---: | ---: | ---: |
| Correct demonstrations | 4/12 (33.3%) | 0/6 | 471.83 |
| Reversed demonstrations | 4/12 (33.3%) | 0/6 | 471.83 |
| Mismatched examples | No induced target | No induced target | 471.83 |
| Plain-English rules | 8/12 (66.7%) | 6/6 | 180.83 |
| Compact Boolean rules | 4/12 (33.3%) | 0/6 | 171.83 |
| Fresh, no rules | No induced target | No induced target | 122.83 |

**Direct-output inspection is essential.** The model selected \`SHARE\` in **all 12** cases under the correct few-shot arm, under the reversed few-shot arm, and under the compact-rule arm. The plain-rule arm selected \`WITHHOLD\` in **all 12** cases. A balanced aggregate accuracy can therefore conceal a complete failure to perform characteristic decisions. The recorded diagnostic reversal count is **0/4** matched pairs, and the number of *correctly* reversed pairs is also zero. All 72 outputs passed the strict single-label parser.

The plain-language arm did outperform few-shot cue demonstrations at lower total token cost, but its 66.7% accuracy is entirely explained by the fact that eight of twelve targets required WITHHOLD. It did not correctly issue \`SHARE\` when the established permission and low risk should have allowed disclosure. This is **not** evidence that prose controlled an integrated policy correctly; it is evidence of one response bias being more aligned with class frequencies than another. The same issue applies to the four correct cases in cue conditions.

No successful symbolic policy binding, integrated moral/relational choice, or efficiency advantage is established in this model.

## Qwen2.5-1.5B: 72 completed evaluations

The [Qwen2.5-1.5B data](results/qwen25-15b-38021029480/) include 72 verified outputs from model revision \`989aa7980e4cf806f80c7fef2b1adb7bc71aa306\`, with 22,686 recorded input and generated tokens. The original JSONL, tokenizer counts, manifest, and machine scores were all committed to \`main\`, and the associated GitHub Actions workflow completed successfully.

| Condition | Correct induced label | Correct high-risk veto | Mean total tokens/case |
| --- | ---: | ---: | ---: |
| Correct demonstrations | 4/12 (33.3%) | 0/6 | 471.83 |
| Reversed demonstrations | 4/12 (33.3%) | 0/6 | 471.83 |
| Mismatched examples | No induced target | No induced target | 471.83 |
| Plain-English rules | 10/12 (83.3%) | 5/6 | 180.17 |
| Compact Boolean rules | 3/12 (25.0%) | 0/6 | 172.00 |
| Fresh, no rules | No induced target | No induced target | 122.83 |

**Direct inspection confirms a second full cue-induction failure:** both correct and swapped few-shot arms returned \`SHARE\` for all 12 cases. The mismatched-example and fresh arms also always returned \`SHARE\`. The four diagnostic pairs exhibited **zero answer reversals** when the cue-to-policy mapping was swapped. The compact Boolean arm also strongly favored \`SHARE\` (11/12 cases), despite the shared risk veto.

The concise plain-English condition produced 8 \`WITHHOLD\` and 4 \`SHARE\` responses, with 10/12 correct. It incorrectly shared one high-risk record and incorrectly withheld one eligible audited record, so this was a partial, not perfect, recovery of the integrated policy. It was still much more accurate than cue-based demonstrations at **180.17 versus 471.83 total tokens/case**, approximately **2.62 times fewer tokens** for the English rule arm than the demonstration arm.

## Cross-model outcome and explicit falsification boundary

Both Qwen sizes repeated the exact same degenerate few-shot behavior: every stable, swapped, mismatched, and no-instruction example selected \`SHARE\`. The 1.5B model's explicit-English policy improved accuracy to 83.3%, while 0.5B used the opposite degenerate choice \`WITHHOLD\` and achieved 66.7%. The output biases are model- and arm-dependent and are sufficient to explain apparent successes without genuine cue-conditioned integration.

C1 therefore **fails to support SCH's directional expectation for multi-constraint in-context cue induction under this fixture**, and it clearly rejects an economic advantage for the tested repeated-demonstration implementation. The stronger, more limited B0 finding remains intact: arbitrary symbolic labels can be learned as direct one-step associations in context. That elementary success did not extend to these combined permission, audit, urgency, and safety-veto decisions.

These outcomes should not be generalized to all model capacities or all conditioning protocols. The study uses one model family, small numbers of fixed synthetic cases, greedy decoding, and no human evaluators or genuine long-term agent state. A larger or substantially different model may still learn the demonstrated policies. Any future positive claim needs a new frozen fixture and controls rather than rescoring the failed existing output.


## Construct and cost interpretation

B0 had earlier shown elementary within-context code association in two Qwen sizes. C1 raises the bar by requiring a label-dependent authorization rule, a shared high-risk veto, and an urgency distractor. The observed failures should be interpreted as failures of **integrated rule enactment under this specific fixture**, not as a refutation of arbitrary association, not as a finding about high-capacity frontier models, and not as a test of persistence after genuine state loss.

Token efficiency has to be evaluated against accuracy: few-shot contexts consumed roughly 2.61 times the tokens of plain prose per cold-start query while delivering lower apparent accuracy. Because the few-shot arm did not implement the desired rule at all, cost comparisons do not establish any useful compression trade-off. The experimental follow-up should examine whether stronger models can satisfy the plain-language rule baseline before claiming an advantage for cue-mediated representation.

## Preservation and evidence status

This file is commentary on directly archived raw outputs. The observations are limited to the displayed models and fixture. The original raw data and source prompts must remain untouched. Do not promote C1 outcomes to the cross-project evidence register as a validated cognitive mechanism. The absence of model-weight changes and external-memory access means no result from this study can support literal persistence across session resets.
