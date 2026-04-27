🛡️ CYBER INTEL — April 26, 2026

⚠️ Top threat today: CVE-2024-57728
  Affected: SimpleHelp (remote support software) — admin users with file upload access
  Severity: CVSS 9.1 (Critical) — actively exploited since Apr 24, patch deadline May 8

🔓 Active threat activity:
ShinyHunters (the same group behind previous ADT breaches in Aug & Oct 2024) struck again — compromising an ADT employee's Okta SSO via vishing (voice phish), then accessing Salesforce and exfiltrating data for ~10M customers. Names, phone numbers, addresses, and in some cases DOBs + SSN last 4 digits were stolen. No payment data. ADT confirmed the breach Apr 20. The group set an extortion deadline of April 27 — "pay or we leak."

Separately, UNC6692 (tracked by Mandiant/Google) is using Microsoft Teams as a helpdesk impersonation channel to deploy "Snow" malware — a full suite with browser extension (SnowBelt), backdoor (SnowBasin), and tunneler (SnowGlaze). Targets get socially engineered via email bombing, then tricked into installing a fake "spam patch." The malware persists via Chrome extension + scheduled tasks, enabling credential dumping, lateral movement via pass-the-hash, and domain takeover using LimeWire for exfiltration.

🔧 Tool/technique trending: OAuth token theft + SSO bypass via vishing — ShinyHunters has been chaining this across Okta/Microsoft Entra/Google Workspace targets since 2025. The attack chain: voice phish employee → steal SSO session → access SaaS apps (Salesforce, M365, Slack, etc.) → exfil data → ransom demand. Awareness training is the primary defense.

📚 Career path — CTF/Practical (Days 22–31 of curriculum):
Concept: Pass-the-Hash (PtH) — an attacker steals a password hash (not the plaintext password) and reuses it to authenticate to other systems on the network. Since NTLM/LM hashes are transmitted during auth, they can be captured from LSASS memory or network traffic and replayed to gain lateral movement without cracking the actual password.
Why it matters: PtH is how UNC6692 moved from a single compromised host to the domain controller in the Snow malware campaign — it's a go-to technique in real-world intrusions and almost every AD-focused CTF.
Learn it: TryHackMe room "Attacking Kerberos" — covers PtH, golden/silver tickets, and Kerberoasting in a controlled lab.
Practice today: On a Kali box, run `responder -I eth0` to capture NTLM hashes in a CTF lab network, then use `hashcat` or `john` to crack simple ones. Next, replay a captured hash with `evil-winrm` to log into a second host as that user.

🎯 Career tip: Add "Active Directory pentesting" to your LinkedIn if you've done any HTB/TryHackMe AD labs. Even "beginner" AD skills are in demand — blue teams need people who understand how attackers move laterally.