# SCH Follow-up Results: A2, B1, and B0

**Study date:** October 9, 2026 (America/Chicago). Logs and GitHub timestamps use UTC on October 10.  
**Evidence class:** Exploratory computation with preserved raw generations, not preregistered confirmatory replication.  
**Primary comparisons:** A2 tests cue-associated generic discourse; B1 tests arbitrary cue-to-conditional-policy inference; B0 separates elementary within-context label association from B1's compositional decision rule.  
**Scope:** No persistence, no model-weight modification, no autobiographical personhood test, and no metaphysical interpretation.

## Results verified on two models

The [Qwen2.5-0.5B-Instruct A2/B1 artifact](results/qwen25-05b-38014716712/) contains 80 independently constructed conversations at model commit \`7ae557604adf67be50417f59c2c2f167def9a775\`. There were 40 zero-shot A2 cases and 40 within-context B1 cases. The runner recorded 13,474 total prompt and generated tokens. The A2 ceremonial familiar word reached a mean 0.9299 predeclared lexical markers per 100 generated words, while the comparable neutral and nonce controls were both zero; the related candle emoji also scored zero. No compact cue achieved a positive lexical score in the A2 recursive target, while explicit phrasing averaged 1.1458. The ceremonial explicit instruction averaged 0.9039, roughly like the ceremonial familiar word. Only 10/40 A2 answers satisfied the 30 to 45 word requirement, though just 2/40 reached the generation cap. Thus the indicator is contaminated by length variability and not a validated semantic style measurement. These patterns do not establish robust P1 cue advantages.

The Qwen0.5 B1 condition scored 6/8 (75%) under stable mapping, 5/8 (62.5%) under swapped mapping, and 5/8 (62.5%) under compact explicit rules. The unpaired control agreed with the canonical reference in 7/8 cases (87.5%), despite its inconsistent demonstrations; the fresh no-training condition agreed in 4/8. Only **1 of 4** same-tag, same-question diagnostic conflict pairs changed answer when the training rule was reversed. This does not demonstrate robust cue-specific logical policy induction, even when raw stable accuracy appears above baseline. The B1 example suite presents all four Boolean feature combinations during training; test prompts paraphrase those combinations but do not test genuinely novel feature configurations, an important limit on transfer claims.

The [SmolLM2-360M-Instruct A2/B1 artifact](results/smollm2-360m-38014802469/) contains another 80 responses at model commit \`a10cc1512eabd3dde888204e902eca88bddb4951\`. A2 suffered severe noncompliance: 27/40 outputs reached the 112-token cap and none met the intended 30 to 45 word window. Its A2 lexical marker frequencies are not a comparable measure of completed discourse. B1 strict format validity was zero for all 24 demonstration-conditioned outputs, largely because of trailing punctuation or repeated prompt material. A post hoc tolerance check that permits only a single terminal period recovered 6/8 stable and 8/8 swapped outputs as valid labels, but observed performance was only 4/8 on each respective induced mapping, which is chance-level for these balanced outputs. The same-tag diagnostic reversal count was **0 of 4**. The model-family comparison is therefore inconclusive for sophisticated cue-based rule induction.

## B0, minimum-association capacity calibration

The B0 fixture strips B1's conditional rule down to a simple invented tag-to-codename mapping. In [Qwen2.5-0.5B B0](results/b0-qwen25-05b-38015425441/), stable demonstration mapping was reproduced in **7/8** test cases and reversed mapping in **8/8**. In **7/8** matched prompts, swapping the trained mapping flipped the answer. Concise direct instructions reached 7/8, while fresh/no-demonstration prompts matched the canonical mapping in only 1/8. This provides **positive exploratory evidence of elementary contextual cue association and reversal** for this specific model and fixture, not durable memory or cross-session persistence. The inconsistent-mapping arm nevertheless matched the canonical key on 6/8 prompts, a substantial control anomaly that must remain visible. The demonstration-conditioned arms consumed roughly 174 tokens per completed case versus 88 for short explicit instructions. There is currently **no demonstrated token-efficiency advantage** to the demonstration approach.

In [SmolLM2-360M B0](results/b0-smollm2-360m-38015425441/), stable and reversed strict accuracies were 2/8 and 4/8 respectively, and matched-prompt reversals occurred in **0/8**. Format compliance was inconsistent even for this simplest task, and no reliable association was isolated. Exact-string scoring and punctuation-tolerant sensitivity were both archived.

## Interpretation

A narrow cue-binding effect is observable in the Qwen0.5 minimum-association calibration, while the same model does not reliably reverse a more complex rule mapping. The distinction supports the methodological need to separate addressable labels, conditional integration, and autobiographical reconstruction. The preceding symbol-only A2 study does not yet show a robust meaningful-symbol advantage in generic discourse induction. Strong claims about latent self-structure, continuity across resets, or representation-level causality would be unsupported.

## Pending model at time of initial report

The Qwen2.5-1.5B A2/B1 job and B0 calibration job were still generating during the initial writing of this report. These are **pending**, not missing or negative, until outputs and complete workflow status are verified. When available, report their results without rewriting or replacing the preceding raw datasets.

## Raw reproducibility paths

The complete training and test prompts, output texts, actual model tokenizer counts, model revision IDs, procedural statuses, and per-condition scores are stored in the linked immutable-named results folders. Scripts are [run.py](run.py) and [b0.py](b0.py), with versioned stimuli in [conditions.json](conditions.json) and [b0_conditions.json](b0_conditions.json). GitHub Actions runs are [A2/B1](https://github.com/Azimn/Attractomancy/actions/runs/38014716712), [SmolLM2 A2/B1](https://github.com/Azimn/Attractomancy/actions/runs/38014802469), and [B0](https://github.com/Azimn/Attractomancy/actions/runs/38015425441).

No source catalog efficacy labels have been promoted, and no external memory mechanism has been validated by these tests.
