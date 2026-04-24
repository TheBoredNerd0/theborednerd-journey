#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const OPENAI_MODEL = 'openai-codex/gpt-5.4';
const FALLBACK_MODEL = 'minimax/MiniMax-M2.7';
const TELEGRAM_CHAT = '370423423';
const STATE_PATH = '/Users/bored/.openclaw/workspace/memory/fallback-watchdog.json';

const JOBS = [
  { id: '4d5c23e6-ee74-48b1-86ff-25f48bcc6958', name: 'upgrade_agent' },
  { id: 'de8167d1-297c-43d9-8a65-e7ed950484de', name: 'business_agent' },
  { id: '4f6e0492-0333-4172-b2a2-26e7951c9427', name: 'content_agent' },
  { id: '153e1da4-8a6b-41c9-a1b8-222bfb594176', name: 'music_agent' },
  { id: '2ab973c5-c0ff-482a-82eb-8975d0896846', name: 'cyber_agent' },
  { id: '621bd060-c89b-4f4e-8113-54ee5ce625dc', name: 'investment_agent' },
  { id: '47037c47-0c37-4d24-b602-7f027d8f610b', name: 'law_agent' },
  { id: '3abf507a-7eda-4641-a467-b3a52759d1df', name: 'software_agent' },
  { id: 'a340911f-bbc7-4241-825f-2c99fcc2669c', name: 'news_agent' },
  { id: '4af594ff-8842-4f8c-a7cf-66ea6852085d', name: 'youtube_video_agent' },
  { id: '0dac064f-2bcc-4907-847d-91adb7c08345', name: 'progress_agent' },
  { id: 'a8790e0d-2add-4669-8fff-6a0ab314e564', name: 'token_agent' },
  { id: '1b96c507-eea3-4dcd-9945-3ec705662714', name: 'it_agent' }
];

function sh(cmd) {
  return execSync(cmd, { encoding: 'utf8' }).trim();
}

function readState() {
  try { return JSON.parse(fs.readFileSync(STATE_PATH, 'utf8')); }
  catch { return { activeModel: OPENAI_MODEL, lastAlert: null }; }
}

function writeState(state) {
  fs.mkdirSync(path.dirname(STATE_PATH), { recursive: true });
  fs.writeFileSync(STATE_PATH, JSON.stringify(state, null, 2));
}

function getRuns(jobId) {
  try {
    const raw = sh(`openclaw cron runs --id ${jobId}`);
    return JSON.parse(raw).entries || [];
  } catch {
    return [];
  }
}

function isOpenAIFailure(entry) {
  const text = `${entry.error || ''} ${entry.summary || ''}`.toLowerCase();
  return entry.status === 'error' && (
    text.includes('openai') ||
    text.includes('gpt-5') ||
    text.includes('quota') ||
    text.includes('rate limit') ||
    text.includes('oauth') ||
    text.includes('auth') ||
    text.includes('provider')
  );
}

function recentFailures() {
  let count = 0;
  for (const job of JOBS) {
    const runs = getRuns(job.id).slice(0, 2);
    for (const run of runs) {
      if (isOpenAIFailure(run)) count++;
    }
  }
  return count;
}

function patchJobs(model) {
  for (const job of JOBS) {
    try {
      sh(`openclaw cron edit ${job.id} --model ${model}`);
    } catch (e) {
      // keep going
    }
  }
}

function notify(text) {
  try {
    sh(`openclaw cron wake --text ${JSON.stringify(text)} --mode now`);
  } catch {}
}

function main() {
  const state = readState();
  const failures = recentFailures();

  if (state.activeModel === OPENAI_MODEL && failures >= 2) {
    patchJobs(FALLBACK_MODEL);
    state.activeModel = FALLBACK_MODEL;
    state.lastAlert = Date.now();
    writeState(state);
    notify(`⚠️ OpenAI appears to be failing or quota-limited. Switched cron jobs to MiniMax fallback (${FALLBACK_MODEL}).`);
    return;
  }

  if (state.activeModel === FALLBACK_MODEL && failures === 0) {
    patchJobs(OPENAI_MODEL);
    state.activeModel = OPENAI_MODEL;
    state.lastAlert = Date.now();
    writeState(state);
    notify(`✅ OpenAI appears healthy again. Switched cron jobs back to primary model (${OPENAI_MODEL}).`);
    return;
  }

  writeState(state);
}

main();
