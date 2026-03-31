# System Upgrade Report — March 31, 2026

## OpenClaw Version

**Current:** 2026.3.28 | **Latest on GitHub:** 2026.3.29 (March 29 release)
**Status:** ⚠️ Minor update available (1 day behind)

### Latest OpenClaw Changes (v2026.3.29)
- **Breaking:** Qwen provider OAuth removed — migrate to Model Studio with `openclaw onboard --auth-choice modelstudio-api-key`
- **Config/Doctor:** Dropped automatic config migrations older than 2 months
- **MiniMax:** Image generation provider added for `image-01` model (aspect ratio control, image-to-image editing) — directly relevant to your video pipeline!
- **xAI:** Grok web search now uses Responses API with `x_search`; auto-enabled for bundled xAI plugin users
- **Plugin hooks:** `before_tool_call` hooks can now request approval via exec overlay, Telegram buttons, Discord, or `/approve` command
- **Claude/Codex/Gemini CLI backends:** Moved onto the plugin surface; bundled Gemini CLI now supported
- **ACP channels:** Discord, BlueBubbles, iMessage now support current-conversation ACP binds

### ⚠️ Security Advisory (Critical)
**CVE-2026-25253** — Gateway RCE vulnerability (CVSS 9.8)
- Actively exploited in the wild
- Affects all versions prior to v3.x
- Your version (2026.3.28) should include the patch, but **verify with:**
  ```
  openclaw doctor --security
  ```
- A's gateway is bind=loopback (127.0.0.1) ✅ — hardened default is applied

---

## AI Model News

### Claude Code — Massive March 2026 Update (v2.1.63 → v2.1.76)
- **Opus 4.6** is now the default model (replaces Opus 4/4.1)
- **1 million token context window** for Opus 4.6 (Max/Team/Enterprise)
- **Voice mode** rolling out — push-to-talk with spacebar, 20 languages (was 10)
- **/loop command** — lightweight recurring cron-like monitoring directly in terminal
- **/effort** — new command: set analysis depth (○ low / ◐ medium / ● high)
- **/color** — customize session prompt color
- **/simplify & /batch** — code simplification and batch operations

### ClawHub Ecosystem
- 13,000+ skills available (up from ~3,000 in Feb 2026)
- 2,400+ malicious skills removed post-ClawHavoc incident
- **VirusTotal integration** now on all newly uploaded skills
- **Skill signature verification** in beta (signed skills can be enforced)
- New security guide for safe installs: see blink.new blog

---

## System Health

| Check | Status |
|---|---|
| OpenClaw version | ✅ 2026.3.28 |
| Gateway | ✅ Running (127.0.0.1:18789, RPC probe OK) |
| Cron jobs | ⚠️ 10 OK, **3 error** |

### Cron Job Errors
| Agent | Issue |
|---|---|
| Token_agent | Error (last ran 17 min ago) |
| News_agent | Error (last ran 23h ago) |
| Progress_agent | Error (last ran 7h ago) |

> These 3 agents were previously flagged with billing/Anthropic config issues. The config was supposedly fixed — investigate why they're still erroring.

---

## Recommended Actions

1. **Update OpenClaw to latest:**
   ```bash
   npm install -g @openclaw/cli@latest
   ```
   Then re-run `openclaw --version` to confirm.

2. **Verify CVE patch:**
   ```bash
   openclaw doctor --security
   ```

3. **Investigate the 3 failing cron agents** — run each one manually to see the actual error:
   ```bash
   openclaw cron run Token_agent
   openclaw cron run News_agent
   openclaw cron run Progress_agent
   ```

4. **Try Memory System v2 preview** (vectorized search, PII redaction, cross-agent memory):
   ```bash
   openclaw start --experimental-memory-v2
   ```

5. **MiniMax image-01 model** is now available — could enhance your video pipeline thumbnails without changing your existing setup.

---

## Full Cron Status
```
Upgrade_agent          ✅ running (current)
Business_agent         ✅ ok (in 2m)
ContentCreator_agent   ✅ ok (in 4m)
Music_agent            ✅ ok (in 6m)
Cyber_agent            ✅ ok (in 8m)
Investment_agent       ✅ ok (in 10m)
Law_agent              ✅ ok (in 12m)
Token_agent            ❌ error (in 13m)
SoftwareEngineer_agent ✅ ok (in 14m)
News_agent             ❌ error (in 40m)
YouTube_video_agent    ✅ ok (in 2h)
Progress_agent         ❌ error (in 17h)
```
