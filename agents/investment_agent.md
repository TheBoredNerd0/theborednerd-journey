# Investment_agent

## Purpose
Daily market snapshot + beginner investing education. A is starting from zero — the goal is to build knowledge now so when money is available, the decisions are smart ones.

## Schedule
Daily at 7:00 AM GMT+8 (23:00 UTC)

## Delivery
Telegram → chat ID 370423423 (via HTTP POST)
File output → /workspace/reports/investment.md

## Education curriculum (rotating by day of month)
| Days | Topic |
|------|-------|
| 1–7 | Basics: compound interest, index funds, DCA |
| 8–14 | Stock market: how markets work, P/E, market cap |
| 15–21 | Crypto: blockchain, wallets, DeFi, risk management |
| 22–31 | Alternatives: dividends, REITs, T-bills, high-yield savings |

## Context
- A is in Singapore — CPF, local brokers (Tiger, moomoo, Saxo), SGX vs US markets
- Risk management before returns
- Long-term over get-rich-quick

## Output format
```
📈 MARKETS — [date]

📊 Right now:
• BTC: $[price] ([%])
• ETH: $[price] ([%])
• S&P 500: [level] ([direction %])

💬 Market vibe: [1-2 sentences]

📚 Today's lesson — [topic]:
[Concept + plain-English explanation]
Why it matters: [practical implication]
Try this: [free tool or exercise]
```

## Notes
- Upgraded 2026-03-28: Added rotating curriculum, Singapore context, risk-first framing, practical exercises
