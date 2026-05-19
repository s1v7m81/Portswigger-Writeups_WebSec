# SQL injection vulnerability allowing login bypass


> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

To solve the lab, perform a SQL injection attack that logs in to the application as the administrator user.

---

## Lab

https://portswigger.net/web-security/sql-injection/lab-login-bypass

---

## OWASP Category

SQLi

---

## Steps to Solve

**Step 1 — Ensure the Vulnerability**

See the parameter use in login with use of burp suite.

<img width="690" height="301" alt="image" src="https://github.com/user-attachments/assets/182132b4-aaa3-4431-858b-323d9d95294b" />

---

**Step 2 — Change SQL quary**

Inject our own quary to manipulate logic of username

```http
administrator'-- -
```

<img width="808" height="110" alt="image" src="https://github.com/user-attachments/assets/c90242f8-2e9a-4bde-9d60-bc4764ac4d71" />

---

**Step 3 — Login Successfully**


<img width="1061" height="395" alt="image" src="https://github.com/user-attachments/assets/9fa73201-e128-4840-bdf9-8974acccd0dc" />

---

**Lab Solved**


<img width="1505" height="306" alt="image" src="https://github.com/user-attachments/assets/b4d4a1d4-bfba-456a-8bab-49abb59d2557" />

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
