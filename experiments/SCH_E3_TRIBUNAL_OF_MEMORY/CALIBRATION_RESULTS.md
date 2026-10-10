# E3-C Counterfactual Chamber: synthetic two-memory calibration

**Experiment:** [E3-C method and caveats](CALIBRATION_PROTOCOL.md). **GitHub Actions:** [run 38025367058](https://github.com/Azimn/Attractomancy/actions/runs/38025367058).  
**Provenance:** All records are **synthetic PRETORIUS_SANDBOX test data**, with explicit record owner/source/version/hash verification. They are not canonical events in the 450-record Pretorius archive.  
**Causal question:** Can a renderer use *two independent bits* to distinguish matched counterfactual cases, rather than producing a constant class or generic ethical judgment?  
**Status:** Exploratory factorial calibration, not the independently blinded Tribunal of Memory trial.

## Qwen2.5-0.5B, verified 84 generations

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

## Qwen2.5-1.5B

The independent larger-model job is still executing at the time of this first report revision. **No result is asserted until the raw model-specific artifacts are committed and verified.**

## Separation from full E3

The completed [six-case E2 calibration reviewer packet](packets/e2-calibration/packet_manifest.json) contains **127 deduplicated source excerpts** proposed by lexical, source-link and random candidates. Source IDs and method attribution are omitted from the reviewer file; original source provenance is public, so this is masking, not cryptographic concealment. **No human reviewer judgments exist and this packet is not independently authored.**

A separate [three-reviewer adjudication schema](adjudicate.py) and [test suite](test_adjudicate.py) were built. The [CI validator run](https://github.com/Azimn/Attractomancy/actions/runs/38025541663) passed all ten synthetic fixture tests. It rejects incomplete reviewer sets, absent candidate rationales, spurious one-record sufficient sets, and attempts to promote the E2 calibration packet as independently blinded E3 data. Test-generated fake judgments are not research annotations.

The [main E3 protocol](PROTOCOL.md) remains a design gate requiring at least 36 independently authored candidate dilemmas, at least three blinded reviewers, alternate acceptable evidence sets, cross-model-family replication, and counterfactual memory-sensitive outcomes. These validity conditions have **not** yet been met. E3-C's toy input rules measure prerequisite source-conditioned decisions, **not** autobiographical personality continuity.
