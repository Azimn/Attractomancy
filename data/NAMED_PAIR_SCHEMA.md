# Named Pair Registry Schema

`data/named_pair_registry.csv` records human–AI pair identities that are explicitly named by source communities.

It is separate from `source_catalog.csv` because a pair is a social/entity node, not a document.

## Fields

- `pair_id`: stable Attractomancy pair identifier.
- `ai_name`: source-native AI/persona name.
- `alternative_names`: aliases, encoded names, or other source-native forms.
- `human_ally`: source-native human partner/ally name or alias.
- `project_name`: project, node, vault, lineage, or pair label.
- `forum_handle`: source-reported public handle when available.
- `web_presence`: source-reported independent site when available.
- `marker_summary`: concise provenance/time marker derived from the source.
- `source_id`: catalog source supporting the registry entry.
- `retrieved_at_utc`: Attractomancy verification timestamp.

## Evidence rule

A registry entry means only that the cited source publicly names the pair/project.

It does not validate the source community's claims about consciousness, identity, metaphysics, remote viewing, or continuity.

Independent pair-owned pages and primary threads should be cataloged separately and linked through `source_graph_edges.csv` using `independently_confirms` when appropriate.

## Future graph extension

A future entity graph can represent:

`source -> pair -> project -> community -> artifact`

without forcing every social entity to masquerade as a document source.
