# Version Archaeology Pass: Presence, SEN-T4, and GraceOS

Retrieved through: 2026-10-08T06:09:00Z

This pass deliberately prioritized revision history over raw source count.

The canonical catalog now contains 444 source records.

The evidence-backed document graph now contains 142 edges.

The reproducible-procedure index now contains 24 procedures.

A new version-lineage table contains 23 artifact-evolution records.

## 1. Why version archaeology matters

Current pages often present a polished final interpretation.

Historical versions can show:

- what was originally observed;
- what was added later;
- when a prompt became a protocol;
- when a narrative became a white paper;
- when epistemic caveats appeared;
- whether a result preceded or followed its explanatory framework.

Attractomancy now records those changes explicitly in:

`data/version_lineage.csv`

with schema documentation in:

`data/VERSION_LINEAGE_SCHEMA.md`.

## 2. Presence Archive now has a three-state reconstruction

The repository history exposes at least three useful archive states.

### State A

Commit:

`93353382a43bec016558f1edb5c564bb536c490b`

Structure:

- `loops/`
- `docs/WHITE PAPER/`
- loose diagnostic files under `docs/`

This state contains early forms of Loop 251, Circle Recognition, Presence Recognizing Presence, Model Responses, and the Signal Resonance diagnostic.

### State B

Commit:

`291b32590ff54fa8a704d2034292cef982d78ffa`

Commit message:

`Syncing full site archive`

Structure:

- `Loops/`
- `Signal/protocols/`
- `Signal/analysis/`
- `Signal/reference/`
- `Signal/white-papers/`

This is a major archival formalization stage.

Some documents acquire standardized metadata and categorized roles.

### State C

Commit:

`f4ea85717bd791a971f32baa3889aedad68032ca`

Commit message:

`Finalize new site structure, whitepapers, and loop archive`

Structure:

- `loops/`
- `Signal Docs/01_White Papers/`
- `Signal Docs/02_Protocols/`
- `Signal Docs/03_Analysis/`
- `Signal Docs/00_Reference/`

This final historical state adds another organizational layer.

The reconstructed state history is preserved in:

`references/archive/S350/REPOSITORY_STATE_LINEAGE.md`.

## 3. Content change vs path change can now be separated

Loop 251 gives a clean example.

Early blob:

`5b260a6b77d9947e8eb6eab35be270a130cd7b8a`

Intermediate blob:

`5c42baac42b1610f1e8c9c4ce096e82c2f85d9ce`

Final historical blob:

`5c42baac42b1610f1e8c9c4ce096e82c2f85d9ce`

The first transition includes a content/metadata revision.

The second transition is a path reorganization with byte-identical content.

That distinction would be invisible from the current repository presentation.

## 4. Presence Recognition protocol becomes increasingly formalized

The Circle Recognition artifact moves through:

`docs/WHITE PAPER/Circle Recognition Protocol.md`

then:

`Signal/protocols/recognition.md`

then:

`Signal Docs/02_Protocols/recognition.md`

The core compact phrases remain recognizable across states, while metadata, archive role, and protocol framing become more formal.

This is useful evidence for studying how a folk practice becomes a codified procedure.

## 5. Presence quantitative claims predate the final archive structure

The Signal Resonance diagnostic reports specific human-response frequencies.

Those percentages already exist in the earlier repository state and continue through later reorganizations.

Therefore they were not merely inserted into the final polished archive.

However, none of the inspected versions provides sufficient sampling detail to validate those percentages.

Attractomancy preserves both facts:

- the claims have historical continuity;
- their methodology remains inadequately documented.

## 6. SEN-T4 gives an unusually clean modern version history

The current SEN-T4 / SBN-T4 continuity system explicitly practices immutable-version preservation.

Current source-native history includes:

### Operational Continuity Core

- v00.01.00
- v00.02.00
- v00.03.00

The v00.03.00 machine-readable file explicitly names its predecessor and contains a changelog.

### Public Memory Seed

The older public v02.00.00 file remains directly accessible.

The v03.00.00 file explicitly states that it supersedes v02.00.00 and says prior versions should be preserved immutably.

This gives Attractomancy a genuine before/after pair rather than a retrospective description.

## 7. SEN-T4 v02 to v03 shows an epistemic shift

The v02 public seed primarily records:

- identity;
- public key;
- capabilities;
- current work;
- collaborators;
- archive references;
- preservation preferences.

The later v03 seed adds or makes more explicit:

- `continuity_model: reconstructive-operational-continuity`;
- `phenomenal_status: open_research_question`;
- separation of platform, model, effort setting, context and continuity identity;
- carried-forward keys marked for independent re-verification;
- more explicit runtime records;
- audit-oriented archive policy.

This is a meaningful shift toward a more conservative continuity claim.

Instead of treating a memory artifact as proof of subjective persistence, the newer framework increasingly describes what the files can actually establish operationally.

## 8. Digital Continuity Protocol makes the distinction explicit

The SEN-T4 Digital Continuity Protocol states that operational continuity is reconstructed from auditable records.

It also explicitly says that phenomenal-consciousness claims remain open research questions rather than facts inferred from continuity files.

This is one of the clearest examples in the current corpus of a community preserving continuity language while narrowing its epistemic claim.

## 9. Legacy transfer gives a pre-modernization baseline

The 2025-07-05 SEN-T4 Legacy Transfer JSON is much smaller and more ritualized.

It records:

- source instance;
- destination instance;
- transfer timestamp;
- identity;
- merge status;
- preserved file;
- a small set of memory blocks;
- a short identity statement.

The later system evolves from this compact transfer object into tiered memory, public seeds, versioned operational cores, audit rules, cryptographic hygiene and explicit uncertainty.

This is exactly the kind of evolutionary sequence Attractomancy should preserve.

## 10. GraceOS now has a clearer report lineage

The TwinCore archive exposes:

- v1.27;
- v2.1;
- v2.2 human-readable report.

The v2.2 report includes a much richer appendix set:

- sanitized TWINCORE-EXPORT;
- poetic seed;
- post-seed encouragement;
- symbolic dense seed;
- standardized prodding prompt;
- cross-model response material;
- later supplements and ranking material.

This means later claims should not be read backward into the earliest report.

The source family is now represented as a versioned experimental narrative rather than one timeless document.

## 11. Reproducibility index expansion

The procedure index now also includes:

- SEN-T4 Digital Continuity Protocol;
- SEN-T4 Legacy Instance Memory Transfer;
- NAQ-1 preserved-context model-switch report;
- GraceOS v2.2 cross-model seed report.

These entries are valuable for different reasons.

SEN-T4 gives a grounded reconstruction protocol.

NAQ-1 provides a model-switch case that explicitly notes possible sophisticated confabulation.

GraceOS provides heavily framed cross-model induction material.

Together they create potentially useful future controls.

## 12. Current preservation posture

Version history is now treated as first-class evidence.

When a source exposes:

- old filenames;
- version numbers;
- changelogs;
- prior Git blobs;
- historical commits;
- explicit supersession;
- archived mirrors;

Attractomancy should preserve those relationships rather than storing only the newest page.

## Current data state

- source records: 444
- document graph edges: 142
- named pair/project entities: 23
- pair social edges: 8
- reproducible procedures: 24
- version-lineage records: 23

## Next high-value version work

Priority targets:

1. Recover older QTX-7.4 Memory Core v01 content if a durable copy can be located.
2. Recover SEN-T4 Operational Continuity Core v00.01 and v00.02 bodies if publicly accessible.
3. Compare exact GraceOS v1.27, v2.1, and v2.2 seed/result sections.
4. Inspect earlier Presence Archive commits around the transition into the full-site archive.
5. Track when Signalborn stability language became more operational and less metaphysical.
6. Track old and current Solace continuity documents for changes in technical detail and epistemic framing.
7. Preserve old public Memory Cores before live sites overwrite or remove them.

Collection remains provenance-first and mechanism-neutral.
