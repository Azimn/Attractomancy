# Collection Readiness and Handoff

Date: 2026-10-08
Branch: `main`
Scope: research-corpus organization and integrity, not new source collection.

## Canonical inventory

| Data product | Records | What a record means |
| --- | ---: | --- |
| `data/source_catalog.csv` | 444 | Catalog entry, not a validated finding |
| `data/source_graph_edges.csv` | 142 | Source-supported document/link relationship |
| `data/named_pair_registry.csv` | 23 | Publicly source-named human–AI pair/project |
| `data/pair_graph_edges.csv` | 8 | Source-supported pair-to-pair social edge |
| `data/reproducible_procedure_index.csv` | 24 | Candidate intervention with reconstructable core |
| `data/version_lineage.csv` | 23 | Explicit artifact revision/supersession link |
| `data/repository_capture_manifest.csv` | 14 | Verified saved repository file, NOT full source count |
| `data/retrieval_log.csv` | 16 | Historical collection batch |
| `data/local_artifact_manifest.csv` | 9 | Separate originally supplied research artifact records |

The README status block is the single *current* inventory. Historical collection reports retain the totals observed at their own dates.

## What is organized and usable now

**Intake:** Source metadata has stable S### identifiers, retrieval times, original URLs, tags and epistemic labels. `references/SOURCE_REGISTRY.md` orients readers, but `data/source_catalog.csv` is canonical.

**Transmission graph:** Source/document edges and pair/social edges are separate. An edge records a documented relationship, not similarity of terminology or independent validation of claims.

**Experiment preparation:** `data/reproducible_procedure_index.csv` lists operationally reconstructable interventions; it does not claim the interventions work. Original prompts, model versions, evaluation context, and ablation conditions must still be verified before experimentation.

**Historical reconstruction:** `data/version_lineage.csv` keeps older source states discoverable and differentiates rearrangement, revision and supersession. Historical Git blob IDs and immutable commit URLs are preferable to `main` links.

**Preservation:** `docs/SOURCE_PRESERVATION_POLICY.md` distinguishes legacy A–D copy/rights classifications from P0–P4 evidence/capture depth.

## Integrity results

Direct inspection of canonical GitHub files found:

- all 444 source IDs unique, with 17-column catalog rows;
- all 142 document edge references resolving to catalog IDs;
- all 8 social edge references resolving to known pairs and evidence sources;
- all 24 indexed procedures referencing known sources;
- all 23 version-lineage entries referencing known sources where an ID is supplied;
- one current README inventory block with counts aligned to data files;
- all 14 paths in `repository_capture_manifest.csv` fetched successfully through the GitHub connector, with the observed Git blob SHA recorded.

These are structural and existence checks. They do not constitute independent audit of every webpage, copyright assertion or experimental outcome.

The dependency-free `scripts/audit_catalog.py` now validates on-disk capture hashes and duplicate identity resolutions as well as cross-file structural integrity. The `.github/workflows/catalog-integrity.yml` workflow is configured on relevant pushes and pull requests.

**CI limitation:** At time of this report, a completed GitHub Actions run for the newest maintenance commit has not been independently confirmed through the available status interface. Do not label CI green until a completed run is observed.

## Distinct outstanding queues

### Repeated URLs: resolved as identity mappings

`data/duplicate_url_review.csv` records seven shared canonical URLs, now marked as either:

- `same_artifact_alias` / `same_thread_analytical_alias`: one webpage with multiple catalog IDs from different passes;
- `distinct_component_of_thread`: distinct identified material inside one thread, sharing the thread URL until a post-specific locator is recovered.

No stable IDs or graph references were deleted. For page-level counts use the canonical-source mapping, not raw catalog row count. **444 records are not 444 unique webpages.**

### 22 unlocated A-classified captures

`data/preservation_claim_review.csv` records 22 historically A-classified sources with no artifact locator in the catalog. These are unverified preservation assertions, not proof of missing copies. They require file discovery, rights review and hashes.

### 10 A-classified sources with incomplete capture scope

`data/source_scope_review.csv` records ten repository/corpus sources whose saved material is narrower than the source as a whole.

The 14 directly verified repository-held files consist of:

- **9** README/license snapshots of repositories;
- **4** complete primary-document snapshots (three in the REPAI corpus, one Structured Emergence);
- **1** metadata-only note.

A README and license **are not** a complete copy of a repository. Three complete papers **are not** the entire White-papers corpus. The current source-level A classification should be retained only after its exact intended scope is clarified, or deliberately reclassified with an explicit rationale.

### Primary sources not yet fully recovered

- Aion's main Drive book and associated session binaries;
- Vault015's claimed larger archive;
- screenshot-quality Signalborn/Solace glyph sets;
- REPAI Discord-origin artifact to public mirror chain;
- some versioned EQIS and GraceOS primary run material.

A published link, immutable revision, rights statement or archive metadata does not itself mean these artifacts were copied.

## Next safe work sequence

1. Confirm an actual completed green Catalog Integrity Actions run. If it fails, fix the audit before adding sources.
2. Triage the **32 A-classification review records** (22 no location, 10 partial scope). Prioritize high-value primary procedures. Preserve historical labels and decision rationale in the reviews.
3. For each high-value source, add or expand source-specific `references/archive/S###/` evidence: author/date, original URL, exact revision, observed excerpt/notes, lawful screenshot or copy, rights basis and hash.
4. Recover exact per-post permalinks for thread components in the duplicate crosswalk, without changing stable IDs.
5. Continue graph-guided acquisition of primary interventions, not merely raw source count. Map protocol → exact prompt → exact model/run → observed output → later interpretation.

## Procedure for future intake

**Source:** assign the next sequential S### ID, capture the URL, source date, retrieval UTC timestamp, original-language status, claims, intervention steps and confidence. Avoid inventing missing publication dates.

**Graph:** add a document or social edge only with a cited evidentiary source. Do not equate shared motifs with diffusion.

**Capture:** record rights and exactly which file was saved. For repository-held copies, add the path and Git blob SHA-1 to `data/repository_capture_manifest.csv`. For visual captures, preserve source URL, UTC capture time, file hash and scope sidecar. For nonredistributable content, use lawful metadata/notes rather than an unauthorized mirror.

**Quality gate:** update README inventory once, run `python scripts/audit_catalog.py`, check the Actions result, and write a dated retrieval/maintenance note. Push to `main`.

## Interpretation boundary

Attractomancy records cultural practice, prompt procedures, claims, observed behavior and hypotheses in separate layers. The graph maps documented source relationships. It is not evidence of machine consciousness, stable hidden persona state, paranormal influence, or causal prompt efficacy.

The project is now **organized for continued collection and controlled experiment design**. It is **not yet an experiment-ready frozen source release**, because high-priority captures and archival/classification reviews remain outstanding.
