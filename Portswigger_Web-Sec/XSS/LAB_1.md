# Reflected XSS into HTML context with nothing encoded
> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

This lab contains a simple reflected cross-site scripting vulnerability in the search functionality.
To solve the lab, perform a cross-site scripting attack that calls the alert function.

---

## Lab

https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded

---

## OWASP Category

XSS

---

## Steps to Solve

**Step 1 — Find type of XSS**

<img width="1577" height="898" alt="image" src="https://github.com/user-attachments/assets/8bb93a08-1bf5-4688-a113-5127dcd9ba72" />


We search sample text in search box function in website to see which type XSS.


<img width="1253" height="642" alt="image" src="https://github.com/user-attachments/assets/c47f9b04-cdc1-430d-84c0-ad9433eb6ea2" />


In URL box we found parameter **?search=test**. May be **Reflected XSS**


---

**Step 2 — Upload Payload**

Upload payload line in parameter **search**.

```http
<script>alert("HACKER")</script>
```

<img width="816" height="359" alt="image" src="https://github.com/user-attachments/assets/6c431048-d379-4442-b3cc-58c7fb83da86" />


After that we check source code before refresh and after refresh.**1** is before refresh and **2** is after refresh

**1**
<img width="734" height="127" alt="image" src="https://github.com/user-attachments/assets/5009ac43-bda4-497a-aa2f-e438dbdc390a" />


**2**
<img width="681" height="122" alt="image" src="https://github.com/user-attachments/assets/c75e8c86-198c-4e95-ae4f-42700b0e593d" />


After refresh no script is visible upload by us. It conformed that this is **Refelcted XSS**.That only refelct http perticular request by server that manuplate by attecker not stored that on server.

**Lab Solved**

<img width="1656" height="303" alt="image" src="https://github.com/user-attachments/assets/6195227e-1f22-4373-af0a-edd40365e479" />

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
