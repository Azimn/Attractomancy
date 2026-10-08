# Reproducible Procedure Index Schema

`data/reproducible_procedure_index.csv` is a collection aid for primary interventions that are described precisely enough to reproduce later.

It is **not** an experimental-results table.

## Fields

- `procedure_id`: stable Attractomancy procedure identifier.
- `source_id`: source-catalog ID.
- `name`: source-native or neutral procedure name.
- `family`: broad procedure family.
- `exact_prompt_or_steps_available`: yes / partial / no.
- `versioned`: yes / no / unclear.
- `cross_model_claim`: yes / no / unclear.
- `frame_or_ablation_present`: yes / no / partial.
- `preservation_state`: pointer / metadata / local snapshot / historical git.
- `future_replication_priority`: critical / high / medium.
- `notes`: concise collection note.

## Inclusion rule

A source enters this index only when the public artifact provides enough operational detail to reconstruct at least the core intervention.

Narrative descriptions such as "we used resonance" are not enough.

## Interpretation rule

Inclusion does not validate the source's claimed mechanism or outcome.

The index exists so later work can compare source-native procedures with neutral rewrites, component ablations, and engineering controls.
