# 🛡️ Cyber Intel Report — March 30, 2026

## ⚠️ Top Threats

### CVE-2026-3055 — Citrix NetScaler ADC/Gateway (CVSS 9.3)
- **What:** Insufficient input validation leading to memory overread
- **Risk:** Sensitive information leakage; being actively scanned by threat actors
- **Affected:** Citrix NetScaler ADC and NetScaler Gateway (multiple versions)
- **Action:** Patch immediately if exposed. Treat as critical if accessible from internet.

### CVE-2025-53521 — F5 BIG-IP Access Policy Manager (CVSS 9.3)
- **What:** Remote code execution (RCE)
- **Status:** Added to CISA KEV catalog — evidence of active exploitation confirmed
- **Affected:** F5 BIG-IP APM deployments
- **Action:** Patch urgently. Already being exploited in the wild.

---

## 🔓 Active Threat Activity

**Handala Hack Team (Iran-linked)** — breached FBI Director Kash Patel's personal email account, leaked photos and documents. Also deployed wiper attack against Stryker (medical device manufacturer). This group is politically motivated, targeting US government and critical infrastructure.

**TA446 (Russian state-sponsored)** — running targeted spear-phishing campaigns using the **DarkSword iOS exploit kit**. High-confidence attribution. If you have political/government-adjacent exposure, treat iOS devices as high-priority for patching.

**TeamPCP (supply chain)** — pushed malicious versions 4.87.1 and 4.87.2 of the `telnyx` Python package to PyPI. Stealer hidden in WAV files. If you use `telnyx`, audit your installed version now:
```bash
pip show telnyx
```

**Apple** — sending Lock Screen alerts en masse to out-of-date iPhones warning of active web-based exploits. Update iOS immediately.

---

## 🔧 Tool/Technique Trending: Attack Surface Management (ASM)

The security community is heavily discussing **Attack Surface Management** tools — automated platforms that continuously discover external-facing assets, misconfigs, and exposed services across your infrastructure. Thinkof it as "always-on recon."

Popular open-source tools in this space:
- **Naabu** — fast port scanner
- **httpx** — probe for HTTP responses, titles, tech stacks
- ** nuclei** — vulnerability scanner templated against known CVEs

For defenders: ASM helps you see what attackers see. For job hunters: familiarity with ASM workflow (recon → discovery → prioritization → remediation) is a real SOC/blue team skill.

---

## 📚 Career Path — CTF / Practical Skills (Week 4)

**Concept:** Capture The Flag (CTF) competitions
**Why it matters:** CTFs are the #1 way to build practical hacking skills and demonstrate ability to employers. They're essentially gamified real-world security challenges.

### Learn it:
- **Start here:** [TryHackMe Pre-Security Path](https://tryhackme.com/path/outline/presecurity) — teaches networking, Linux, web basics through hands-on labs. Free. ~8 hours total.
- **Then:** [Hack The Box (HTB) Academy — Starting Point](https://academy.hackthebox.com/) — beginner-friendly guided boxes.

### Practice today (15-30 min):
1. Create a free [TryHackMe](https://tryhackme.com) account
2. Complete the "Network Security" room → [Nmap](https://tryhackme.com/room/rpnmap) task (15 min)
3. Or: Solve the first 2 flags on [Hack The Box Starting Point Tier 0](https://app.hackthebox.com/starting-point) — "Meow" and "Fawn" are intentionally trivial and walk you through the basics.

### CTF Resources to Bookmark:
- [CTFtime.org](https://ctftime.org) — upcoming competitions, writeups, team rankings
- [ picoCTF](https://picoctf.org) — Google-run beginner CTF, always available
- [ROP Emporium](https://ropemporium.com) — binary exploitation practice

---

## 🎯 Career Progress Tip

**This week:** Add "CTF Participant" to your LinkedIn if you've solved even one challenge. Link to your TryHackMe/HackTheBox profile. Hiring managers at security firms *do* check these profiles — a rank or completed rooms signals genuine self-motivation.

**Cert to research:** [eJPT](https://elearnsecurity.com/product/ejpt-certification/) (eLearning Penetration Testing) — $200, entirely practical, no memorize-heavy theory. Great first cert for your resume.

---

## 📅 Rotation Reminder
- Days 1-7: Networking
- Days 8-14: Linux
- Days 15-21: Web App Security
- Days 22-31: **CTF / Practical ← YOU ARE HERE**
