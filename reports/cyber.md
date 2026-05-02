# 🛡️ Cyber Intel — 2026-05-02

## ⚠️ Top Threat Today: CVE-2026-41940
- **Affected:** Anyone running WebPros cPanel & WHM or WP2 (WordPress Squared)
- **Severity:** CRITICAL — Auth bypass in login flow, unauthenticated remote attackers can gain full control panel access
- **CVSS:** Likely 9.0+ (authentication bypass for critical function)
- **Due Date:** ⚠️ **May 3, 2026** (patch TOMORROW)

Also watch:
- **CVE-2026-31431** — Linux Kernel privilege escalation (added May 1)
- **CVE-2026-32202** — Microsoft Windows spoofing via Shell (added Apr 28)

---

## 🔓 Active Threat Activity

**"AccountDumpling" campaign** — A Vietnamese-linked threat operation is using Google AppSheet as a phishing relay to compromise Facebook accounts. ~30,000 accounts stolen so far, sold back via an illicit storefront. Uses legitimate Google infrastructure to bypass email filters.

**Cordial Spider + Snarky Spider** — Two cybercrime groups conducting rapid SaaS extortion attacks using vishing (voice phishing) combined with SSO abuse. They move fast, operate almost entirely within SaaS environments, and leave minimal forensic traces. High-speed data theft + account takeover.

---

## 🔧 Tool/Technique Trending
**SSO/OAuth token theft** — With the rise of SSO-abuse attacks, attackers are targeting identity provider tokens (Azure AD, Google Workspace) rather than traditional passwords. The "pass-the-token" technique is trending hard in criminal forums right now.

---

## 📚 Career Path — Networking Fundamentals (Day 2 of 7)

**Concept:** The OSI 7-Layer Model — the conceptual framework that governs how data moves across networks.

| Layer | What it does | Examples |
|-------|-------------|---------|
| L7 Application | User-facing protocols | HTTP, DNS, SMTP |
| L6 Presentation | Data formatting, encryption | TLS, SSL |
| L5 Session | Connection management | NetBIOS |
| L4 Transport | Reliable delivery | TCP, UDP |
| L3 Network | Routing, logical addressing | IP, routers |
| L2 Data Link | MAC addresses, switches | Ethernet, ARP |
| L1 Physical | Signals, cables | Fiber, copper |

**Why it matters:** Every security control (firewalls, IDS/IPS, VPN, TLS) operates at specific layers. If you don't know which layer something works at, you can't understand how to secure it — or how attackers bypass it.

**Learn it:** [TryHackMe — OSI Model](https://tryhackme.com/room/oscpfull) or just draw the 7 layers from memory right now.

**Practice today (15 min):**
1. On your Mac, run `netstat -an` — identify what's listening, what states exist (ESTABLISHED, LISTEN, TIME_WAIT)
2. Run `curl -I https://example.com` — spot which layer HTTP, TLS, and TCP operate at
3. Bonus: Run `arp -a` to see your local ARP cache (L2/L3 mapping in action)

---

## 🎯 Career Tip
**Add to LinkedIn today:** "OSI model fundamentals" or start a tryhackme.com profile and note it in your skills. Hiring managers for SOC analyst/Junior security roles ask OSI questions in almost every interview.