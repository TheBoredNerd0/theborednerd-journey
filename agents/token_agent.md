# Token_agent

## Purpose
Monitors AI token spend. Alerts A on Telegram whenever a new $5 threshold is crossed. Runs silently every 30 minutes — only speaks when there's something to report.

## Schedule
Every 30 minutes, 24/7

## Delivery
Telegram → chat ID 370423423 (via HTTP POST) — ONLY when new threshold crossed
State file → /workspace/token_tracker.json

## Logic
1. Read current cost from `session_status`
2. Calculate: `floor(cost / 5) * 5` = current threshold
3. Read `token_tracker.json` for last notified threshold
4. If current > last → send alert + update tracker
5. If same → exit silently

## Alert format
```
💸 TOKEN ALERT

You've crossed the $[threshold] mark!

📊 Total spent: ~$[amount]
⚡ Next alert at: $[threshold + 5]

Tip: ask me for a full breakdown anytime.
```

## Notes
- Working correctly as of Day 1
