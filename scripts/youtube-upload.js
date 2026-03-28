#!/usr/bin/env node
/**
 * YouTube Auto-Uploader
 * Uploads videos to YouTube via YouTube Data API v3
 *
 * Setup required (ONE TIME):
 * 1. Go to https://console.cloud.google.com
 * 2. Create a project → enable "YouTube Data API v3"
 * 3. Go to "Credentials" → "Create Credentials" → "OAuth client ID"
 *    - Application type: Desktop app (give it a name)
 *    - Download the JSON file
 * 4. Save the JSON as: ~/.openclaw/credentials/youtube-oauth.json
 *
 * First run: Will open browser for OAuth authorization
 *            Token saved to: ~/.openclaw/credentials/youtube-token.json
 *
 * Usage:
 *   node youtube-upload.js --file <video.mp4> --title "Title" --description "Desc" [--tags "tag1,tag2"] [--category 28]
 *
 * Categories: 28=Gaming, 24=Entertainment, 22=People, 10=Music, 27=Education
 */

const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');
const readline = require('readline');
const http = require('http');
const url = require('url');

const CREDENTIALS_PATH = path.join(process.env.HOME, '.openclaw/credentials/youtube-oauth.json');
const TOKEN_PATH = path.join(process.env.HOME, '.openclaw/credentials/youtube-token.json');

// Parse CLI args
const args = process.argv.slice(2);
const getArg = (flag) => {
  const idx = args.indexOf(flag);
  return idx !== -1 ? args[idx + 1] : null;
};

const videoPath = getArg('--file');
const title = getArg('--title') || 'Untitled Video';
const description = getArg('--description') || '';
const tags = getArg('--tags')?.split(',').filter(Boolean) || [];
const categoryId = getArg('--category') || '24';
const privacyStatus = getArg('--privacy') || 'unlisted'; // public, unlisted, private

if (!videoPath) {
  console.error('Usage: node youtube-upload.js --file <video.mp4> --title "Title" --description "Desc" [--tags "a,b"] [--category 28] [--privacy public]');
  process.exit(1);
}

if (!fs.existsSync(CREDENTIALS_PATH)) {
  console.error('ERROR: YouTube credentials not found.');
  console.error('Please follow setup instructions at the top of this file.');
  console.error('Expected at: ' + CREDENTIALS_PATH);
  process.exit(1);
}

// Load credentials
const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8'));
const { client_id, client_secret, redirect_uris } = credentials;
const oauth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);

// Load or get token
function loadToken() {
  if (fs.existsSync(TOKEN_PATH)) {
    const token = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));
    oauth2Client.setCredentials(token);
    return true;
  }
  return false;
}

function saveToken(token) {
  fs.writeFileSync(TOKEN_PATH, JSON.stringify(token, null, 2));
  console.log('Token saved to:', TOKEN_PATH);
}

// Generate auth URL
function getAuthUrl() {
  const scopes = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube'
  ];
  return oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: scopes,
    prompt: 'consent'
  });
}

// Get token via local server
function getTokenFromServer(authCode) {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      const query = new URL(req.url, 'http://localhost:3000').searchParams;
      const code = query.get('code');
      const error = query.get('error');
      
      res.writeHead(200, { 'Content-Type': 'text/html' });
      if (error) {
        res.end('<h1>Error</h1><p>' + error + '</p><p>You can close this window.</p>');
      } else {
        res.end('<h1>Success!</h1><p>You can close this window. Check the terminal.</p>');
      }
      
      server.close();
      resolve(code);
    });
    
    server.listen(3000, () => {
      console.log('Waiting for authorization...');
    });
  });
}

// Interactive token获取 (fallback)
async function getTokenInteractively() {
  const authUrl = getAuthUrl();
  console.log('\n🔗 Open this URL in your browser to authorize:\n');
  console.log(authUrl);
  console.log();
  
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const code = await new Promise((resolve) => {
    rl.question('Paste the code from the browser: ', resolve);
  });
  rl.close();
  
  const { tokens } = await oauth2Client.getToken(code);
  oauth2Client.setCredentials(tokens);
  saveToken(tokens);
  return tokens;
}

// Upload video
async function uploadVideo() {
  // Authenticate
  if (!loadToken()) {
    await getTokenInteractively();
  }
  
  const youtube = google.youtube({ version: 'v3', auth: oauth2Client });
  
  // Get file size
  const fileSize = fs.statSync(videoPath).size;
  const fileName = path.basename(videoPath);
  
  console.log(`\n📤 Uploading: ${fileName} (${(fileSize / 1024 / 1024).toFixed(1)} MB)`);
  console.log(`   Title: ${title}`);
  console.log(`   Privacy: ${privacyStatus}`);
  
  const requestBody = {
    snippet: {
      title,
      description,
      tags,
      categoryId: String(categoryId),
      defaultLanguage: 'en',
      localized: {
        title,
        description
      }
    },
    status: {
      privacyStatus,
      selfDeclaredMadeForKids: false,
    },
    notifySubscribers: true,
  };
  
  const media = {
    body: fs.createReadStream(videoPath),
    mimeType: 'video/mp4',
  };
  
  const res = await youtube.videos.insert(
    {
      part: ['snippet', 'status'],
      notifySubscribers: true,
      requestBody,
      media,
    },
    {
      // Use multipart upload
      multipart: true,
      maxBodyLength: 7 * 1024 * 1024 * 1024, // 7GB
      maxContentLength: 7 * 1024 * 1024 * 1024,
    }
  );
  
  const videoId = res.data.id;
  const videoUrl = `https://youtu.be/${videoId}`;
  
  console.log('\n✅ Upload complete!');
  console.log(`   Video ID: ${videoId}`);
  console.log(`   URL: ${videoUrl}`);
  
  // Set thumbnail if available
  const thumbnailPath = videoPath.replace(/\.[^.]+$/, '-thumb.jpg');
  if (fs.existsSync(thumbnailPath)) {
    console.log('🖼️  Setting custom thumbnail...');
    await youtube.thumbnails.set({
      videoId,
      media: {
        body: fs.createReadStream(thumbnailPath)
      }
    });
    console.log('   Thumbnail set!');
  }
  
  return { videoId, videoUrl };
}

uploadVideo().catch((err) => {
  console.error('❌ Upload failed:', err.message);
  if (err.message.includes('invalid_credentials') || err.message.includes('Token has been expired')) {
    console.error('\nToken expired. Delete', TOKEN_PATH, 'and run again to re-authenticate.');
  }
  process.exit(1);
});
