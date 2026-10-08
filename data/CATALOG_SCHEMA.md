# Source Catalog Schema

The canonical research index is `data/source_catalog.csv`. CSV is used as the primary catalog because it is directly readable by GitHub, Excel, Google Sheets, LibreOffice, Python, R, and database import tools while remaining diffable and version-controlled.

Each row represents one recoverable source, artifact, community, repository, paper, thread, guide, or unresolved lead.

## Fields

- `id`: stable Attractomancy identifier. Never reuse an ID.
- `retrieved_at_utc`: ISO 8601 UTC timestamp for the retrieval or verification event recorded in this row.
- `source_date`: publication, post, file, or release date when known.
- `title`: source title or concise identifying label.
- `platform`: GitHub, Reddit, Google Docs, arXiv, journal, Substack, Hugging Face, local research copy, etc.
- `source_type`: artifact, repository, community, thread, guide, paper, dataset, post, or lead.
- `author_or_community`: author, handle, subreddit, organization, or source community when known.
- `url`: canonical or best currently recoverable public URL.
- `status`: recovered, verified, lead, unavailable, superseded, or local-only.
- `preservation_level`: A through D according to `references/README.md`.
- `local_artifact`: local filename when a research copy exists.
- `primary_domain`: prompt-engineering, persona-continuity, companion-practice, consciousness-discourse, human-AI-research, anthropology, HCI, etc.
- `technique_tags`: Attractomancy technique codes from `references/TECHNIQUE_TAXONOMY.md`.
- `phenomenon_tags`: descriptive social or cultural tags such as companion, awakening, recursion, spirituality, attachment, migration, drift, grief, jailbreak, or ritual.
- `evidence_class`: primary-intervention, community-practice, community-discourse, technical-architecture, empirical-research, theoretical-research, or unresolved-lead.
- `confidence`: high, medium, or low confidence in the record's identification and relevance.
- `notes`: concise research note. Claims made by a source are recorded as source claims, not as established facts.

## Preservation-code compatibility

The `preservation_level` column retains the legacy A–D codes defined in `references/README.md`. The P0–P4 taxonomy in `docs/SOURCE_PRESERVATION_POLICY.md` measures separate preservation depth and must not be inserted into this column. P4 immutable/versioned evidence is not necessarily a publicly redistributable A-level source.

A `local_artifact` value may identify an analytic metadata note, historical-path index, or rights-cleared full copy; it is **not** proof that source content itself was mirrored. Confirm the type and license in the referenced record.

Stable source IDs are never reused. Duplicate URLs may occur when one page acts as evidence for distinct source-level or artifact-level records; document their review in `data/duplicate_url_review.csv` rather than silently deleting or merging source IDs.

## Timestamp policy

The catalog records when Attractomancy retrieved or verified a source, not merely when the source was originally published. If a source is revisited after a major edit, deletion, migration, or version change, add a new retrieval event to the retrieval log and update the catalog row's latest verification timestamp.

## Version and disappearance tracking

A URL is not treated as permanent. For volatile sources, record immutable commit hashes, file hashes, archive URLs, post IDs, document IDs, version numbers, or other stable identifiers when available.

## Public-repository preservation

The public repository should not mirror full copyrighted artifacts merely because they might disappear. When redistribution status is unclear, keep the catalog record, provenance, hashes, lawful excerpts, analytical notes, and archival references. Full research copies can remain outside the public mirror until redistribution rights are established.
