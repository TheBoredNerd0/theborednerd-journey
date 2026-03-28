# THEBOREDNERD BACKUP & RESTORE GUIDE

Last updated: 2026-03-28

---

## ✅ WHAT'S ALREADY BACKED UP TO GITHUB

The entire workspace is a git repo pushed to:
→ `https://github.com/TheBoredNerd0/theborednerd-journey`

This includes:
- `agents/` — all 14 agent spec files
- `scripts/` — video_pipeline.py, youtube-upload.js, youtube-auth.py
- `reports/` — daily report outputs
- `docs/` — HTML digest pages for GitHub Pages
- `AGENTS.md`, `SOUL.md`, `USER.md`, `IDENTITY.md`, `TOOLS.md`, `MEMORY.md`
- `memory/` — daily memory files

---

## ⚠️ WHAT'S NOT ON GITHUB (NEEDS MANUAL BACKUP)

These are in `~/.openclaw/credentials/` and system files:

### API Keys & Tokens
```
~/.openclaw/credentials/
  youtube-oauth.json       ← Google OAuth client ID + secret
  youtube-token.json       ← YouTube access/refresh token
  video-apis.json         ← Pexels + Pixabay + Kling API keys
  telegram-*.json          ← Telegram session credentials
```

### Shell Environment Variables
```
~/.zshrc                  ← PEXELS_API_KEY, PIXABAY_API_KEY, KLING_ACCESS/SECRET_KEY
```

### Video Processing Environment
```
~/.venv/video/           ← Python virtual env with moviepy, Pillow, requests
```

### Cron Jobs & LaunchAgents
```
~/.openclaw/              ← Gateway config, cron schedules, agent state
~/Library/LaunchAgents/    ← OpenClaw LaunchAgent
```

### Homebrew Packages
```
/opt/homebrew/bin/        ← yt-dlp, ffmpeg, node/npm
```

---

## 🔧 ONE-COMMAND BACKUP

Run this to back up EVERYTHING to a USB drive or external disk:

```bash
BACKUP_DIR="/path/to/backup/drive"  # <-- change this!

mkdir -p "$BACKUP_DIR/TheBoredNerd_backup"

# 1. Clone/pull the GitHub repo (workspace)
cd ~/.openclaw/workspace && git push origin main

# 2. Copy all credentials and keys
mkdir -p "$BACKUP_DIR/TheBoredNerd_backup/credentials"
cp -r ~/.openclaw/credentials/ "$BACKUP_DIR/TheBoredNerd_backup/"
cp ~/.zshrc "$BACKUP_DIR/TheBoredNerd_backup/zshrc_backup.txt"

# 3. Export cron jobs config
cp -r ~/.openclaw/cron/ "$BACKUP_DIR/TheBoredNerd_backup/cron/"

# 4. Export OpenClaw config
cp ~/.openclaw/openclaw.json "$BACKUP_DIR/TheBoredNerd_backup/openclaw.json"

# 5. Copy virtual environment (large - ~500MB)
cp -r ~/.venv/video "$BACKUP_DIR/TheBoredNerd_backup/"

# 6. List of installed brew packages
brew bundle dump --file="$BACKUP_DIR/TheBoredNerd_backup/Brewfile" 2>/dev/null

echo "✅ Backup complete → $BACKUP_DIR/TheBoredNerd_backup/"
```

---

## 🚀 RESTORE ON A NEW MAC (or after wipe)

### Step 1: Clone GitHub repo
```bash
git clone https://github.com/TheBoredNerd0/theborednerd-journey.git ~/.openclaw/workspace
```

### Step 2: Restore API keys
```bash
# From your backup drive, copy credentials back
cp -r /path/to/backup/TheBoredNerd_backup/credentials/* ~/.openclaw/credentials/
cp /path/to/backup/TheBoredNerd_backup/zshrc_backup.txt ~/.zshrc
source ~/.zshrc
```

### Step 3: Reinstall OpenClaw
```bash
brew install openclaw
openclaw setup
```

### Step 4: Reinstall video processing tools
```bash
brew install yt-dlp ffmpeg
python3 -m venv ~/.venv/video
~/.venv/video/bin/pip install moviepy requests Pillow pydub googleapis
```

### Step 5: Restart gateway
```bash
openclaw gateway restart
```

---

## 📋 KEY FILES REFERENCE

| Item | Location |
|------|----------|
| Workspace (git) | `~/.openclaw/workspace/` |
| OpenClaw config | `~/.openclaw/openclaw.json` |
| Gateway credentials | `~/.openclaw/credentials/` |
| API keys (env) | `~/.zshrc` |
| Video pipeline | `~/.venv/video/` |
| YouTube upload script | `~/.openclaw/workspace/scripts/youtube-upload.js` |
| Video pipeline script | `~/.openclaw/workspace/scripts/video_pipeline.py` |
| Daily HTML digest | `~/.openclaw/workspace/docs/index.html` |

---

## 🔑 WHERE TO FIND API KEYS

| Service | Where it's stored |
|---------|------------------|
| Pexels | `~/.zshrc` + `~/.openclaw/credentials/video-apis.json` |
| Pixabay | `~/.zshrc` + `~/.openclaw/credentials/video-apis.json` |
| Kling AI | `~/.zshrc` + `~/.openclaw/credentials/video-apis.json` |
| YouTube OAuth | `~/.openclaw/credentials/youtube-oauth.json` + `youtube-token.json` |
| Telegram | `~/.openclaw/credentials/telegram-*.json` |

---

## 💡 PRO TIP: ENCRYPTED OFFSITE BACKUP

For extra safety, also copy the `credentials/` folder to a password-protected ZIP:
```bash
zip -er credentials_backup.zip ~/.openclaw/credentials/
# stores encrypted — safe to upload to Google Drive/iCloud
```
