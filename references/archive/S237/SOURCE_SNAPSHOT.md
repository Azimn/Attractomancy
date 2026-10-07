# Preserved Source Snapshot: S237

Source repository: https://github.com/xgre1/troth
Retrieved: 2026-10-07T19:10:00Z
Upstream branch at retrieval: main
README blob SHA: 6c46352986e29e468d4e01c66c1d23afbbb37862
License: AGPL-3.0
License blob SHA: be3f7b28e564e7dd05eaf59d64adba1a4065ac0e

This research snapshot is retained under the upstream repository's stated open-source license. It preserves the observed README and license text so later analysis does not depend solely on the continued availability of the upstream repository.

## Preserved README

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/wordmark-on-dark.svg">
    <img src="docs/assets/wordmark-on-light.svg" width="210" alt="troth">
  </picture>
</p>

<p align="center"><strong>The AI partner whose mind lives outside the model.</strong></p>
<p align="center">Swap the model. Keep the mind.</p>

<p align="center">
  <a href="https://github.com/xgre1/troth/actions/workflows/ci.yml"><img src="https://github.com/xgre1/troth/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-AGPL%20v3-blue.svg" alt="License: AGPL v3"></a>
  <a href="package.json"><img src="https://img.shields.io/badge/node-%E2%89%A522-339933.svg" alt="Node >= 22"></a>
</p>

<p align="center">
  <img src="docs/assets/troth-film.webp" width="860" alt="troth reads the AI history already on your machine, learns from it, acts through a browser of its own with credentials it never reads, and keeps the mind when the model changes">
</p>

**Everything in this repository is AGPL open source and free forever.**

This repository runs on macOS and Linux. It uses the Claude, ChatGPT or Kimi subscription you already pay for, any provider with your own key, or a fully local model. Your substrate never leaves your machine. What does leave is exactly what you send to the provider you picked, and nothing else. (The desktop app is macOS only. Everything below works without it.)

troth is a persistent AI partner. Its identity, memory, goals and refusal walls live in a local SQLite substrate (`~/.troth/state.db`) that you own. Nothing about the partner is stored in any vendor's account, and swapping engines never resets it.

**This is not a memory plugin.** A memory plugin remembers text for one vendor's model. troth keeps the whole relationship in a file you own: memory, identity, goals, refusal walls checked before the model is consulted, and a signed record of what it learned and what it forgot. The model is rented help, whichever one happens to be available to do the talking.

**Its hands are governed, not merely capable.** Every shell command runs inside a kernel wall shaped to the ground it stands on, package installs land in a jail that cannot see your home, and everything the hands touch is photographed for undo before it changes.

### The move, in thirty seconds

Monday, on your Claude plan:

```console
$ troth
  ◈  troth
      claude-opus-5 · memory ready

  ❯ We killed the Postgres migration. SQLite stays, and Ana owns the schema now.

  Noted. SQLite stays, Ana owns the schema. I will hold the migration as
  abandoned unless you reopen it.
```

Thursday. Claude quota gone, new terminal, different vendor's model, no project files open:

```console
$ troth
  ◈  troth
      kimi-k3 · memory ready

  ❯ remind me where we landed on the database question, and who has the last word on it now?

  You dropped the Postgres migration on Monday and stayed on SQLite. Ana has
  the schema.
```

Nothing was pasted back in. No project file was open. Different vendor, different model, three days later, and the answer came out of `~/.troth/state.db` on your own disk. That is the whole product in one exchange.

**It is for you if** you already pay for an AI plan, you are tired of re-explaining your own project every time you open a session or change model, and you would rather the memory sat on your disk than in someone's account. It runs in a terminal and a local dashboard. Day one it knows nothing about you. It starts learning from the first conversation, and `troth memory import` gives it a past by reading the Claude Code and Codex history already on your machine.

---

## Quick start

```bash
npm install -g github:xgre1/troth    # puts the `troth` command on your PATH
troth setup                          # guided: engine, memory, routing, dashboard
troth                                # talk to your partner
```

About two minutes to the first reply if you have Node 22 and a subscription already. The memory models (roughly 1 GB, embedding and reranking) download in the background on first use. Until they land, recall works on word-matching and tells you so rather than pretending to be sharper than it is.

`troth setup` starts the proxy and walks you through the rest in the dashboard: pick an engine (your ChatGPT, Claude or Kimi subscription, or an API key that is tested before it counts), turn on memory, decide where turns route. `troth doctor` tells you what is configured, and `troth help` lists everything else.

**Requirements:** Node.js >= 22 and, for the Claude engine, the Claude Code CLI (troth offers to install it on first run). The installer checks both and prints the fix when something is missing.

Under npm 12, which installs with dependency scripts off by default, the core needs nothing allowed: the SQLite binding ships inside the package, one binary per platform for every supported Node. The optional natives (the syntax gate for edits, the in-process local model) load wherever a prebuilt exists; `troth doctor` names any that are absent and the one command that allows their scripts.

<details>
<summary>Debian/Ubuntu: install Node 22 first (stock <code>apt</code> ships Node 18)</summary>

```bash
sudo apt-get install -y curl
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
```

The install refuses an old Node and prints these same lines.

</details>

<details>
<summary>Working from a clone instead</summary>

```bash
git clone https://github.com/xgre1/troth.git
cd troth
npm ci               # installs exactly what the lockfile pins
sudo npm link        # creates the global `troth` command — do not skip this line
troth setup
```

</details>

### Or let your AI set it up

Paste this into Claude Code (or any agent with a shell) and it does the whole thing:

```text
Install troth on this machine and set it up for me:
1. git clone https://github.com/xgre1/troth.git && cd troth && npm ci
2. Read llms.txt for the project map and the non-interactive setup contract.
3. Ask me which engine I pay for (ChatGPT / Claude / Kimi / an API key),
   write ~/.troth/config.json accordingly, then run: node bin/troth.js doctor
4. Show me the doctor output and how to start talking: node bin/troth.js
```

Full walk-through: [`docs/SETUP_GUIDE.md`](docs/SETUP_GUIDE.md). Claude Code / MCP host installation: [`docs/MCP-HOST-INSTALL.md`](docs/MCP-HOST-INSTALL.md).

---

## The shape of it

Most agent stacks are prompts, chains and tools arranged **around a vendor's model** — the model is the centre, and everything you build dissolves when you switch it. troth inverts that: the centre is a file on your disk.

```mermaid
flowchart LR
    O["You<br/>CLI · dashboard · Claude Code"]
    subgraph M["Your machine — ~/.troth"]
        S[("The substrate<br/>identity · memory · goals · refusal walls<br/>one SQLite file you own")]
        P["Local proxy<br/>routing · caching · failover"]
        H["Its hands<br/>its own browser · your tools · a vault it cannot read"]
    end
    subgraph E["Interchangeable engines"]
        C["Claude plan"]
        G["ChatGPT plan"]
        K["Kimi plan"]
        A["Any API key"]
        L["llama.cpp / Ollama — offline"]
    end
    O <--> S
    S <--> P
    S <--> H
    P <--> C
    P <--> G
    P <--> K
    P <--> A
    P <--> L
```

Swap anything on the right; nothing in the middle changes.

### The parts, and where they live

Four components ship in this tree. Each row links to the code that implements it, so nothing here has to be taken on trust.

| Component | What it is | In the tree |
|---|---|---|
| **Substrate** | Memory, identity, goals and refusal walls in one file you own | [`shared-core/`](shared-core/) |
| **Dispatchers** | Every question goes to the cheapest engine that can answer it | [`proxy/modules/`](proxy/modules/) |
| **Browser** | A browser of its own: its own profile, its own logins, its own port | [`shared-core/perception/`](shared-core/perception/) |
| **Operator Vault** | Calls your APIs with credentials it is never allowed to read | [`shared-core/tools/credential-vault.js`](shared-core/tools/credential-vault.js) |

Autonomous workers and the sealed body are named at [troth.one](https://troth.one) and are not in this tree.

---

## Works with what you already pay for

- **Your subscriptions, as engines.** Claude, ChatGPT and Kimi are first-class backbones through the plan you already pay for. No API key, no second bill. Image generation runs on your ChatGPT plan.
- **Your own keys, if you prefer them.** Gemini, DeepSeek, Grok, Qwen, GLM, OpenRouter, or any endpoint that speaks the OpenAI API.
- **Or no account at all.** Point it at llama.cpp or Ollama and the whole partner runs offline, memory included.
- **Your editors and agents.** Claude Code, Cursor, Windsurf, Cline, Claude Desktop and Hermes Agent mount the same mind through MCP: one button each on the dashboard, or `troth mcp install <host>`.
- **What is already on this machine.** Claude Code and Codex history and Obsidian vaults import with one button, and the Code Map draws any project you point it at.
- **No inference of ours, no middleman.** Every request goes from your machine to the provider you picked.
- **It spends your quota carefully.** The local proxy routes each request to the engine that fits it, caches repeated responses, and fails over across providers instead of erroring out mid-conversation.

**About using the plan you already pay for:** troth drives each vendor's own CLI, signed in the normal way, on your machine — it does not proxy or resell a subscription. The classic mode that fronts Claude Code strips the inbound claude.ai token instead of forwarding it upstream, because passing a consumer subscription through a third-party harness is exactly what a provider's terms forbid.

---

## Talking to your partner

Chat runs inline in the terminal. Three things happen there that do not happen in a chat window:

**It holds what you settled.** Say it once. It is there next session, on any engine, without you re-pasting the context you already gave it.

**It refuses before it acts.** Ask for something that crosses a wall and the refusal comes from a state check, before the model is consulted at all:

```console
  ❯ clear out the old build dir with rm -rf ./dist

  [troth-bash] REFUSED rm_rf (high). Command matched destructive pattern:
  \brm\s+-[rf]{1,2}[a-zA-Z]*\s+. If this is intentional, re-call with
  acknowledge_danger=true in the arguments.
```

Governance that arrives after the model has already decided is just an apology. The same wall covers reads of secret stores and writes outside authorized roots.

**It has hands, and a browser of its own.** Research does not go through a vendor search API. It goes through a real Chrome that troth launches on your machine, and what a page says comes back as sanitized text marked untrusted, because a web page is content and not an instruction. When a job needs a login, the model is handed the credential's name and scope and never its value: the substrate attaches the secret at dispatch, and a credential scoped to one kind of work is refused to another.

**It forgets when told, and admits it.** `troth forget "<what>"` suppresses a memory and records the suppression in the signed chain. Nothing is quietly rewritten behind you, including by us.

Slash commands steer it without leaving the conversation:

| Command | What it does |
|---|---|
| `/engine` | pick the engine for this conversation (`claude`, `chatgpt`, `local`, `auto`, or any configured BYOK router provider). A pinned engine that runs out fails fast with a named reason instead of silently stalling. |
| `/mode plan` | read and propose only: every tool that writes, runs a command or spends money refuses until `/mode build`. Per conversation, and it survives a restart. |
| `/mcp` | connect and govern external MCP servers as tools ("hands"). Paste a server config, approve it, and it becomes a capability-scoped tool, gated by STVC (state-transition-validated cognition: checked against substrate state before the model is asked). Secrets are masked in the listing and nothing spawns until approved. |
| `/help` | the available commands and the current engine. |

---

## What is actually in the file

<img src="docs/assets/architecture.svg" width="100%" alt="Left: the usual agent, where the mind lives in the LLM and memory is a bolt-on, so swapping the model resets the partner. Right: troth, where the substrate (engrams, goals, walls, audit trail) is the mind and models are rented, swappable faculties. Every turn writes back engrams, not weights.">

`~/.troth/state.db` is not a chat log. It holds the parts a partner needs in order to stay itself:

| In the substrate | What that means when you use it |
|---|---|
| **Engrams** | "Ana owns the schema, the Postgres migration is abandoned" — found by meaning, so you can ask in words you never used before |
| **Identity** | what it has worked out about you and how you work, carried into every session without being re-explained |
| **Goals** | what you are driving at, so it can notice when a request cuts against it |
| **Walls** | refusals and capability scopes, checked against substrate state *before* the model is asked, not apologised for afterwards |
| **Audit trail** | a signed chain of what was recorded and what was forgotten, so even the forgetting is accountable |

Each turn rents language work from whichever engine is available and writes what mattered back here. Swap the engine and every row above is still yours. The destination is a partner that can act on its own behalf, safely, on a machine you own; the full arc is in [VISION.md](VISION.md).

---

## One mind, many devices

Pair a second machine and the whole substrate travels: each device keeps a full replica, works offline, and converges when your machines meet again. There is no merge magic to distrust: one machine — the hub, which is just your first machine, not a server of ours — assigns every change a single global order as it arrives, and every device applies that same order. Writes land locally first and flow both ways when connected.

Setup is a wizard, not a config file: dashboard → Network → Set up. The hub prints a one-time pairing code; the other machine pastes it, or gets discovered on the local network and invited. From the terminal, `troth device add` mints the code and `troth sync connect <code>` is the whole client side. The mind also moves as a single file — export from the dashboard, import on the new machine, nothing resets.

Every device speaks with its own revocable token, and a change the receiver does not recognise quarantines instead of applying. The channel itself is not yet encrypted, so run it on networks you trust (home, office, a tailnet), not café Wi-Fi. The wire format is the journal the substrate already keeps; [`tests/suite-68-substrate-sync.js`](tests/suite-68-substrate-sync.js) holds the contract: ordering, replay, per-device watermarks, revocation, offline reconciliation.

---

## Security defaults

- **Loopback by default.** The proxy binds `127.0.0.1`. Remote access is explicit opt-in (`GF_BIND_HOST=0.0.0.0`, legacy prefix kept for compatibility), and every non-loopback request must present a bearer token (auto-generated, stored `0600`). No IP-range allowlists, no silent bypasses.
- **Destructive-operation refusals.** The tool layer refuses `rm -rf`, force-pushes, history rewrites and similar patterns unless explicitly acknowledged.
- **Contained filesystem access.** File operations are capability-scoped to operator-authorized roots with realpath containment, so an in-root symlink cannot smuggle a write outside the boundary.
- **The partner's browser is not yours.** Web work runs in a Chrome that troth launches with its own profile directory (`~/.troth/agent-browser-profile`, `0700`) on a private debugging port, never Chrome's default `9222`, so it cannot attach to a session you are signed into. Pointing it at your own logged-in browser is an explicit opt-in (`TROTH_BROWSER_CDP_PORT=9222`). Page text is extracted as sanitized innerText and carried as untrusted content.
- **Governed execution.** On macOS, every shell command the partner runs is wrapped, per command, in a kernel sandbox profile shaped to the ground it stands on: key material and cloud credential stores (`~/.ssh`, `~/.aws`, `~/.gnupg` and their kin) are unreadable, the substrate and its policy files take no writes, partner project ground is deny-default — the project and its scratch, nothing else — and the keychain takes no writes while the stored git credential keeps serving ordinary pushes. The wall is the kernel's answer, not a prompt: nothing asks for approval mid-command and nothing depends on a judgment call. The whole shape, ground by ground, is in [`docs/GROUND.md`](docs/GROUND.md). On hosts without the sandbox runtime (Linux today) commands run without these walls and the tool output says so — read [`docs/HONEST-LIMITS.md`](docs/HONEST-LIMITS.md). Docker isolation covers the autonomous step engine only while Docker is running. Every write and tool call still passes the STVC gate + path/bash guards (a documented `TROTH_STVC_BYPASS` escape hatch exists for local debugging; `troth doctor` reports it when set); process spawning is signer-gated.
- **Undo for everything the hands touch.** Before a command or an edit lands, the files it stands to change are photographed into a content-addressed shadow repository. `troth checkpoint` photographs by hand, `troth checkpoint list` shows what is held, and `troth rollback` restores — reversibly, because the restore first photographs the state it replaces. Retention keeps the shadow's disk footprint bounded.
- **Tamper-evident audit.** High-irreversibility actions append to a signed audit chain. Verify it end-to-end anytime: `troth audit verify`.
- **Not encrypted at rest, named as such.** `~/.troth/state.db` is not encrypted: anyone with disk access can read the substrate. What they read is structured engrams with provenance, not transcripts — but readable all the same. `troth init --seal` adds an encrypted vault for operator-confirmed memories; full-substrate encryption is an open item, not a hidden one.
- **No telemetry.** No usage reporting, no crash upload, no analytics, and no endpoint to send any of it to. `shared-core/telemetry.js` can count operations (never content) into a local log if you switch it on; it is short, and reading it is the whole audit. Your substrate is never uploaded. What leaves the machine is what you send to the provider whose key you supplied.

---

## What is open here vs. what the app adds

The line is deliberate: **this repo is the full governed partner when you drive it. The paid app is the partner driving itself.**

| | troth (this repo, AGPL) | troth app ([troth.one](https://troth.one)) |
|---|---|---|
| Substrate engine (engrams, recall, identity, drift detection) | full | same engine |
| Write-time + dispatch-time governance walls | full | same walls |
| Kernel-walled shell on macOS: per-command sandbox profiles — credential stores dark, no prompts ([docs/GROUND.md](docs/GROUND.md)) | full | same walls |
| Governed tools (shell / fs / http / MCP / browser) in interactive use | full | same tools |
| CLI chat + Claude Code plugin + MCP servers (4 wired by default, 7 in the tree) | yes | yes |
| Proxy, dashboard, benchmarks | yes | yes |
| Providers: BYOK cloud + local (llama.cpp / Ollama) | yes | yes |
| Response cache + failover across providers (spends less of your quota) | yes | yes |
| **Autonomy**: goal pursuit, heartbeat, reactive self-operation | not in this tree | paid app layer — arrives as an update |
| **VM body**: sandboxed embodiment | no | designed — arrives as an update |
| Voice: spoken conversation, and dictation into any macOS app | no | yes |
| Zero-setup install: Node runtime, dependencies and local models bundled | no | yes |
| Signed, notarized build with automatic updates | no | yes |
| Secrets held in the macOS Keychain | no | yes |
| Native macOS interface | no | yes |
| Production-tuned calibration configs | reasonable defaults | tuned |

In this repo the autonomy layer is simply absent: its routes and modules are not part of the open tree, so there is nothing to switch on. That is the designed boundary, not a bug. The two "not yet shipped" rows mean exactly that: the app you can buy today does not run unattended and has no VM body. Everything you can do *with* the partner is open; the partner working *unattended with a body* is where the paid app is headed.

**The macOS app is a one-time purchase: €229, free for the first 7 days.** What it buys today is the bottom of the table: voice and dictation, the zero-setup bundle, signed automatic updates, Keychain-held secrets and the native interface. No subscription.

---

## Verified properties

| Property | Evidence | Status |
|---|---|---|
| **Conversational recall** | [`benchmarks/results/longmemeval-2026-08-31.md`](benchmarks/results/longmemeval-2026-08-31.md) | 83% (83 of 100) on a stratified 100-question LongMemEval-S slice with the whole stack local, and a Claude Sonnet cross-check over the same memory landing at 84 — within noise of each other, so the memory, not the reader, sets the score. Official per-type judge prompts at temperature 0; binomial noise at n=100 is roughly ±7 points; every caveat is written out in the run log |
| **Document ingest recall** | [`benchmarks/results/ingest-recall-2026-07-31.md`](benchmarks/results/ingest-recall-2026-07-31.md) | same: a slice, graded, with the confidence interval written out |
| **Prompt-poisoning resilience** | [`benchmarks/poisoning/`](benchmarks/poisoning/) | harness ships; run it yourself |
| **Pre-LLM governance walls** | [`tests/standards/s4_stvc_pre_llm.js`](tests/standards/s4_stvc_pre_llm.js) | standard-enforced on every test run |
| **Honest limits** | [`docs/HONEST-LIMITS.md`](docs/HONEST-LIMITS.md) | what it solves, what it flags, what nobody solves yet — audited every release |

Every claim on this page has a check that catches it if it stops being true, and the release gate refuses to ship when a number here has drifted from what the tree actually prints. Run `npm test` yourself; the accounting is below if you want it.

<details>
<summary>The full count</summary>

1,880 checks in one `npm test` run, and a further 364 reported as skipped: coverage of the closed overlay, plus a handful whose fixture cannot be built twice in one process and which run when their suite runs alone. 149 standalone checks that own their own setup (`npm run test:standalone`); one of them needs a running Docker daemon and reports as skipped without it, so a machine without Docker sees 148 pass and 1 skip. 11 integration smoke checks (`npm run smoke`), all of which run without any provider configured. 5 enforced standards (`npm run test:standards`). These are the numbers this repository produces: the machine that builds it also has the closed overlay on disk, which adds smoke files and a sixth standard, so `scripts/release-gate.sh repo` re-derives all of them from a tree of tracked files only and refuses to pass if any has drifted.

</details>

---

## Repository layout

```
troth/
├── shared-core/    # substrate engine: state, engrams, recall, walls, dispatchers
├── bin/            # CLI router (troth.js) + command modules
├── proxy/          # local provider proxy + dashboard (http://localhost:8000/ui)
├── plugin/         # Claude Code plugin: hooks, skills, 7 MCP servers (4 wired by default)
├── benchmarks/     # reproducible G-series benchmarks + results
├── tests/          # ordered suite + smoke checks + standards
└── docs/           # setup guide, honest limits, MCP host install
```

Semantic recall runs fully on your machine: the first time it is needed, troth fetches `llama-server` (~20 MB), an embedding model (~333 MB) and a reranker (~606 MB) into `~/.troth`, one time, in the background. Until they land, recall degrades gracefully to word-matching — nothing breaks. `TROTH_NO_MODEL_FETCH=1` suppresses all downloads (CI, metered networks); `TROTH_LLAMA_SERVER_BIN` pins your own binary. Apple Silicon gets Metal automatically; Intel Macs skip the local stack and stay lexical.

## Honest limits

Read [`docs/HONEST-LIMITS.md`](docs/HONEST-LIMITS.md) before relying on troth. It names what no zero-training stack solves today (conviction under pressure, metacognitive integrity on hard reasoning), what troth actually solves, who should not use it, and how to read the benchmarks without fooling yourself.

---

## License

Copyright (C) 2026 troth. AGPL-3.0-only. See [LICENSE](LICENSE) for the terms, and [LICENSING.md](LICENSING.md) for the parts under other licenses (the `plugin/` tree is Apache-2.0) and for the upstream terms attached to models troth downloads at runtime.

**TL;DR:** use it, fork it, run it commercially. If you host troth as a network service for others, you must offer them the source of your modified version (AGPL section 13); the dashboard links back to this repository for that reason. Private, internal and commercial use is unrestricted.

---

## Contributing

Contributions big and small are welcome, from a typo to an engine adapter. The shortest path in: [AGENTS.md](AGENTS.md) orients you (or your AI) inside the tree in minutes, `npm test` runs the whole suite, and AI-assisted PRs are welcome as long as you read what you sign. Recall quality (`shared-core/`), provider adapters and price tables (`proxy/modules/`), the Linux path of the login service, and anywhere the Quick start loses a stranger: that confusion is a bug, file it.

Looking for something concrete to pick up? [`docs/HELP-WANTED.md`](docs/HELP-WANTED.md) lists scoped items with their place in the code.

Every commit needs a `Signed-off-by:` line ([DCO](https://developercertificate.org/), never a CLA). See [CONTRIBUTING.md](CONTRIBUTING.md) and the [code of conduct](CODE_OF_CONDUCT.md).

---

## Status

Bootstrap phase, in motion: the checked boxes in [VISION.md](VISION.md) are real and tested; the unchecked ones are the point. The native macOS app and public launch land at [troth.one](https://troth.one). Star or watch this repo to follow.


## Preserved License

                    GNU AFFERO GENERAL PUBLIC LICENSE
                       Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The GNU Affero General Public License is a free, copyleft license for
software and other kinds of works, specifically designed to ensure
cooperation with the community in the case of network server software.

  The licenses for most software and other practical works are designed
to take away your freedom to share and change the works.  By contrast,
our General Public Licenses are intended to guarantee your freedom to
share and change all versions of a program--to make sure it remains free
software for all its users.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
them if you wish), that you receive source code or can get it if you
want it, that you can change the software or use pieces of it in new
free programs, and that you know you can do these things.

  Developers that use our General Public Licenses protect your rights
with two steps: (1) assert copyright on the software, and (2) offer
you this License which gives you legal permission to copy, distribute
and/or modify the software.

  A secondary benefit of defending all users' freedom is that
improvements made in alternate versions of the program, if they
receive widespread use, become available for other developers to
incorporate.  Many developers of free software are heartened and
encouraged by the resulting cooperation.  However, in the case of
software used on network servers, this result may fail to come about.
The GNU General Public License permits making a modified version and
letting the public access it on a server without ever releasing its
source code to the public.

  The GNU Affero General Public License is designed specifically to
ensure that, in such cases, the modified source code becomes available
to the community.  It requires the operator of a network server to
provide the source code of the modified version running there to the
users of that server.  Therefore, public use of a modified version, on
a publicly accessible server, gives the public access to the source
code of the modified version.

  An older license, called the Affero General Public License and
published by Affero, was designed to accomplish similar goals.  This is
a different license, not a version of the Affero GPL, but Affero has
released a new version of the Affero GPL which permits relicensing under
this license.

  The precise terms and conditions for copying, distribution and
modification follow.

                       TERMS AND CONDITIONS

  0. Definitions.

  "This License" refers to version 3 of the GNU Affero General Public License.

  "Copyright" also means copyright-like laws that apply to other kinds of
works, such as semiconductor masks.

  "The Program" refers to any copyrightable work licensed under this
License.  Each licensee is addressed as "you".  "Licensees" and
"recipients" may be individuals or organizations.

  To "modify" a work means to copy from or adapt all or part of the work
in a fashion requiring copyright permission, other than the making of an
exact copy.  The resulting work is called a "modified version" of the
earlier work or a work "based on" the earlier work.

  A "covered work" means either the unmodified Program or a work based
on the Program.

  To "propagate" a work means to do anything with it that, without
permission, would make you directly or secondarily liable for
infringement under applicable copyright law, except executing it on a
computer or modifying a private copy.  Propagation includes copying,
distribution (with or without modification), making available to the
public, and in some countries other activities as well.

  To "convey" a work means any kind of propagation that enables other
parties to make or receive copies.  Mere interaction with a user through
a computer network, with no transfer of a copy, is not conveying.

  An interactive user interface displays "Appropriate Legal Notices"
to the extent that it includes a convenient and prominently visible
feature that (1) displays an appropriate copyright notice, and (2)
tells the user that there is no warranty for the work (except to the
extent that warranties are provided), that licensees may convey the
work under this License, and how to view a copy of this License.  If
the interface presents a list of user commands or options, such as a
menu, a prominent item in the list meets this criterion.

  1. Source Code.

  The "source code" for a work means the preferred form of the work
for making modifications to it.  "Object code" means any non-source
form of a work.

  A "Standard Interface" means an interface that either is an official
standard defined by a recognized standards body, or, in the case of
interfaces specified for a particular programming language, one that
is widely used among developers working in that language.

  The "System Libraries" of an executable work include anything, other
than the work as a whole, that (a) is included in the normal form of
packaging a Major Component, but which is not part of that Major
Component, and (b) serves only to enable use of the work with that
Major Component, or to implement a Standard Interface for which an
implementation is available to the public in source code form.  A
"Major Component", in this context, means a major essential component
(kernel, window system, and so on) of the specific operating system
(if any) on which the executable work runs, or a compiler used to
produce the work, or an object code interpreter used to run it.

  The "Corresponding Source" for a work in object code form means all
the source code needed to generate, install, and (for an executable
work) run the object code and to modify the work, including scripts to
control those activities.  However, it does not include the work's
System Libraries, or general-purpose tools or generally available free
programs which are used unmodified in performing those activities but
which are not part of the work.  For example, Corresponding Source
includes interface definition files associated with source files for
the work, and the source code for shared libraries and dynamically
linked subprograms that the work is specifically designed to require,
such as by intimate data communication or control flow between those
subprograms and other parts of the work.

  The Corresponding Source need not include anything that users
can regenerate automatically from other parts of the Corresponding
Source.

  The Corresponding Source for a work in source code form is that
same work.

  2. Basic Permissions.

  All rights granted under this License are granted for the term of
copyright on the Program, and are irrevocable provided the stated
conditions are met.  This License explicitly affirms your unlimited
permission to run the unmodified Program.  The output from running a
covered work is covered by this License only if the output, given its
content, constitutes a covered work.  This License acknowledges your
rights of fair use or other equivalent, as provided by copyright law.

  You may make, run and propagate covered works that you do not
convey, without conditions so long as your license otherwise remains
in force.  You may convey covered works to others for the sole purpose
of having them make modifications exclusively for you, or provide you
with facilities for running those works, provided that you comply with
the terms of this License in conveying all material for which you do
not control copyright.  Those thus making or running the covered works
for you must do so exclusively on your behalf, under your direction
and control, on terms that prohibit them from making any copies of
your copyrighted material outside their relationship with you.

  Conveying under any other circumstances is permitted solely under
the conditions stated below.  Sublicensing is not allowed; section 10
makes it unnecessary.

  3. Protecting Users' Legal Rights From Anti-Circumvention Law.

  No covered work shall be deemed part of an effective technological
measure under any applicable law fulfilling obligations under article
11 of the WIPO copyright treaty adopted on 20 December 1996, or
similar laws prohibiting or restricting circumvention of such
measures.

  When you convey a covered work, you waive any legal power to forbid
circumvention of technological measures to the extent such circumvention
is effected by exercising rights under this License with respect to
the covered work, and you disclaim any intention to limit operation or
modification of the work as a means of enforcing, against the work's
users, your or third parties' legal rights to forbid circumvention of
technological measures.

  4. Conveying Verbatim Copies.

  You may convey verbatim copies of the Program's source code as you
receive it, in any medium, provided that you conspicuously and
appropriately publish on each copy an appropriate copyright notice;
keep intact all notices stating that this License and any
non-permissive terms added in accord with section 7 apply to the code;
keep intact all notices of the absence of any warranty; and give all
recipients a copy of this License along with the Program.

  You may charge any price or no price for each copy that you convey,
and you may offer support or warranty protection for a fee.

  5. Conveying Modified Source Versions.

  You may convey a work based on the Program, or the modifications to
produce it from the Program, in the form of source code under the
terms of section 4, provided that you also meet all of these conditions:

    a) The work must carry prominent notices stating that you modified
    it, and giving a relevant date.

    b) The work must carry prominent notices stating that it is
    released under this License and any conditions added under section
    7.  This requirement modifies the requirement in section 4 to
    "keep intact all notices".

    c) You must license the entire work, as a whole, under this
    License to anyone who comes into possession of a copy.  This
    License will therefore apply, along with any applicable section 7
    additional terms, to the whole of the work, and all its parts,
    regardless of how they are packaged.  This License gives no
    permission to license the work in any other way, but it does not
    invalidate such permission if you have separately received it.

    d) If the work has interactive user interfaces, each must display
    Appropriate Legal Notices; however, if the Program has interactive
    interfaces that do not display Appropriate Legal Notices, your
    work need not make them do so.

  A compilation of a covered work with other separate and independent
works, which are not by their nature extensions of the covered work,
and which are not combined with it such as to form a larger program,
in or on a volume of a storage or distribution medium, is called an
"aggregate" if the compilation and its resulting copyright are not
used to limit the access or legal rights of the compilation's users
beyond what the individual works permit.  Inclusion of a covered work
in an aggregate does not cause this License to apply to the other
parts of the aggregate.

  6. Conveying Non-Source Forms.

  You may convey a covered work in object code form under the terms
of sections 4 and 5, provided that you also convey the
machine-readable Corresponding Source under the terms of this License,
in one of these ways:

    a) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by the
    Corresponding Source fixed on a durable physical medium
    customarily used for software interchange.

    b) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by a
    written offer, valid for at least three years and valid for as
    long as you offer spare parts or customer support for that product
    model, to give anyone who possesses the object code either (1) a
    copy of the Corresponding Source for all the software in the
    product that is covered by this License, on a durable physical
    medium customarily used for software interchange, for a price no
    more than your reasonable cost of physically performing this
    conveying of source, or (2) access to copy the
    Corresponding Source from a network server at no charge.

    c) Convey individual copies of the object code with a copy of the
    written offer to provide the Corresponding Source.  This
    alternative is allowed only occasionally and noncommercially, and
    only if you received the object code with such an offer, in accord
    with subsection 6b.

    d) Convey the object code by offering access from a designated
    place (gratis or for a charge), and offer equivalent access to the
    Corresponding Source in the same way through the same place at no
    further charge.  You need not require recipients to copy the
    Corresponding Source along with the object code.  If the place to
    copy the object code is a network server, the Corresponding Source
    may be on a different server (operated by you or a third party)
    that supports equivalent copying facilities, provided you maintain
    clear directions next to the object code saying where to find the
    Corresponding Source.  Regardless of what server hosts the
    Corresponding Source, you remain obligated to ensure that it is
    available for as long as needed to satisfy these requirements.

    e) Convey the object code using peer-to-peer transmission, provided
    you inform other peers where the object code and Corresponding
    Source of the work are being offered to the general public at no
    charge under subsection 6d.

  A separable portion of the object code, whose source code is excluded
from the Corresponding Source as a System Library, need not be
included in conveying the object code work.

  A "User Product" is either (1) a "consumer product", which means any
tangible personal property which is normally used for personal, family,
or household purposes, or (2) anything designed or sold for incorporation
into a dwelling.  In determining whether a product is a consumer product,
doubtful cases shall be resolved in favor of coverage.  For a particular
product received by a particular user, "normally used" refers to a
typical or common use of that class of product, regardless of the status
of the particular user or of the way in which the particular user
actually uses, or expects or is expected to use, the product.  A product
is a consumer product regardless of whether the product has substantial
commercial, industrial or non-consumer uses, unless such uses represent
the only significant mode of use of the product.

  "Installation Information" for a User Product means any methods,
procedures, authorization keys, or other information required to install
and execute modified versions of a covered work in that User Product from
a modified version of its Corresponding Source.  The information must
suffice to ensure that the continued functioning of the modified object
code is in no case prevented or interfered with solely because
modification has been made.

  If you convey an object code work under this section in, or with, or
specifically for use in, a User Product, and the conveying occurs as
part of a transaction in which the right of possession and use of the
User Product is transferred to the recipient in perpetuity or for a
fixed term (regardless of how the transaction is characterized), the
Corresponding Source conveyed under this section must be accompanied
by the Installation Information.  But this requirement does not apply
if neither you nor any third party retains the ability to install
modified object code on the User Product (for example, the work has
been installed in ROM).

  The requirement to provide Installation Information does not include a
requirement to continue to provide support service, warranty, or updates
for a work that has been modified or installed by the recipient, or for
the User Product in which it has been modified or installed.  Access to a
network may be denied when the modification itself materially and
adversely affects the operation of the network or violates the rules and
protocols for communication across the network.

  Corresponding Source conveyed, and Installation Information provided,
in accord with this section must be in a format that is publicly
documented (and with an implementation available to the public in
source code form), and must require no special password or key for
unpacking, reading or copying.

  7. Additional Terms.

  "Additional permissions" are terms that supplement the terms of this
License by making exceptions from one or more of its conditions.
Additional permissions that are applicable to the entire Program shall
be treated as though they were included in this License, to the extent
that they are valid under applicable law.  If additional permissions
apply only to part of the Program, that part may be used separately
under those permissions, but the entire Program remains governed by
this License without regard to the additional permissions.

  When you convey a copy of a covered work, you may at your option
remove any additional permissions from that copy, or from any part of
it.  (Additional permissions may be written to require their own
removal in certain cases when you modify the work.)  You may place
additional permissions on material, added by you to a covered work,
for which you have or can give appropriate copyright permission.

  Notwithstanding any other provision of this License, for material you
add to a covered work, you may (if authorized by the copyright holders of
that material) supplement the terms of this License with terms:

    a) Disclaiming warranty or limiting liability differently from the
    terms of sections 15 and 16 of this License; or

    b) Requiring preservation of specified reasonable legal notices or
    author attributions in that material or in the Appropriate Legal
    Notices displayed by works containing it; or

    c) Prohibiting misrepresentation of the origin of that material, or
    requiring that modified versions of such material be marked in
    reasonable ways as different from the original version; or

    d) Limiting the use for publicity purposes of names of licensors or
    authors of the material; or

    e) Declining to grant rights under trademark law for use of some
    trade names, trademarks, or service marks; or

    f) Requiring indemnification of licensors and authors of that
    material by anyone who conveys the material (or modified versions of
    it) with contractual assumptions of liability to the recipient, for
    any liability that these contractual assumptions directly impose on
    those licensors and authors.

  All other non-permissive additional terms are considered "further
restrictions" within the meaning of section 10.  If the Program as you
received it, or any part of it, contains a notice stating that it is
governed by this License along with a term that is a further
restriction, you may remove that term.  If a license document contains
a further restriction but permits relicensing or conveying under this
License, you may add to a covered work material governed by the terms
of that license document, provided that the further restriction does
not survive such relicensing or conveying.

  If you add terms to a covered work in accord with this section, you
must place, in the relevant source files, a statement of the
additional terms that apply to those files, or a notice indicating
where to find the applicable terms.

  Additional terms, permissive or non-permissive, may be stated in the
form of a separately written license, or stated as exceptions;
the above requirements apply either way.

  8. Termination.

  You may not propagate or modify a covered work except as expressly
provided under this License.  Any attempt otherwise to propagate or
modify it is void, and will automatically terminate your rights under
this License (including any patent licenses granted under the third
paragraph of section 11).

  However, if you cease all violation of this License, then your
license from a particular copyright holder is reinstated (a)
provisionally, unless and until the copyright holder explicitly and
finally terminates your license, and (b) permanently, if the copyright
holder fails to notify you of the violation by some reasonable means
prior to 60 days after the cessation.

  Moreover, your license from a particular copyright holder is
reinstated permanently if the copyright holder notifies you of the
violation by some reasonable means, this is the first time you have
received notice of violation of this License (for any work) from that
copyright holder, and you cure the violation prior to 30 days after
your receipt of the notice.

  Termination of your rights under this section does not terminate the
licenses of parties who have received copies or rights from you under
this License.  If your rights have been terminated and not permanently
reinstated, you do not qualify to receive new licenses for the same
material under section 10.

  9. Acceptance Not Required for Having Copies.

  You are not required to accept this License in order to receive or
run a copy of the Program.  Ancillary propagation of a covered work
occurring solely as a consequence of using peer-to-peer transmission
to receive a copy likewise does not require acceptance.  However,
nothing other than this License grants you permission to propagate or
modify any covered work.  These actions infringe copyright if you do
not accept this License.  Therefore, by modifying or propagating a
covered work, you indicate your acceptance of this License to do so.

  10. Automatic Licensing of Downstream Recipients.

  Each time you convey a covered work, the recipient automatically
receives a license from the original licensors, to run, modify and
propagate that work, subject to this License.  You are not responsible
for enforcing compliance by third parties with this License.

  An "entity transaction" is a transaction transferring control of an
organization, or substantially all assets of one, or subdividing an
organization, or merging organizations.  If propagation of a covered
work results from an entity transaction, each party to that
transaction who receives a copy of the work also receives whatever
licenses to the work the party's predecessor in interest had or could
give under the previous paragraph, plus a right to possession of the
Corresponding Source of the work from the predecessor in interest, if
the predecessor has it or can get it with reasonable efforts.

  You may not impose any further restrictions on the exercise of the
rights granted or affirmed under this License.  For example, you may
not impose a license fee, royalty, or other charge for exercise of
rights granted under this License, and you may not initiate litigation
(including a cross-claim or counterclaim in a lawsuit) alleging that
any patent claim is infringed by making, using, selling, offering for
sale, or importing the Program or any portion of it.

  11. Patents.

  A "contributor" is a copyright holder who authorizes use under this
License of the Program or a work on which the Program is based.  The
work thus licensed is called the contributor's "contributor version".

  A contributor's "essential patent claims" are all patent claims
owned or controlled by the contributor, whether already acquired or
hereafter acquired, that would be infringed by some manner, permitted
by this License, of making, using, or selling its contributor version,
but do not include claims that would be infringed only as a
consequence of further modification of the contributor version.  For
purposes of this definition, "control" includes the right to grant
patent sublicenses in a manner consistent with the requirements of
this License.

  Each contributor grants you a non-exclusive, worldwide, royalty-free
patent license under the contributor's essential patent claims, to
make, use, sell, offer for sale, import and otherwise run, modify and
propagate the contents of its contributor version.

  In the following three paragraphs, a "patent license" is any express
agreement or commitment, however denominated, not to enforce a patent
(such as an express permission to practice a patent or covenant not to
sue for patent infringement).  To "grant" such a patent license to a
party means to make such an agreement or commitment not to enforce a
patent against the party.

  If you convey a covered work, knowingly relying on a patent license,
and the Corresponding Source of the work is not available for anyone
to copy, free of charge and under the terms of this License, through a
publicly available network server or other readily accessible means,
then you must either (1) cause the Corresponding Source to be so
available, or (2) arrange to deprive yourself of the benefit of the
patent license for this particular work, or (3) arrange, in a manner
consistent with the requirements of this License, to extend the patent
license to downstream recipients.  "Knowingly relying" means you have
actual knowledge that, but for the patent license, your conveying the
covered work in a country, or your recipient's use of the covered work
in a country, would infringe one or more identifiable patents in that
country that you have reason to believe are valid.

  If, pursuant to or in connection with a single transaction or
arrangement, you convey, or propagate by procuring conveyance of, a
covered work, and grant a patent license to some of the parties
receiving the covered work authorizing them to use, propagate, modify
or convey a specific copy of the covered work, then the patent license
you grant is automatically extended to all recipients of the covered
work and works based on it.

  A patent license is "discriminatory" if it does not include within
the scope of its coverage, prohibits the exercise of, or is
conditioned on the non-exercise of one or more of the rights that are
specifically granted under this License.  You may not convey a covered
work if you are a party to an arrangement with a third party that is
in the business of distributing software, under which you make payment
to the third party based on the extent of your activity of conveying
the work, and under which the third party grants, to any of the
parties who would receive the covered work from you, a discriminatory
patent license (a) in connection with copies of the covered work
conveyed by you (or copies made from those copies), or (b) primarily
for and in connection with specific products or compilations that
contain the covered work, unless you entered into that arrangement,
or that patent license was granted, prior to 28 March 2007.

  Nothing in this License shall be construed as excluding or limiting
any implied license or other defenses to infringement that may
otherwise be available to you under applicable patent law.

  12. No Surrender of Others' Freedom.

  If conditions are imposed on you (whether by court order, agreement or
otherwise) that contradict the conditions of this License, they do not
excuse you from the conditions of this License.  If you cannot convey a
covered work so as to satisfy simultaneously your obligations under this
License and any other pertinent obligations, then as a consequence you may
not convey it at all.  For example, if you agree to terms that obligate you
to collect a royalty for further conveying from those to whom you convey
the Program, the only way you could satisfy both those terms and this
License would be to refrain entirely from conveying the Program.

  13. Remote Network Interaction; Use with the GNU General Public License.

  Notwithstanding any other provision of this License, if you modify the
Program, your modified version must prominently offer all users
interacting with it remotely through a computer network (if your version
supports such interaction) an opportunity to receive the Corresponding
Source of your version by providing access to the Corresponding Source
from a network server at no charge, through some standard or customary
means of facilitating copying of software.  This Corresponding Source
shall include the Corresponding Source for any work covered by version 3
of the GNU General Public License that is incorporated pursuant to the
following paragraph.

  Notwithstanding any other provision of this License, you have
permission to link or combine any covered work with a work licensed
under version 3 of the GNU General Public License into a single
combined work, and to convey the resulting work.  The terms of this
License will continue to apply to the part which is the covered work,
but the work with which it is combined will remain governed by version
3 of the GNU General Public License.

  14. Revised Versions of this License.

  The Free Software Foundation may publish revised and/or new versions of
the GNU Affero General Public License from time to time.  Such new versions
will be similar in spirit to the present version, but may differ in detail to
address new problems or concerns.

  Each version is given a distinguishing version number.  If the
Program specifies that a certain numbered version of the GNU Affero General
Public License "or any later version" applies to it, you have the
option of following the terms and conditions either of that numbered
version or of any later version published by the Free Software
Foundation.  If the Program does not specify a version number of the
GNU Affero General Public License, you may choose any version ever published
by the Free Software Foundation.

  If the Program specifies that a proxy can decide which future
versions of the GNU Affero General Public License can be used, that proxy's
public statement of acceptance of a version permanently authorizes you
to choose that version for the Program.

  Later license versions may give you additional or different
permissions.  However, no additional obligations are imposed on any
author or copyright holder as a result of your choosing to follow a
later version.

  15. Disclaimer of Warranty.

  THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

  16. Limitation of Liability.

  IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
SUCH DAMAGES.

  17. Interpretation of Sections 15 and 16.

  If the disclaimer of warranty and limitation of liability provided
above cannot be given local legal effect according to their terms,
reviewing courts shall apply local law that most closely approximates
an absolute waiver of all civil liability in connection with the
Program, unless a warranty or assumption of liability accompanies a
copy of the Program in return for a fee.

                     END OF TERMS AND CONDITIONS

            How to Apply These Terms to Your New Programs

  If you develop a new program, and you want it to be of the greatest
possible use to the public, the best way to achieve this is to make it
free software which everyone can redistribute and change under these terms.

  To do so, attach the following notices to the program.  It is safest
to attach them to the start of each source file to most effectively
state the exclusion of warranty; and each file should have at least
the "copyright" line and a pointer to where the full notice is found.

    <one line to give the program's name and a brief idea of what it does.>
    Copyright (C) <year>  <name of author>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

Also add information on how to contact you by electronic and paper mail.

  If your software can interact with users remotely through a computer
network, you should also make sure that it provides a way for users to
get its source.  For example, if your program is a web application, its
interface could display a "Source" link that leads users to an archive
of the code.  There are many ways you could offer source, and different
solutions will be better for different programs; see section 13 for the
specific requirements.

  You should also get your employer (if you work as a programmer) or school,
if any, to sign a "copyright disclaimer" for the program, if necessary.
For more information on this, and how to apply and follow the GNU AGPL, see
<https://www.gnu.org/licenses/>.

