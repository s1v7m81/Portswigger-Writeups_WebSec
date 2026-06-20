# Username Enumeration via Different Responses

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

Enumerate a valid username, brute-force this user's password, then access their account page.

---

## Lab

https://portswigger.net/web-security/authentication/other-mechanisms/lab-username-enumeration-via-different-responses

---

## OWASP Category

A07:2021 – Identification and Authentication Failures

---

## Core Concept

**Username Enumeration** occurs when the application's response **changes visibly** depending on whether a username exists or not. This lets an attacker build a list of valid usernames before even attempting passwords.

```
Login with INVALID username → "Invalid username"
Login with VALID username + wrong password → "Invalid password"
                                                    ↑
                                          Different message = username confirmed!
```

This converts a 2-unknown problem (username AND password) into two separate 1-unknown problems — massively reducing brute-force time.

---

## Steps to Solve

---

**Step 1 — Identify the Difference in Responses**

Go to the login page and submit clearly invalid credentials:

```
Username: invaliduser12345
Password: invalidpass12345
```

Response:
```
"Invalid username"
```

<img width="965" height="430" alt="image" src="https://github.com/user-attachments/assets/293bd801-909e-401c-b92a-74a52cca26a7" />

---

**Step 2 — Enumerate Valid Username with ZAP Fuzzer**

Intercept a login POST request:

```http
POST /login HTTP/1.1
Host: lab-id.web-security-academy.net

username=invalid&password=invalid
```

**ZAP Fuzzer Setup:**

Mark `invalid` (username value) as payload position:
```http
username=§invaliduser§&password=invalid
```

Payload type: `File` — candidate usernames wordlist (from PortSwigger)

**Filter results:**

| Response Text | Meaning |
|---------------|---------|
| "Invalid username" | Username does not exist |
| "Invalid password" | Username EXISTS |

<img width="1324" height="796" alt="image" src="https://github.com/user-attachments/assets/314bbb0a-a78c-4243-a290-82667c302b5d" />

Valid username found: **americas**

---

**Step 3 — Brute-Force the Password**

Now fix the username and fuzz the password:

```http
username=foundusername&password=§invalidpass§
```

Payload type: `File` — candidate passwords wordlist

**Filter results:**

| Response | Meaning |
|----------|---------|
| "Invalid password" | Wrong password |
| Redirect / 302 / different status | Correct password |

<img width="1516" height="792" alt="image" src="https://github.com/user-attachments/assets/9c8d9dd9-0a09-45c4-84d5-9fe3e8fefc5a" />

Password found: **jessica**

---

**Step 4 — Log In and Access Account Page**

```
Username: americas
Password: jessica
```

---

**Lab Solved**

<img width="1503" height="751" alt="image" src="https://github.com/user-attachments/assets/9bbdc24d-d9dd-47b5-a36e-d548b1734439" />

---

## Key Detection Signals

| Signal | Example |
|--------|---------|
| Different error text | "Invalid username" vs "Invalid password" |
| Different status code | 200 vs 302 |
| Different page content | Login form vs account dashboard |
| Different response length | Subtle byte differences |

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
