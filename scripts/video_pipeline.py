#!/usr/bin/env python3
"""
AI Video Pipeline — TheBoredNerd
Turns a topic/title into a YouTube-ready video automatically.

Prerequisites (one-time setup):
  python3 -m venv ~/.venv/video
  ~/.venv/video/bin/pip install moviepy requests Pillow pydub

Usage:
  ~/.venv/video/bin/python3 video_pipeline.py \
    --title "Why AI Will Change Everything in 2026" \
    --topic "AI trends" \
    --duration 180 \
    --output ~/Videos/ai-video.mp4

The pipeline:
  1. Generate script (TopicResearcher + ScriptWriter)
  2. Download stock footage from Pexels (free API)
  3. Generate voiceover using macOS 'say' TTS
  4. Download thumbnail from Unsplash
  5. Assemble video clips + voiceover using MoviePy
  6. Output YouTube-ready MP4 + thumbnail
"""

import argparse
import json
import os
import sys
import subprocess
import time
import re
from pathlib import Path

# Add virtual env paths
VENV_BIN = Path.home() / ".venv" / "video" / "bin"
PYTHON = VENV_BIN / "python3"

import requests
from moviepy import (
    VideoFileClip, AudioFileClip, ImageClip, concatenate_videoclips,
    CompositeVideoClip, ColorClip, TextClip
)
from PIL import Image
import urllib.request

# ─── CONFIG ──────────────────────────────────────────────────────────────────

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")
OUTPUT_DIR = Path.home() / "Videos" / "YouTube"
THUMBNAIL_DIR = Path.home() / "Videos" / "Thumbnails"
TTS_VOICE = "Samantha"  # macOS voice — run `say -v '?'` to see all voices
TTS_SPEED = 165  # words per minute — adjust for pacing

# ─── SETUP ────────────────────────────────────────────────────────────────────

def setup():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📁 Output dir: {OUTPUT_DIR}")

# ─── SCRIPT GENERATOR ─────────────────────────────────────────────────────────

def generate_script(topic: str, duration_sec: int = 180) -> str:
    """
    Generate a YouTube video script for the given topic.
    Returns a string with intro, body sections, and outro.
    The script is written to be spoken aloud — conversational, punchy.
    """
    print(f"\n✍️  Generating script for: {topic} ({duration_sec}s)")

    prompt = f"""You are a YouTube scriptwriter for an AI/tech channel called TheBoredNerd.
Write a {duration_sec}-second YouTube video script for the topic: "{topic}".

Rules:
- Written in first person, casual but informative — like explaining to a smart friend
- Hook in the first 10 seconds — make someone stop scrolling
- Use 3-4 distinct sections, each ~30-40 seconds
- Include a "wait for it" moment or surprising stat in the middle
- End with a clear call to action (like, subscribe, comment)
- NO markdown, NO asterisks — plain text only
- Write for speaking — short sentences, punchy delivery
- Total spoken words should be approximately {int(duration_sec * 1.5)} words

Format:
[INTRO] — hook + who this is for
[SECTION 1] — first key point
[SECTION 2] — second key point with the surprising fact/stat
[SECTION 3] — third key point
[OUTRO] — summary + CTA

Write only the script. Start directly with the hook. No "Title:", no headers in output."""

    try:
        # Use the OpenAI-compatible API via the configured proxy, or fallback to a simple generation
        # Since we don't have direct OpenAI key exposed here, we'll use a local approach
        # Actually, we'll call out to the OpenClaw gateway or use a simple heuristic
        
        # Try using the MiniMax API directly for script generation
        response = generate_with_minimax(prompt)
        return response
    except Exception as e:
        print(f"⚠️  Script generation failed: {e}")
        return fallback_script(topic, duration_sec)

def generate_with_minimax(prompt: str) -> str:
    """Call MiniMax M2.7 API for script generation."""
    api_key = os.environ.get("MINIMAX_API_KEY", "")
    if not api_key:
        raise ValueError("MINIMAX_API_KEY not set")
    
    # Read the config for base URL
    import json as _json
    config_path = Path.home() / ".openclaw" / "openclaw.json"
    if config_path.exists():
        cfg = _json.load(open(config_path))
        base_url = cfg["models"]["providers"]["minimax"]["baseUrl"]
    else:
        base_url = "https://api.minimax.io/anthropic"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    
    payload = {
        "model": "MiniMax-M2.7",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    resp = requests.post(f"{base_url}/v1/messages", headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    
    # Extract text from response
    if "content" in data:
        for block in data["content"]:
            if block.get("type") == "text":
                return block["text"]
    
    # Fallback
    raise ValueError(f"No text in MiniMax response: {data}")

def fallback_script(topic: str, duration_sec: int) -> str:
    """Emergency fallback script if API call fails."""
    return f"""[INTRO]
What's going on everyone, it's TheBoredNerd here. And today we're diving into something that's been absolutely blowing up in the AI world — {topic}.

If you've been paying attention lately, you know this stuff is moving faster than ever. So buckle up, because by the end of this video you're going to understand exactly why this matters for you.

[SECTION 1]
Here's the first thing you need to know about {topic}. The speed at which this has evolved is genuinely insane. We're talking months, not years. And the implications for people like you and me are massive.

[SECTION 2]
But here's what really got me — the numbers. Recent data shows that AI adoption has hit a point where ignoring it is no longer an option if you want to stay competitive. Whether you're a student, a creator, or someone just curious about the future, this affects you directly.

[SECTION 3]
So what's the play here? Three things. First, stay curious. Second, experiment with the tools available to you. And third, don't wait for permission to start building. The best time to get involved was yesterday. The second best time is right now.

[OUTRO]
Alright everyone, that's a wrap. If this was helpful, smash that like button, subscribe if you haven't already, and drop a comment below — I read every single one. I'll see you in the next one. Peace."""

# ─── TTS VOICEOVER ────────────────────────────────────────────────────────────

def generate_voiceover(script: str, output_path: str, speed_wpm: int = 165):
    """Generate macOS TTS voiceover from script text."""
    print(f"\n🎙️  Generating voiceover with voice: {TTS_VOICE}")
    
    # Extract just the spoken text (remove [INTRO], [SECTION], etc. markers)
    clean_script = re.sub(r'\[(INTRO|SECTION \d+|OUTRO|TOPIC|BREAK)\]', '', script)
    clean_script = re.sub(r'\s+', ' ', clean_script).strip()
    
    # Write to temp text file for say command
    text_file = output_path.replace('.m4a', '.txt')
    with open(text_file, 'w') as f:
        f.write(clean_script)
    
    # Generate AAC audio using macOS say command
    # -v: voice, -r: rate (words per min), -o: output file
    cmd = [
        'say',
        '-v', TTS_VOICE,
        '-r', str(speed_wpm),
        '-o', output_path,
        '-f', text_file
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"⚠️  say command failed: {result.stderr}")
        raise ValueError(f"TTS generation failed: {result.stderr}")
    
    # Convert AIFF to M4A (more YouTube-friendly)
    m4a_path = output_path
    aiff_path = output_path + '.aiff'
    if os.path.exists(aiff_path):
        subprocess.run([
            'afconvert', '-f', 'm4af', '-d', 'aac', 
            aiff_path, m4a_path
        ], capture_output=True)
        Path(aiff_path).unlink()
    
    # Get audio duration
    result = subprocess.run([
        'afinfo', m4a_path
    ], capture_output=True, text=True)
    
    duration = None
    for line in result.stdout.split('\n'):
        if 'estimated duration' in line.lower() or 'duration' in line.lower():
            match = re.search(r'(\d+\.?\d*)', line)
            if match:
                duration = float(match.group(1))
                break
    
    print(f"✅ Voiceover: {m4a_path} ({duration or '?'}s)")
    os.unlink(text_file)
    return m4a_path, duration or 60

# ─── STOCK FOOTAGE ───────────────────────────────────────────────────────────

def search_pexels_videos(query: str, per_page: int = 5):
    """Search Pexels for free stock videos."""
    if not PEXELS_API_KEY:
        print("⚠️  PEXELS_API_KEY not set — using fallback stock footage")
        return []
    
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": per_page, "orientation": "landscape"}
    
    try:
        resp = requests.get(
            "https://api.pexels.com/videos/search",
            headers=headers, params=params, timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("videos", [])[:per_page]
    except Exception as e:
        print(f"⚠️  Pexels search failed: {e}")
        return []

def download_pexels_video(video_url: str, output_path: str) -> bool:
    """Download a Pexels video file."""
    try:
        resp = requests.get(video_url, stream=True, timeout=60)
        resp.raise_for_status()
        with open(output_path, 'wb') as f:
            for chunk in resp.iter_content(65536):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"⚠️  Download failed: {e}")
        return False

def get_stock_clips(topic: str, duration_sec: int, clip_dir: Path) -> list:
    """
    Get stock video clips for the topic.
    Returns list of (clip_path, duration) tuples.
    """
    print(f"\n🎬 Fetching stock footage for: {topic}")
    clip_dir.mkdir(parents=True, exist_ok=True)
    
    clips = []
    
    # Search Pexels for relevant videos
    searches = [
        topic,
        f"{topic} technology",
        f"{topic} abstract",
        "tech abstract futuristic",
        "artificial intelligence",
        "data flow network"
    ]
    
    for query in searches[:3]:
        videos = search_pexels_videos(query, per_page=3)
        for v in videos:
            video_id = v["id"]
            # Get the HD video files
            video_files = v.get("video_files", [])
            # Pick the best quality available (prefer 1280x720 or similar)
            best = None
            for vf in video_files:
                if vf.get("width", 0) >= 1280:
                    best = vf
                    break
            if not best and video_files:
                best = video_files[-1]  # fallback to smallest
            
            if not best:
                continue
            
            filepath = clip_dir / f"clip_{video_id}.mp4"
            
            if download_pexels_video(best["link"], str(filepath)):
                # Get actual duration
                try:
                    clip = VideoFileClip(str(filepath))
                    dur = clip.duration
                    clips.append((str(filepath), dur))
                    clip.close()
                    print(f"  ✓ Downloaded: {filepath.name} ({dur:.1f}s)")
                except Exception as e:
                    print(f"  ⚠️  Can't read clip: {e}")
                    filepath.unlink()
            
            if sum(d for _, d in clips) >= duration_sec + 10:
                break
        
        if sum(d for _, d in clips) >= duration_sec + 10:
            break
    
    return clips

# ─── THUMBNAIL ────────────────────────────────────────────────────────────────

def download_thumbnail(topic: str, output_path: str):
    """Download a thumbnail image from Unsplash."""
    print(f"\n🖼️  Fetching thumbnail for: {topic}")
    
    # Use Unsplash Source API (random image based on topic)
    url = f"https://source.unsplash.com/1280x720/?{topic.replace(' ', ',')}"
    
    try:
        resp = requests.get(url, timeout=15, allow_redirects=True)
        resp.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(resp.content)
        print(f"✅ Thumbnail saved: {output_path}")
    except Exception as e:
        print(f"⚠️  Thumbnail fetch failed: {e}")
        # Create a placeholder with PIL
        try:
            img = Image.new('RGB', (1280, 720), color=(20, 20, 40))
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img)
            draw.text((640, 350), f"TheBoredNerd\n{topic}", 
                     fill=(255, 255, 255), anchor='mm')
            img.save(output_path)
            print(f"✅ Placeholder thumbnail created")
        except:
            pass

# ─── VIDEO ASSEMBLER ──────────────────────────────────────────────────────────

def assemble_video(
    clips: list,
    audio_path: str,
    output_path: str,
    title: str,
    duration_sec: int
):
    """Assemble stock clips + voiceover into a final video."""
    print(f"\n🎞️  Assembling video... ({len(clips)} clips)")
    
    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration
    
    # If no clips, create a color slide video
    if not clips:
        print("⚠️  No clips available — creating slide-style video")
        slide = ColorClip(size=(1280, 720), color=(10, 10, 20)).with_duration(audio_duration)
        
        # Add title text
        txt_clip = TextClip(
            text=title,
            font_size=48,
            font='Helvetica',
            color='white',
            size=(1180, 620),
            method='caption'
        ).with_duration(audio_duration)
        txt_clip = txt_clip.with_position('center')
        
        video = CompositeVideoClip([slide, txt_clip]).with_audio(audio)
        video = video.with_duration(audio_duration)
        video.write_videofile(output_path, fps=24, codec='libx264', 
                             audio_codec='aac', bitrate='3000k',
                             logger=None)
        video.close()
        audio.close()
        print(f"✅ Video saved: {output_path}")
        return
    
    # Calculate clip timings to match audio
    clips_needed = []
    remaining = audio_duration
    clip_idx = 0
    
    while remaining > 0 and clip_idx < len(clips):
        clip_path, clip_dur = clips[clip_idx]
        use_dur = min(clip_dur, remaining)
        
        try:
            clip = VideoFileClip(clip_path)
            clip = clip.subclip(0, use_dur)
            
            # Resize to 1280x720 if needed
            if clip.size[0] != 1280 or clip.size[1] != 720:
                clip = clip.resize((1280, 720))
            
            # Clip is already resized below — just use as-is
            
            clips_needed.append(clip)
            remaining -= use_dur
            clip_idx += 1
        except Exception as e:
            print(f"⚠️  Error loading clip {clip_path}: {e}")
            clip_idx += 1
            continue
    
    if not clips_needed:
        raise ValueError("No valid clips could be loaded")
    
    # Concatenate clips
    final_clip = concatenate_videoclips(clips_needed, method="compose")
    
    # Trim to audio length
    final_clip = final_clip.with_duration(audio_duration)
    
    # Add audio
    final_clip = final_clip.with_audio(audio)
    
    # Write output
    print(f"📦 Rendering video ({audio_duration:.0f}s, {len(clips_needed)} clips)...")
    final_clip.write_videofile(
        output_path,
        fps=24,
        codec='libx264',
        audio_codec='aac',
        bitrate='4000k',
        logger=None  # Suppress moviepy verbose output
    )
    
    # Cleanup
    for clip in clips_needed:
        clip.close()
    audio.close()
    final_clip.close()
    
    print(f"✅ Video saved: {output_path}")

# ─── MAIN PIPELINE ────────────────────────────────────────────────────────────

def run_pipeline(title: str, topic: str, duration_sec: int = 180, output_name: str = None):
    """Run the full video pipeline."""
    setup()
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', title)[:50]
    
    clip_dir = OUTPUT_DIR / f"clips_{timestamp}"
    clip_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = str(OUTPUT_DIR / f"{safe_name}_{timestamp}.mp4")
    audio_path = str(OUTPUT_DIR / f"audio_{timestamp}.m4a")
    thumb_path = str(THUMBNAIL_DIR / f"{safe_name}_thumb.jpg")
    
    # Step 1: Script
    script = generate_script(topic, duration_sec)
    print(f"\n📝 Script ({len(script)} chars):\n{script[:200]}...")
    
    # Step 2: Voiceover
    audio_path, actual_duration = generate_voiceover(script, audio_path)
    
    # Step 3: Stock footage
    clips = get_stock_clips(topic, actual_duration, clip_dir)
    
    # Step 4: Thumbnail
    download_thumbnail(topic, thumb_path)
    
    # Step 5: Assemble
    assemble_video(clips, audio_path, output_path, title, actual_duration)
    
    # Cleanup clips
    import shutil
    shutil.rmtree(clip_dir, ignore_errors=True)
    
    # Write metadata
    meta_path = output_path.replace('.mp4', '_meta.json')
    with open(meta_path, 'w') as f:
        json.dump({
            "title": title,
            "topic": topic,
            "script": script,
            "audio_path": audio_path,
            "thumbnail_path": thumb_path,
            "video_path": output_path,
            "duration_sec": actual_duration,
            "clips_used": len(clips),
            "created": timestamp
        }, f, indent=2)
    
    print(f"\n{'='*50}")
    print(f"🎉 VIDEO COMPLETE!")
    print(f"{'='*50}")
    print(f"📹 Video:   {output_path}")
    print(f"🖼️  Thumb:  {thumb_path}")
    print(f"🎙️  Audio:  {audio_path}")
    print(f"📄 Meta:    {meta_path}")
    print(f"\n⏱️  Duration: {actual_duration:.0f}s")
    print(f"🎬 Clips used: {len(clips)}")
    print(f"\n💡 Next: Review the video, then upload with:")
    print(f"   node {Path.home()}/.openclaw/workspace/scripts/youtube-upload.js \\")
    print(f"     --file '{output_path}' \\")
    print(f"     --title '{title}' \\")
    print(f"     --description '{script[:500]}...' \\")
    print(f"     --tags 'AI,technology,tech,2026' \\")
    print(f"     --privacy public")
    
    return {
        "video": output_path,
        "thumbnail": thumb_path,
        "audio": audio_path,
        "meta": meta_path,
        "script": script,
        "duration": actual_duration
    }

# ─── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Video Pipeline for YouTube")
    parser.add_argument("--title", required=True, help="Video title")
    parser.add_argument("--topic", required=True, help="Topic/keyword for stock footage search")
    parser.add_argument("--duration", type=int, default=180, help="Target duration in seconds")
    parser.add_argument("--output", help="Output MP4 path (default: auto)")
    
    args = parser.parse_args()
    
    try:
        result = run_pipeline(
            title=args.title,
            topic=args.topic,
            duration_sec=args.duration,
            output_name=args.output
        )
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Pipeline error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
