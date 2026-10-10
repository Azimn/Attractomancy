# SCH C1: Integrated Character-Policy Cue Transfer and Cost

**Prepared:** October 9, 2026, America/Chicago  
**Status:** Exploratory pilot with frozen machine-readable fixtures; not confirmatory  
**Parent paper:** [Synthematic Cue Hypothesis](../../papers/synthematic-cue-hypothesis/PAPER.md) v0.2.1  
**Prior calibration:** [A2/B1/B0 results](../SCH_FOLLOWUP_2026_10_09/RESULTS_STATUS.md)

## Causal target

B0 demonstrated reversible arbitrary label-to-codename association in two Qwen model sizes, yet B1 did not demonstrate reliable reversal of more complex conditional policies. C1 tests the next level: can an arbitrary cue control a compact multi-constraint decision policy when the model must integrate independent conditions and a safety veto? The protocol deliberately distinguishes surface label association, characteristic choice, and cost effectiveness.

The fictitious archive office has two indexed policy identities, VORNA and KELVO. VORNA shares a file only with consent. KELVO shares a file only with a public audit. Both withhold every file when risk is high, regardless of consent or audit. Urgency is an irrelevant distraction, not an override. These are *synthetic operational policies*, not psychological identities, and none of their records comes from a person or real archive.

## Design and prediction

Six prespecified training combinations are available to the few-shot arms. The six held-out cases all contain urgent requests and several feature configurations not in the examples. They require integrating the relevant permission or audit condition with the shared risk veto while ignoring urgency. Each combination is independently queried under both character labels, for 12 scored cases per condition.

The six arms are: a fixed correct example-to-label mapping; the same examples with the policy-to-label mapping reversed; a mislabeled-example control with matching count and output frequency but no valid rule; a minimal English specification of both rules; a compact Boolean specification; and a no-policy fresh-session baseline. The experiment is assessed on *induced mappings*, so a swapped arm is scored against the swapped rules. The preregistered positive prediction is that a learned cue will outperform the mismatched-example and fresh conditions on new integrated decisions, and that responses will change in the proper direction on the diagnostic pairs after label reversal. The prediction of practical superiority over short explicit rules is deliberately more skeptical: few-shot cue induction is expected to **cost more tokens** per cold-start query than direct descriptions without achieving higher accuracy.

The main outcome is exact SHARE or WITHHOLD accuracy, with punctuation-only tolerance a separately reported sensitivity check. The most diagnostic outcomes are T1 and T2 for both labels: their permission and audit factors conflict, so policy swapping should reverse the expected answer. T3 tests simultaneous permission and audit; T4 and T6 test override by high risk; T5 checks abstention when no authorization and risk is high. None is considered evidence of persistence across clean sessions: every call constructs a new context containing its assigned training intervention.

## Limitations and identification

Compared with B1, the training examples and tests are not semantically identical strings, and the novel 'urgent' setting appears only in the held-out cases. However, the behavioral policy is still a toy binary classifier, not an autobiographical character or a long-running, socially situated agent. Urgency invariance does not fully establish compositional generalization. Rule identification is not guaranteed by finite examples alone; even successful classifications may reflect pattern completion. A weak result on a small model does not falsify SCH for larger architectures.

The *mismatched examples* control preserves example inputs and counts but intentionally breaks the canonical input-output association. As in previous pilots, high accidental scores in this control must be reported rather than interpreted as proof of the cue effect.

The concise-English and Boolean arms are not information-matched to few-shot demonstrations; they are **engineering alternatives** containing explicit rules. The cleanest association comparison is stable versus reversed versus mismatched demonstrations. Engineering comparisons use actual input and output tokens and must not hide the setup examples or repeated prompt history. Cost parity is not assumed by design.

Greedy decoding produces one deterministic output per unique case, not stochastic replicates. Two sizes of Qwen2.5 within the same model family do not constitute cross-family replication. Results must be labeled exploratory and cannot revise the previous pilot datasets.

## Data capture

Fixture: [conditions.json](conditions.json), execution script: [run.py](run.py). Save each independent chat transcript and exact response, model/version, fixture SHA-256, decoding settings, tokenizer-derived input and output counts, original and swapped target labels, diagnostic flag, strict and relaxed scores, and per-arm means in a unique model/run directory. Maintain the raw JSONL even when an arm fails.

## Decision rule

A cue-specific integration effect requires positive performance on held-out cases *and* correctly reversed responses on diagnostic examples, with superiority over mismatched controls. Practical utility further requires a quality-cost advantage against direct English or compact Boolean instructions at comparable quality. Failure on either condition is recorded separately. No claim of identity persistence, latent selfhood, or supernatural efficacy follows from a positive toy-policy result.
