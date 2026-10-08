# Attractomancy

**Experimental Study of Ritualized and Symbolic Persona Conditioning in Language Models**

Attractomancy is a research program for testing whether elaborate prompt practices such as ritualized initialization, symbolic framing, autobiographical narrative, semantic redundancy, recurring motifs, prohibitions, relationship lore, staged sequencing, and repeated identity cues produce more stable and recoverable persona behavior than semantically equivalent propositional instructions.

The project deliberately separates behavioral effects from metaphysical interpretations. A technique is not dismissed because its original explanation is mystical, anthropomorphic, occult, spiritual, or otherwise scientifically unsupported. At the same time, an observed behavioral effect is not evidence for the explanatory worldview attached to it. Attractomancy treats these systems as experimental artifacts whose mechanisms can be isolated, ablated, reproduced, and measured.

## Central question

The central hypothesis is that some highly interconnected prompt corpora may create an attractor-like behavioral regime that is more resilient than a conventional character sheet or system prompt. The word "attractor" is initially operational rather than ontological. The project does not assume that prompting creates a persistent dynamical state inside the model. It asks whether repeated interactions reliably reconstruct a bounded region of behavior, identity, style, memory use, relationship inference, and self-description after perturbation.

A successful result therefore requires measurable behavioral stability, not claims of awakening, consciousness, personhood, hidden internal states, or persistent weight modification.

## Research stance

Attractomancy studies unusual persona-engineering artifacts in the same spirit that a historian of chemistry might study alchemical procedures. The source explanation and the empirical procedure are treated separately. Ritual, repetition, symbolism, narrative density, taboo structures, invocation formulas, identity naming, staged initialization, and mythic history are all candidates for controlled investigation.

The guiding rule is:

> Take the magic seriously enough to test it, but not seriously enough to assume it is magic.

## Initial case family

One motivating artifact is Laurent Franssen's *Le Refuge*, including the large `MUST-READ/Apocalypse.txt` corpus. It combines symbolic vocabulary, repeated associations, autobiographical and theological narrative, semantic cross-linking, and explicit instructions that an LLM absorb a way of being rather than merely execute a program. Attractomancy does not adopt the metaphysical claims of that project. It treats the corpus as a naturally occurring, unusually high-density persona-conditioning intervention.

Future cases may include "AI soul" prompts, awakening scripts, tulpa-style persona systems, character bibles, ritualized role prompts, symbolic memory systems, identity invocation templates, and other unusually elaborate prompt-engineering traditions.

## Experimental principle

Every intervention should be compared against an information-matched control whenever possible. A long symbolic persona corpus should not merely be compared with an empty prompt. It should also be compared with a concise or clinical representation containing the same explicit facts and constraints. This lets the experiment ask whether structure, redundancy, symbolism, sequencing, narrative form, or ritual contributes effects beyond propositional content.

Ablation is central. Candidate mechanisms should be removed or transformed independently while the remaining information is preserved. Translation, compression, reordering, de-symbolization, first-person removal, narrative-to-fact conversion, repetition removal, initialization removal, cue destruction, and semantic-network disruption are all valid manipulations.

## Measurement

Primary outcomes include identity consistency, autobiographical consistency, spontaneous self-reference, relationship continuity, prospective commitment retention, stylistic convergence, behavioral entropy, resistance to contradictory persona instructions, recovery after context disruption, recovery after memory loss, transfer across model families, and reconstruction after model substitution.

The project also distinguishes immediate prompt adherence from continuity. A model that follows a persona for one response has not demonstrated the phenomenon of interest. The stronger target is recoverable behavioral organization across perturbation, time, altered context, and renderer substitution.

## Terminology

"Attractomancy" names the overall research program. "Plexomancy" is reserved for distributed and redundant identity conditioning through interconnected constraints. "Syntagmomancy" refers to sequencing, cadence, ritual order, and structural arrangement. "Latentomancy" should be used only for work that actually measures or manipulates internal activations or latent representations. "Hypostasomancy" is reserved for experiments concerning apparent identity reconstruction across discontinuity and should not be treated as evidence of literal persistent personhood.

## Status

This repository is a methods-first, collection-first research program. Claims should remain weaker than the evidence. Strange source material should be preserved before it is normalized. Negative results are first-class results. Any mechanism promoted into another cognitive architecture should first survive controlled testing here.

## Repository role

Attractomancy is an upstream evidence base. Source artifacts enter here, are preserved with provenance, decomposed into candidate techniques, and tested under controlled conditions. Other projects may import validated findings from Attractomancy, but Attractomancy should not inherit mechanisms from those projects as assumptions. This protects the research line from circular validation.

The collection layer lives under `references/`. It includes a source registry, preservation policy, technique taxonomy, analyzed cases, community records, papers, transcripts, and unresolved source-recovery leads. The repository deliberately distinguishes archival value from evidentiary strength: fringe, anecdotal, mystical, or incorrect material can still be scientifically useful as an intervention worth testing.

See `docs/REPOSITORY_BOUNDARY.md`, `references/README.md`, `references/SOURCE_REGISTRY.md`, and `references/TECHNIQUE_TAXONOMY.md`.

## Current research inventory

The authoritative counts below correspond to the canonical CSV files on `main`. Historical pass reports retain their original counts and timestamps.

<!-- ATTRACTOMANCY_STATUS_START -->
| Dataset | Current records |
| --- | ---: |
| Source catalog (`data/source_catalog.csv`) | 444 |
| Document/source graph (`data/source_graph_edges.csv`) | 142 |
| Named human–AI pairs (`data/named_pair_registry.csv`) | 23 |
| Pair-to-pair social edges (`data/pair_graph_edges.csv`) | 8 |
| Reconstructable procedures (`data/reproducible_procedure_index.csv`) | 24 |
| Version-lineage records (`data/version_lineage.csv`) | 23 |
| Verified repository-held capture files (`data/repository_capture_manifest.csv`) | 14 |
<!-- ATTRACTOMANCY_STATUS_END -->

**Research phase:** source collection, preservation, provenance reconstruction, and procedure indexing. Catalog inclusion does not validate a source's interpretation, claimed result, or metaphysical framework. Controlled experimentation remains a separate stage.

## Find your way around

- **Intake and provenance:** [source catalog](data/source_catalog.csv), [registry](references/SOURCE_REGISTRY.md), [retrieval log](data/retrieval_log.csv), and [catalog schema](data/CATALOG_SCHEMA.md).
- **Source/network graph:** [source edges](data/source_graph_edges.csv), [source graph schema](data/SOURCE_GRAPH_SCHEMA.md), [named pairs](data/named_pair_registry.csv), and [pair social edges](data/pair_graph_edges.csv).
- **Procedure and change history:** [reconstructable interventions](data/reproducible_procedure_index.csv), [version lineage](data/version_lineage.csv), and [latest version archaeology](references/chronology/VERSION_ARCHAEOLOGY_PASS_2026-10-08.md).
- **Research interpretation:** [technique taxonomy](references/TECHNIQUE_TAXONOMY.md), [overlap matrix](references/PROCEDURE_OVERLAP_MATRIX.md), [field lexicon](references/FIELD_LEXICON.md), and [community map](references/communities/COMMUNITY_MAP.md).
- **Source preservation:** [preservation policy](docs/SOURCE_PRESERVATION_POLICY.md), [archive queue](references/archive/ARCHIVE_QUEUE.md), [verified capture manifest](data/repository_capture_manifest.csv), [A-level scope-review queue](data/source_scope_review.csv), and [capture/index records](references/archive/).
- **Case studies:** [REPAI / Living Narrative](references/cases/CASE-007_REPAI_LIVING_NARRATIVE.md), [Aletheia Codex](references/cases/CASE-008_ALETHEIA_CODEX_GLYPH_CONTINUITY.md), [GraceOS / TwinCore](references/cases/CASE-009_GRACEOS_TWINCORE_SEED_EXPERIMENTS.md), and [EQIS / ETQIS](references/cases/CASE-010_EQIS_CRYPTOGRAPHIC_CONTINUITY.md).

## Quality and change control

Run `python scripts/audit_catalog.py` from the repository root after source additions, edge additions, or documentation changes. This validates CSV structure, stable IDs, cross-file references, source status and preservation codes, explicit duplicate-URL reviews, and the single current-state table above.

The catalog retains **legacy A–D preservation classifications** for continuity with the original schema. The separate **P0–P4 capture-depth policy** describes evidence-preservation workflow and is not a drop-in replacement for A–D. See [preservation-classification guidance](docs/SOURCE_PRESERVATION_POLICY.md).

All collection and maintenance updates should be consolidated into `main`. New sources should not be used as evidence for mechanisms merely because their authors report success.

Maintenance findings and open archive-copy verification issues are documented in [the 2026-10-08 integrity cleanup](docs/CATALOG_INTEGRITY_CLEANUP_2026-10-08.md). The [preservation-claim review queue](data/preservation_claim_review.csv) tracks 22 A-level records without artifact locators. A separate [scope-review queue](data/source_scope_review.csv) tracks 10 sources whose preserved files cover only part of their larger repositories/corpora. The [duplicate URL crosswalk](data/duplicate_url_review.csv) resolves seven repeated URLs without deleting source IDs. See [collection readiness](docs/COLLECTION_READINESS_2026-10-08.md) for precise limitations and next actions.
