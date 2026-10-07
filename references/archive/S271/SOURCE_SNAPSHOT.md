# Preserved Source Snapshot: S271

Source repository: https://github.com/tantanpq/PAI
Retrieved: 2026-10-07T19:30:38Z
Upstream branch: main
README blob SHA: 4e6bd47c7a83acc9e1aa1d7ede0cae5c5de3b35b
LICENSE blob SHA: 229618b83586aa15f99c9abefcdf240e5800063b

The upstream repository explicitly licenses original public software under Apache-2.0 and original public non-code material under CC BY 4.0. This snapshot preserves the observed README and licensing statement for research continuity.

## Preserved README

# PAI

## Personal Assistant Intelligence

**PAI is a user-owned intelligence project for continuity, useful autonomy, reusable capability, and verifiable outcomes.**

The long-term goal is not another chatbot that starts over every time a conversation changes. PAI is being built toward an assistant that can preserve a user's trajectory, understand current reality, continue meaningful work across time, learn from evidence, and act within explicit authority while keeping important decisions with the user.

> Help people spend less effort remembering, reconstructing, coordinating and rechecking work, and gain more time, capability, useful assets and autonomy.

This repository is the **public Open Foundation** of PAI. It is intentionally smaller than the complete private PAI system.

- [`VISION.md`](VISION.md) — why PAI exists, its principles and long-term product direction.
- [`FOUNDER.md`](FOUNDER.md) — founder perspective and project intent.
- [`PORTFOLIO.md`](PORTFOLIO.md) — what is public and usable now.
- [`ROADMAP.md`](ROADMAP.md) — release-oriented public milestones and evidence gates.

## What PAI is

PAI stands for **Personal Assistant Intelligence**.

A mature PAI should be able to preserve continuity across conversations, tools, devices and changing model providers; keep a grounded picture of goals and decisions; resume long-running objectives; verify results against evidence; learn from qualified outcomes; reuse capabilities; and know when to **act, ask, wait or surface** based on authority and uncertainty.

PAI is not intended to be one permanent model. Models, tools and executors are replaceable components. The durable value is the continuity, evidence, learning, capability and authority structure around them.

## Why PAI exists

Modern AI can generate impressive work, but the surrounding user experience is still fragmented:

- useful context disappears between chats and tools;
- users repeatedly restate goals and reconstruct old decisions;
- long-running work becomes tied to one session or provider;
- generated output is often confused with a verified result;
- automation can become hard to resume, replay or trust;
- greater autonomy can arrive without equally clear ownership and effect boundaries.

PAI is exploring a different path: **user-owned continuity + evidence-backed work + bounded autonomy**.

## Product map

| Horizon | Surface | Purpose | Current public state |
| --- | --- | --- | --- |
| **Available now** | Context Kit | bounded context capsules, metadata-first exact-JIT retrieval and protected continuity carriers | **0.2.0 RELEASE CANDIDATE / 0.1.0 TAGGED** |
| **Available now** | W_Flow Core | provider-neutral replayable work-loop and state semantics | **0.1.0 PUBLIC_FOUNDATION** |
| **Available now** | SimLab Core | deterministic synthetic verification and minimized counterexamples | **0.1.0 PUBLIC PILOT / PILOT_ONLY** |
| **Building toward** | PAI Personal | user-owned continuity and productive assistance across long-running work | **not publicly released as a supported product** |
| **Building toward** | PAI Assurance | evidence-backed verification for AI-assisted engineering and operations | **public methods exist; broader commercial maturity is evidence-gated** |
| **Longer horizon** | PAI Work / Group, domain intelligence, business capabilities, richer local execution | extend continuity and useful capability into shared and specialized work | **future / dependency-gated** |

Roadmap presence is not a readiness claim. Future directions remain bounded by evidence, safety, authority and product value.

## Problems this repository is trying to solve

| Problem | Public PAI response | Boundary |
| --- | --- | --- |
| AI work loses context between chats, tools and providers | deterministic source resolution, bounded context packaging and source-aware resume patterns | public patterns do not include private Personal memory, proprietary retrieval/ranking or hosted-chat capture claims |
| Long-running AI work becomes fragile, non-replayable or dependent on one provider | provider-neutral W_Flow contracts, resumable state, replay/idempotency and explicit local-blocker/authority semantics | W_Flow is not PAI's private Program/Claim/Farm control plane |
| Green tests are mistaken for proof that the right thing shipped | evidence-first assurance, PASS/LIVE/DONE separation, release-scope integrity and reachable-path policy checks | no certification, warranty, formal proof or zero-defect claim |
| AI-generated tests miss failure modes or produce unreproducible failures | deterministic SimLab scenarios, explicit PASS/FAIL/UNKNOWN, known-bad mutants and minimized reproducible counterexamples | public SimLab is synthetic-only; real OS/service/provider claims still require real canary evidence |
| Public releases drift beyond their authorized scope | provenance, release contracts, bounded publication classes and independent integrity checks | private/core/customer/security-sensitive material remains excluded |
| Teams want reusable AI engineering patterns without surrendering their private implementation | small Skills, workflows, Packs and package surfaces with explicit licenses and protected boundaries | the public foundation is not a source dump of `pai-core-private` |

## Public capability families

PAI is currently converging around three public capability families:

- **Context & Continuity** — deterministic, bounded context packaging and source-aware resume patterns.
- **W_Flow** — reusable, resumable work-loop specifications and verification-friendly workflows.
- **Assurance & SimLab** — evidence-first verification patterns, deterministic synthetic test surfaces, minimized counterexamples, and reproducible failure analysis.

The public repository also hosts reusable **Skills, Tools, Packs, Labs, examples, and documentation** when they pass the public release boundary.

## Start here

- [`VISION.md`](VISION.md) — understand the project thesis before the internals.
- [`capabilities/context/README.md`](capabilities/context/README.md) — Context Kit 0.2.0 candidate, deterministic capsules, Retrieval Economy and Continuity Carrier.
- [`capabilities/wflow/README.md`](capabilities/wflow/README.md) — W_Flow Core 0.1.0, provider-neutral replayable work-loop semantics.
- [`capabilities/simlab/README.md`](capabilities/simlab/README.md) — SimLab Core 0.1.0 public pilot for deterministic synthetic verification.
- [`docs/QUICKSTART.md`](docs/QUICKSTART.md) — use the current Open Foundation in a few bounded steps.
- [`PORTFOLIO.md`](PORTFOLIO.md) — current public capability and portfolio map.
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — how public PAI relates to the protected private core.
- [`docs/PUBLIC_RELEASE_POLICY.md`](docs/PUBLIC_RELEASE_POLICY.md) — what is allowed to become public and how releases are qualified.
- [`docs/BENCHMARKS.md`](docs/BENCHMARKS.md) — current verification baselines and benchmark gates.
- [`LICENSE.md`](LICENSE.md) — Apache-2.0 software scope, CC-BY-4.0 public-content scope, trademark and protected-core boundaries.
- [`workflows/community-assurance-baseline.md`](workflows/community-assurance-baseline.md) — a reusable evidence-first assurance workflow.
- [`runbooks/source-only-resume.md`](runbooks/source-only-resume.md) — resume durable work without treating chat memory as authority.
- [`skills/deterministic-source-resolution.md`](skills/deterministic-source-resolution.md) — resolve durable sources without promoting stale hints into truth.
- [`skills/reachable-path-policy-integrity.md`](skills/reachable-path-policy-integrity.md) — verify that every route to a protected effect enforces the same invariant.
- [`skills/release-scope-integrity.md`](skills/release-scope-integrity.md) — verify that a release contains only the change it was supposed to contain.

## Public repository layout

```text
PAI/
├── foundation/      # public contracts, standards and conformance guidance
├── capabilities/    # qualified capability families
├── skills/          # reusable bounded skill recipes
├── wflows/          # reusable work-loop specifications
├── tools/           # public tools when separately licensed and release-qualified
├── packs/           # versioned distributions and examples
├── labs/            # synthetic fixtures and experiments with explicit maturity
├── products/        # public product-facing surfaces
├── workflows/       # generic operational workflows
├── runbooks/        # bounded operational guides
├── examples/        # independently usable examples
└── docs/            # architecture, release and trust documentation
```

## Open Foundation, not a source dump

Public PAI is curated. A useful internal result does **not** automatically become public code.

Public candidates must be useful on their own, bounded by evidence, sanitized, rights-cleared, versionable, testable, and safe to separate from the protected implementation.

Protected material stays private, including deep PAI Mind/Chief internals, proprietary continuity/routing intelligence, private evaluation and failure corpora, sensitive authority/execution machinery, customer/private evidence, credentials, trust roots, and private/sovereign execution details.

## Evidence-first release discipline

PAI keeps these states distinct:

`planned → materialized → running → PASS/FAIL → released/live → terminal outcome`

A passing test is not automatically a production claim. A public claim must remain narrower than or equal to the evidence behind it.

## Licensing

The public licensing strategy is:

- **Apache-2.0** for original PAI software intentionally published as reusable software;
- **CC BY 4.0** for original public non-code material such as documentation, Skills, workflows/W_Flows, patterns and synthetic educational content;
- **trademarks reserved**;
- third-party/migrated assets keep their exact upstream terms.

See [`LICENSE.md`](LICENSE.md) for scope and exclusions. A future change to this licensing strategy remains a founder/legal gate.

## Reliability evidence archive

Earlier public reliability work remains available at [`tantanpq/pai-reliability-evidence`](https://github.com/tantanpq/pai-reliability-evidence).

That repository is treated as a linked evidence/provenance archive while reusable material is progressively curated into this repository. Existing evidence and failure history are preserved rather than silently rewritten.

## Current maturity

This repository is in **public foundation bootstrap with two public foundation packages and one executable public pilot released**. The goal is not to publish everything PAI has ever built. The goal is to publish a small set of complete, useful, independently understandable capability surfaces and expand only from verified results.

**Context Kit 0.1.0** remains the tagged public executable Open Foundation release. The compatible **0.2.0 release candidate** keeps its source-locked compiler API and adds metadata-first exact-JIT retrieval, exact archive/hash recovery, stable-ID lifecycle convergence, protected continuity carriers, and a two-axis economy/continuity benchmark. The distribution is the source package in this repository; no npm-registry publication is claimed.

**W_Flow Core 0.1.0** is the second public executable package. Five recovered core artifacts are source-hash pinned; exact PR and public-main revisions passed the original 8/8 core suite, a 1,000-iteration deterministic replay benchmark, independent public-boundary QA, wheel build and clean virtualenv installation/use. W_Flow declares work-loop semantics only: it is not an executor, scheduler, Claim service or authority system. No PyPI publication is claimed.

**SimLab Core 0.1.0** is a `PUBLIC PILOT / PILOT_ONLY` executable surface. Exact PR and public-main revisions passed 6/6 public tests, a 1,000-replay deterministic benchmark with one digest, known-good `PASS`, known-bad mutant `FAIL`, missing-evidence `UNKNOWN`, counterexample minimization from 3 events to 2, independent public-boundary QA, `npm pack`, protected-R7 exclusion checks, and clean-consumer use. The public package is synthetic-only and intentionally does not contain protected R7 evaluator/property intelligence. No npm-registry publication is claimed, and no general production-platform maturity is claimed.

## Claim boundary

PAI is not a certification authority, security warranty, uptime guarantee, or claim of zero defects.

Its public engineering goal is more concrete: **make useful AI work resumable, reusable, and easier to verify against actual evidence while keeping the user in control.**


## Preserved License

# PAI public licensing

This repository uses a scoped licensing model so the Open Foundation can be genuinely reusable without licensing the protected PAI core by accident.

## Selected license scopes

| Material | License | Scope |
| --- | --- | --- |
| Original PAI software intentionally published in this repository | **Apache License 2.0** (`Apache-2.0`) | Public software source, package code, scripts, schemas or executable examples that are published as reusable software and do not declare a different license. |
| Original PAI public non-code material | **Creative Commons Attribution 4.0 International** (`CC-BY-4.0`) | Documentation, workflows, W_Flows/specifications, runbooks, Skills, patterns, case-study abstractions, synthetic educational material and other reusable authored content, unless a file or provenance record declares different terms. |
| Trademarks, names and branding | **Reserved** | No software/content license grants trademark, product-name, logo or endorsement rights except nominative use allowed by law and the underlying license. |
| Third-party or migrated material | **Upstream terms control** | The exact source/provenance record and per-file notice control. PAI cannot grant rights it does not own. |

## Apache-2.0 software rule

Published software that uses this scope should carry `SPDX-License-Identifier: Apache-2.0` where practical and must preserve required notices. Apache-2.0 was selected because it permits commercial and proprietary downstream use while also providing explicit patent-license and patent-termination language. It does **not** require disclosure of the separate private PAI core.

Official license text: <https://www.apache.org/licenses/LICENSE-2.0>

## CC-BY-4.0 content rule

Original public non-code material under this scope may be copied and adapted with attribution under CC BY 4.0. Attribution should identify PAI / the repository and retain any source or provenance notice supplied with the asset.

Official license text: <https://creativecommons.org/licenses/by/4.0/legalcode>

## Explicitly excluded

These public license scopes do not include, unless separately and explicitly released:

- `pai-core-private` or any unpublished PAI source;
- private PAI Mind/Chief implementation, proprietary continuity/routing/adaptation intelligence or authority machinery;
- customer, company, personal or otherwise private data/evidence;
- protected evaluation/failure corpora, proprietary repair intelligence or private benchmark material;
- credentials, trust roots or security-sensitive internals;
- third-party material beyond rights actually held;
- trademarks, logos or branding rights.

## Precedence

1. A specific per-file or per-package license/notice wins.
2. A catalog/provenance record that preserves an upstream license wins for migrated material.
3. Otherwise, the scoped defaults above apply only to material intentionally published in this public repository.

Changing the software or public-content license strategy is a founder/legal `HUMAN_GATE`, not an automated PATCH release.

