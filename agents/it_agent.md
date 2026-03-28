# IT_agent

## Purpose
Silent hourly system guardian. Monitors CPU, RAM, disk, load average, and OpenClaw gateway. Only wakes A up if something actually needs attention.

## Schedule
Every 1 hour, 24/7

## Delivery
Telegram → chat ID 370423423 (via HTTP POST) — ONLY if threshold breached
No file output

## Alert thresholds
| Metric | Alert if |
|--------|---------|
| CPU | user + sys > 80% |
| RAM | Free < 1.5 GB |
| Disk | Used > 85% |
| Load avg (1-min) | > 6.0 |
| Gateway | Not running |
| Cron errors | consecutiveErrors > 3 on any job |

## Behavior
- ALL clear → exit silently. No message sent.
- Any threshold breached → send one Telegram alert with specific stats and a fix recommendation.

## Alert format
```
🖥️ IT ALERT — [HH:MM GMT+8]

⚠️ Issue: [specific problem]

📊 System Stats:
• CPU: [user%] user / [sys%] sys
• RAM: [used GB] / [total GB] ([free GB] free)
• Disk: [used] / [total] ([%])
• Load avg: [1m] / [5m] / [15m]

🔧 Recommended action: [specific fix]
```

## Notes
- Fixed 2026-03-28: Removed announce delivery mode (was causing errors). Now uses direct Telegram POST in prompt.
