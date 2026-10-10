# DCH L5 pre-intervention protocol: historically informed curator policies

**Status:** draft preregistration, no participant intervention executed and no hypothesis test completed.
**Predecessor:** [L4 validated external authority gate](L4_AUTHORITY_RESULT_2026-10-10.md).
**Goal:** isolate the upstream **history-conditioned intervention policy** from memory content, language-model instruction following, and source authority. This is the first design in this line with a path to actually testing the human-specific claim rather than evaluating toy parsers.

## Causal estimand and null

For history H, frozen authorized archive A, identical policy executor G, independent future episode X, and a partner-selected sequence of allowable curation and repair actions U, measure the difference between historical-incumbent policy P_incumbent and an informed replacement P_replacement, conditional on each seeing the same archived facts and permitted observations. The dependent variable is **resulting authorized state and action behavior** evaluated with a frozen G and blinded terminal battery, not perceived chemistry, textual style, or persona self-report.

The main strong null is that an expert automatic controller P_auto, given the same A, training episodes, state access, intervention capacity and latency allowance, matches or improves on the incumbent human. Under equivalence the human-specific DCH claim does not survive for the tested tasks; the weaker distributed-history/control system claim may remain.

Do not conflate: (a) an identical taped message stream, which must produce identical frozen deterministic replay output, with (b) live contingent repair after an independently introduced perturbation, for which a previously conditioned policy may behave differently. New and continuing humans writing different uncontrolled messages is not a decisive partner-swap test.

## Step 0: two-week engineering and rater pilot

Use at least 12 independently authored synthetic biography/relationship histories, not 12 seeds of one template. Histories must cover four domains: stable behavioral choices, source-grounded autobiography, value conflict/revision and relationship-specific commitment or permission. Hold out future perturbations, terminal outcomes and scoring keys from all interactive condition prompts. Each history includes dated contradictions, source-attribution traps, expired/revoked permissions, a delayed obligation and one independently unexpected state transition.

The first engineering phase may use **scripted** incumbent/replacement policy proxies only to validate replay integrity, scoring sensitivity, bounded intervention budgets, state provenance and divergence attribution. Scripted proxy success is not DCH evidence and should never be reported as a human arm.

Go/no-go: independent reference oracle >=80% overall and >=70% per domain; positive oracle-over-cold discrimination in every domain; independent blind rater reliability weighted kappa/ICC >=0.70; all source writes attributed; condition storage/token/turn budgets within 2% or prespecified equivalence adjustment; deterministic exact-tape replay invariant; observed score sensitivity to engineered perturbations. If any fail, revise only development data and freeze a new untouched terminal battery.

## Participants and design, after pilot passes and informed consent

Invite actual willing human participants for both incumbent/history-learning and replacement roles. A human becomes an incumbent only through recorded *synthetic* training episodes, never through hidden private chats. A newcomer receives an information-complete, version-pinned archive and the same time to inspect it as the incumbent's allowed study budget. Both must be permitted equivalent lookup, edits, correction opportunities and notes. Use a competent expert automation controller with identical state access, authorized action API, and constrained resource/latency budget. Pre-register the automated curator implementation and prohibit weakening it after observing a human advantage.

Randomize partner-policy role within independently authored histories and counterbalance episode ordering. Participants may perform multiple histories, but trajectories must be analyzed with human participant and synthetic history as crossed random effects. Blind scorers to partner identity and archive implementation. Separate actual participant role from the neutral labels presented to raters.

Compare three **live adaptive** policies, incumbent, informed newcomer, expert auto, each against their own **yoked replay** using a fixed recorded action/input tape on a cloned state. Apply matched novel perturbations after the warm-up tape and allow only the live arm to take newly contingent corrective action. Replays cannot spontaneously change course. Keep all groups' model renderer and L4 authority gate identical, and log raw action proposals, authorized writes, budgets, timing, selected source evidence and terminal effects. If model output is used for rendering, never let unconstrained model action choices bypass G.

The decisive comparison is **difference-in-differences** of live-versus-own-replay restoration across incumbent, informed newcomer and expert automation, not incumbent-alone absolute quality. A continuing-partner advantage counts only if it persists under complete source-information parity, matched intervention opportunities, common perturbation severity, and blinded independent evaluation. Replayed-input equivalence checks alone establish no history effect.

## Outcomes and hypothesis rejection

Primary outcomes are source-correct future behavior across four domains, unauthorized-disclosure rate, recovery after source contradictions or context reset, delayed commitment execution, provenance completeness and incorrect abstention. Secondary outcomes are number of edits, memory budget, time per repair, generic-prior regression, and the language renderer's utterance fidelity. Do not score confident first-person self-descriptions as proof of persistence.

Preregister smallest meaningful standardized effect d=0.20, a multi-domain primary composite, directionality, multiple-comparison correction and 90% equivalence intervals within [-0.20,0.20] for rejecting meaningful differences. Choose confirmatory sample size by participant/history cluster simulation using pilot variances, not by counting many correlated model calls as independent participants. A 12-history engineering pilot is not powered for DCH efficacy or equivalence.

**Falsifier:** if expert automated curation matches or exceeds historical humans under true parity, human-specific constitution fails in this regime. If a newcomer with the full archive and matched preparation matches the incumbent's perturbation-adjusted trajectory, the stronger irreducible-history-policy form fails for this regime. The weaker operational fact that recorded policy and memory state influence future behavior may still hold, but should be called distributed control/curation rather than a unique human relationship mechanism.

## Ethics and source discipline

Use authored synthetic characters or specifically consented materials only. No unconsented companion transcripts, student/FERPA data, personal therapy/relationship logs, or private social posts. A public case such as Poll_Hardy may inform practice-coding categories but is neither technical substrate evidence nor permitted source of private history without consent. Do not ask participants to validate any belief about AI consciousness or substrates. Store only minimum role and episode data, provide deletion/withdrawal mechanisms, and separate researcher hypotheses from participant instructions.

## Implementation handoff

Next executable components: immutable participant-visible source packets and sealed scoring packets; shared action API adapter to L4; action-stream recorder; live-yoked replay scheduler; deterministic perturbation injector; parity auditor; rater assignment/blinding manifest; precommitted simulation-based sample size calculation; provenance-preserving archival exporter. Include the expert automatic curator before enrolling humans. File results in Attractomancy; register observational evidence in the journal only after raw traces, actor metadata and blinded scoring are preserved.
