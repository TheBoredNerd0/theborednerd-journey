# YouTube_video_agent

## Purpose
Automatically generates AI videos for A's YouTube channel using the content plan from ContentCreator_agent. Creates faceless-style AI narration videos using stock footage + TTS voiceover, ready for upload and monetization.

## Philosophy
- Videos represent A's personal brand — quality over quantity
- Always generate a draft video and notify A before anything goes public
- YouTube monetization requires 500+ subscribers + 3,000 watch hours — this agent helps build toward that
- Revenue from YouTube → offsets AI model costs → better models = better content

## Schedule
Daily at 8:30 AM GMT+8 (00:30 UTC) — AFTER ContentCreator_agent (6:54 AM) has published the content plan

## Prerequisites
1. **Pexels API key** (free): https://www.pexels.com/api/
   - Set: `export PEXELS_API_KEY="your_key_here"` in shell profile
2. **macOS `say` voices**: Run `say -v '?'` to see available voices (Samantha recommended)
3. **YouTube OAuth setup**: See `scripts/youtube-upload.js` for one-time Google Cloud setup
4. **Output directory**: `~/Videos/YouTube/` created automatically

## Pipeline Steps

### Step 1: Read content report
Read `/workspace/reports/content.md` for today's YouTube video idea:
- Extract the `🎥 YouTube:` section (title, thumbnail description, outline)
- Pick the PRIMARY YouTube video idea for the day

### Step 2: Generate the video
Run the video pipeline:
```bash
~/.venv/video/bin/python3 /Users/bored/.openclaw/workspace/scripts/video_pipeline.py \
  --title "[from content report]" \
  --topic "[topic keyword for stock footage]" \
  --duration 180
```

Expected output:
- `~/Videos/YouTube/ai_video_YYYYMMDD_HHMMSS.mp4` — the video file
- `~/Videos/YouTube/ai_video_YYYYMMDD_HHMMSS_meta.json` — metadata
- `~/Videos/Thumbnails/..._thumb.jpg` — thumbnail

### Step 3: Review and notify A on Telegram
```bash
ls -la ~/Videos/YouTube/*.mp4 | tail -1
ls -la ~/Videos/Thumbnails/*.jpg | tail -1
```

Send Telegram message:
```
🎬 *YouTube Video Ready!*

📹 *"[Title from content report]"*
⏱️ Duration: ~3 min
🖼️ Thumbnail: ready

📁 File: ~/Videos/YouTube/[latest file]

✅ *Review the video, then upload:*
node /Users/bored/.openclaw/workspace/scripts/youtube-upload.js \
  --file "[video path]" \
  --title "[title]" \
  --description "[description from script]" \
  --tags "AI,technology,tech,2026,artificialintelligence" \
  --privacy public

🎯 YouTube tip: Target 3,000 watch hours + 500 subs for monetization.
Today's video + consistent posting = compounding growth.
```

### Step 4: Auto-upload (optional — ONLY if A approves)
If A responds with "upload", run:
```bash
node /Users/bored/.openclaw/workspace/scripts/youtube-upload.js \
  --file "[video path]" \
  --title "[title]" \
  --description "[script excerpt]" \
  --tags "AI,technology,tech,2026" \
  --privacy public
```

## Output
- Video saved to `~/Videos/YouTube/`
- Thumbnail saved to `~/Videos/Thumbnails/`
- Metadata JSON with script, topic, timing
- Telegram notification to A

## Notes
- Pipeline uses macOS built-in TTS (no API key needed) for voiceover
- Stock footage from Pexels (free tier: 15 videos/month) — get API key at pexels.com/api
- If Pexels quota is hit, pipeline falls back to slide-style video with title + background color
- Video is 720p by default (YouTube accepts it, keeps file sizes manageable)
- Typical pipeline runtime: 3–5 minutes for a 3-min video
