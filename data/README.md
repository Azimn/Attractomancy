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
