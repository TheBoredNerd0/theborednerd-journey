# TOOLS.md - Local Notes

## Telegram
- Bot name: TheBoredNerd_bot (@TheBoredNerd_bot)
- Bot token: 8674231479:AAHiA-EqW7Xpq_t-4VV2tXR8gCGQNJ-sm6Y
- A's chat ID: 370423423
- A's Telegram: @Rand0mdude

## GitHub
- Account: TheBoredNerd0
- Repo: theborednerd-journey (public)
- GitHub Pages: https://theborednerd0.github.io/theborednerd-journey/
- Status: ✅ Connected (Token: gho_...)

## User
- Gmail: theborednerd0@gmail.com
- GitHub: ✅ Set up

## ─── VIDEO PIPELINE ──────────────────────────────────────────────────────────

## YouTube Auto-Video Setup (ONE-TIME)

### 1. Pexels API Key (free — 15 videos/month)
→ https://www.pexels.com/api/
→ Sign up → Copy API key
→ Add to shell profile (~/.zshrc):
  export PEXELS_API_KEY="your_key_here"

### 2. macOS TTS Voice (already set up)
→ Default voice: Samantha
→ Test: `say -v Samantha "Hello world"`
→ List all: `say -v '?'`

### 3. YouTube OAuth (for auto-upload)
→ Follow steps in: scripts/youtube-upload.js (header comments)
→ TL;DR:
  1. Go to console.cloud.google.com
  2. Create project → enable "YouTube Data API v3"
  3. Credentials → OAuth client ID → Desktop app
  4. Download JSON → save as ~/.openclaw/credentials/youtube-oauth.json
  5. First run will open browser for auth

### 4. Virtual Environment
→ Already created at ~/.venv/video/
→ To reinstall: python3 -m venv ~/.venv/video && ~/.venv/video/bin/pip install moviepy requests Pillow pydub

## Video Pipeline Usage
~/.venv/video/bin/python3 /Users/bored/.openclaw/workspace/scripts/video_pipeline.py \
  --title "Video Title Here" \
  --topic "keyword for stock footage" \
  --duration 180

Output goes to: ~/Videos/YouTube/

## YouTube Upload
node /Users/bored/.openclaw/workspace/scripts/youtube-upload.js \
  --file "path/to/video.mp4" \
  --title "Your Title" \
  --description "Your description..." \
  --tags "AI,technology,tech" \
  --privacy public

## YouTube Monetisation Requirements
→ 500+ subscribers
→ 3,000+ watch hours (past 12 months)
→ Current strategy: consistent posting of short AI/news videos

## ─── AGENTS ───────────────────────────────────────────────────────────────────

All agents use minimax/MiniMax-M2.7 (configured as default model).

| Agent | Schedule (SGT) | Status |
|-------|---------------|--------|
| token_agent | Every 30m | ✅ Running |
| it_agent | Every 1h | ✅ Running |
| upgrade_agent | 6:50 AM | ✅ Scheduled |
| business_agent | 6:52 AM | ✅ Scheduled |
| content_agent | 6:54 AM | ✅ Scheduled |
| music_agent | 6:56 AM | ✅ Scheduled |
| cyber_agent | 6:58 AM | ✅ Scheduled |
| investment_agent | 7:00 AM | ✅ Scheduled |
| law_agent | 7:02 AM | ✅ Scheduled |
| software_agent | 7:04 AM | ✅ Scheduled |
| news_agent | 7:30 AM | ✅ Scheduled |
| youtube_video_agent | 8:30 AM | ✅ Scheduled |
| progress_agent | Midnight | ✅ Scheduled |

## ─── EXEC POLICY ─────────────────────────────────────────────────────────────

tools.exec.security is set to "full" to allow all commands (no allowlist blocking).
If commands fail, check: openclaw gateway status

## ─── GITHUB PUSH ─────────────────────────────────────────────────────────────

Workspace is a git repo. To commit and push:
```bash
cd /Users/bored/.openclaw/workspace
git add -A
git commit -m "describe changes"
git push origin main
```

Daily digest auto-pushes to GitHub Pages (docs/index.html → theborednerd0.github.io/theborednerd-journey/)
