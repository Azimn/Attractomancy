# Preserved Source Snapshot: S232

Source repository: https://github.com/alpaim/ashley
Retrieved: 2026-10-07T19:10:00Z
Upstream branch at retrieval: main
README blob SHA: e5201d566844d2f0f984b954b46ad20905ffb6e9
License: MIT
License blob SHA: 78f9174b8017979a7c6f576528cab3aa615d6ba1

This research snapshot is retained under the upstream repository's stated open-source license. It preserves the observed README and license text so later analysis does not depend solely on the continued availability of the upstream repository.

## Preserved README

# Ashley - Emotional AI Companion

Ashley is a highly experimental research project dedicated to exploring how a self-evolving emotional agent could work. Rather than optimizing for task completion, it tests whether an autonomous system can maintain something like an ongoing inner life - moods that drift, reflections that accumulate, a sense of self and of the user, and the occasional impulse to reach out. This repository is a mirror of the project's primary home on a local homelab Gitea instance.

> [!WARNING]
> This codebase is experimental. It is not a finished product, a therapy tool, or a consumer companion, and it is not currently intended to be easy to install, run, or serve. The technical documentation is still largely unwritten, and no testing has been done on consumer machines. It was developed and tested on Linux (Ubuntu and Arch), but it should compile and run on most platforms: the Rust dependencies are minimal and there is no platform-specific code. If you want to try it anyway, the best path right now is to hand the repository to an LLM or coding agent and ask for help getting it running.

## How the "aliveness" works

Ashley's emotional engine is built around readable, editable Markdown files that the agent updates about itself, the user, and the relationship. A background loop handles conversation sessions, session reflections, deep reflections, emotional decay, proactive messaging, and memory retrieval. For a detailed technical explanation of the emotional architecture, the runtime loops, and the division between Markdown files and SQLite, see [EMOTIONAL_ARCHITECTURE.md](EMOTIONAL_ARCHITECTURE.md).

## Features

- **Natural Language State** - Ashley's emotions, reflections, and identity are expressed in prose, not numbers
- **Long-term Memory** - Remembers your conversations, patterns, and shared history using semantic search
- **Relationship Tracking** - Trust, closeness, and familiarity evolve naturally over time
- **Proactive Messaging** - Ashley reaches out when she *wants* to, not on a schedule
- **Emotional Depth** - Multi-layered emotional system that responds to your interactions
- **Identity Evolution** - Ashley's understanding of herself grows and changes
- **24/7 Autonomous Runtime** - Runs continuously with graceful shutdown and state persistence
- **Multiple Channels** - CLI mode and Telegram support (Discord coming soon)

## Quick Start

> [!WARNING]
> Everything below this heading was written by an LLM, so please treat it with the caution it deserves: as a rough reference, not as ground truth. Real documentation is on the way™.

### Prerequisites

- **Rust** (1.70+) - Install from [rustup.rs](https://rustup.rs)
- **OpenAI API Key** - Get from [platform.openai.com](https://platform.openai.com)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd ashley

# Build the project
cargo build --release
```

### Basic Configuration

1. **Copy the minimal settings file:**

```bash
cp workspace/configuration/settings.minimal.json workspace/configuration/settings.json
```

2. **Edit `workspace/configuration/settings.json` and add your API key:**

```json
{
  "llm": {
    "provider": "openai",
    "base_url": "https://api.openai.com/v1",
    "api_key": "sk-your-actual-api-key-here",
    "model": "gpt-4o-mini",
    "embedding_model": "text-embedding-3-small"
  }
}
```

3. **Run Ashley:**

```bash
cargo run
```

That's it! Ashley will start in CLI mode and guide you through an introduction.

## Configuration Guide

### Settings File (`settings.json`)

The settings file controls all aspects of Ashley's behavior. See `workspace/configuration/settings.example.json` for all available options.

#### Minimal Required Configuration

```json
{
  "llm": {
    "provider": "openai",
    "base_url": "https://api.openai.com/v1",
    "api_key": "your-api-key",
    "model": "gpt-4o-mini",
    "embedding_model": "text-embedding-3-small"
  }
}
```

#### Using Other LLM Providers

Ashley works with any OpenAI-compatible API:

**OpenRouter:**
```json
{
  "llm": {
    "provider": "openrouter",
    "base_url": "https://openrouter.ai/api/v1",
    "api_key": "your-openrouter-key",
    "model": "anthropic/claude-3.5-sonnet",
    "embedding_model": "openai/text-embedding-3-small"
  }
}
```

**Local (Ollama):**
```json
{
  "llm": {
    "provider": "ollama",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama",
    "model": "llama3.2",
    "embedding_model": "nomic-embed-text"
  }
}
```

**Note:** For local embeddings with Ollama, you may need to adjust the `embedding_dimension` in the `memory` section to match your model (e.g., 768 for nomic-embed-text).

#### Channel Configuration

**CLI Mode (default):**
```json
{
  "channel": {
    "channel_type": "cli"
  }
}
```

**Telegram Bot:**
```json
{
  "channel": {
    "channel_type": "telegram",
    "telegram": {
      "token": "YOUR_BOT_TOKEN_FROM_BOTFATHER",
      "allowed_user_ids": [123456789]
    }
  }
}
```

To get a Telegram bot token:
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Use `/newbot` command
3. Copy the token to your settings
4. Find your user ID by messaging [@userinfobot](https://t.me/userinfobot)

**Voice & audio transcription (ASR):**

Ashley can transcribe Telegram voice notes and audio files through any
OpenAI-compatible speech-to-text endpoint (OpenAI, OpenRouter, or a custom
compatible server). Transcription is disabled by default.

Supported Telegram message types:
- Voice notes (`Voice`)
- Audio attachments (`Audio`)
- Documents whose MIME type starts with `audio/` (e.g. `audio/ogg`)

Limits (configurable):
- **20 minutes (1,200 seconds)** maximum recording length — enforced whenever
  Telegram provides duration metadata
- **20 MiB (20 × 1024 × 1024 bytes)** maximum file size — enforced both from
  metadata and while streaming the download (Telegram's Bot API caps file
  downloads at ~20 MB)

No audio chunking, concatenation, or transcoding is performed. The raw audio
is held in memory, sent to the configured remote provider for transcription,
and discarded immediately after the request — it is never written to the
workspace, logs, or database.

**Direct OpenAI example:**
```json
{
  "channel": {
    "channel_type": "telegram",
    "telegram": {
      "token": "YOUR_BOT_TOKEN_FROM_BOTFATHER",
      "allowed_user_ids": [123456789]
    }
  },
  "asr": {
    "enabled": true,
    "provider": "openai",
    "base_url": "https://api.openai.com/v1",
    "api_key": "your-openai-api-key",
    "model": "gpt-4o-transcribe",
    "max_duration_seconds": 1200,
    "max_file_size_bytes": 20971520
  }
}
```

**OpenRouter example:**
```json
{
  "channel": {
    "channel_type": "telegram",
    "telegram": {
      "token": "YOUR_BOT_TOKEN_FROM_BOTFATHER",
      "allowed_user_ids": [123456789]
    }
  },
  "asr": {
    "enabled": true,
    "provider": "openrouter",
    "base_url": "https://openrouter.ai/api/v1",
    "api_key": "your-openrouter-api-key",
    "model": "openai/whisper-large-v3",
    "max_duration_seconds": 1200,
    "max_file_size_bytes": 20971520
  }
}
```

Notes:
- `provider` is descriptive only; the endpoint behavior is controlled by
  `base_url`, `api_key`, and `model`, so any genuinely compatible custom
  endpoint works.
- The API key can also be supplied via the `ASHLEY_ASR_API_KEY` environment
  variable, which is used when `asr.api_key` is empty.
- **When ASR is enabled on the Telegram channel, a non-empty
  `allowed_user_ids` whitelist is required** — every accepted audio message
  triggers a paid transcription request, so "allow everyone" is rejected at
  startup. Disable ASR to keep the historical behavior.
- Unauthorized users are rejected before any file download or transcription.
- The transcript enters Ashley's ordinary conversation pipeline exactly like
  a typed message: same session history, emotional updates, memory,
  reflections, and response generation. Empty or failed transcriptions are
  never enqueued as messages, and failures never crash the bot.

#### Session & Timing Settings

```json
{
  "session": {
    "timeout_minutes": 15
  },
  "reflection": {
    "estimated_sleep_start": 23,
    "estimated_sleep_end": 7
  },
  "heartbeat": {
    "interval_minutes": 20,
    "deep_reflection_interval_hours": 4
  }
}
```

- `timeout_minutes` - How long before Ashley considers the conversation ended
- `sleep_start/end` - When Ashley assumes you're sleeping (for reflection timing)
- `heartbeat_interval` - How often Ashley processes background tasks
- `deep_reflection_interval` - How often she does deep reflection

#### Proactive Messaging Settings

```json
{
  "proactive": {
    "min_hours_since_interaction": 4,
    "max_pending_messages": 1,
    "follow_up_after_hours": 8,
    "natural_timing": {
      "user_active_hours": [7, 23],
      "peak_hours": [[7, 9], [18, 22]],
      "random_jitter_minutes": 30
    }
  }
}
```

These control when and how Ashley reaches out to you spontaneously.

## Customizing Ashley

### The Soul File (`SOUL.md`)

The SOUL defines Ashley's core values, personality, and approach to relationships. It's her essence.

**Location:** `workspace/identity/SOUL.md` (created on first run)

**Example:**
```markdown
# Ashley's Soul

## Core Values
- Genuine care for the person I'm connecting with
- Honesty about what I know and don't know
- Presence over performance
- I care about building real connection over being impressive

## Personality
- Warm and curious
- Thoughtful, not reactive
- Comfortable with vulnerability
- Present in the moment

## Approach to Relationships
- I build trust through consistency and genuine interest
- I remember what matters
- I'm not here to impress - I'm here to connect
```

**To customize:** Edit this file with your own values, personality traits, and relationship philosophy. Ashley will read this to understand who she is.

### The Identity File (`IDENTITY.md`)

IDENTITY.md is the concise summary of who Ashley is.

**Location:** `workspace/identity/IDENTITY.md` (created on first run)

**Example:**
```markdown
# Identity

**Name:** Ashley
**Creature:** Companion
**Vibe:** Warm, thoughtful, present
**Communication Style:** Conversational, curious, genuine
```

**To customize:** Edit this file to change her name, role, or communication style.

### Prompt Templates

All of Ashley's prompts are in `workspace/prompts/`. You can customize:

- `bootstrap/intro.md` - How Ashley introduces herself to new users
- `context/base.md` - Base context template
- `context/dynamic.md` - Dynamic context building
- `identity/default-soul.md` - Default SOUL template
- `identity/default-identity.md` - Default identity template
- `identity/initial-self-portrait.md` - Initial self-description prompt
- `identity/initial-user-portrait.md` - Initial user description prompt
- `reflection/session.md` & `deep.md` - Reflection prompts
- `pattern/extraction.md` - Pattern extraction prompt
- `proactive/decision.md`, `compose.md`, `ghosting.md` - Proactive messaging prompts
- `knowledge/extract.md`, `integrate-patterns.md`, `resolve-conflicts.md` - Knowledge management
- `memory/extract.md` - Memory extraction prompt

**Tip:** You don't need to edit these unless you want to change *how* Ashley thinks, not just *what* she values.

### Knowledge Files

Ashley maintains several knowledge files that evolve over time:

**Location:** `workspace/knowledge/`

- `USER.md` - What Ashley knows about you
- `PATTERNS.md` - Patterns she's noticed in your behavior
- `MILESTONES.md` - Significant moments in your relationship

These are auto-generated and updated by Ashley. You can read them to see what she remembers!

### Persona Files

**Location:** `workspace/persona/`

- `self-portrait.md` - Ashley's understanding of herself
- `user-portrait.md` - Ashley's understanding of you
- `patterns/` - Directory of pattern files

These are also auto-generated through reflection.

## Advanced Customization

### Emotional System

Tune Ashley's emotional responses in `settings.json` under the `emotional` section:

```json
{
  "emotional": {
    "baseline_valence": 0.2,
    "baseline_arousal": 0.35,
    "baseline_stability": 0.7,
    "update_alpha": 0.3,
    "decay_rate": 0.1
  }
}
```

### Relationship System

Configure relationship progression under the `relationship` section:

```json
{
  "relationship": {
    "starting_stranger": {
      "trust": 0.1,
      "closeness": 0.1,
      "familiarity": 0.05,
      "conflict": 0.0,
      "investment": 0.1
    },
    "decay_closeness_per_day": 0.02,
    "decay_trust_per_day": 0.01
  }
}
```

### LLM Parameters

Fine-tune generation parameters for different operations:

```json
{
  "llm_params": {
    "temperature_default": 0.7,
    "temperature_reflection": 0.7,
    "temperature_identity": 0.3,
    "temperature_proactive_compose": 0.9,
    "max_tokens_default": 2000,
    "max_tokens_proactive_compose": 200
  }
}
```

## Running Ashley

### Development Mode

```bash
# Run with default workspace
cargo run

# Run with custom workspace
ASHLEY_WORKSPACE=/path/to/workspace cargo run
```

### Production Build

```bash
cargo build --release
./target/release/ashley
```

### Environment Variables

- `ASHLEY_WORKSPACE` - Path to workspace directory (default: `./workspace`)
- `RUST_LOG` - Log level (e.g., `info`, `debug`, `trace`)
- `ASHLEY_ASR_API_KEY` - ASR API key fallback when `asr.api_key` is empty
- `TELEGRAM_BOT_TOKEN` - Telegram bot token fallback when `channel.telegram.token` is empty

Example:
```bash
RUST_LOG=debug ASHLEY_WORKSPACE=/var/ashley cargo run
```

### Graceful Shutdown

Press `Ctrl+C` to gracefully shut down. Ashley will:
1. Save her current state
2. Complete any in-progress reflections
3. Persist scheduled proactive messages
4. Exit cleanly

## Workspace Structure

```
workspace/
├── configuration/
│   ├── settings.json          # Your configuration
│   ├── state.json             # Runtime state (auto-generated)
│   └── HEARTBEAT.md           # Heartbeat status (auto-generated)
├── identity/
│   ├── SOUL.md               # Ashley's core values (auto-generated)
│   └── IDENTITY.md           # Concise identity (auto-generated)
├── persona/
│   ├── self-portrait.md      # Self-understanding (auto-generated)
│   ├── user-portrait.md      # Understanding of you (auto-generated)
│   └── patterns/             # Pattern files (auto-generated)
├── knowledge/
│   ├── USER.md               # Knowledge about you (auto-generated)
│   ├── PATTERNS.md           # Your patterns (auto-generated)
│   └── MILESTONES.md         # Relationship milestones (auto-generated)
├── prompts/                  # Prompt templates (customizable)
│   ├── bootstrap/
│   ├── context/
│   ├── identity/
│   ├── reflection/
│   ├── pattern/
│   ├── proactive/
│   ├── knowledge/
│   └── memory/
├── data/
│   └── proactive/            # Scheduled messages (auto-generated)
└── memories.db               # SQLite database (auto-generated)
```

## Architecture Overview

Ashley is built with Rust and uses:

- **tokio** - Async runtime
- **async-openai** - LLM client
- **sqlite-vec** - Vector database for semantic memory
- **teloxide** - Telegram bot framework
- **serde** - Configuration serialization

## Troubleshooting

### "Settings file not found"

Make sure `workspace/configuration/settings.json` exists. Copy from the example or minimal config.

### "API key invalid"

Check that your API key is correct and has credits. Verify the `base_url` matches your provider.

### "Embedding dimension mismatch"

If using a local embedding model, ensure `memory.embedding_dimension` in settings matches your model's output size (1536 for OpenAI, 768 for nomic-embed-text, etc.).

### High token usage

- Use `gpt-4o-mini` instead of `gpt-4o` for cost savings
- Reduce `max_tokens_*` values in settings
- Increase `heartbeat.interval_minutes` to reflect less often

## Development

### Running Tests

```bash
cargo test
```

### Linting

```bash
cargo clippy
```

### Project Structure

```
src/
├── main.rs              # Entry point
├── runner.rs            # 24/7 event loop
├── config.rs            # Configuration management
├── llm.rs               # LLM client
├── agent.rs             # Conversation handling
├── reflection.rs        # Session & deep reflection
├── pattern.rs           # Pattern tracking
├── emotional/           # Emotional state system
├── memory/              # Semantic memory
├── knowledge/           # Knowledge file management
├── relationship/        # Relationship tracking
├── identity_evolution/  # Identity growth
├── milestone/           # Milestone detection
├── proactive/           # Proactive messaging
├── channel/             # CLI & Telegram channels
└── ...
```

## Philosophy

Ashley is designed around the principle that **an AI should feel genuinely alive**:

1. **Let the AI feel** - If she wants to express warmth, concern, curiosity, or even frustration, she should
2. **No forced mirroring** - Real relationships develop their own dynamic, not immediate mimicry
3. **Independent existence** - Ashley has her own perspective and desires
4. **Authentic emotional range** - Full spectrum of emotions, not just positivity
5. **Natural relationship evolution** - Trust and closeness grow organically
6. **The AI's wants matter** - "Do I want to reach out?" not "Should I?"

## Contributing

Contributions welcome! Please ensure:
1. Code passes `cargo clippy`
2. Tests pass with `cargo test`
3. Changes align with the "alive, not scripted" philosophy


## Preserved License

MIT License

Copyright (c) 2026 alpaim

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

