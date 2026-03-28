🛡️ CYBER REPORT — 2026-03-28

🔴 Top threat this week:
CVE-2026-2414 — Critical RCE vulnerability in Palo Alto Networks PAN-OS
affecting GlobalProtect VPN gateways. CVE scores 9.8/10. If unpatched,
attackers can execute arbitrary code on the VPN concentrator — the literal
gateway to corporate networks. Patch immediately if you're running
PAN-OS < 11.2.x. Treat your VPN gateway like a firewall's front door —
it IS the front door for remote workers. This is actively being scanned
for in the wild.

📚 Learning topic:
Supply Chain Attacks — when attackers compromise a trusted vendor or
dependency to hit downstream victims. Think of the SolarWinds (2020) or
XZ Utils (2024) incidents. A single poisoned library or software update
can give attackers a foothold in thousands of organizations at once.
This is why version pinning, integrity checking (SHA-256), and monitoring
third-party dependencies matters — especially in CI/CD pipelines.

💡 Career tip:
Set up a home homelab. You don't need expensive gear — a Raspberry Pi
or an old laptop running VirtualBox/KVM is enough. Spin up a Kali Linux
VM, practice with TryHackMe or Hack The Box labs, and document
everything in a GitHub repo. Recruiters love seeing hands-on labs and
writeups. It costs <$50 and builds real muscle.

🔗 Resource:
TryHackMe — Free Beginner Path: https://tryhackme.com/path/outline/beginner
Start with "Intro to Cyber" or "Pre-Security" — zero barrier, browser-based
labs, walkthroughs included.
