# Username Enumeration via Account Lock

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

Enumerate a valid username, brute-force this user's password, then access their account page.

---

## Lab

https://portswigger.net/web-security/authentication/other-mechanisms/lab-username-enumeration-via-account-locking

---

## OWASP Category

A07:2021 – Identification and Authentication Failures

---

## Core Concept

This application tries to prevent brute-forcing by **locking the account** after too many failed attempts. However, the **lockout message itself leaks whether the username is valid**:

```
Invalid username, any password    → "Invalid username or password"
Valid username, wrong password x1 → "Invalid username or password"
Valid username, wrong password x4 → "Your account is locked"
                                            ↑
                                  Only VALID usernames can be locked!
                                  Invalid usernames never show this message
```

This means: if we submit several wrong passwords for a given username and **eventually see a lockout message**, that proves the username is valid — even though individual attempts looked identical before the lock triggered.

---

## Steps to Solve

---

**Step 1 — Confirm the Lockout Behavior**

Try a known invalid username repeatedly with wrong passwords:

```
invaliduser12345 / wrong1
invaliduser12345 / wrong2
invaliduser12345 / wrong3
invaliduser12345 / wrong4
```

Response is always:
```
"Invalid username or password"
```

Never locks — because the username doesn't exist.

<img width="1866" height="224" alt="image" src="https://github.com/user-attachments/assets/eb926f07-570f-45dc-9f12-72525b41d0a2" />

---

**Step 2 — Enumerate Usernames with ZAP Fuzzer (Multiple Attempts Each)**

Since one wrong attempt looks the same regardless of validity, we need **multiple attempts per username** to trigger the lock if it's valid.

**Approach — for each candidate username, send 5 wrong password attempts:**

```http
POST /login HTTP/1.1

username=§candidate§&password=wrong1
```

Run the **same username 5 times** with different wrong passwords, OR use a script to automate "try each username 4 times then check for lock message". For **5 time** repeatation we add payload position at **worng[here]** as numberuzz type with 1 to 4 number. Also we add **thread 2 per second** for better result.

<img width="1083" height="412" alt="image" src="https://github.com/user-attachments/assets/1d5c34a1-abc1-4120-86ee-71344e537165" />

**Simplified ZAP approach:**

1. Fuzz with candidate usernames wordlist, same wrong password each time
2. Repeat the entire fuzzing run **5 times** (or until accounts get locked)
3. On the final run, filter for **"locked"** in response — those usernames are valid

<img width="1741" height="390" alt="image" src="https://github.com/user-attachments/assets/318e5bcd-c26c-479a-a05c-7865d249f8de" />

Valid username found: **adkit**

---

**Step 3 — Wait for Lock to Clear (if needed) or Use Different Approach**

If the account is now locked, we cannot brute-force it directly. Some labs allow continued attempts to still reveal the correct password via timing or the lock simply prevents login but we still confirmed the username.

Check if a **different response occurs for the correct password even while locked**:

```
Locked account + WRONG password → "Account locked"
Locked account + CORRECT password → sometimes different message or behavior or no error saw!
```

---

**Step 4 — Brute-Force Password**

Using the found username, fuzz passwords:

```http
username=adkit&password=§candidatepass§
```

Look for the differentiating response that indicates the correct password (even within lock messaging). We found that correct password have **no error message** with smallest size of response after account even locked.

<img width="1748" height="106" alt="image" src="https://github.com/user-attachments/assets/1fd4b632-40ff-40c9-a4ab-3f0dc686c54a" />

Password found: **666666**

---

**Lab Solved**

<img width="1508" height="758" alt="image" src="https://github.com/user-attachments/assets/0ef61767-a7c7-40bc-803e-4ae6d7604173" />

---

## Key Insight

```
Account locking protects against:
Targeted brute-force of ONE specific account

Account locking does NOT protect against:
Username enumeration (lock message itself leaks validity)
Brute-forcing MANY accounts with FEW passwords each (see Lab 6)
Credential stuffing attacks
```

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
