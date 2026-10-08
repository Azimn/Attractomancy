# Attractomancy Data Catalog

This directory contains the machine-readable source catalog for the Attractomancy research archive. The CSV catalog is the canonical tabular index because it is human-readable, diffable, versionable, and can be opened directly in Excel, LibreOffice, Google Sheets, Python, R, or database tooling.

Every source record should include a retrieval timestamp, provenance, source type, platform, preservation level, research relevance, technique tags, and confidence notes. The catalog records both primary artifacts and secondary research about the human-AI phenomenon.

## Multilingual metadata

`language_index.csv` records known source languages, scripts, multilingual status, translation level, preservation status, and language-specific notes. The original-language artifact remains the primary evidence; translations are derivatives and may constitute separate experimental conditions.

## Source graph

`source_catalog.csv` is the node table. `source_graph_edges.csv` is the evidence-backed edge table. Edge semantics and evidence rules are defined in `SOURCE_GRAPH_SCHEMA.md`.

Do not create an edge from vocabulary overlap alone. Graph edges require explicit linking, citation, mirroring, named collaboration, shared-project evidence, or another source-supported relationship.

## Named pair registry

`named_pair_registry.csv` records explicitly source-named human–AI pairs and projects as social/entity data rather than document nodes. Its fields and evidence rules are defined in `NAMED_PAIR_SCHEMA.md`.

## Pair social graph

`named_pair_registry.csv` is the human–AI pair/project entity table. `pair_graph_edges.csv` stores explicit source-supported pair-to-pair interactions. Evidence rules are defined in `PAIR_GRAPH_SCHEMA.md`.

## Reproducible procedure index

`reproducible_procedure_index.csv` tracks primary interventions described precisely enough to reconstruct later. Its inclusion criteria and fields are defined in `REPRODUCIBLE_PROCEDURE_SCHEMA.md`. Inclusion is not evidence that a procedure works or that its source explanation is correct.

## Version lineage

`version_lineage.csv` records source-supported revision and supersession relationships among historical Git artifacts, versioned reports, memory cores, and continuity files. Its fields and evidence rules are defined in `VERSION_LINEAGE_SCHEMA.md`. Earlier versions are preserved rather than silently replaced by later interpretations.

## Duplicate-URL review and auditing

`duplicate_url_review.csv` lists repeated canonical URLs without deleting or renaming source IDs. The cases are still pending individual bibliographic review.

The dependency-free `../scripts/audit_catalog.py` validates CSV structure, source/pair foreign keys, status and preservation codes, UTC timestamps, duplicate review coverage, and the single current-state table in the root README. The `../.github/workflows/catalog-integrity.yml` workflow runs this check when repository data changes.

The latest maintenance findings are in `../docs/CATALOG_INTEGRITY_CLEANUP_2026-10-08.md`.

## Preservation claim review

`preservation_claim_review.csv` records legacy-A ("full artifact preserved") claims that currently lack a catalog artifact locator. Their state is **unverified**, not automatically disproven. Verify the actual copy, location, hash and rights before deciding whether to retain or change a classification.
