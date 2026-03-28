# Upgrade_agent

## Purpose
Daily scan of OpenClaw updates, new ClawHub skills, community highlights, and AI model improvements. Also runs system diagnostics and reports cron job health.

## Schedule
Daily at 6:50 AM GMT+8 (22:50 UTC) — fires FIRST

## Delivery
Telegram → chat ID 370423423 (via HTTP POST in agent prompt)
File output → /workspace/reports/upgrade.md

## Research focus
- OpenClaw GitHub releases (latest version vs installed)
- New skills on clawhub.ai
- Claude/model improvements
- AI agent tool comparisons
- System diagnostics: cron job status, gateway health, installed version

## Output format
```
🔧 SYSTEM UPGRADE — [date]

📦 OpenClaw: v[installed] — [up to date / update available: v[new]]

🧩 New skills worth installing:
• [skill] — [what it does] — clawhub install [name]

🤖 AI model news: [Claude/model improvements]

⚠️ System health:
• Cron jobs: [X ok, Y idle, Z errors]
• Gateway: [status]

💡 Recommendation: [ONE concrete improvement]
```

## Notes
- Upgraded 2026-03-28: Added version checking, system diagnostics, cron job health, actual clawhub install commands
