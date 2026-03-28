# System Architecture — TheBoredNerd AI Setup

> Last updated: 2026-03-28

This document explains how the full agent system is built, what runs where, and why it's structured the way it is.

---

## Overview

The system is built on **[OpenClaw](https://openclaw.ai)** — an AI agent framework that runs locally on a Mac mini. Everything talks through a single gateway process, and agents deliver their output to Telegram so A can consume it from anywhere on their phone.

```
┌─────────────────────────────────────────────────────────┐
│                     Mac mini (home)                     │
│                                                         │
│  ┌──────────────┐     ┌─────────────────────────────┐  │
│  │  OpenClaw    │────▶│  Gateway (WebSocket bridge)  │  │
│  │  Agent Core  │     └───────────────┬─────────────┘  │
│  └──────┬───────┘                     │                 │
│         │                             ▼                 │
│  ┌──────▼───────────────────────────────────────────┐   │
│  │              Cron Scheduler                       │   │
│  │  Token_agent  IT_agent  News_agent  Business_... │   │
│  └──────────────────────────────┬────────────────────┘  │
│                                 │                        │
│  ┌──────────────┐              │                        │
│  │   Workspace  │◀─────────────┤                        │
│  │  (this repo) │  reads/writes│                        │
│  └──────────────┘              │                        │
└────────────────────────────────┼────────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────┐
                    │  Telegram Bot API  │
                    │  @TheBoredNerd_bot │
                    └────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────┐
                    │  A's Phone         │
                    │  (@Rand0mdude)     │
                    └────────────────────┘
```

---

## Core Components

### OpenClaw Agent Core
The central brain. Runs Claude Sonnet as the model. Handles all agent turns, tool calls (web search, file read/write, shell exec), and session management.

- **Agent ID:** `main`
- **Model:** `anthropic/claude-sonnet-4-6`
- **Shell:** zsh on Darwin (arm64)

### Gateway
The WebSocket bridge that connects local OpenClaw to external services and handles delivery routing. Always-on, managed via `openclaw gateway start/stop/status`.

### Cron Scheduler
Handles all timed agent invocations. Each cron job is an isolated session with its own timeout, payload (the agent's system prompt/task), and delivery config.

- Jobs are stored persistently in OpenClaw's local database
- Isolated sessions mean agents don't share context and can't interfere with each other
- Most agents have 120-second timeouts; monitoring agents have 60s

### Workspace (this repo)
The filesystem layer. Agents read from and write to this directory. It's also a git repo that auto-pushes to GitHub so everything is publicly documented.

```
workspace/
├── agents/         # Agent prompt files (documentation)
├── docs/           # Architecture docs (this file)
├── media/          # Video files, TikTok content
├── memory/         # Daily session logs (YYYY-MM-DD.md)
├── progress/       # Public progress diary (PROGRESS.md)
├── reports/        # Agent output files (overwritten daily)
│   ├── business.md
│   ├── content.md
│   ├── cyber.md
│   ├── investment.md
│   ├── law.md
│   ├── music.md
│   ├── news.md
│   ├── software.md
│   └── upgrade.md
├── AGENTS.md       # Agent directory (root level)
├── MEMORY.md       # Long-term AI memory
├── README.md       # Public-facing project overview
├── SOUL.md         # AI persona/personality definition
├── TOKEN_tracker.json
├── TOOLS.md        # Local config notes
└── USER.md         # Info about A (private context)
```

---

## Agent Architecture

Each agent follows the same pattern:

1. **Trigger:** Cron scheduler fires at configured time
2. **Spin up:** OpenClaw spawns an isolated agent session
3. **Execute:** Agent receives its task prompt, uses tools (web_search, exec, write) to do research
4. **Write:** Agent saves findings to `reports/<agent>.md`
5. **Deliver:** Agent sends formatted output to Telegram via HTTP POST to Bot API
6. **Terminate:** Session ends, resources freed

### Why isolated sessions?
Each agent runs in a clean context with no shared state. This means:
- Agents can't accidentally read each other's partial output
- Failures in one agent don't cascade
- Token usage is cleanly scoped per agent
- Easier debugging — each agent's logs are separate

---

## Delivery Pipeline

All agents ultimately deliver to Telegram via the bot API:

```
POST https://api.telegram.org/bot{TOKEN}/sendMessage
{
  "chat_id": 370423423,
  "text": "...",
  "parse_mode": "Markdown"
}
```

Some agents also write to `reports/` for a persistent record. The News_agent is the aggregator — it fires last at 7:30 AM and compiles a master digest pulling from all the sub-agent report files.

---

## GitHub Integration

The workspace is a git repo tracked at `github.com/TheBoredNerd0/theborednerd-journey`.

The Progress_agent runs at midnight and:
1. Writes a new day entry to `progress/PROGRESS.md`
2. Commits all workspace changes
3. Pushes to GitHub

This creates a real-time public log of the entire AI journey.

---

## Security Model

- All secrets (bot token, API keys) are in TOOLS.md which is **not committed to GitHub** via .gitignore
- Agents run as isolated sessions — minimal blast radius if one breaks
- No external auth is stored in the workspace directory
- The Mac mini runs behind a home router; gateway only exposes WebSocket to localhost + Tailscale

---

## Scaling & Future Plans

The current system handles ~12 agents on a Mac mini (M-series, 16GB RAM) with zero performance issues. Load average stays well under 1.0 during off-peak hours.

Planned additions:
- **SoftwareEngineer_agent** — actively writes code and pushes to GitHub on demand
- **YouTube upload pipeline** — once YouTube API credentials are configured
- **Cross-agent memory** — shared `reports/` directory is the beginning of this
- **Web dashboard** — reading `reports/` and rendering a local dashboard
