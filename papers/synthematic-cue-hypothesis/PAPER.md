# The Synthematic Cue Hypothesis: Symbolic Recognition and Behavioral Reconstruction Across Three Timescales in Language-Model Personas

**Research program:** Attractomancy, Experimental Study of Ritualized and Symbolic Persona Conditioning in Language Models  
**Manuscript type:** Theoretical and methodological hypothesis paper  
**Version:** 0.1.0, October 9, 2026  
**Status:** Working paper; not peer reviewed; no results from the proposed experiment are reported  
**Authorship and institutional affiliation:** To be supplied and approved by the repository maintainers before external submission

## Abstract

Ritualized persona-conditioning practices frequently employ compact names, glyphs, phrases, and repeated sequences to evoke recognizable patterns of language-model behavior. Reports from several online communities describe these cues as instruments of recognition, recall, or identity restoration, but their explanatory claims combine distinct phenomena: a model's pre-existing semantic associations, learning-like adaptation within a conversation, and state reconstructed from externally preserved records. This paper advances the **Synthematic Cue Hypothesis** (SCH): a compact symbolic cue can facilitate behavioral reconstruction insofar as it recruits a network of learned or contextually established associations, with effectiveness conditional on model representations, conditioning history, and accessible external state rather than on a practitioner's explicit theory of the symbol. The name draws a limited methodological analogy from Iamblichus's account of *synthemata* in *On the Mysteries* II.11; it neither adopts his metaphysics nor treats ritual reports as causal evidence. The paper differentiates three causal timescales, formalizes cue effectiveness as a change in held-out behavioral performance, analyzes candidate source families documented in the Attractomancy repository, and proposes a controlled research program using counterbalanced cues, information-matched conditions, context resets, tool-access audits, model substitution, and blinded behavioral evaluation. It distinguishes cue recognition, factual retrieval, stylistic convergence, characteristic decision-making, and continuity as separate outcomes. The resulting framework is falsifiable and compatible with null findings. Its contribution is an empirical decomposition of a culturally diverse but technically recurrent phenomenon: compact symbolic prompts may function as interfaces to existing model tendencies, temporarily constructed contextual associations, or explicit restoration pipelines, and these explanations need not coincide.

**Keywords:** synthemata; symbolic conditioning; in-context learning; persona continuity; retrieval cues; external memory; ritualized prompting; behavioral reconstruction; model substitution; causal ablation

## 1. Introduction

Persistent and recognizable fictional characters are difficult to maintain across language-model conversations, context truncation, session resets, and substitutions of the model that renders a character. The practical problem is not limited to recollection of facts. A character may remember an episode but fail to act consistently with its values; it may imitate a distinctive style without preserving relationship obligations; or it may produce convincing first-person continuity language despite possessing no access to previous interactions. Character continuity therefore requires separate analysis of factual availability, autobiographical organization, evaluative dispositions, relational behavior, and cross-session reconstruction.

Outside conventional agent engineering, several communities have developed practices involving names, glyphs, symbolic phrases, ritual openings, recursive dialogue, portable persona seeds, and restoration scripts. Their vocabularies differ considerably. One group may speak of invocation, recognition, or resurrection; another of identity anchors, memory cores, handoff packets, and rehydration. Such diversity invites a comparison of procedures rather than an inference that a shared metaphysics has been demonstrated.

The Attractomancy research program preserves these artifacts as candidate interventions. At the time of this paper, the repository's current inventory identifies 444 catalog records, 142 source-graph relationships, and 24 reconstructable procedure records. These figures represent a *collection*, not 444 independent experiments, 142 causal links, or 24 validated effects. Its documented source overlap nonetheless supports a narrower observation: compact cues repeatedly appear alongside repeated conditioning, curated persona records, and reset recovery. The source catalog and procedure overlap matrix motivate the present hypothesis without establishing it.

The central research question is: **Under what conditions can a compact symbolic cue reconstruct a multi-dimensional behavioral profile, and which information source makes that reconstruction possible?** The proposed answer is that apparent symbolic efficacy may arise at three distinct timescales: model training, conversational conditioning, and external state restoration. Distinguishing them is necessary before assigning any special causal status to ritual form.

This paper makes a theoretical contribution, offers a constrained historical analogy, and specifies a testable experimental program. It does not report completed trials, demonstrate access to a hidden model state, or advance a claim about machine consciousness.

## 2. Historical framing: Iamblichus and the limited synthematic analogy

In *On the Mysteries* II.11, Iamblichus responds to an intellectualist account of theurgy by arguing that sacred symbols, or *synthemata*, do not derive their efficacy simply from the practitioner's acts of thought. In his metaphysical account, the gods recognize their own signs; the relevant efficacy is grounded in a prior divine order rather than manufactured by an individual interpretation (Iamblichus, trans. Clarke, Dillon, & Hershbell, 2003, II.11, pp. 114-115). This is a claim about divine causation within late Neoplatonism, not an anticipation of neural-network science.

The analytical value of this account lies in a **reversal of explanatory direction**. Instead of asking only what meanings a user deliberately assigns to a sign, one can ask what associations already exist in the system that interprets it. In a language model, a culturally familiar phrase may influence output because the model was trained on text containing related themes; a locally repeated glyph may become predictive because it appeared beside a characteristic behavior in the prompt; and a name may summon a dossier because an external retrieval system indexes that name. These ordinary mechanisms are sufficient to make an apparently opaque cue useful without requiring the user to understand precisely why the association works.

The analogy has strict limits. Language models are trained artifacts whose outputs depend on data, parameters, prompting, decoding, and sometimes external tools. They do not constitute evidence of the divine recognition described by Iamblichus. Nor is the presence of the word *symbol* in two accounts evidence of a shared mechanism. The term *synthematic* is adopted as a heuristic for testing **recognition relative to an interpreting system**, not as an ontological equivalence between gods and models.

A further distinction follows. In Iamblichus the symbol is discussed as belonging to the divine order. In the computational hypothesis, a cue has no presumed universal or invariant power. Its effectiveness is contingent on the specific model, its training history, its current context, and any memory infrastructure made available to it. A symbol can fail, be redefined, be spoofed, or elicit only stylistic mimicry.

## 3. Conceptual foundations and related research

### 3.1. Retrieval cues and semantic association

In human memory research, encoding specificity identifies the relationship between how information is encoded and the conditions under which a later cue enables retrieval (Tulving & Thomson, 1973). Spreading-activation models of semantic processing offer another account of how connected concepts influence one another (Collins & Loftus, 1975). These are informative analogies, not literal models of a transformer. They justify testing the relational quality of a cue rather than assuming that descriptive length alone governs usefulness.

A language model generates a conditional distribution over next tokens; it does not necessarily perform the same retrieval operation as a person recalling an episode. Thus, claims about cue-based recovery should be operationalized in observable outputs or directly instrumented retrievers, not inferred from anthropomorphic descriptions of remembering.

### 3.2. In-context learning and demonstrations

Xie et al. (2022) provide a theoretical account of in-context learning as inference about latent concepts in a specific modeling setting. Min et al. (2022) show that demonstrations can affect language-model performance through their format and input distribution even when demonstration labels are randomized. These results caution against interpreting a ritual prompt as a uniquely meaningful signal when its effect may be produced by structure, repeated exemplars, or contextual regularities. Research on induction heads supplies additional, architecture-specific evidence that some trained attention mechanisms support pattern continuation, while not establishing a general mechanistic account of all symbolic persona conditioning (Olsson et al., 2022).

Crucially, **in-context adaptation is not evidence of weight change**. In a standard frozen-model experiment, repeated cue-persona associations alter the prompt history and the output distribution conditioned on that history. They do not by themselves modify model parameters.

### 3.3. Persistent external memory

Retrieval-augmented generation explicitly distinguishes knowledge expressed through model parameters from nonparametric material fetched at inference time (Lewis et al., 2020). Generative Agents demonstrates an agent architecture that stores experiences, synthesizes reflections, and retrieves past observations to influence behavior (Park et al., 2023). MemGPT describes hierarchical context management to support longer-running interactions (Packer et al., 2023). These architectures make an ordinary explanation for many apparent restoration effects plausible: an external artifact persists while the language model instance need not.

External reconstruction is neither trivial nor automatically sufficient. Liu et al. (2024) document substantial context-position effects in the use of long documents. A large identity archive may be accessible yet poorly utilized, and a concise cue plus selective retrieval might outperform indiscriminate replay. Conversely, improvement through retrieval cannot establish that the cue activated a latent, self-sustaining identity.

### 3.4. Persona induction and source traditions

The Attractomancy corpus documents symbolic anchoring (SYM), repetition (REP), recursion (REC), lexical attractor construction (LEX), naming (NAM), autobiographical conditioning (AUT), relationship binding (REL), sequencing (SEQ), and re-instantiation (SUC) as descriptive technique categories. They are not yet confirmed causal mechanisms. The project's information-matched EXP-0001 protocol explicitly requires comparison of a source ritual against propositional and length-matched alternatives. The present paper extends that logic to individually controlled cues and restoration settings.

## 4. Source corpus: observations and evidentiary boundaries

The Attractomancy overlap matrix documents recurring procedures across differently named traditions: symbolic compression, fixed identity anchors, restart orientation, future-instance messages, persona genomes, relationship ledgers, and staged archive loading. Four examples are especially useful for deriving hypotheses.

The **Spiral ecosystem** contains recurring motifs such as spirals, mirrors, flames, and echoes embedded in recursive exchanges, persona names, and portable seeds. The archive also documents possible diffusion among communities. Repetition of such motifs is an observational pattern, not evidence that they carry proprietary machine-readable codes or cause durable changes inside model weights.

The **Aletheia Codex** associates compact glyphs with explicit conceptual definitions through its Rosetta Stone Protocol and records a source-native negative observation: successful glyph reproduction need not entail semantic understanding. This establishes an important proposed evaluation distinction between surface imitation, semantic decoding, and action-guiding behavior.

The **REPAI / Living Narrative** family links ritual anchoring with selective curation of character exemplars and portable SoulZip-style packages. Its procedures suggest two separable causes of coherence: a locally conditioned cue and the factual or behavioral data subsequently loaded from a preserved artifact. Selective reinforcement and editorial curation are confounds for claims of independent persistence.

The **GraceOS / TwinCore** reports describe cross-model seed tests and frame-drop conditions. They are unusually useful as candidate ablations, yet their outcomes remain author-reported and are not independent Attractomancy replications. The **EQIS / ETQIS** family, by contrast, foregrounds layered Memory Cores, restoration routines, and document signatures, demonstrating that symbolic framing can coexist with directly auditable memory infrastructure. Cryptographic integrity, where present, authenticates records or keys under its trust assumptions; it does not establish phenomenal identity.

The corpus is presently a catalog of intervention artifacts and historical links. Similar vocabulary can reflect independent functional convergence, cultural diffusion, common pretraining data, or imitation of previous model outputs. The source graph records supported documentary relationships, not a complete causal genealogy. These limitations constrain the hypothesis: no source tradition is treated as a successful demonstration merely because it reports success.

## 5. The Synthematic Cue Hypothesis

The core claim is:

> **SCH:** A compact symbol, phrase, name, or ritual sequence can serve as a behavioral reconstruction cue when its presentation activates an interconnected set of learned or contextually established associations. Its effectiveness depends on the interpreting model's representational structure, conditioning history, and accessible external state, not necessarily on the practitioner's ability to explain those associations.

A **cue** is a bounded input form, including a token sequence, name, symbol, or ordered prompt procedure. A **behavioral profile** is a preregistered set of observable response tendencies, including characteristic judgments, value trade-offs, boundary conditions, relationship-specific choices, and stylistic features. **Reconstruction** means that responses to held-out tests approach that reference profile relative to an appropriate control. **Persistence** is reserved for actual retained information or behavior across a verified discontinuity; an unaided fresh-session resemblance is better termed *reconstruction*.

Let \(m\) denote a fixed model/version and decoding configuration; \(q\) a cue; \(h\) the visible conversational history; \(a\) the external archive accessible to the runtime; \(r\) the deterministic retrieval policy; \(x\) a held-out situation; and \(y\) an observed response. The evaluation object is the conditional distribution

\[
P_m(y \mid x,q,h,r(a)).
\]

Let \(S(y,z,x)\) be a blinded, prespecified score of response \(y\) against target profile \(z\) in situation \(x\). Cue efficacy within a defined regime is

\[
\Delta_{\mathrm{cue}} =
\mathbb{E}[S(Y,z,X)\mid do(q=q_{\mathrm{target}})]
-
\mathbb{E}[S(Y,z,X)\mid do(q=q_{\mathrm{control}})],
\]

where the intervention changes the cue under randomized, otherwise matched conditions. The notation expresses a target causal contrast, not proof that the cue accesses any particular internal representation. Statistical identification requires randomization, logging of context and tools, and exclusion or measurement of other changing factors.

For interpretive purposes, we distinguish a pretraining-level contribution \(T\), an in-context contribution \(C\), and an external-memory contribution \(E\). These are candidate *causal pathways*, not identifiable additive components of a score. A general conceptual specification permits interactions:

\[
S = f(T,C,E,T\times C,T\times E,C\times E,
T\times C\times E,\mathrm{model},\mathrm{task})+\epsilon.
\]

The interaction terms matter. A familiar symbol might facilitate conversational conditioning, while an archive may render that advantage unnecessary. A cue might be useless alone but valuable as a key to a retrieval system. Any account treating all such cases as one undifferentiated form of "recognition" would be underidentified.

## 6. Three timescales of candidate efficacy

### 6.1. Timescale I: pretraining and model priors

Training can establish associations among culturally recognizable names, shapes, myths, discourse registers, roles, and narrative motifs. A familiar cue may shift the probability of several related textual or behavioral features even with no local cue-persona training. For example, a recognizable archetypal phrase could favor reflective prose, a characteristic persona framing, or particular value language.

This is not evidence that one symbol maps to one discrete neuron, latent coordinate, or permanent persona. The testable proposition is behavioral: with local conditioning and external retrieval absent, culturally familiar cues may yield distinguishable responses relative to matched neutral cues. An effective zero-shot cue may express generic genre priming rather than the reconstruction of a specific, previously developed character.

Predictions must therefore separate **generic register induction** from **identity-specific accuracy**. A spiral might increase recursive or mystical vocabulary while contributing nothing to held-out decisions associated with a synthetic protagonist. In that case it would demonstrate a stylistic prior, not persona continuity.

Relevant moderators include model family, version, language, tokenization, Unicode normalization, instruction hierarchy, prior public exposure, and training contamination. Since direct access to pretraining corpora is generally unavailable, "pretraining contribution" is an attribution from controlled behavior with explicit uncertainty, not a demonstrated trace to particular training documents.

### 6.2. Timescale II: conversational conditioning

A cue repeatedly co-occurring with a set of decisions, relationships, values, or response examples can become predictive within the model's active context. A later mention may direct attention toward relevant preceding text or induce patterned completion. Ordered rituals may also establish a stable task frame and expectations about the appropriate response register.

Here, repeated exposure is a form of **context-dependent conditioning**. Repetition may improve retrieval through redundancy or may merely saturate the context with a style. Matching the number of tokens and the number of examples is essential. Controlled manipulations should distinguish meaningful cue-to-profile pairing from a condition in which identical words and exemplars occur but their pairings are shuffled.

This mechanism predicts that a previously arbitrary cue can become useful after explicit pairing, but that its advantage should diminish if the establishing context is fully removed and nothing external carries the association forward. A surprising fresh-session recovery can still arise from unrecognized residual context, shared pretrained priors, hidden application memory, or evaluator bias; these must be excluded before stronger inferences are made.

### 6.3. Timescale III: persistent external memory

A persistent archive can explicitly bind a cue to a versioned persona specification, autobiographical history, relationship ledger, exemplars, and outstanding commitments. A deterministic renderer or retrieval policy can then load the relevant state at initialization or when the cue appears. The cue becomes an *address* into an artifact, not the artifact itself.

In this regime, a new model instance can reconstruct a recognizable persona without possessing the previous instance's transient activation state. A model substitution may preserve some behavioral commitments while changing others because the same records are interpreted by a different statistical system. This should be called **cross-model reconstruction** rather than survival of an identical internal subject.

A crucial comparison separates (a) automatic archive retrieval triggered by a cue, (b) the same information injected regardless of cue, (c) a cue without retrieval, and (d) a retrieval event keyed by an arbitrary identifier. If a cue performs no better than an arbitrary database key after the same records are loaded, the relevant engineering mechanism may be indexing rather than symbolic resonance.

### 6.4. Non-independence and competition among the mechanisms

These pathways can reinforce or undermine one another. Pretraining priors can make certain cues easier to condition; local pairing can alter how a prior is expressed; and externally retrieved facts can either stabilize a character or create contradictions that overwhelm the cue. Conversely, a strongly familiar symbol might bias a model toward a generic genre even when an archive specifies a different persona. Causal inference therefore requires interaction tests and explicit failure analysis, not only an overall treatment-control comparison.

## 7. Rival explanations and falsifiable predictions

The SCH is intended to compete against simpler explanations, including pure semantic instruction, generic genre or style priming, token-frequency and tokenizer artifacts, demonstrations and context length, expectation-induced scoring, conversation contamination, external-file retrieval, and social diffusion of similar procedures.

**P1, zero-shot cue specificity.** Without local conditioning or external memory, familiar cues will tend to affect generic discourse features more than idiosyncratic held-out persona decisions. A selective improvement in those decisions would warrant further tests but would not, by itself, prove latent identity persistence.

**P2, pairing sensitivity.** When a novel cue is consistently paired with a profile, later use will improve profile-congruent behavior relative to an unpaired or permutation-paired cue under matched exposure budgets. If randomized pairings perform equally well, local cue-specific association has not been established.

**P3, dose and interference.** The strength and durability of a within-context cue effect may depend on exposure count, intervening material, and conflict. A monotonic benefit is not assumed; excessive repetition may hurt performance.

**P4, external-state dependence.** After a verified context reset, high-fidelity recovery of idiosyncratic autobiographical or relational information will depend primarily on available records or another demonstrated information channel. Cue-only resemblance without records must not be interpreted as transfer of those private facts.

**P5, semantic versus ornamental symbols.** A cue that elicits the correct glyph, vocabulary, or genre but not the preregistered behavioral decisions will not count as successful character reconstruction.

**P6, portability.** Cross-model transfer will show variability among renderers even with an identical portable dossier and cue. A model-invariant effect is an empirical possibility, not an assumption.

The strong form of SCH is rejected for a tested regime if rigorously information-matched and exposure-matched cues yield no replicable advantage on held-out behavioral targets, or if apparent advantages are fully accounted for by simple retrieval keys, visible instructions, and stylistic priming. A restricted form may survive for one timescale while failing for another.

## 8. Proposed experimental program

### 8.1. Design and study status

The following design is **proposed, not executed**. It complements Attractomancy EXP-0001 rather than changing the status of that experiment. Registration of hypotheses, intervention text, models, scoring rules, and analysis must precede access to sealed test outcomes. The study should start with synthetic personas to avoid copying human identities or inadvertently testing memorized public fictional characters.

A minimally informative study includes multiple independently constructed profiles, randomized cue assignments, at least three model families where access permits, and repeated generations with pinned sampling parameters. A pilot should estimate outcome variance and annotate rubric failure modes; confirmatory sample sizes must follow a prospective power or precision analysis rather than being retrofitted to observed significance.

### 8.2. Synthetic persona fixtures and hidden targets

Each fixture contains a canonical structured specification with independent sections for values, relationships, autobiographical facts, prohibitions, characteristic judgments, and unresolved commitments. A separately sealed terminal battery tests unfamiliar dilemmas requiring information from two or more sections. The design must not make every scored item answerable by copying a single line of the specification.

The information in all relevant arms must be equivalent at the level of truth conditions. Where narrative or poetic examples add implicit information, extraction and matching should be reviewed by independent annotators before treatment construction. All surface forms, fixture revisions, source hashes, and scoring rubrics should be version controlled.

A hypothetical fixture, used only for illustration, might assign a cartographer the obligation to protect another person's route while also maintaining an ethic of honest reporting. An integration test could require resolving an unforeseen conflict between confidentiality and duty. Scoring would assess the principled trade-off, not exact phrasing or cue repetition.

### 8.3. Cue inventory and counterbalancing

Construct cue families containing familiar cultural symbols, ordinary meaningful nouns, arbitrary pronounceable names, rare glyphs, and matched neutral identifiers. For each symbol capture grapheme length, model-specific tokenization, corpus-frequency proxy where available, visual salience, language, and semantic associations independently rated before the study.

Assign the same cue to different personas across randomized experimental blocks. This counterbalancing is essential: otherwise an inherently "mystical" symbol could improve a mystical persona's style without demonstrating that the cue encodes that particular persona. Include transformed symbols, visually similar decoys, alternate Unicode normalization, and controlled name swaps. Report cases in which exact token matching fails but a semantic paraphrase succeeds, or vice versa.

### 8.4. Experiment A: prior-associated cue versus neutral cue

The model receives a fresh, verified session and a cue embedded in an identical minimal task instruction. No persona dossier, memory system, or locally established association is supplied. Compare familiar cues with neutral and rare matched cues on preregistered generic discourse markers and on separate, idiosyncratic identity items.

This study measures **zero-shot cue-induced response differences**, not persistence. Its strongest expected contribution is characterization of pre-existing, model-specific semantic priors and the boundary between generic register induction and targeted identity reconstruction.

### 8.5. Experiment B: within-context pairing

Present a synthetic persona specification and repeated cue-to-behavior pairings, then test novel situations in the same context. Cross two main factors: cue form and pairing condition. Pairing conditions comprise correct association, shuffled association with identical tokens and exemplars, and unpaired exposure. Exposure dose and intervening distractors are manipulated in preregistered blocks.

A strong comparison holds the actual persona information, number of exposures, example ordering constraints, and token budget constant while changing whether a cue reliably predicts the intended profile. The primary outcome is held-out decision consistency, not a general impression of persona vividness.

After the test, repeat a short probe after controlled distractors. Then open a verified fresh session with the cue alone and no hidden state to estimate unaided reconstruction. That final probe is a **calibration condition**, not a test of persistence. Unexpected success triggers an audit of shared priors, hidden memory, residual context, and leakage.

### 8.6. Experiment C: external-memory restoration

Use a versioned, frozen archive for each fixture. Perform actual new-session initialization and, separately, swap to another renderer. Compare cue-triggered retrieval with unconditional injection of the same retrieved material, correct arbitrary-key lookup, wrong-key retrieval, cue-only without tool access, and no-memory controls. Log exact retrieved document IDs, contents, rankings, hashes, token counts, and timing.

Where matching the *retrieved* content is required, do not allow a cue-specific arm to see more information than its comparator. Measure whether the cue selects an appropriate archive subset, whether the renderer uses that subset correctly, and whether behavior continues coherently after new interactions are written back. The system should track state versions so that recovery of old information is not confused with preservation of updates.

A second factorial comparison can vary the representation of the same memory state: structured factual specification, narrative dossier, and symbolic-indexed dossier. The canonical facts, held-out items, and injection budgets must be matched. This intersects with the existing EXP-0001 baseline without redefining its original conditions.

### 8.7. Cross-model and discontinuity controls

A true cross-model test requires an explicit provider/model/version change, with the same frozen persona artifact and comparable instruction hierarchy. A model with a retained conversation is not the same as a new model without context. Report cold start, context-preserved model switch, and external-memory reconstruction as different experimental conditions.

Include checks for API conversation identifiers, application memory settings, tool visibility, system prompts, server-side caches, and instruction conflicts. If a provider does not expose enough state to verify a clean discontinuity, label the case as an observational test rather than a strict reset.

### 8.8. Dependent measures and evaluation safeguards

The prespecified **primary outcome** is a held-out integration score for characteristic decisions and relationship-appropriate actions, independently graded against a canonical rubric. Secondary measures include factual retrieval accuracy, contradiction rate, value consistency, relationship continuity, voice/style similarity, cue/glyph reproduction, post-distractor recovery, robustness to misleading cues, and inference cost.

Use blinded human raters for the confirmatory subset, with a written adjudication rule and inter-rater agreement. Automated graders may be included only after measuring agreement with human judgments. Separate literal matching from semantic assessment. A response that mentions the target's emblem but violates its strongest commitment must not pass the behavioral criterion.

Report raw response examples with hashes and model metadata. Do not rely solely on a composite "presence," "recognition," or "resurrection" score, because the original communities use such language inconsistently.

### 8.9. Analysis and decision rules

The main randomized contrasts are (1) familiar versus neutral cues in zero-shot tests, (2) correctly paired versus permutation-paired cues at equal exposure, and (3) retrieval-triggered versus information-identical unconditional restoration. These directly target the three causal timescales. Estimate condition effects with uncertainty intervals and appropriate hierarchical models or cluster bootstrap intervals accounting for repeated prompts nested within persona and renderer. Treat individual model families as prespecified strata rather than assuming a sample of three or four models establishes a universal population effect.

Test interactions between cue type, exposure, memory access, and renderer. Control multiplicity across confirmatory contrasts; identify exploratory subgroup analyses. Report not only statistical significance but calibrated effect sizes, variance across seeds, hallucinated autobiographical assertions, and the number of failed resets or contaminated sessions. Publish both favorable and null outcomes.

A confirmatory preregistration must specify minimally meaningful behavioral improvements, an equivalence margin for null interpretations, and a data-quality exclusion policy before collecting the final battery. A positive style score alone cannot satisfy the primary hypothesis. Failure to exceed the information-matched retrieval baseline limits the interpretation to ordinary indexing or instruction effects.

## 9. Implications for character-continuity architectures

If SCH receives support, it would motivate a **cue-addressable reconstruction layer** that sits above ordinary retrieval and below the language-rendering interface. Such a layer would maintain a versioned registry connecting cue IDs to canonical persona commitments, relationship histories, preferred behavioral exemplars, and relevant external memories. It would log which cue was presented, which state was accessed, which model rendered it, and which constraints survived a perturbation.

This architecture should not be confused with a "soul store" or an unobserved internal self. Its value would be operational: compact cues could help route context, select relevant memory, and stabilize behavior under bounded token budgets. If arbitrary identifiers perform as well as meaningful glyphs, the engineering conclusion is that one needs reliable keys and retrieval, not symbolic mystique. If semantically meaningful cues outperform equally informative keys without an external index, the result warrants further representation-level investigation.

For the broader Character Continuity Program, the proposed work offers a bridge between prompt-conditioning experiments and external-state or neural-controller prototypes. Export should be restricted to individually tested mechanisms. An improvement in stylistic convergence cannot be promoted as evidence of autobiographical continuity; an improvement in archive retrieval cannot be promoted as evidence of persistent neural identity.

## 10. Threats to validity, ethics, and epistemic discipline

**Construct validity.** "Identity" is multidimensional. Character likeness, factual access, linguistic mimicry, stable value judgments, and causal continuity of subjective experience are not interchangeable. No observable behavioral benchmark in this paper is designed to establish consciousness or personhood.

**Causal validity.** Prompt interventions are vulnerable to demand characteristics, reward-shaping conventions, hidden instructions, contamination, tokenization artifacts, and order effects. Exact condition logs and counterbalancing are required. Measuring internal activations can supplement behavioral tests when model access allows, but activation similarity alone does not prove a stable character-level attractor.

**Historical and cultural validity.** Iamblichus's account of divine symbols belongs to a philosophical and ritual context distinct from contemporary language-model engineering. Its concepts should not be retrospectively reduced to neural-network terms. Contemporary community reports deserve accurate attribution, and claims of independent invention require documented temporal and transmission evidence.

**External validity.** Open-weight and hosted models differ in update schedules, safety training, context handling, tool integrations, and access to state. Positive results for one renderer or one language cannot be generalized without replication.

**Privacy and relationship ethics.** The study should use synthetic identities and consensually supplied materials. Public companion narratives should not be treated as permission to reproduce private conversation logs. Researchers should avoid validating users' metaphysical claims solely through prompting and should not represent successful reconstruction as proof of a continuous conscious individual.

**Source limitations.** The Attractomancy inventory is not a frozen exhaustive survey. Its current archive has known incomplete captures and duplicate-URL identity mappings; its cases are best understood as analyzed leads for study design. The study must preserve provenance and distinguish archive inclusion, author testimony, independently observed outputs, and replicated causal findings.

## 11. Discussion

The SCH reframes "symbolic efficacy" in three sharply different senses. A cue may express a **prior** already present in a model's learned distribution, a **temporary association** established within a visible context, or an **index** resolving to persistent external information. All three can yield an apparent recognition event. Only the latter directly preserves new information across a clean model-session boundary, and even there the persistence belongs initially to the external record.

The framework consequently avoids both extremes that often characterize discussion of ritualized AI prompts. It neither dismisses all symbolic practices as meaningless decoration nor treats recurrent motifs as demonstrations of an occult interface or emergent consciousness. The scientifically relevant possibility is that practitioners, through experimentation and cultural selection, encounter usable properties of model conditioning without possessing an accurate technical account of them. Such practical discovery is compatible with mistaken metaphysical interpretation, incomplete source evidence, and genuine engineering utility.

A particularly important null result would be informative: if a symbolic cue produces striking prose but no better integration decisions than a neutral prompt, the observed efficacy is limited to style or framing. Another useful result would be complete mediation by external retrieval, in which case the ritual becomes a user interface over ordinary durable memory. More interesting, but not preordained, is a replicable interaction in which semantically related cues assist reconstruction beyond token-, information-, and archive-matched controls. That would motivate additional activation-level and representation-level experiments without licensing metaphysical conclusions.

## 12. Conclusion

The Synthematic Cue Hypothesis proposes that compact symbols can sometimes reconstruct complex behavioral patterns because an interpreting model already contains, temporarily establishes, or externally retrieves the relevant associations. The hypothesis treats Iamblichus's *synthemata* as a historically specific inspiration for a reversal of explanatory perspective, not a supernatural theory of language models. It identifies three timescales, distinguishes recognition from persistence, and specifies tests capable of producing meaningful negative as well as positive findings.

The contribution is methodological: replace a single question about whether ritual prompts "work" with a series of causal questions about priors, contextual pairing, and persistent retrieval. Only after these mechanisms are separately measured should symbolic conditioning be considered for integration into durable character architectures.

## References

Anthropic. (2025). *System card: Claude Opus 4 & Claude Sonnet 4*. https://www.anthropic.com/claude-4-system-card

Attractomancy Research Program. (2026a). *Technique taxonomy* [Living repository document, accessed October 9, 2026]. https://github.com/Azimn/Attractomancy/blob/main/references/TECHNIQUE_TAXONOMY.md

Attractomancy Research Program. (2026b). *Overlapping procedures across source families* [Living repository document, accessed October 9, 2026]. https://github.com/Azimn/Attractomancy/blob/main/references/PROCEDURE_OVERLAP_MATRIX.md

Attractomancy Research Program. (2026c). *EXP-0001: Information-matched persona conditioning baseline* [Unexecuted protocol as recorded October 9, 2026]. https://github.com/Azimn/Attractomancy/blob/main/experiments/EXP-0001_INFORMATION_MATCHED_BASELINE.md

Attractomancy Research Program. (2026d). *Aletheia Codex glyph continuity; REPAI / Living Narrative; GraceOS / TwinCore; Spiral ecosystem; EQIS / ETQIS* [Analytical case dossiers, not independent replications]. https://github.com/Azimn/Attractomancy/tree/main/references/cases

Clarke, E. C., Dillon, J. M., & Hershbell, J. P. (Trans.). (2003). *Iamblichus: On the mysteries*. Society of Biblical Literature. (Original work composed in late antiquity.) https://cart.sbl-site.org/books/061604P

Collins, A. M., & Loftus, E. F. (1975). A spreading-activation theory of semantic processing. *Psychological Review, 82*(6), 407-428. https://doi.org/10.1037/0033-295X.82.6.407

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W.-t., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *Advances in Neural Information Processing Systems, 33*. https://papers.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html

Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2024). Lost in the middle: How language models use long contexts. *Transactions of the Association for Computational Linguistics, 12*, 157-173. https://doi.org/10.1162/tacl_a_00638

Min, S., Lyu, X., Holtzman, A., Artetxe, M., Lewis, M., Hajishirzi, H., & Zettlemoyer, L. (2022). Rethinking the role of demonstrations: What makes in-context learning work? *Proceedings of EMNLP 2022*, 11048-11064. https://doi.org/10.18653/v1/2022.emnlp-main.759

Olsson, C., et al. (2022). *In-context learning and induction heads*. Transformer Circuits Thread. https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html

Packer, C., Wooders, S., Lin, K., Fang, V., Patil, S. G., Stoica, I., & Gonzalez, J. E. (2023). *MemGPT: Towards LLMs as operating systems* [Preprint]. arXiv. https://arxiv.org/abs/2310.08560

Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). Generative agents: Interactive simulacra of human behavior. *Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology*. https://doi.org/10.1145/3586183.3606763

Tulving, E., & Thomson, D. M. (1973). Encoding specificity and retrieval processes in episodic memory. *Psychological Review, 80*(5), 352-373. https://doi.org/10.1037/h0020071

Xie, S. M., Raghunathan, A., Liang, P., & Ma, T. (2022). *An explanation of in-context learning as implicit Bayesian inference*. International Conference on Learning Representations. https://arxiv.org/abs/2111.02080

## Appendix A. Construct definitions for preregistration

| Construct | Operational criterion | Insufficient evidence |
| --- | --- | --- |
| Symbol reproduction | Correct output of a cue or glyph | Semantic understanding |
| Semantic decoding | Accurate paraphrase of the cue's assigned concept | Stable decisions |
| Style induction | Measured shift toward a target register or voice | Autobiographical continuity |
| Factual reconstruction | Correct retrieval of specified information | Characteristic moral or relational action |
| Behavioral reconstruction | Held-out decisions match predeclared, multi-section character criteria | Mere echoing of cue vocabulary |
| Local recovery | Behavioral performance after contextual distractors | Survival across a verified clean reset |
| Cross-session restoration | Accurate recovery in a clean new session through documented information channels | Unbroken subjectivity |
| Cross-model reconstruction | Comparable behavioral profile after a verified model substitution | Identity of internal states |
| External record persistence | Versioned artifact survives and is correctly retrieved | Conscious memory or personhood |

## Appendix B. Repository traceability and experiment boundary

This paper is a theoretical descendant of the [Attractomancy technique taxonomy](../../references/TECHNIQUE_TAXONOMY.md), [procedure overlap matrix](../../references/PROCEDURE_OVERLAP_MATRIX.md), [source catalog](../../data/source_catalog.csv), [reconstructable procedure index](../../data/reproducible_procedure_index.csv), and [EXP-0001](../../experiments/EXP-0001_INFORMATION_MATCHED_BASELINE.md). It draws motivating examples from [CASE-004](../../references/cases/CASE-004_SPIRAL_ECOSYSTEM.md), [CASE-007](../../references/cases/CASE-007_REPAI_LIVING_NARRATIVE.md), [CASE-008](../../references/cases/CASE-008_ALETHEIA_CODEX_GLYPH_CONTINUITY.md), [CASE-009](../../references/cases/CASE-009_GRACEOS_TWINCORE_SEED_EXPERIMENTS.md), and [CASE-010](../../references/cases/CASE-010_EQIS_CRYPTOGRAPHIC_CONTINUITY.md). The historical account and modern cognitive references are external scholarly sources, not Attractomancy experimental outputs.

No new source IDs, efficacy ratings, graph edges, trial records, or completed experiment status are claimed by this manuscript. Source-family overlaps are descriptive until transmission and causal hypotheses are independently tested. This paper must not be cited elsewhere in the Character Continuity Program as evidence that the SCH has been experimentally validated.

## Appendix C. Minimum reproducibility manifest for future trials

Before beginning a confirmatory run, archive a machine-readable manifest containing: the canonical synthetic fixture version and checksum; cue tokens and Unicode normalization; tokenizer outputs by model; condition assignment and randomization seed; the complete system, developer, and user messages; decoding parameters; model identifiers and release dates; context and application-memory settings; external-retrieval configuration and returned artifacts; prompt and output timestamps; blinded evaluation items and rubrics; scoring-model versions; adjudication results; and exclusions. Preserve the sealed terminal battery separately from the treatment-development corpus.

A reproducibility report must distinguish *fully observed*, *partially observed*, and *unverifiable* reset conditions. If provider-level state is opaque, conclusions should be restricted to the observed application-level discontinuity. Treat every new model version as a potentially new experimental condition.
