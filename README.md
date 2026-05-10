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

## Writeups

> Click any category to expand. Click a lab name to open the writeup.

<details>
<summary><b>SQL Injection</b> &nbsp;|&nbsp; A03:2021 – Injection &nbsp;|&nbsp; 0 / 18 solved</summary>

<br>

| Lab | Difficulty | CVSSv3 | Writeup |
|---|---|---|---|
| *(no writeups yet)* | — | — | — |

<!--
EXAMPLE ROW — copy and fill when you solve a lab:
| SQL injection vulnerability in WHERE clause | Apprentice | 9.8 Critical | [open](./writeups/sql-injection/writeup-where-clause.md) |
-->

</details>

---

<details>
<summary><b>Cross-Site Scripting (XSS)</b> &nbsp;|&nbsp; A03:2021 – Injection &nbsp;|&nbsp; 0 / 30 solved</summary>

<br>

| Lab | Difficulty | CVSSv3 | Writeup |
|---|---|---|---|
| SQL injection in WHERE clause | Apprentice | 9.8 Critical | [open](./writeups/sql-injection/writeup-where-clause.md) |
<!--
EXAMPLE ROW:
| Reflected XSS into HTML context | Apprentice | 6.1 Medium | [open](./writeups/xss/writeup-reflected-html-context.md) |
-->

</details>

---

<details>
<summary><b>Cross-Site Request Forgery (CSRF)</b> &nbsp;|&nbsp; A01:2021 – Broken Access Control &nbsp;|&nbsp; 0 / 12 solved</summary>

<br>

| Lab | Difficulty | CVSSv3 | Writeup |
|---|---|---|---|
| *(no writeups yet)* | — | — | — |

</details>

---

<details>
<summary><b>Server-Side Request Forgery (SSRF)</b> &nbsp;|&nbsp; A10:2021 – SSRF &nbsp;|&nbsp; 0 / 7 solved</summary>

<br>

| Lab | Difficulty | CVSSv3 | Writeup |
|---|---|---|---|
| *(no writeups yet)* | — | — | — |

</details>

---

<details>
<summary><b>XML External Entity (XXE)</b> &nbsp;|&nbsp; A05:2021 – Security Misconfiguration &nbsp;|&nbsp; 0 / 9 solved</summary>

<br>

| Lab | Difficulty | CVSSv3 | Writeup |
|---|---|---|---|
| *(no writeups yet)* | — | — | — |

</details>

---

<details>
<summary><b>Access Control</b> &nbsp;|&nbsp; A01:2021 – Broken Access Control &nbsp;|&nbsp; 0 / 28 solved</summary>

<br>

| Lab | Difficulty | CVSSv3 | Writeup |
|---|---|---|---|
| *(no writeups yet)* | — | — | — |

</details>

---

<details>
<summary><b>Authentication</b> &nbsp;|&nbsp; A07:2021 – Identification Failures &nbsp;|&nbsp; 0 / 14 solved</summary>

<br>

| Lab | Difficulty | CVSSv3 | Writeup |
|---|---|---|---|
| *(no writeups yet)* | — | — | — |

</details>

---

<details>
<summary><b>OS Command Injection</b> &nbsp;|&nbsp; A03:2021 – Injection &nbsp;|&nbsp; 0 / 5 solved</summary>

<br>

| Lab | Difficulty | CVSSv3 | Writeup |
|---|---|---|---|
| *(no writeups yet)* | — | — | — |

</details>

---

<details>
<summary><b>Business Logic</b> &nbsp;|&nbsp; A04:2021 – Insecure Design &nbsp;|&nbsp; 0 / 11 solved</summary>

<br>

| Lab | Difficulty | CVSSv3 | Writeup |
|---|---|---|---|
| *(no writeups yet)* | — | — | — |

</details>

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
