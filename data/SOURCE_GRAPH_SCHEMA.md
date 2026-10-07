# Source Graph Schema

Attractomancy uses `data/source_catalog.csv` as the node table and `data/source_graph_edges.csv` as the edge table.

The graph records **documented relationships between sources**, not inferred similarity.

## Edge fields

- `edge_id`: stable edge identifier.
- `retrieved_at_utc`: when the relationship was verified.
- `from_id`: source-catalog ID of the linking or evidentiary source.
- `to_id`: source-catalog ID of the linked or related source.
- `relation`: controlled relationship label.
- `evidence_source_id`: source whose content directly supports the edge, normally the same as `from_id`.
- `confidence`: high, medium, or low.
- `notes`: concise explanation of why the edge exists.

## Relation vocabulary

- `links_to`: source directly links the target.
- `mirror_of`: source is a mirror/republication of the target.
- `same_project`: sources are explicitly presented as parts of the same named project.
- `same_framework`: sources are explicitly parts of one named framework/method.
- `requires_reading`: source tells participants to read/load the target before proceeding.
- `cross_posts_to`: source explicitly identifies another platform as a cross-posting/embassy channel.
- `names_collaborator`: source explicitly identifies the target source/project or its author as collaborator/peer.
- `inspired_by`: source explicitly credits the target source/project for an idea, licensing choice, or method.
- `uses_seed_from`: experiment/report uses a seed or protocol documented in the target.
- `documents_evolution_of`: later source explicitly continues or revises an earlier source/procedure.
- `hosts_component_of`: source is an index/container for the target artifact.
- `community_bridge`: source explicitly connects two otherwise distinct communities/projects.
- `preservation_mirror`: mirror created to preserve or make another source machine-readable.
- `independently_confirms`: a separate primary or external record corroborates a person, pair, project, date, artifact, or relationship asserted by another source without necessarily linking to it.

## Evidence rule

Similarity of terminology is **not** enough to create an edge.

If two communities both use words such as `glyph`, `resonance`, or `soul` but no documented link has been found, they remain unconnected nodes until evidence appears.
