# 2FA Simple Bypass

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

Access Carlos's account page without his 2FA verification code.

- Your credentials: `wiener:peter`
- Victim's credentials: `carlos:montoya`

---

## Lab

https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-simple-bypass

---

## OWASP Category

A07:2021 – Identification and Authentication Failures

---

## Core Concept

Many 2FA implementations use a **multi-step flow**: enter password → redirected to a separate page → enter verification code → land on account page. The flaw here is that the server sometimes considers the user **already authenticated** after step 1, and never actually re-checks whether step 2 (the code) was completed before serving "logged-in only" pages.

```
Step 1: POST /login         (username + password)   → 200 OK, redirect to /login2
Step 2: GET  /login2                                  → shows verification code form
              ↑
    If the server already treats you as "logged in" here,
    you can skip straight to /my-account without ever
    submitting a code at all.
```

---

## Steps to Solve

---

**Step 1 — Log In with Your Own Credentials**

```
Username: wiener
Password: peter
```

You're redirected to the 2FA verification code page:

```
GET /login2
```

<img width="980" height="585" alt="image" src="https://github.com/user-attachments/assets/92f422e8-80e4-42af-8b11-83a6f1be5e8d" />

---

**Step 2 — Try Navigating Directly to the Account Page**

Without entering any verification code, manually browse to:

```
GET /my-account
```

If the account page loads successfully — the server never checked whether step 2 was completed.

<img width="1531" height="767" alt="image" src="https://github.com/user-attachments/assets/909c5b63-4d6d-43c1-9734-d3aa6ccff5a1" />

---

**Step 3 — Repeat as Carlos**

Log out, then log in with the victim's credentials:

```
Username: carlos
Password: montoya
```

You're redirected to the 2FA code page — but again, skip it entirely:

```
GET /my-account
```

<img width="1146" height="778" alt="image" src="https://github.com/user-attachments/assets/b8dea4bf-c0ba-49d0-917a-fe1afc87cf7a" />

---

**Lab Solved**

<img width="1537" height="557" alt="image" src="https://github.com/user-attachments/assets/345d5888-da46-4d1d-83a1-f5f04971b948" />

---

## Why This Works

```
Server logic (flawed):
POST /login (correct username + password)
   → server marks session as "authenticated" immediately
   → redirects to /login2 (just a UI suggestion, not enforced)

GET /my-account
   → server checks: "is session authenticated?" YES
   → serves the page
   → never checks: "did this session complete step 2?"
```

The verification code page is purely a **UI redirect** — the actual access control decision was already made (incorrectly) after step 1.

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
