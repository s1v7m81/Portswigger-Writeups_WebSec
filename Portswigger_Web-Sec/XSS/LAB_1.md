# [Lab Title]

[![Platform](https://img.shields.io/badge/Platform-PortSwigger_Web_Academy-orange?style=flat-square)](https://portswigger.net/web-security)
[![Standard](https://img.shields.io/badge/Standard-OWASP_WSTG-blue?style=flat-square)](https://owasp.org/www-project-web-security-testing-guide/)
[![Status](https://img.shields.io/badge/Status-Solved-brightgreen?style=flat-square)]()
[![Difficulty](https://img.shields.io/badge/Difficulty-Practitioner-yellow?style=flat-square)]()

---

## Lab Information

| Field | Details |
|---|---|
| **Lab Name** | [Full lab name from PortSwigger] |
| **Category** | [e.g. SQL Injection / XSS / CSRF / SSRF / XXE] |
| **Difficulty** | Apprentice / Practitioner / Expert |
| **OWASP Category** | [e.g. A03:2021 – Injection] |
| **CWE** | [e.g. CWE-89 – Improper Neutralization of SQL Commands] |
| **CVSSv3 Score** | [e.g. 9.8 Critical / 7.5 High / 5.0 Medium] |
| **Lab URL** | [Link](https://portswigger.net/web-security/) |
| **Date Solved** | YYYY-MM-DD |
| **Author** | [Your GitHub Username] |

---

## Objective

> Paste or paraphrase the lab goal from PortSwigger.

---

## Vulnerability Overview

### Definition

[Vulnerability Name] is a security weakness that occurs when **[root cause]**. An attacker can exploit this to **[impact]**. This is classified under **[OWASP Category]** and **[CWE-XXX]**.

### CVSS Risk Factors

| Factor | Value |
|---|---|
| **Attack Vector** | Network / Adjacent / Local / Physical |
| **Attack Complexity** | Low / High |
| **Privileges Required** | None / Low / High |
| **User Interaction** | None / Required |
| **Confidentiality Impact** | None / Low / High |
| **Integrity Impact** | None / Low / High |
| **Availability Impact** | None / Low / High |

---

## Impact Assessment

| Severity | Detail |
|---|---|
| Critical | [e.g. Full authentication bypass] |
| High | [e.g. Sensitive data exposure] |
| Medium | [e.g. Privilege escalation] |
| Low | [e.g. Information disclosure] |

Applicable to this lab:

- [ ] Authentication Bypass
- [ ] Sensitive Data Exposure
- [ ] Remote Code Execution
- [ ] Privilege Escalation
- [ ] Data Manipulation
- [ ] Other: ___________

---

## Tools Used

| Tool | Purpose |
|---|---|
| Burp Suite Community / Pro | Intercept and manipulate HTTP traffic |
| Firefox / Chrome | Lab interaction |
| [Additional tool] | [Purpose] |

---

## Reconnaissance

### Step 1 — Identify the Attack Surface

- URL: `https://[lab-id].web-security-academy.net/[path]`
- Observed: [what you noticed — e.g. login form, search bar, URL parameter]
- Hypothesis: [why it might be vulnerable]

**Screenshot:**

![Recon - Attack Surface](./screenshots/01-recon-attack-surface.png)

---

### Step 2 — Probe for Vulnerability

**Test Request:**

```http
GET /path?param=test' HTTP/1.1
Host: [lab-id].web-security-academy.net
Cookie: session=[token]
```

**Observed Response:**

```
[Paste relevant part of response or describe behavior change]
```

**Screenshot:**

![Recon - Probe](./screenshots/02-probe-response.png)

> Finding: [What confirmed the vulnerability — error message, behavior difference, response time change.]

---

## Exploitation

### Step 1 — [Action Title]

**Action:**
> [Explain what you did in this step and why.]

**Request:**

```http
POST /login HTTP/1.1
Host: [lab-id].web-security-academy.net
Content-Type: application/x-www-form-urlencoded

username=administrator'--&password=anything
```

**Response:**

```http
HTTP/1.1 302 Found
Location: /my-account
```

**Screenshot:**

![Step 1](./screenshots/03-step1.png)

> Result: [What happened? What access did you gain?]

---

### Step 2 — [Action Title]

**Action:**
> [Explain what you did next.]

**Payload:**

```
[Paste payload or relevant input]
```

**Screenshot:**

![Step 2](./screenshots/04-step2.png)

> Result: [What happened?]

---

### Step 3 — [Action Title]

> Add or remove steps as needed. Keep each step focused on one action.

**Screenshot:**

![Step 3](./screenshots/05-step3.png)

> Result: [What happened?]

---

## Proof of Concept

**Final Payload:**

```
[Exact payload that solved the lab]
```

**Final Request:**

```http
POST /login HTTP/1.1
Host: [lab-id].web-security-academy.net
Content-Type: application/x-www-form-urlencoded

username=administrator'--&password=x
```

**Screenshot:**

![Lab Solved](./screenshots/06-lab-solved.png)

---

## Remediation

### Root Cause

[Explain why the vulnerability existed — e.g. unsanitized user input passed directly into a SQL query without parameterization.]

### Vulnerable vs Secure Code

```[language]
// VULNERABLE
$query = "SELECT * FROM users WHERE username='" . $_POST['username'] . "'";

// SECURE — Use parameterized queries
$stmt = $pdo->prepare("SELECT * FROM users WHERE username = ?");
$stmt->execute([$_POST['username']]);
```

### Remediation Checklist

| Priority | Recommendation |
|---|---|
| Critical | Use parameterized queries or prepared statements |
| High | Validate and sanitize all user-supplied inputs |
| Medium | Apply least-privilege principle to database accounts |
| Medium | Deploy WAF rules targeting common injection patterns |
| Low | Conduct regular security code reviews and SAST scanning |

---

## References

| Resource | Link |
|---|---|
| PortSwigger Lab | [Lab URL](https://portswigger.net/web-security/) |
| PortSwigger Learning Material | [Topic Page](https://portswigger.net/web-security/) |
| OWASP – [Vulnerability] | [OWASP Reference](https://owasp.org/www-community/attacks/) |
| CWE-[XXX] | [CWE Reference](https://cwe.mitre.org/data/definitions/XXX.html) |
| CVSS v3 Calculator | [NVD Calculator](https://nvd.nist.gov/vuln-metrics/cvss/v3-calculator) |

---

## Notes

> Things I learned, struggled with, or want to remember for similar labs.

- 
- 

---

*Author: [Your Name] | [GitHub](https://github.com/yourusername) | Reports follow [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)*
