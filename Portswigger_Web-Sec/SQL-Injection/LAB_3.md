# SQL injection UNION attack, determining the number of columns returned by the query

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

To solve the lab, determine the number of columns returned by the query by performing a SQL injection UNION attack that returns an additional row containing null values.

---

## Lab

https://portswigger.net/web-security/sql-injection/union-attacks/lab-determine-number-of-columns

---

## OWASP Category

SQLi-UNION

---

## Steps to Solve

**Step 1 — Check the pet parameter**

Try to see one parameter on web app.

<img width="1084" height="685" alt="image" src="https://github.com/user-attachments/assets/ea7bfeac-df7c-425f-9972-59eaa47bba5c" />


---

**Step 2 — Payload in URL**

Inject the SQL payload in url to check number of columns use by current web app from databse.
We use **UNION** keyword to check the columns. Although we can use **ORDER BY** that see same result.

```http
' UNION SELECT NULL,NULL,NULL--
```

Until **same columns** found **UNION based** atteck **saw error** likely **internal server** error but ater same number of columns found then error not appear.

<img width="1230" height="315" alt="image" src="https://github.com/user-attachments/assets/ab237755-1036-4408-b416-1332fbe95d83" />


---

**Step 3 — After successfull payload**

<img width="1523" height="486" alt="image" src="https://github.com/user-attachments/assets/4ebc644e-15b0-4d31-92dc-f3f5c026a793" />


---

**Lab Solved**

<img width="1522" height="740" alt="image" src="https://github.com/user-attachments/assets/0aa76bc3-3e11-48bc-b6da-51e757a5942b" />


---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
