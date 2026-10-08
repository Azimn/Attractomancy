# SOURCE PRESERVATION POLICY

Effective: 2026-10-07

Attractomancy studies an unusually fragile body of public material: Reddit posts, forum threads, personal blogs, Substack essays, small GitHub repositories, prompt files, screenshots, and community documents that may be edited, deleted, made private, or lost when platforms close.

A URL is therefore discovery evidence, not sufficient archival evidence.

## Preservation objective

For every high-value source, preserve enough lawful research evidence that later investigators can establish:

1. what source was observed;
2. where it was observed;
3. when it was retrieved;
4. what version or state was observed;
5. which portions informed Attractomancy's analysis;
6. whether a local copy exists;
7. whether the source can still be independently retrieved.

## Two independent classification systems

The catalog's existing `preservation_level` field uses the **legacy A–D access/rights scale** described in `references/README.md`:

- **A**: a complete research artifact is preserved and can be redistributed under known rights.
- **B**: a lawful local research copy exists, but the public repository holds only metadata.
- **C**: publicly accessible URL and source/archive metadata are recorded; a linked metadata file does not by itself establish a full local copy.
- **D**: unresolved discovery lead.

The **P0–P4 scale below** is a *separate capture-depth/workflow measure*. It describes the form of preserved research evidence and is not an automatic conversion from A–D: an unlicensed Git source may have P4-quality immutable version identifiers while still being cataloged as C, and a legitimately preserved unversioned file can be A without being P4.

**Do not bulk-convert historical A–D catalog codes into P0–P4.** Any future machine-readable capture-depth register should use its own field or table, with explicit evidence and timestamps. This preserves the meaning of existing records.

## Preservation levels

**P0 — Pointer only**
URL and metadata. Temporary discovery state.

**P1 — Verified metadata**
URL, title, author/community, publication date when available, retrieval timestamp, platform, source type, and research notes.

**P2 — Research capture**
P1 plus a lawful research excerpt, structured notes, screenshots when available and appropriate, and/or captured metadata sufficient to document the observed state.

**P3 — Local artifact**
A locally stored copy when redistribution and repository storage are permitted, such as an openly licensed file, public-domain artifact, user-supplied research file, or source whose license explicitly permits archival redistribution. Record license and retrieval date.

**P4 — Versioned primary artifact**
For GitHub or other versioned sources, preserve exact commit/blob identifiers, relevant paths, license, and retrieval date. If licensing permits, store a research copy. Otherwise retain the immutable upstream identifier and analytical record.

## Copyright and ethical constraint

Do not mirror entire copyrighted articles, paywalled posts, private-community content, or personal material merely because it is technically accessible.

For such sources, preserve metadata, provenance, concise research excerpts within applicable limits, analytical notes, and screenshots only where appropriate for research documentation.

The archive should preserve evidence without turning Attractomancy into an unauthorized republication service.

## Screenshots

Screenshots are particularly useful for:

- ephemeral social posts;
- formatting-dependent prompts;
- symbolic layouts;
- diagrams;
- deleted/edited-post risk;
- interfaces where text extraction loses structure;
- proof that an artifact existed in the observed form.

Every screenshot should have a sidecar metadata record containing source URL, UTC retrieval time, platform, source ID, description, and capture scope.

A screenshot does not replace text metadata or a source URL.

## Hashing

Locally stored artifacts should receive SHA-256 hashes when practical. Hashes establish that the research copy has not silently changed after collection.

## GitHub sources

Record repository owner/name, file path, exact commit SHA or blob SHA when possible, default branch, retrieval time, and license.

Prefer immutable commit URLs over branch-head URLs in research notes.

## Translation

Never replace an original-language artifact with its translation. Preserve the original as primary evidence and treat translations as derivatives under the multilingual policy.

## Deletion checks

High-value sources should eventually be rechecked periodically. If a source disappears:

- do not erase its catalog entry;
- mark upstream status as unavailable;
- preserve the last verified timestamp;
- retain lawful local research evidence;
- record the date disappearance was detected.

## Repository layout

Recommended structure:

`references/archive/<source_id>/metadata.md`
`references/archive/<source_id>/notes.md`
`references/archive/<source_id>/captures/`
`references/archive/<source_id>/artifacts/`

Not every source requires every directory.

## Priority

Preservation effort should be proportional to both research value and disappearance risk.

Highest priority:

- original prompt/incantation artifacts;
- detailed procedures;
- rare community documents;
- sources with distinctive symbolic formatting;
- small personal sites;
- posts repeatedly cited by a community;
- documents that appear to establish terminology or lineage;
- material already known to have moved or disappeared elsewhere.

Discovery can remain broad. Preservation should become progressively deeper as a source's importance becomes clearer.
