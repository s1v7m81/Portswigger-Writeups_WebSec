# 2FA Broken Logic

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

Access Carlos's account page by exploiting flawed 2FA logic.

- Your credentials: `wiener:peter`
- Victim's username: `carlos`
- You have access to the email server to receive your own 2FA code.

---

## Lab

https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-broken-logic

---

## OWASP Category

A07:2021 – Identification and Authentication Failures

---

## Core Concept

After step 1 (password) succeeds, the user is sent to a `GET /login2` request that **generates and sends a fresh 2FA code** for whichever account is named in the `verify` parameter:

```http
GET /login2?verify=wiener
```

This same `verify` parameter is then echoed into the `POST /login2` request when submitting the code:

```http
POST /login2
verify=wiener&mfa-code=123456
```

**The flaw:** nothing ties the `verify` parameter back to the credentials we actually entered in step 1. Since the value travels as a regular request parameter (not a server-side session attribute), we can:

1. Send our own `GET /login2?verify=carlos` request directly — this **generates a brand-new 2FA code for Carlos** and (in the lab) makes that code guessable via brute-force, since it's now a "live" pending code
2. Submit `POST /login2` with `verify=carlos` and brute-force the `mfa-code` value

```
We log in as:        wiener / peter   (any valid credentials work to reach this stage)
We request:          GET /login2?verify=carlos   → generates a fresh code FOR CARLOS
We brute-force:      POST /login2  verify=carlos & mfa-code=§code§
Server checks:       "is this code correct for carlos?"
                              ↑
              We never needed Carlos's password — only his username
```

---

## Steps to Solve

---

**Step 1 — Log In and Observe the verify Parameter**

```
Username: wiener
Password: peter
```

With Burp/ZAP running, watch the requests around the 2FA step. After password submission you'll see:

```http
GET /login2?verify=wiener HTTP/1.1
```

followed by the code submission:

```http
POST /login2 HTTP/1.1

verify=wiener&mfa-code=482913
```

Notice the `verify` parameter is what determines whose account the code check applies to.

---

**Step 2 — Log Out**

Log out of your `wiener` session so you can re-trigger the flow cleanly.

---

**Step 3 — Generate a Code for Carlos**

Send the `GET /login2` request to Repeater and change `verify` to `carlos`:

```http
GET /login2?verify=carlos HTTP/1.1
```

Send it. This causes the server to generate a temporary 2FA code **for Carlos's account**, even though we're not authenticated as him.

<img width="940" height="205" alt="image" src="https://github.com/user-attachments/assets/ea935244-e588-4c4f-9e87-7cbba96efef7" />

---

**Step 4 — Trigger Your Own Login to Reach the Code Submission Page**

Go to the login page and enter your own valid credentials again:

```
Username: wiener
Password: peter
```

When prompted for the 2FA code, submit any **invalid** code just to get past the form and capture the resulting `POST /login2` request structure.

<img width="846" height="270" alt="image" src="https://github.com/user-attachments/assets/dafce975-64b8-4ec1-94a7-b9b27532f4a6" />

---

**Step 5 — Send the POST /login2 Request to Intruder**

Intercept the `POST /login2` request from Step 4 and send it to Intruder:

```http
POST /login2 HTTP/1.1

verify=wiener&mfa-code=1111
```

<img width="846" height="270" alt="image" src="https://github.com/user-attachments/assets/09a74400-9d39-4993-b143-5a9ed126d59b" />

---

**Step 6 — Set verify to Carlos and Brute-Force mfa-code**

In Intruder, manually set `verify=carlos` (no payload marker needed here — it's a fixed value), and mark **only** `mfa-code` as the payload position:

```http
verify=carlos&mfa-code=§0000§
```

Use a **File** payload type, **0000–9999.txt have list of numbers from 0000 to 9999**, zero-padded to **4 digits**. Start the fuzzer.

<img width="588" height="388" alt="image" src="https://github.com/user-attachments/assets/6e1001d2-c448-4237-a479-a85b911c6093" />

<img width="971" height="351" alt="image" src="https://github.com/user-attachments/assets/95104850-337f-4722-9a96-01112ca06e57" />


Sort results by **status code / length** — the correct code returns a `302` redirect instead of the usual error response.

<img width="1900" height="197" alt="image" src="https://github.com/user-attachments/assets/f86bbcf2-a7b6-404d-9599-628a4169571b" />

---

**Step 7 — Load the 302 Response in the Browser**

Take the request that returned `302` and load it in the browser (or follow the redirect manually) to obtain Carlos's authenticated session.

<img width="1724" height="825" alt="image" src="https://github.com/user-attachments/assets/59712b96-f960-482b-94f8-c0d5d0c77a62" />

---

**Step 8 — Access My Account**

Click **My account** to confirm you're logged in as Carlos.

<img width="827" height="254" alt="image" src="https://github.com/user-attachments/assets/0e2401ed-e488-4797-8de8-b9283ae9368d" />

---

**Lab Solved**

<img width="1585" height="347" alt="image" src="https://github.com/user-attachments/assets/09552500-4d1d-48e6-9344-5d3adcd5a4c9" />

---

## Why This Works

```
Server logic (flawed):
GET  /login2?verify=X   → generates/sends a fresh 2FA code for user X
                           (no check that "we" are actually X)
POST /login2  verify=X & mfa-code=Y
                        → checks: "is Y correct for user X?"
                        → never verifies that X matches who completed
                          the password step, or that we're authorized
                          to even be requesting a code for X at all
```

The `verify` parameter is meant to be an internal tracking value carried through the multi-step flow, but since it's a **regular client-supplied parameter** with no server-side binding to the authenticated session, it becomes the entire trust boundary for the second factor — and worse, it lets us *trigger code generation* for an arbitrary account on demand.

---

## How This Differs from Lab 7

| | Lab 7 (Simple Bypass) | Lab 8 (Broken Logic) |
|--|--|--|
| Flaw | Server doesn't enforce step 2 at all | `verify` parameter controls whose account is checked, with no binding to the actual session |
| Need victim's password | No | No |
| Need victim's 2FA code | No | No — generated on demand via `verify=carlos`, then brute-forced |
| Technique | Skip directly to account page | Generate Carlos's code via `GET /login2?verify=carlos`, then brute-force `mfa-code` via Intruder |

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
