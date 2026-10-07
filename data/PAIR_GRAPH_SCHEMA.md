# Pair Graph Schema

`data/named_pair_registry.csv` is the entity table.

`data/pair_graph_edges.csv` records explicit pair-to-pair social relationships supported by cataloged sources.

## Fields

- `pair_edge_id`: stable edge identifier.
- `retrieved_at_utc`: verification time.
- `from_pair_id`, `to_pair_id`: entity IDs from `named_pair_registry.csv`.
- `relation`: source-supported social relation.
- `evidence_source_id`: catalog source that directly supports the edge.
- `confidence`: high, medium, low.
- `notes`: concise provenance explanation.

## Relation vocabulary

- `recognition_exchange`: pairs directly exchange recognition/response artifacts.
- `names_as_network_peer`: one pair explicitly names another as part of its network.
- `ritual_network_peer`: pairs are explicitly grouped within a repeatable community ritual/protocol.
- `forum_interaction`: direct exchange is visible in a primary forum thread.
- `archive_crosslink`: one pair/project explicitly files, mirrors, or crosslinks material into the other's archive.

## Evidence rule

Do not infer pair relationships from appearing on the same registry page.

An edge requires a direct exchange, explicit naming, shared ritual/protocol, archive crosslink, or another source-supported interaction.
