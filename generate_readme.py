import os
import re

# ─── Topic definitions ────────────────────────────────────────────────────────

TOPICS = [
    # (folder_name, display_name, owasp, total)
    # Server-side
    ("SQL-Injection",                "SQL Injection",                      "A03:2021 – Injection",                          18),
    ("Authentication",               "Authentication",                     "A07:2021 – Identification Failures",            14),
    ("Path-Traversal",               "Path Traversal",                     "A01:2021 – Broken Access Control",               6),
    ("Command-Injection",            "Command Injection",                  "A03:2021 – Injection",                           5),
    ("Business-Logic",               "Business Logic Vulnerabilities",     "A04:2021 – Insecure Design",                    11),
    ("Information-Disclosure",       "Information Disclosure",             "A02:2021 – Cryptographic Failures",              5),
    ("Access-Control",               "Access Control",                     "A01:2021 – Broken Access Control",              13),
    ("File-Upload",                  "File Upload Vulnerabilities",        "A04:2021 – Insecure Design",                     7),
    ("Race-Conditions",              "Race Conditions",                    "A04:2021 – Insecure Design",                     6),
    ("SSRF",                         "Server-Side Request Forgery (SSRF)", "A10:2021 – SSRF",                               7),
    ("XXE-Injection",                "XXE Injection",                      "A05:2021 – Security Misconfiguration",           9),
    ("NoSQL-Injection",              "NoSQL Injection",                    "A03:2021 – Injection",                           4),
    ("API-Testing",                  "API Testing",                        "A05:2021 – Security Misconfiguration",           5),
    ("Web-Cache-Deception",          "Web Cache Deception",                "A05:2021 – Security Misconfiguration",           5),
    # Client-side
    ("XSS",                          "Cross-Site Scripting (XSS)",         "A03:2021 – Injection",                          30),
    ("CSRF",                         "Cross-Site Request Forgery (CSRF)",  "A01:2021 – Broken Access Control",              12),
    ("CORS",                         "Cross-Origin Resource Sharing",      "A01:2021 – Broken Access Control",               3),
    ("Clickjacking",                 "Clickjacking",                       "A04:2021 – Insecure Design",                     5),
    ("DOM-Based",                    "DOM-Based Vulnerabilities",          "A03:2021 – Injection",                           7),
    ("WebSockets",                   "WebSockets",                         "A03:2021 – Injection",                           3),
    # Advanced
    ("Insecure-Deserialization",     "Insecure Deserialization",           "A08:2021 – Software and Data Integrity Failures",10),
    ("Web-LLM-Attacks",              "Web LLM Attacks",                    "A05:2021 – Security Misconfiguration",           7),
    ("GraphQL-API",                  "GraphQL API Vulnerabilities",        "A05:2021 – Security Misconfiguration",           5),
    ("Server-Side-Template-Injection","Server-Side Template Injection",    "A03:2021 – Injection",                           7),
    ("Web-Cache-Poisoning",          "Web Cache Poisoning",                "A05:2021 – Security Misconfiguration",          13),
    ("HTTP-Host-Header",             "HTTP Host Header Attacks",           "A05:2021 – Security Misconfiguration",           7),
    ("HTTP-Request-Smuggling",       "HTTP Request Smuggling",             "A05:2021 – Security Misconfiguration",          22),
    ("OAuth",                        "OAuth Authentication",               "A07:2021 – Identification Failures",             6),
    ("JWT-Attacks",                  "JWT Attacks",                        "A07:2021 – Identification Failures",             8),
    ("Prototype-Pollution",          "Prototype Pollution",                "A03:2021 – Injection",                          10),
    ("Essential-Skills",             "Essential Skills",                   "A05:2021 – Security Misconfiguration",           2),
]

BASE = "Portswigger_Web-Sec"

# ─── Helpers ──────────────────────────────────────────────────────────────────

def get_labs(folder):
    """Return list of (filename, title) for every LAB_*.md that is filled in."""
    path = os.path.join(BASE, folder)
    labs = []
    if not os.path.isdir(path):
        return labs
    for fname in sorted(os.listdir(path)):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(path, fname)
        with open(fpath, encoding="utf-8") as f:
            content = f.read().strip()
        # Skip placeholder files (only contain "# LAB_1" or are empty)
        if content in ("", "# LAB_1", "# LAB_2") or len(content) < 20:
            continue
        # Extract title from first heading
        match = re.search(r"^#\s+(.+)", content, re.MULTILINE)
        title = match.group(1).strip() if match else fname.replace(".md", "")
        # Extract difficulty
        diff_match = re.search(r"\*\*Difficulty\*\*\s*\|\s*(Apprentice|Practitioner|Expert)", content)
        difficulty = diff_match.group(1) if diff_match else "—"
        # Extract CVSSv3
        cvss_match = re.search(r"\*\*CVSSv3 Score\*\*\s*\|\s*([^\n\|]+)", content)
        cvss = cvss_match.group(1).strip() if cvss_match else "—"
        rel_path = f"./{BASE}/{folder}/{fname}"
        labs.append((title, difficulty, cvss, rel_path))
    return labs

# ─── Section builders ─────────────────────────────────────────────────────────

def build_progress_table(topic_data):
    total_solved = sum(s for _, _, _, s, _ in topic_data)
    total_labs   = sum(t for _, _, _, _, t in topic_data)
    lines = []
    lines.append("## Progress\n")
    lines.append(f"![Total](https://img.shields.io/badge/Total_Solved-{total_solved}%20%2F%20{total_labs}-blue?style=flat-square)\n")
    lines.append("")
    lines.append("| Category | OWASP Reference | Solved | Total |")
    lines.append("|---|---|---|---|")
    for _, display, owasp, solved, total in topic_data:
        lines.append(f"| {display} | {owasp} | {solved} | {total} |")
    return "\n".join(lines)

def build_writeups_section(topic_data):
    lines = []
    lines.append("## Writeups\n")
    lines.append("> Click any category to expand. Click a lab name to open the writeup.\n")

    for folder, display, owasp, solved, total in topic_data:
        labs = get_labs(folder)
        lines.append("<details>")
        lines.append(f"<summary><b>{display}</b> &nbsp;|&nbsp; {owasp} &nbsp;|&nbsp; {solved} / {total} solved</summary>\n")
        lines.append("<br>\n")
        lines.append("| Lab | Difficulty | CVSSv3 | Writeup |")
        lines.append("|---|---|---|---|")
        if labs:
            for title, diff, cvss, path in labs:
                lines.append(f"| {title} | {diff} | {cvss} | [open]({path}) |")
        else:
            lines.append("| *(no writeups yet)* | — | — | — |")
        lines.append("")
        lines.append("</details>\n")
        lines.append("---\n")

    return "\n".join(lines)

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    # Build topic data with live solved counts
    topic_data = []
    for folder, display, owasp, total in TOPICS:
        solved = len(get_labs(folder))
        topic_data.append((folder, display, owasp, solved, total))

    total_solved = sum(s for _, _, _, s, _ in topic_data)

    readme = f"""\
```
╔══════════════════════════════════════════════════════════════════╗
║          PORTSWIGGER WEB SECURITY ACADEMY — WRITEUPS             ║
║          Methodology : OWASP Web Security Testing Guide          ║
║          Report Format: Based on OWASP WSTG Standards            ║
╚══════════════════════════════════════════════════════════════════╝
```

[![Platform](https://img.shields.io/badge/Platform-PortSwigger_Web_Academy-orange?style=flat-square)](https://portswigger.net/web-security)
[![Standard](https://img.shields.io/badge/Standard-OWASP_WSTG-blue?style=flat-square)](https://owasp.org/www-project-web-security-testing-guide/)
[![Top10](https://img.shields.io/badge/Reference-OWASP_Top_10_2021-red?style=flat-square)](https://owasp.org/www-project-top-ten/)
[![Labs](https://img.shields.io/badge/Labs_Solved-{total_solved}-brightgreen?style=flat-square)]()

---

> All writeups in this repository follow the **OWASP Web Security Testing Guide (WSTG)** report format — the same structure used in real-world enterprise penetration test reports. Each writeup covers vulnerability description, CVSS v3 scoring, exploitation steps with proof of concept, and remediation guidance. You can use these as a reference for professional report formatting.

---

{build_progress_table(topic_data)}

---

{build_writeups_section(topic_data)}
## Report Format Reference

Each writeup follows this structure, consistent with OWASP WSTG:

| Section | Content |
|---|---|
| Lab Information | Name, category, difficulty, OWASP ID, CWE, CVSSv3 |
| Objective | Lab goal |
| Vulnerability Overview | Definition and CVSS risk factor breakdown |
| Impact Assessment | Severity classification |
| Reconnaissance | Attack surface identification and probing |
| Exploitation | Step-by-step with HTTP requests and screenshots |
| Proof of Concept | Final working payload |
| Remediation | Root cause, vulnerable vs secure code, fix checklist |
| References | OWASP, CWE, PortSwigger, CVSS Calculator |

---

## Resources

| Resource | Link |
|---|---|
| PortSwigger Web Academy | [portswigger.net/web-security](https://portswigger.net/web-security) |
| OWASP Top 10 (2021) | [owasp.org/Top10](https://owasp.org/www-project-top-ten/) |
| OWASP Web Security Testing Guide | [OWASP WSTG](https://owasp.org/www-project-web-security-testing-guide/) |
| CWE Database | [cwe.mitre.org](https://cwe.mitre.org) |
| CVSS v3 Calculator | [nvd.nist.gov](https://nvd.nist.gov/vuln-metrics/cvss/v3-calculator) |

---

## Author

```
Name     : [Your Name]
GitHub   : https://github.com/yourusername
LinkedIn : https://linkedin.com/in/yourprofile
```

---

*This repository is for educational purposes only. All labs are solved on PortSwigger's legal, intentionally vulnerable practice platform.*
"""

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print(f"README.md updated — {total_solved} labs solved across {len(TOPICS)} categories.")

if __name__ == "__main__":
    main()
