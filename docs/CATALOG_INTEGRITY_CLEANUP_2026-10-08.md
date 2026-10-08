# Catalog Integrity and Documentation Cleanup

Date: 2026-10-08
Repository: `Azimn/Attractomancy`
Target branch: `main`
Mode: maintenance only, with no new source or relationship claims.

## Canonical inventory audited

| File | Rows |
| --- | ---: |
| `data/source_catalog.csv` | 444 |
| `data/source_graph_edges.csv` | 142 |
| `data/named_pair_registry.csv` | 23 |
| `data/pair_graph_edges.csv` | 8 |
| `data/reproducible_procedure_index.csv` | 24 |
| `data/version_lineage.csv` | 23 |
| `data/retrieval_log.csv` | 16 |
| `data/language_index.csv` | 29 |
| `data/local_artifact_manifest.csv` | 9 |

These are record counts, not independently verified experiments or confirmed instances of consciousness.

## Structural findings

The pre-cleanup machine-readable audit found:

- source catalog rows: 444, with 444 distinct source IDs;
- no duplicate source IDs;
- no incorrectly sized CSV records in the audited core data files;
- zero unresolved source IDs in the document edge graph;
- zero missing pair endpoints in the social graph;
- zero missing source IDs in the reproducible-procedure index;
- zero missing source references in the version-lineage table;
- no missing source references in the multilingual index where a source ID is provided;
- one catalog record (S080) whose values had shifted across fields;
- seven canonical URLs recorded under more than one source ID;
- two non-equivalent preservation-classification scales in circulation;
- multiple outdated progress totals in the root README.

The source identifiers and historical retrieval timestamps were not rewritten.

## Repairs completed

### One malformed catalog record

S080, the Sherry Turkle/Financial Times discussion record, had source type, author, URL, status, preservation level and downstream fields displaced by a missing column.

The field positions were corrected while preserving:

- source ID `S080`;
- retrieval timestamp;
- original URL;
- original title and note;
- original meaning as a secondary lead.

No new verification of the article's substance is implied by this structural repair.

### Current-state consolidation

The README previously repeated obsolete states, including 108 and 129 document edges, alongside the authoritative 142-edge state.

The collection section was replaced with a **single canonical inventory table** and a short navigation index.

Historical pass reports are left intact as dated snapshots, not silently revised to today's counts.

### Preservation-classification compatibility

Two distinct vocabularies were previously used:

- legacy **A–D** catalog codes;
- newer **P0–P4** capture-depth/workflow levels.

These are now explicitly documented as *independent axes* in:

- `docs/SOURCE_PRESERVATION_POLICY.md`;
- `references/README.md`;
- `data/CATALOG_SCHEMA.md`.

A GitHub blob SHA alone does not establish a full rights-cleared local copy. Conversely an authorized local copy can exist without immutable Git history.

**No bulk conversion of historical preservation levels occurred.**

### Duplicate URL review

Seven normalized URL pairs were recorded in:

`data/duplicate_url_review.csv`

They are awaiting case-by-case review. A repeated URL may represent a true duplicate bibliographic entry or one page containing separately described procedural/social artifacts.

To avoid breaking source edges, retrieval provenance, or established citation IDs, **no source IDs were deleted or merged**.

### Repeatable audit

A dependency-free structural validator was added:

`scripts/audit_catalog.py`

It checks:

- CSV shapes and unique IDs;
- contiguous source-ID sequence;
- controlled status, confidence and legacy preservation codes;
- UTC retrieval timestamps;
- referential integrity among document edges, pair edges, source pairs, procedures and version records;
- deliberate review of normalized duplicate URLs;
- consistency of the README inventory with the actual CSV row counts.

A matching GitHub Actions workflow was added:

`.github/workflows/catalog-integrity.yml`

The workflow is configured to run on relevant `main` pushes, pull requests, and manual dispatch.

## Validation boundary

The structural counts and reference checks above were inspected against the actual `main` branch using the GitHub connector.

The Python audit and the newly created Actions workflow are now in the repository, but a completed Actions run has **not yet been confirmed** in this report.

This is a structural integrity check, not an independent re-verification of the 444 individual webpages, copyright permissions, scientific claims, or whether preservation screenshots exist.

## Next maintenance and research work

1. Confirm a completed CI audit and correct any check failure.
2. Review the seven duplicate-URL cases without deleting stable IDs.
3. Add an artifact-type/capture-depth register when source preservation work resumes so that metadata notes cannot be mistaken for full archived content.
4. Continue the previously identified version archaeology and primary-artifact recovery after the catalog infrastructure is stable.

The objective is to keep Attractomancy both broad enough for anthropological source discovery and exact enough for eventual reproducible experiments.
