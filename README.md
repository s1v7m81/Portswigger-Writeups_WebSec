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
[![Labs](https://img.shields.io/badge/Labs_Solved-0-brightgreen?style=flat-square)]()

---

> All writeups in this repository follow the **OWASP Web Security Testing Guide (WSTG)** report format — the same structure used in real-world enterprise penetration test reports. Each writeup covers vulnerability description, CVSS v3 scoring, exploitation steps with proof of concept, and remediation guidance. You can use these as a reference for professional report formatting.

---

## Progress

| Category | OWASP Reference | Solved | Total |
|---|---|---|---|
| SQL Injection | A03:2021 – Injection | 0 | 18 |
| Cross-Site Scripting (XSS) | A03:2021 – Injection | 0 | 30 |
| Cross-Site Request Forgery | A01:2021 – Broken Access Control | 0 | 12 |
| Server-Side Request Forgery | A10:2021 – SSRF | 0 | 7 |
| XML External Entity (XXE) | A05:2021 – Security Misconfiguration | 0 | 9 |
| Access Control | A01:2021 – Broken Access Control | 0 | 28 |
| Authentication | A07:2021 – Identification Failures | 0 | 14 |
| OS Command Injection | A03:2021 – Injection | 0 | 5 |
| Business Logic | A04:2021 – Insecure Design | 0 | 11 |

---

## Repository Structure

```
portswigger-web-security-academy/
│
├── writeups/
│   ├── sql-injection/
│   │   ├── writeup-[lab-name].md
│   │   └── writeup-[lab-name].md
│   ├── xss/
│   │   ├── writeup-[lab-name].md
│   │   └── writeup-[lab-name].md
│   ├── csrf/
│   ├── ssrf/
│   ├── xxe/
│   ├── access-control/
│   ├── authentication/
│   ├── os-command-injection/
│   └── business-logic/
│
├── writeup-template.md
└── README.md
```

> Screenshots for each lab are embedded directly inside the writeup file.
> Each writeup is self-contained — no separate folders needed.

---

## Writeups Index

### SQL Injection

| Lab | Difficulty | OWASP | CVSSv3 | Writeup |
|---|---|---|---|---|
| *(labs will appear here as solved)* | — | — | — | — |

---

### Cross-Site Scripting (XSS)

| Lab | Difficulty | OWASP | CVSSv3 | Writeup |
|---|---|---|---|---|
| *(labs will appear here as solved)* | — | — | — | — |

---

### Cross-Site Request Forgery (CSRF)

| Lab | Difficulty | OWASP | CVSSv3 | Writeup |
|---|---|---|---|---|
| *(labs will appear here as solved)* | — | — | — | — |

---

### Server-Side Request Forgery (SSRF)

| Lab | Difficulty | OWASP | CVSSv3 | Writeup |
|---|---|---|---|---|
| *(labs will appear here as solved)* | — | — | — | — |

---

### XML External Entity (XXE)

| Lab | Difficulty | OWASP | CVSSv3 | Writeup |
|---|---|---|---|---|
| *(labs will appear here as solved)* | — | — | — | — |

---

### Access Control

| Lab | Difficulty | OWASP | CVSSv3 | Writeup |
|---|---|---|---|---|
| *(labs will appear here as solved)* | — | — | — | — |

---

### Authentication

| Lab | Difficulty | OWASP | CVSSv3 | Writeup |
|---|---|---|---|---|
| *(labs will appear here as solved)* | — | — | — | — |

---

### OS Command Injection

| Lab | Difficulty | OWASP | CVSSv3 | Writeup |
|---|---|---|---|---|
| *(labs will appear here as solved)* | — | — | — | — |

---

### Business Logic

| Lab | Difficulty | OWASP | CVSSv3 | Writeup |
|---|---|---|---|---|
| *(labs will appear here as solved)* | — | — | — | — |

---

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
