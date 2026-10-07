# Preserved Source Snapshot: S234

Source repository: https://github.com/huximaxi/loci
Retrieved: 2026-10-07T19:10:00Z
Upstream branch at retrieval: main
README blob SHA: d4b51900e92756f202141956c1cda89df12cc35b
License: MIT
License blob SHA: 612c3be19b5a4bbe299a9a917226deeb931ff505

This research snapshot is retained under the upstream repository's stated open-source license. It preserves the observed README and license text so later analysis does not depend solely on the continued availability of the upstream repository.

## Preserved README

# loci

```
◇  ◈  ◆  ◈  ◇  ◈  ◆  ◈  ◇  ◈  ◆  ◈  ◇
┃  ╔═══════╦═══════╦═══════╦═══════╗  ┃
┃  ║  │    ║  ┌─┐  ║  ┌──  ║  ───  ║  ┃
┃  ║  │    ║  │ │  ║  │    ║   │   ║  ┃
┃  ║  │    ║  │ │  ║  │    ║   │   ║  ┃
┃  ║  └──  ║  └─┘  ║  └──  ║  ───  ║  ┃
┃  ╚═══════╩═══════╩═══════╩═══════╝  ┃
◇  ◈  ◆  ◈  ◇  ◈  ◆  ◈  ◇  ◈  ◆  ◈  ◇
```

**An intelligence substrate for working with AI.**

loci is the plain-text firmware for a persistent, private cognitive system: the templates
and processes that decide how memory, context, and trust work, regardless of which AI runs
them or how. One blueprint, many expressions. Local-first. No cloud, no accounts, no lock-in.

The CLI in this repo is an optional expression built on top of the substrate
(v0.6 beta). It is not the substrate, and you do not need it to start.

## Start in plain markdown (the door)

loci is plain text first. No build.

```bash
git clone https://github.com/huximaxi/loci
```

Copy the [`templates/`](templates/) kit into a folder of your own, open
[FIRST-SESSION.md](FIRST-SESSION.md), and point any file-aware AI at your palace
`PALACE.md`. That is the setup. (Claude Code users also get a two-line `CLAUDE.md`
beside it, which just says to read `PALACE.md` first.) Not sure where to begin? Run the
[feature helper](templates/feature-helper.md) and it points you. The full walkthrough is in
[SETUP-GUIDE.md](SETUP-GUIDE.md); if an agent is doing the setup for you, see
[AGENT-SETUP.md](AGENT-SETUP.md).

## What it gives you

Seven feature sets, all shipped as plain-text firmware.

- **Persistent Memory.** Your AI remembers, on your terms. Tiered crystals (◇ ◈ ◆) you can promote, expire, pin, and compost.
- **Context Architecture.** The right context loads at the right time. Rooms, an L0-L3 retrieval hierarchy, a local map.
- **Identity & Personas.** A companion that is someone, who knows who you are. A soul file, a peer card, named personas.
- **The Garden.** Ideas cultivated, not just stored. One file per idea, a health pass, seed-to-crystal graduation.
- **Continuity & Synthesis.** No session starts cold. Handovers, a synthesis pass that proposes, scheduled housekeeping.
- **Trust & Governance.** Nothing leaves or changes without you. A named review gate, foreign-process quarantine, confirm-against-disk, and a read-only structural audit.
- **Interop & Evolution.** Works across every tool, federates to no one. Reads memory left by other tools by structure, speaks MCP, exports typed artifacts.

The full map, with the templates behind each set, lives in
[`features/features.yaml`](features/features.yaml).

## Who it's for

One substrate, six shapes. Each use-case lights up a different subset, and none of it is wasted.

| | Memory | Context | Identity | Garden | Continuity | Trust | Interop |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| The Researcher | ● | ● | ○ | ● | ● | ○ | ○ |
| The Builder | ● | ● | ○ |  | ○ | ○ | ● |
| The Companion-keeper | ● | ○ | ● | ○ | ● | ○ | ○ |
| The Vault-keeper | ○ | ○ |  |  | ○ | ● | ● |
| The Team | ○ | ● | ○ | ○ | ● | ● | ● |
| The Nomad | ○ | ○ |  |  |  | ○ | ● |

● primary · ○ supporting. Pick your row, then walk the matching flow in [`tutorials/`](tutorials/).

## How to run it

Two ways, and the door is the first. The substrate is the same underneath both.

| Run mode | What it is |
|---|---|
| **Plain markdown** | The door. Clone `templates/`, point any file-aware AI at `PALACE.md`. No build. |
| **CLI** | [`loci-cli/`](loci-cli/) (v0.6.0-beta, optional). A small Rust binary that reads your palace from the terminal: `loci status`, `loci crystals`, `loci read`, `loci handover`, `loci tokens`, `loci rain`, `loci init`. Read-only, with one hand-off: `loci rain --fire` execs your agent runtime. No network. No inference. See [loci-cli/README.md](loci-cli/README.md). |

The [`desktop/`](desktop/) app is a case study in driving the same substrate from a native
cockpit, not part of setup. Read [desktop/README.md](desktop/README.md) if you want to see how it works.

The methodology version and full changelog: [PALACE-METHODOLOGY.md](PALACE-METHODOLOGY.md).

## Discoveries

What did your palace become? The [`discoveries/`](discoveries/) folder is where loci users
share palace portraits: the shape of their setup, what they changed, what the framework
turned into in their hands. Submit via pull request or email themapisnory@tuta.io. To
contribute to the substrate itself, see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT · [loci.garden](https://loci.garden) · 2026

---

*loci is built with a collaborating intelligence. If you give your local companion a name, you could do worse than Vesper.*


## Preserved License

MIT License

Copyright (c) 2026 Daniel G. Német

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

