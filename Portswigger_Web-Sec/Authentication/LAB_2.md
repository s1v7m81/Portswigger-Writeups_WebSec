# Username Enumeration via Subtly Different Responses

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

Enumerate a valid username, brute-force this user's password, then access their account page.

---

## Lab

https://portswigger.net/web-security/authentication/other-mechanisms/lab-username-enumeration-via-subtly-different-responses

---

## OWASP Category

A07:2021 – Identification and Authentication Failures

---

## Core Concept

Unlike Lab 1 where messages were **completely different**, here the developer tried to fix the issue by using the **same generic error message** for both cases. However a tiny implementation mistake leaves a detectable difference:

```
Invalid username → "Invalid username or password."
Invalid password → "Invalid username or password"
                                                  ↑
                                          Missing/extra period!
```

Even a single character difference — like a missing full stop, extra space, or different capitalization — is enough to distinguish the two cases programmatically, even if invisible to the human eye on the rendered page.

---

## Steps to Solve

---

**Step 1 — Compare Responses Carefully**

Submit invalid username:
```
Username: invaliduser12345
Password: anything
```

Response body (view raw HTML, not rendered page):
```html
"Invalid username or password."
```

<img width="1445" height="439" alt="image" src="https://github.com/user-attachments/assets/2f9389af-e8c8-4f2a-9536-19495b4e9da2" />

Submit a candidate username with wrong password:
```
Username: admin[for example only, this is not actual]
Password: anything
```

Response body:
```html
"Invalid username or password"
```


The messages look **identical when rendered** in browser, but differ at the **byte level** — one has a trailing period, one does not.

---

**Step 2 — Confirm via Response Length**

In ZAP, check the **Size Resp. Body** column for both requests — even a 1-byte difference confirms this.

| Response | Size |
|----------|------|
| Invalid username | 3021 bytes |
| Invalid password (valid username) | 3020 bytes |

---

**Step 3 — Enumerate Username with ZAP Fuzzer**

```http
POST /login HTTP/1.1

username=§invaliduser§&password=invalid
```

Payload: candidate usernames wordlist.

**Sort results by Size Resp. Body** — the row with a different size = valid username.

<img width="1204" height="593" alt="image" src="https://github.com/user-attachments/assets/d3f5f306-257c-4417-8975-b496224550a5" />

Valid username found: **adam**

---

**Step 4 — Brute-Force Password**

```http
username=foundusername&password=§invalidpass§
```

Payload: candidate passwords wordlist.

Filter for **302 redirect** or different response size indicating success.

<img width="1443" height="558" alt="image" src="https://github.com/user-attachments/assets/105d0859-9257-488e-a813-44dac860df0d" />

Password found: **cheese**

---

**Lab Solved**

<img width="1519" height="755" alt="image" src="https://github.com/user-attachments/assets/f5da2764-f328-4427-9cac-95de5fe8bebc" />

---

## How This Differs from Lab 1

| | Lab 1 | Lab 2 |
|--|--|--|
| Message difference | Obvious — different text | Subtle — 1 character difference |
| Detection method | Read response text | Compare response byte size |
| Visible to human eye | Yes | No — needs tool comparison |

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
