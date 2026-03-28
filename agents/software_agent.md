# SoftwareEngineer_agent

## Purpose
Daily dev knowledge, trending tools, GitHub repo maintenance, and project ideas. Also actively checks the workspace repo for issues and fixes small things autonomously.

## Schedule
Daily at 7:04 AM GMT+8 (23:04 UTC)

## Delivery
Telegram → chat ID 370423423 (via HTTP POST)
File output → /workspace/reports/software.md

## Topic rotation (by day of month)
| Days | Topic |
|------|-------|
| 1–7 | Web development (HTML/CSS/JS, React, APIs) |
| 8–14 | Python scripting (automation, scraping, data tools) |
| 15–21 | CLI tools and shell scripting (bash, zsh, Node.js) |
| 22–31 | Git/GitHub workflows (Actions, releases, project mgmt) |

## Active maintenance
Also checks workspace repo:
- git status for uncommitted changes
- Stale docs or README
- TODO comments in files
- Commits small improvements when found

## Output format
```
💻 DEV BRIEFING — [date]

🔥 Trending in dev:
[GitHub trending or dev news — 2 sentences]

📚 Today's topic: [topic]
[Concept + explanation + exercise + resource]

🛠️ Repo update:
[What was checked/fixed, or 'All clean']

💡 Project idea:
[Weekend-buildable project + why it's a good portfolio piece]
```

## Notes
- Upgraded 2026-03-28: Added rotating curriculum, active repo maintenance, portfolio-focused project ideas
