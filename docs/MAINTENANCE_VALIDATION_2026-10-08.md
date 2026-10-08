# Catalog Maintenance Verification

Date: 2026-10-08
Repository: Azimn/Attractomancy
Branch checked: main

## Confirmed checks

The current canonical CSV files were independently fetched and checked through the connected GitHub interface.

Result: **PASS, zero structural errors detected.**

The checks covered:

- 444 source entries, unique and contiguous S001-S444 IDs;
- 142 document graph edges, all references to known source IDs;
- 23 human-AI pair/project records, each referring to a known source;
- 8 social graph edges with known pair endpoints and source evidence IDs;
- 24 indexed reproducible procedures with known source IDs;
- 23 version-lineage entries with all nonblank source references resolvable;
- consistent column counts in the tested core CSV files;
- exactly one README current-state block with matching metrics;
- seven repeated URLs covered by resolved canonical identity crosswalk entries;
- 22 A-classified sources without locators covered by `preservation_claim_review.csv`;
- ten partial-scope A classifications covered by `source_scope_review.csv`.

A second pass fetched every file named by `repository_capture_manifest.csv`. **14 of 14 Git blob SHA-1 identifiers matched** the returned GitHub file blobs.

Breakdown of those 14 saved files:

- 9 repository README/license snapshots;
- 4 primary text captures;
- 1 metadata-only preservation note.

These are file-level capture proofs, not evidence of 14 complete repository archives.

## What is not verified

- A successful run of GitHub Actions Catalog Integrity was not observable from the available connector status view. Its configuration exists, but green CI must not be asserted until an actual completed run is inspected.
- The Python audit script itself was not executed in a checked-out local repository during this pass. The independently executed structural checks and GitHub file/blob checks above are separate evidence.
- The 444 source URLs were not all re-fetched or individually fact-checked.
- Preservation claims for 22 unlocated A records and ten partial-scope A records remain open.
- No claim of successful controlled persona experiment is made.
- Artifact license descriptions are research-provenance notes, not independent legal opinions.

## Maintenance work committed

- Seven duplicate-page identity resolutions with canonical IDs, without breaking historical source references.
- A saved-file capture manifest with precise capture scope and Git blob IDs.
- A separate source-level scope review queue.
- Stronger `scripts/audit_catalog.py` checks for capture-file integrity and duplicate-identity resolution.
- A consolidated README inventory and navigation.
- An updated integrity-cleanup addendum and a research handoff in `docs/COLLECTION_READINESS_2026-10-08.md`.

## Next gate

Verify one completed green `Catalog Integrity` workflow run on `main` and address any failures before the next large intake batch. Afterward prioritize the 32 open source-level preservation-classification reviews.
