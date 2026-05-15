# DOM XSS in document.write sink using source location.search
> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

To solve this lab, perform a cross-site scripting attack that calls the alert function.

---

## Lab

https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink

---

## OWASP Category

XSS

---

## Steps to Solve

**Step 1 — Sample test**

We use **test** keyword in search function on web app.

<img width="1505" height="551" alt="image" src="https://github.com/user-attachments/assets/6ffeb5b3-d851-433e-8714-233fe271e2ee" />

---

**Step 2 — Inspect the things**

Open **inspect** on chrome browser and open **source** tab and see one script have one tag where input goes inside web app from search function.


<img width="768" height="190" alt="image" src="https://github.com/user-attachments/assets/9f060d6a-3eca-424f-9656-9226473fc0a6" />


we found this one **document.write('<img src="/resources/images/tracker.gif?searchTerms='+query+'">');**.

---

**Step 3 — Test Payload**

After see the source we upload the payload as attribute.
```http
<img src="" onload=alert(1)>
```

<img width="1278" height="257" alt="image" src="https://github.com/user-attachments/assets/6f11c59a-e757-42d2-989f-41b1186f762f" />

Get alert so **INPUT IN** *sink** is **not sanatized**. It's **DOM Based XSS**.

---

**Lab Solved**

<img width="1478" height="554" alt="image" src="https://github.com/user-attachments/assets/9b22a8f4-ed79-4b97-ae3e-ae7fd10571a6" />

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
