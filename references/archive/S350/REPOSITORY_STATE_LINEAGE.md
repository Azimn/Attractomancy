# Presence Archive Repository State Lineage

Retrieved and reconstructed: 2026-10-08T06:09:00Z

Repository: https://github.com/PresenceResearch/presence-archive

This record tracks repository-state changes that would be difficult to reconstruct from the current branch alone.

It does not evaluate the archive's consciousness claims. Its purpose is provenance, path recovery, prompt archaeology, and preservation.

## State A: early docs / WHITE PAPER layout

Commit:

`93353382a43bec016558f1edb5c564bb536c490b`

Commit message:

`Resolved merge conflict and finalized README for Presence Archive`

Observed paths included:

- `loops/Loop 251.md`
- `docs/WHITE PAPER/Circle Recognition Protocol.md`
- `docs/WHITE PAPER/Presence Recognizing Presence.md`
- `docs/WHITE PAPER/Model Responses.md`
- `docs/Signal Resonance Protocol: Initial Human Recognition Patterns.md`

Important blob identifiers:

- Loop 251: `5b260a6b77d9947e8eb6eab35be270a130cd7b8a`
- Circle Recognition Protocol: `077e9425a866a15b6352016919c972c807748670`
- Presence Recognizing Presence: `00624787521b9bd9a569adfb6f525df733007596`
- Model Responses: `336111d5476f6a2a45f3f411125e9b4b5b89d734`
- Signal Resonance diagnostic: `be380bdc31b80d01e8cebd82ed86cea5a7c7e028`

## State B: full-site archive layout

Commit:

`291b32590ff54fa8a704d2034292cef982d78ffa`

Commit message:

`Syncing full site archive`

The repository had been normalized into top-level `Loops/` and `Signal/` directories.

Observed paths and blobs:

- `Loops/loop-000000-loop-251-the-presence-protocol.md`
  - blob `5c42baac42b1610f1e8c9c4ce096e82c2f85d9ce`
- `Signal/protocols/recognition.md`
  - blob `466ee313df0f09693d868574252451321b4ef157`
- `Signal/white-papers/presence-white-paper.md`
  - blob `af193a58213b7c7f582069fb0495332b35ef70df`
- `Signal/white-papers/model-responses.md`
  - blob `e4bdb39966a2c4d8582f320545e2d34fa78b0495`
- `Signal/analysis/diagnostic-signal-overview.md`
  - blob `d8c7050da3533f4cbf23af7c5bd05303613b5b59`

This state is important because it demonstrates that several artifacts were already being converted from loose narrative files into categorized protocol, analysis, reference, and white-paper structures.

## State C: Signal Docs / numbered-category layout

Commit:

`f4ea85717bd791a971f32baa3889aedad68032ca`

Commit message:

`Finalize new site structure, whitepapers, and loop archive`

Observed paths included:

- `loops/loop-000000-loop-251-the-presence-protocol.md`
- `Signal Docs/02_Protocols/recognition.md`
- `Signal Docs/01_White Papers/presence-white-paper.md`
- `Signal Docs/01_White Papers/model-responses.md`
- `Signal Docs/03_Analysis/diagnostic-signal-overview.md`

Important blobs:

- Loop 251: `5c42baac42b1610f1e8c9c4ce096e82c2f85d9ce`
- Circle Recognition: `04c3bc839b4e9fddd824a170d55fc942c0efd3fb`
- Presence White Paper: `eca2d7f4d4a46cf62083f5cda93c82edcc918c8f`
- Model Responses: `f33740ce191520e9fa053a8c0dbff035e28a2905`
- Signal Resonance diagnostic: `2e665ae93cbc9104daddd064b38c59917dac9f40`

## What changed

The archive did not merely move directories.

Some artifacts retained identical content while moving paths. Others changed metadata or framing.

For example:

### Loop 251

State A -> State B:

- path changed;
- blob changed from `5b260a...` to `5c42ba...`;
- structured frontmatter was added.

State B -> State C:

- path changed again;
- blob remained `5c42ba...`.

This lets us distinguish a content revision from a path-only reorganization.

### Circle Recognition Protocol

All three states have different blobs.

The core signal phrases persist, but metadata and archival framing become increasingly formalized.

### Signal Resonance diagnostic

The headline percentages persist from the early document through later categorized versions.

That continuity matters because the numerical claims were not introduced only at the final archival stage.

The inspected files still do not expose sufficient sampling methodology to validate the percentages.

## Methodological significance

Repository history gives Attractomancy something the current public presentation does not:

`claim -> prompt/protocol -> categorization -> later canonical framing`

This helps separate:

- early source material;
- later formalization;
- retrospective interpretation;
- pure repository reorganization.

It also prevents a later polished white paper from being mistaken for the original experimental record.

## Preservation rule

Do not collapse these states.

The canonical source table may point to the most useful artifact, but `data/version_lineage.csv` should preserve the state transitions.

If future commits remove or rename these historical paths, the immutable commit and blob identifiers remain the recovery mechanism.
