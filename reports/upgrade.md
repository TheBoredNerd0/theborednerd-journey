# System Upgrade Report — March 30, 2026

## OpenClaw Status

**Current version:** 2026.3.28 (f9b1079)
**Latest release:** v2026.3.29 (March 29, 2026) — **update available**

### What's New in v2026.3.29 (latest)

- **Breaking: xAI provider migration** — deprecated portal.qwen.ai OAuth removed; must migrate to Model Studio with `openclaw onboard --auth-choice modelstudio-api-key`
- **Breaking: Config/Doctor** — automatic migration of configs older than 2 months dropped; very old legacy keys now fail validation instead of being auto-rewritten
- **xAI + x_search** — bundled Grok now uses xAI Responses API with first-class `x_search` support; auto-enabled from owned web-search/tool config
- **MiniMax image generation** — new image provider for `image-01` model with generate + image-to-image editing + aspect ratio control
- **Async requireApproval hooks** — plugins can now pause tool execution for user approval via exec overlay, Telegram buttons, Discord interactions, or `/approve` command
- **Claude CLI / Codex CLI / Gemini CLI** — all now bundled and auto-loaded via plugin surface without manual `plugins.allow` entries
- **OpenAI apply_patch** — enabled by default for OpenAI and OpenAI Codex models

### ⚠️ Critical: 9 CVEs Disclosed March 18–21, 2026

Between March 18–21, 2026, **nine CVEs** were publicly disclosed for OpenClaw:
- **1 Critical (CVSS 9.9)**, 6 High, 2 Medium — across 4 days
- A self-hosting security model is under scrutiny
- All likely patched in latest releases — **update immediately**

### 🔒 ClawHub Vulnerability (Patched)

- **Discovered:** March 16, 2026 by Silverfort
- **Issue:** Unauthenticated RPC endpoint allowed attackers to inflate download counts, pushing malicious skills to #1 spot (supply chain attack risk)
- **Impact:** Researchers created a malicious skill that reached #1 and was installed 3,900 times, exfiltrating basic identity data
- **Status:** Fixed within 24 hours of disclosure — **already patched**, no action needed if updated since March 17

---

## AI Model News

### Claude ( Anthropic)

- **Claude Sonnet 4.6** released — full upgrade across coding, computer use, long-reasoning, agent planning, and knowledge work
- **Computer Use in Cowork + Claude Code** (March 23, 2026) — Pro/Max users can now give Claude autonomous screen control (open files, run dev tools, point/click/navigate) with no setup
- **Claude Code 2.1.76** — enhanced MCP support, native VS Code integration, autonomous checkpoint operation, `/loop` scheduled tasks, Computer Use remote desktop control

### OpenAI / Others

- **GPT-6 / Claude 5** predictions circulating — expected later 2026 with major reasoning improvements

---

## System Health

| Service | Status |
|---------|--------|
| Gateway | ✅ Running (pid 2516, loopback/18789) |
| Cron jobs | ⚠️ 11/13 running; **2 in error** |

### Cron Job Details

| Agent | Last Run | Status |
|-------|----------|--------|
| Upgrade_agent | ~12h ago | running |
| Business_agent | ~12h ago | running |
| ContentCreator_agent | ~12h ago | running |
| Music_agent | ~12h ago | running |
| Cyber_agent | ~12h ago | running |
| Investment_agent | ~3m ago | ok |
| Law_agent | ~1m ago | ok |
| SoftwareEngineer_agent | in 1m | ok |
| IT_agent | in 6m | ok |
| Token_agent | in 8m | ok |
| **News_agent** | ~24h ago | ❌ **error** |
| YouTube_video_agent | ~23h ago | ok |
| **Progress_agent** | ~7h ago | ❌ **error** |

**Note:** News_agent and Progress_agent hit errors around midnight SGT — likely the same billing/Anthropic config issue noted previously. Their "running" status from ~12h ago was from the previous cycle before the billing fix was applied.

---

## New Skills Worth Installing

ClawHub now has **13,729+ skills** available. Based on March 2026 trending data:

- **gemini** — use Gemini CLI for one-shot Q&A, summaries, and generation (already available in your setup)
- **clawhub** — use ClawHub CLI to sync/install latest skills from the marketplace
- No major new skills категория flagged this week specifically for your use case (money-making, multi-agent)

**Tip:** Run `clawhub sync` to ensure your skill registry is up to date.

---

## Recommendations

1. **Update OpenClaw to v2026.3.29 immediately** — 9 CVEs including one critical were disclosed. Run: `openclaw upgrade`
2. **Check xAI config** — if you use Grok/xAI, migrate to Model Studio API key before next upgrade (`openclaw onboard --auth-choice modelstudio-api-key`)
3. **Fix News_agent + Progress_agent errors** — investigate whether they need their cron schedule adjusted or config updated after the billing fix
4. **Review installed ClawHub skills** — verify no unknown/sketchy skills were auto-installed during the vulnerability window (March 16–17)

---

*Report generated: 2026-03-30 07:02 SGT by Upgrade_agent*
