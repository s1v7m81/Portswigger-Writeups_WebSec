# Turbo Intruder — Usage Guide

> A Burp Suite extension for sending large numbers of HTTP requests and analyzing the results. Built to complement Burp Intruder for attacks that need extreme speed, scale, or custom logic.

[![BApp Store](https://img.shields.io/badge/Burp-BApp%20Store-orange)](https://portswigger.net/bappstore/bapps/download/9abaa233088242e8be252cd4ff534988/65)

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Core Concepts](#core-concepts)
- [Step-by-Step: Your First Attack](#step-by-step-your-first-attack)
- [Common Patterns](#common-patterns)
  - [Wordlist / Brute Force](#1-wordlist--brute-force)
  - [Rate-Limited Requests](#2-rate-limited-requests)
  - [Race Conditions (Last-Byte Sync)](#3-race-conditions-last-byte-sync)
  - [Single-Packet Attack (HTTP/2)](#4-single-packet-attack-http2)
  - [Filtering Results with handleResponse](#5-filtering-results-with-handleresponse)
  - [Using Burp's Network Stack](#6-using-burps-network-stack)
- [Running Headless / From the Command Line](#running-headless--from-the-command-line)
- [Tips & Troubleshooting](#tips--troubleshooting)
- [Responsible Use](#responsible-use)
- [Further Reading](#further-reading)

---

## Overview

Turbo Intruder trades the point-and-click simplicity of Burp Intruder for raw throughput and scriptability. Instead of configuring attacks through a GUI wizard, you write a short Python script that tells Turbo Intruder's engine what to send and how to react. This makes it suited for:

- Brute-forcing at high request volume
- Multi-day fuzzing campaigns with flat memory usage
- Race condition testing (including HTTP/2 single-packet attacks)
- Multi-step attack sequences (e.g. fetching a CSRF token, then using it)
- Anything where Burp Intruder's request rate or logic is a bottleneck

Trade-off: it's harder to use than core Intruder, and its custom HTTP stack is less battle-tested than Burp's own.

## Prerequisites

- Burp Suite (Community or Professional) — Turbo Intruder works in both, though some features (e.g. Collaborator integration, `Engine.BURP`/`Engine.BURP2`) assume Pro features are available
- Basic Python familiarity (the attack scripts are plain Python)
- A target you are **authorized to test**

## Installation

**From the BApp Store (recommended):**

1. Open Burp Suite
2. Go to the **Extensions** tab → **BApp Store**
3. Search for **Turbo Intruder**
4. Click **Install**

**From source:**

1. Clone the repo: `git clone https://github.com/PortSwigger/turbo-intruder.git`
2. Build it: `./gradlew build fatJar`
3. In Burp, go to **Extensions → Installed → Add**, and select `build/libs/turbo-intruder-all.jar`

## Core Concepts

| Concept | Description |
|---|---|
| `queueRequests(target, wordlists)` | The entry point Turbo Intruder calls. You build a `RequestEngine` here and queue requests against it. |
| `RequestEngine(...)` | The object that actually sends requests. Configured with the endpoint, concurrency, requests-per-connection, and which network stack to use. |
| `engine.queue(request, payloads, ...)` | Submits one request to be sent. `%s` markers in the request template get replaced with the payload(s) you pass in. |
| `gate` / `engine.openGate(name)` | Used to hold a batch of requests just before they complete, then release them together — the basis of race-condition attacks. |
| `label` | An optional tag on a queued request so you can identify it later in `handleResponse`. |
| `handleResponse(req, interesting)` | Optional callback fired for each response. Use it to filter, log, or store results (e.g. with `table.add(req)`). |
| `Engine.BURP` / `Engine.BURP2` | Tell Turbo Intruder to use Burp's own HTTP/1 or HTTP/2 stack (slower, but supports upstream proxies, Collaborator, etc.) instead of its custom stack. |

## Step-by-Step: Your First Attack

1. **Capture a request.** Browse the target through Burp's proxy, or send a request through Repeater, so it appears somewhere you can right-click it (Proxy history, Repeater, Logger, etc.)
2. **Select the injection point.** Highlight the part of the request you want to fuzz — a parameter value, header, path segment, anything.
3. **Send it to Turbo Intruder.** Right-click → **Extensions → Turbo Intruder → Send to Turbo Intruder**. A new window opens with your request at the top (the highlighted text is now replaced with `%s`) and a Python editor below it.
4. **Write or adapt your attack script.** At minimum you need a `queueRequests` function. A minimal example:

   ```python
   def queueRequests(target, wordlists):
       engine = RequestEngine(
           endpoint=target.endpoint,
           concurrentConnections=5,
           requestsPerConnection=100,
       )

       for word in open('/path/to/wordlist.txt'):
           engine.queue(target.req, word.rstrip())

   def handleResponse(req, interesting):
       table.add(req)
   ```

5. **Launch the attack.** Click **Attack**. A results table opens showing status code, length, word count, and timing per request, with sorting/filtering available — much like Intruder's results view.
6. **Review and pivot.** Sort by length or status to spot anomalies, then send any interesting request to Repeater for manual follow-up.

## Common Patterns

### 1. Wordlist / Brute Force

```python
def queueRequests(target, wordlists):
    engine = RequestEngine(
        endpoint=target.endpoint,
        concurrentConnections=10,
        requestsPerConnection=20,
    )

    for username in open('usernames.txt'):
        for password in open('passwords.txt'):
            engine.queue(target.req, [username.rstrip(), password.rstrip()])

def handleResponse(req, interesting):
    # Only keep responses that look like a successful login
    if req.status == 302:
        table.add(req)
```

Note the list `[username, password]` — when a request has multiple `%s` markers, pass payloads as a list in the order they appear.

### 2. Rate-Limited Requests

If the target throttles or you simply want to be gentler, add a delay inside the loop:

```python
import time

def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint, concurrentConnections=1)

    for word in wordlists.observedWords:
        engine.queue(target.req, word, label='fuzz')
        time.sleep(0.5)  # 500ms between requests
```

### 3. Race Conditions (Last-Byte Sync)

Turbo Intruder can hold a group of requests open and release the final byte of each almost simultaneously, maximizing the chance of hitting a race window:

```python
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint, concurrentConnections=1)

    for i in range(20):
        engine.queue(target.req, gate='race1')

    # Releases the final byte of every 'race1' request at once
    engine.openGate('race1')
    engine.complete(timeout=60)

def handleResponse(req, interesting):
    table.add(req)
```

### 4. Single-Packet Attack (HTTP/2)

For targets that support HTTP/2, requests can be sent in a single TCP packet, which sidesteps network jitter entirely and is the most reliable way to trigger tight race windows:

```python
def queueRequests(target, wordlists):
    engine = RequestEngine(
        endpoint=target.endpoint,
        concurrentConnections=1,
        engine=Engine.BURP2,  # required for the single-packet technique
    )

    for i in range(20):
        engine.queue(target.req, gate='race1')

    engine.openGate('race1')
    engine.complete(timeout=60)
```

Requirements: target must support HTTP/2, and `concurrentConnections` must be `1`.

### 5. Filtering Results with handleResponse

Turbo Intruder's built-in diffing can hide "boring" (expected/baseline) results automatically. You can also filter manually:

```python
def handleResponse(req, interesting):
    # req.status, req.wordcount, req.length, req.response, req.time are available
    if req.status != 401:
        table.add(req)
```

### 6. Using Burp's Network Stack

By default Turbo Intruder uses its own hand-built HTTP stack for speed. If you need upstream proxy support, Collaborator integration, or just more reliability at the cost of raw speed, switch engines:

```python
def queueRequests(target, wordlists):
    engine = RequestEngine(
        endpoint=target.endpoint,
        concurrentConnections=5,
        engine=Engine.BURP,   # or Engine.BURP2 for HTTP/2
    )

    collab_domain = api.collaborator().defaultPayloadGenerator().generatePayload()

    for word in open('wordlist.txt'):
        engine.queue(target.req, word.rstrip())
```

## Running Headless / From the Command Line

Turbo Intruder scripts can also be run outside the Burp GUI for long-running or scripted campaigns. This is useful for multi-day attacks where you don't want a GUI session tying things up. Refer to the project's `cli.py` / documentation in the [GitHub repo](https://github.com/PortSwigger/turbo-intruder) for the exact invocation, since the interface has changed across versions — check the version bundled with your Burp install.

## Tips & Troubleshooting

- **Deadlocks with `gate`:** if you queue more gated requests than `concurrentConnections`, the attack will deadlock — Turbo Intruder will throw an error reminding you to raise `concurrentConnections`.
- **Malformed requests:** the custom HTTP stack can send deliberately malformed requests that other libraries would refuse to send — useful for protocol-level testing, but double-check your template if you get unexpected server errors.
- **Memory over long runs:** Turbo Intruder is built for flat memory usage over multi-day attacks; if you see memory creep, check whether your `handleResponse` callback is accumulating data (e.g. appending to a list) without bound.
- **Picking an engine:** default custom stack = fastest; `Engine.BURP`/`Engine.BURP2` = slower but respects upstream proxy settings and plays nicer with other Burp features.
- **CSRF tokens / multi-step flows:** combine Turbo Intruder with Burp's session handling rules and macros (Settings → Sessions → Macros) so a token-fetching request runs automatically before each attack request.

## Responsible Use

Turbo Intruder is built for **authorized security testing only** — penetration tests, bug bounty programs, and testing your own applications. Sending high-volume or malformed traffic to systems you don't have explicit permission to test is illegal in most jurisdictions and can cause real damage (downtime, data corruption, account lockouts). Always:

- Get written authorization before testing
- Respect the scope of any bug bounty program
- Start with low concurrency and ramp up carefully
- Be especially cautious with destructive payloads (account creation, state-changing requests) in brute-force loops

## Further Reading

- [Turbo Intruder: Embracing the billion-request attack](https://portswigger.net/research/turbo-intruder-embracing-the-billion-request-attack) — the original write-up and demo by James Kettle
- [PortSwigger/turbo-intruder on GitHub](https://github.com/PortSwigger/turbo-intruder) — source code and the `resources/examples/` directory, which contains many ready-to-adapt scripts
- [BApp Store listing](https://portswigger.net/bappstore/bapps/download/9abaa233088242e8be252cd4ff534988/65)

---

*Contributions welcome — feel free to open a PR with additional examples or corrections.*
