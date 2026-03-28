# System Upgrade Report — 2026-03-29

## OpenClaw Version
- **Installed:** 2026.3.24 (cff6dc9)
- **Latest stable:** 2026.3.24 (no newer stable release)
- **Latest beta:** 2026.3.28-beta.1 (pre-release, not recommended for production)

## Beta Highlights (2026.3.28-beta.1)
- **MiniMax image generation** — first-class image-01 model support with generate + image-to-image editing
- **xAI Responses API** — bundled Grok provider migrated to Responses API with x_search
- **async requireApproval hooks** — plugins can now pause tool execution for user approval (e.g., /approve command works for both exec and plugin hooks)
- **OpenAI apply_patch** — enabled by default for OpenAI and Codex models
- **Gemini CLI backend** — now bundled as a plugin backend
- **Slack upload-file** action — explicit file upload support
- **WhatsApp fix** — infinite echo loop in self-chat DM mode resolved
- **Telegram HTML fix** — long messages split at word boundaries instead of mid-word

## AI Model News
- MiniMax trimmed model catalog to M2.7 only (removed legacy M2, M2.1, M2.5, VL-01) — A is on M2.7 ✅
- Google Gemini 3.1 pro/flash/flash-lite provider aliases fixed
- OpenAI Codex image tools now properly registered for media understanding

## ClawHub Skills
- No new skills published on ClawHub this week (site is still very early)
- A can check manually: https://clawhub.ai/skills

## System Health

### Gateway
- **Status:** ✅ Running (pid 42186)
- **Bind:** loopback only (127.0.0.1:18789)
- **RPC probe:** ok

### Cron Jobs
| Agent | Status |
|-------|--------|
| Upgrade_agent | ✅ running |
| IT_agent | ✅ ok |
| Token_agent | ✅ ok |
| News_agent | ⚠️ error |
| YouTube_video_agent | ⏸️ idle |
| Business_agent | ⚠️ error |
| ContentCreator_agent | ⚠️ error |
| Music_agent | ⚠️ error |
| Cyber_agent | ⚠️ error |
| Investment_agent | ⚠️ error |
| Law_agent | ⚠️ error |
| SoftwareEngineer_agent | ⚠️ error |
| Progress_agent | ⚠️ error |

**7 agents stuck in ERROR state.** The TOOLS.md notes this was a billing/config issue that was "supposedly fixed" — but they're still erroring. Likely the same Anthropic API billing issue persisting.

## Recommendations
1. **Investigate the 7 failing cron agents** — they all use `sessionTarget: "isolated"` with `agentTurn` payload. Run `openclaw logs --tail 100` to check if they're hitting `403/billing_required` errors from Anthropic, or check `/tmp/openclaw/openclaw-2026-03-29.log`
2. **Consider upgrading to beta** — 2026.3.28-beta.1 is lightweight to test: `openclaw upgrade --pre`
3. **No new ClawHub skills** to install this week
