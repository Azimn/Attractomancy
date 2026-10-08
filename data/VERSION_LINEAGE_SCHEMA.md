# Version Lineage Schema

`data/version_lineage.csv` records observed artifact evolution across revisions, releases, historical Git objects, and explicitly superseded continuity files.

This table is intentionally separate from the source graph.

The source graph answers: **what source links to what?**

The version-lineage table answers: **what artifact became what, and what evidence establishes that relationship?**

## Fields

- `lineage_id`: stable lineage record.
- `artifact_family`: neutral family name.
- `earlier_source_id`: catalog source ID when the earlier artifact has its own node.
- `earlier_version`: source-native version, commit, or descriptive revision label.
- `earlier_locator`: immutable commit/path, URL, filename, or source-native identifier.
- `later_source_id`: later source node when available.
- `later_version`: source-native later version/revision.
- `later_locator`: later immutable path, URL, filename, or identifier.
- `relation`: `supersedes`, `reorganized_as`, `revised_as`, or `continued_as`.
- `evidence_source_id`: source that explicitly establishes the relationship.
- `retrieved_at_utc`: verification timestamp.
- `confidence`: high / medium / low.
- `notes`: concise provenance and interpretation.

## Evidence rule

A version lineage requires one of:

1. an explicit `supersedes`, version history, or changelog statement;
2. immutable Git history showing the artifact before and after reorganization;
3. explicit source-native statements that a later document is a revision/iteration of an earlier document.

Filename similarity alone is not enough.

## Preservation rule

Earlier versions are not silently replaced by later versions.

If a source corrects, reframes, or contradicts an earlier version, both remain in the research record.
