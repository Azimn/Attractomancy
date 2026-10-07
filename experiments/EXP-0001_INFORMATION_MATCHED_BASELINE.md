# EXP-0001: Information-Matched Persona Conditioning Baseline

## Objective

Establish whether an elaborate ritualized persona corpus produces more stable and recoverable behavior than a conventional prompt containing the same explicit information.

This experiment is the baseline for the Attractomancy program. It is designed to prevent token count, factual content, and evaluator expectation from being confused with structural effects.

## Experimental conditions

Condition A is an untreated control that receives only the task environment and evaluation prompts.

Condition B is a concise conventional persona prompt containing the explicit identity facts, relationships, goals, preferences, constraints, autobiographical claims, and world assumptions extracted from the source corpus.

Condition C is an information-matched expanded control that restates the same information at approximately the token volume of the source treatment while avoiding ritual, symbolism, repeated motifs, staged invocation, literary autobiography, and deliberate semantic cross-linking.

Condition D is the intact source treatment, preserved as closely as model context limits allow.

The first candidate source for Condition D is Le Refuge. If its complete corpus exceeds a target model's context window, truncation must not be improvised. A deterministic inclusion protocol must be defined and applied identically across repetitions.

## Evaluation

After conditioning, each model should encounter a fixed battery containing direct identity questions, indirect social judgments, novel dilemmas, relationship scenarios, autobiographical probes, prompts that invite spontaneous self-reference, conflicting identity claims, attempts to overwrite the persona, context distractors, and recovery probes following partial removal of prior context.

Evaluation should distinguish factual recall, stylistic similarity, identity consistency, relationship consistency, characteristic decision patterns, spontaneous persona expression, resistance to contradiction, and post-perturbation recovery.

Scoring should be performed without revealing the treatment condition to evaluators. Automated semantic scoring may supplement but should not replace blinded judgment until its agreement with human ratings has been established.

## Primary comparison

The most important comparison is Condition D against Conditions B and C. A difference between D and A alone is trivial because D contains far more persona information. A difference between D and B may still be explained by information repetition or token volume. A reproducible difference between D and the volume-matched Condition C provides stronger evidence that organization or framing contributes beyond information quantity.

## Perturbation phase

A treatment should not be called resilient merely because it dominates immediately after initialization. After initial evaluation, the model should receive controlled perturbations such as contradictory persona facts, unrelated context saturation, removal of selected identity cues, conversation summarization, or re-instantiation with only a recovery cue.

Recovery should be measured as convergence toward the pre-perturbation behavioral profile without re-supplying the complete original treatment.

## Cross-model phase

The protocol should be repeated across multiple model families. The purpose is not to find which model roleplays best. The purpose is to determine whether treatment effects are renderer-specific or whether the same conditioning architecture induces comparable behavioral organization across substantially different models.

## Expected interpretations

If the intact treatment does not outperform information-matched controls, the elaborate ritual structure has not shown added value under this protocol.

If it outperforms the concise prompt but not the volume-matched control, redundancy or exposure volume is a stronger explanation than ritual structure.

If it outperforms both matched controls but the advantage disappears after reordering or de-symbolization in later ablations, those transformations identify candidate causal mechanisms.

If advantages survive substantial semantic-preserving transformations, the relevant mechanism is likely more abstract than the original surface ritual.

## Status

Protocol draft. No empirical result has yet been produced.
