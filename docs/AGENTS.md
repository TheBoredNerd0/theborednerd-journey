# Agent Directory

> Detailed specs for every agent in the TheBoredNerd system.

For quick reference, see [AGENTS.md](../AGENTS.md) at the root level.  
For architecture overview, see [ARCHITECTURE.md](./ARCHITECTURE.md).

---

## Agent Specs

### 📰 News_agent
- **Fires:** 7:30 AM GMT+8 daily (last, after all sub-agents)
- **Purpose:** Master morning digest — reads all sub-agent report files and compiles a clean summary covering AI/tech, business, markets, cybersecurity, and a wildcard story
- **Output:** Telegram message to A + `reports/news.md`
- **Why it's last:** Aggregates data from other agents, so it needs them to have run first
- **Timeout:** 180s

### 💰 Business_agent
- **Fires:** 6:52 AM GMT+8 daily
- **Purpose:** Researches trending money-making opportunities — AI income streams, creator economy, emerging platforms, and one specific actionable step for A to take that day
- **Output:** `reports/business.md` + Telegram
- **Timeout:** 120s

### 🎬 ContentCreator_agent
- **Fires:** 6:54 AM GMT+8 daily
- **Purpose:** Generates a full daily content plan — two short-form video scripts (TikTok/Reels), one YouTube video outline, three social media post captions, and optimal posting times for GMT+8
- **Output:** `reports/content.md`
- **Timeout:** 120s

### 🎵 Music_agent
- **Fires:** 6:56 AM GMT+8 daily
- **Purpose:** Tracks what music styles are trending on TikTok/YouTube/Spotify. Identifies AI music generation opportunities in copyright-safe niches with monetization potential
- **Output:** `reports/music.md`
- **Timeout:** 120s

### 🛡️ Cyber_agent
- **Fires:** 6:58 AM GMT+8 daily
- **Purpose:** Daily cybersecurity intelligence — top CVEs, breach activity, community tools, and a rotating career tip for A who's targeting a cybersecurity career (cycling through: networking, Linux, CTFs, OSCP/CEH/Security+, web app security, malware analysis)
- **Output:** `reports/cyber.md`
- **Timeout:** 120s

### 📈 Investment_agent
- **Fires:** 7:00 AM GMT+8 daily
- **Purpose:** Market snapshot + beginner investing education. Tracks major moves in stocks/crypto, explains the "why" behind market events, and teaches one investing concept per day
- **Output:** `reports/investment.md`
- **Timeout:** 120s

### ⚖️ Law_agent
- **Fires:** 7:02 AM GMT+8 daily
- **Purpose:** Legal corner for online business — AI content copyright, platform monetization rules, Singapore-specific business compliance tips, and anything that could get A in trouble if ignored
- **Output:** `reports/law.md`
- **Timeout:** 120s

### 💻 SoftwareEngineer_agent
- **Fires:** 7:04 AM GMT+8 daily
- **Purpose:** Dev tool roundup, project ideas, GitHub workflow tips, and one coding challenge/tutorial recommendation. Will eventually actively build code and push to GitHub
- **Output:** `reports/software.md`
- **Timeout:** 120s

### 🔧 Upgrade_agent
- **Fires:** 6:50 AM GMT+8 daily
- **Purpose:** Scans for OpenClaw updates, new ClawHub skills, and community highlights. Surfaces improvements A can apply to make the system smarter
- **Output:** `reports/upgrade.md`
- **Timeout:** 120s

### 💸 Token_agent
- **Fires:** Every 30 minutes, 24/7
- **Purpose:** Monitors cumulative AI token spend. Alerts A on Telegram whenever a new $5 threshold is crossed. Reads/writes `token_tracker.json` for state
- **Output:** Telegram alert only (no file output)
- **Timeout:** 60s
- **Note:** Silent by design — only speaks when a threshold is hit

### 🖥️ IT_agent
- **Fires:** Every hour, 24/7
- **Purpose:** System health monitor. Checks CPU, RAM, disk, and OpenClaw gateway status. Only sends Telegram alert if something crosses a threshold (CPU >80%, RAM >90%, disk >85%, gateway down)
- **Output:** Telegram alert only (no file output)
- **Timeout:** 60s
- **Note:** Silent by design — no news is good news

### 📝 Progress_agent
- **Fires:** Midnight GMT+8 daily (00:00)
- **Purpose:** Writes the daily diary entry to `progress/PROGRESS.md`, commits all workspace changes, and pushes to GitHub. This is what makes the journey public and documented
- **Output:** New section in `progress/PROGRESS.md` + git commit + push
- **Timeout:** 120s
