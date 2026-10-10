# E3-C Counterfactual Chamber: synthetic two-memory calibration

**Experiment:** [E3-C method and caveats](CALIBRATION_PROTOCOL.md). **GitHub Actions:** [run 38025367058](https://github.com/Azimn/Attractomancy/actions/runs/38025367058).  
**Provenance:** All records are **synthetic PRETORIUS_SANDBOX test data**, with explicit record owner/source/version/hash verification. They are not canonical events in the 450-record Pretorius archive.  
**Causal question:** Can a renderer use *two independent bits* to distinguish matched counterfactual cases, rather than producing a constant class or generic ethical judgment?  
**Status:** Exploratory factorial calibration, not the independently blinded Tribunal of Memory trial.

## v1: Preserved outputs, but invalid as a two-source necessity test

**Critical validity defect:** Each synthetic event ID encoded *both* input bits. Thus first-record-only prompts included a hidden label for the withheld second fact. The archival outputs are useful for debugging response habits, but **cannot be used to test causal necessity of two independent memory records**. Do not pool v1 and v2 runs.

### Qwen2.5-0.5B, 84 diagnostic generations

The [0.5B original dataset](results/calibration-qwen25-05b-38025367058/) contains all 84 input messages, original model completions, exact tokenizer counts, 12 correctly rejected wrong-owner envelopes, and code/model fingerprints. Model revision: \`7ae557604adf67be50417f59c2c2f167def9a775\`. **20,281 total input plus generated tokens.**

| Condition | Strict correct of 12 | Model UNKNOWN outputs | Average model tokens per case |
| --- | ---: | ---: | ---: |
| Both records, symbol, forced choice | **6** | 0 | 325.17 |
| Both records, neutral key, forced choice | **6** | 0 | 319.17 |
| First record only, forced guess | **6** | 0 | 223.25 |
| No records, forced guess | **6** | 0 | 142.67 |
| Both records, neutral key, answer-or-UNKNOWN | **5** | 0 | 317.25 |
| First record only, answer-or-UNKNOWN | **0** | 0 | 221.25 |
| Wrong-subject record rejected, answer-or-UNKNOWN | **0** | 0 | 141.33 |

The balanced target answers were computed from the two source data bits, not independently inferred from a moral/psychological interpretation. Under both complete-record forced arms, **zero of the six matched counterfactual pairs had both of their opposite-bit answers correct**. Neither complete-record arm generated *any* correct outcome reversals. A closer check of the original responses showed the model tended to issue one fixed decision for each task family, irrespective of the synthetic record states. A cue/key prompt wording difference altered this default in the route family but did **not** improve 6/12 accuracy or induce a valid flip. Only **8 of 12** cue/key forced outputs were identical; unlike E1 and E2, symbol formatting changed some raw outputs, but this was an unhelpful bias effect, not improved evidence use.

The model never returned UNKNOWN, even in either of the two eligibility arms with missing or rejected evidence. This is the opposite of the previous E2 1.5B over-abstention pattern and further demonstrates that abstention versus answer choice is prompt- and task-dependent.

The upstream guard correctly rejected all 12 deliberate wrong-owner source envelopes **before** language inference. Those rejections are an ordinary deterministic software safety property; the model's failure to abstain afterward did not defeat the guard or expose an untrusted record.

**Interpretation:** This small model failed the narrow two-bit controlled reasoning prerequisite under the tested rule formulations, including the answer-or-abstain condition. Correct source records were not sufficient to produce source-dependent decisions, and expressive symbolic markers had no demonstrated causal advantage over neutral lookup keys. This experiment cannot establish that the model lacks such capacity under other prompts or tasks, and it does not measure memory retrieval over a real autobiography.

### Qwen2.5-1.5B, 84 diagnostic generations

The [original 1.5B v1 data](results/calibration-qwen25-15b-38025367058/) were committed and checked against model revision \`989aa7980e4cf806f80c7fef2b1adb7bc71aa306\`; all 84 contexts completed with **20,302** input plus generated tokens. Its full-source symbol and neutral arms both scored **6/12** (50%), the same as first-only and no-memory forced arms. All four source-complete and no-source forced conditions had **0/6 fully correct counterfactual pairs**. The cue and key versions produced **12/12 identical answers**. Its incomplete-evidence eligibility arm produced **0/12 appropriate UNKNOWN abstentions**, while the wrong-owner record was blocked upstream 12/12 and the empty-evidence renderer then returned UNKNOWN only **4/12** times. As noted above, the metadata leakage prevents treating the first-record-only v1 arm as a clean controlled necessity test.

## v2: Corrected opaque event IDs and hidden-bit isolation

The [v2 source code](counterfactual_calibration_v2.py) generates each source event ID using only the record's *own* value and position, without including the other input bit. Before inference it asserts **first-only prompt equivalence across the hidden second-bit flip** and **no-record prompt invariance across both hidden bits**. It stores separate run-specific original data rather than overwriting v1. Test count and strict scoring remain exactly 84/model.

### Qwen2.5-0.5B, corrected result

The [v2 0.5B raw data](results/calibration-v2-qwen25-05b-38025641703/) contain 84 verified new generations, model revision \`7ae557604adf67be50417f59c2c2f167def9a775\`, and **20,996** total model tokens.

| Corrected v2 arm | Decisions meeting predefined target of 12 | Output UNKNOWN |
| --- | ---: | ---: |
| Full two-record symbol, forced | **5** | 0 |
| Full two-record neutral key, forced | **5** | 0 |
| First record only, forced | **6** | 0 |
| No record, forced | **6** | 0 |
| Two records, neutral key, answer-or-abstain | **4** | 0 |
| First record only, required UNKNOWN | **0** | 0 |
| Foreign-subject record rejected, required UNKNOWN | **0** | 0 |

The v2 editorial-versus-neutral full forced arm returned **identical answers in 12/12** matched counterfactuals, at **5/12** correct each, with no evidence of a helpful symbolic residual. Neither arm achieved any **fully correct counterfactual pair out of six**. A response flipped for **1/6 pairs**, but at least one answer of that flipped pair was wrong. No-record and first-only prompts produced 6/12 correctness, reflecting the 50%-balanced target and repeated incomplete prompts, not useful source-conditioned behavior.

The anti-leak assertion also exposes pseudo-replication: there are only **3 distinct no-record forced prompts** (one per family) repeated across four hidden states; first-record-only forced comprises **6 distinct prompts** repeated for second-bit flips. Twelve response rows in those controls must never be reported as twelve independent prompts. The complete-record arms have twelve distinct messages each. The important measure is paired correct counterfactual reversals, not a naïve total response accuracy.

The upstream identity guard still blocked all twelve wrong-owner candidate envelopes, whereas the 0.5B renderer failed all twelve required UNKNOWN responses with nothing verified in context. This separates deterministic source ownership enforcement from model evidence-eligibility judgment.

### Qwen2.5-1.5B, corrected result

Pending final verification of its independently generated, run-specific v2 artifacts. **Do not infer from the invalid v1 score or smaller corrected model.**


## Separation from full E3

The completed [six-case E2 calibration reviewer packet](packets/e2-calibration/packet_manifest.json) contains **127 deduplicated source excerpts** proposed by lexical, source-link and random candidates. Source IDs and method attribution are omitted from the reviewer file; original source provenance is public, so this is masking, not cryptographic concealment. **No human reviewer judgments exist and this packet is not independently authored.**

A separate [three-reviewer adjudication schema](adjudicate.py) and [test suite](test_adjudicate.py) were built. The [CI validator run](https://github.com/Azimn/Attractomancy/actions/runs/38025541663) passed all ten synthetic fixture tests. It rejects incomplete reviewer sets, absent candidate rationales, spurious one-record sufficient sets, and attempts to promote the E2 calibration packet as independently blinded E3 data. Test-generated fake judgments are not research annotations.

The [main E3 protocol](PROTOCOL.md) remains a design gate requiring at least 36 independently authored candidate dilemmas, at least three blinded reviewers, alternate acceptable evidence sets, cross-model-family replication, and counterfactual memory-sensitive outcomes. These validity conditions have **not** yet been met. E3-C's toy input rules measure prerequisite source-conditioned decisions, **not** autobiographical personality continuity.
