# Stored XSS into HTML context with nothing encoded

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

This lab contains a stored cross-site scripting vulnerability in the comment functionality.
To solve this lab, submit a comment that calls the alert function when the blog post is viewed.

---

## Lab

https://portswigger.net/web-security/cross-site-scripting/stored/lab-html-context-nothing-encoded

---

## OWASP Category

XSS

---

## Steps to Solve

**Step 1 — Find vulrable function**

<img width="1487" height="571" alt="image" src="https://github.com/user-attachments/assets/9b579df7-9283-49c8-9628-869e2df1aec9" />

We found the **comment section** in every post that may be vulnerable to XSS.


---

**Step 2 — Upload the payload**

As in lab mention , the lab for stored XSS. We add script in vulnrable function in web application.
```http
<script>alert("1")</script>
```

<img width="927" height="310" alt="image" src="https://github.com/user-attachments/assets/b095576b-f904-4bba-9437-21ca551d912f" />


Result after send comment.

<img width="748" height="281" alt="image" src="https://github.com/user-attachments/assets/8fe84e61-9a40-4ad6-9617-e20224edfcfb" />



---

**Step 3 — Is XSS IS PERSISTENT ?**

We refresh the page and see from another device also , we saw same code in source code of web application.**Conformed Stored XSS**

<img width="368" height="82" alt="image" src="https://github.com/user-attachments/assets/0e3a8fa3-ece2-489f-88fa-99882173184d" />


---

**Lab Solved**

<img width="1502" height="492" alt="image" src="https://github.com/user-attachments/assets/8aef9f0a-5ec3-4761-b9fa-840d0ba392e6" />


---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
