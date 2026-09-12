<!--
reps: 0
priority: 0
-->
#Security #SRS

# What is the CIA triad

> [!abstract] Short answer
> The CIA triad is the model that names the three core properties every security program protects: **Confidentiality** (only authorized parties can read), **Integrity** (data and systems are not undetectably altered), and **Availability** (systems serve legitimate users when needed). It is the vocabulary for classifying what a control or an attack actually threatens - and most real incidents damage more than one leg at once.

## The three properties, mapped to real controls and failures

```d2
direction: right
c: "Confidentiality\nencryption, access control" { width: 260; height: 90; style.fill: "#e3f2fd"
i: "Integrity\nhashes, signatures, authz checks" { width: 270; height: 90; style.fill: "#fff3e0"
a: "Availability\nredundancy, backups, rate limits" { width: 260; height: 90; style.fill: "#e8f5e9"
```

**Fig. 1.** Three legs, three control families. A ransomware event hits all three: data exfiltrated (C), tampered/encrypted (I), services down (A).

- **Confidentiality** - secrecy of data: TLS and AES for transport and storage ([[What is AES]], [[What is the TLS handshake]]), access control and least privilege for who sees what ([[What is the principle of least privilege]]), token storage discipline for the browser ([[Where should you store a JWT in a browser]]). Failures: leaks, IDOR, PII exposure.
- **Integrity** - data is what it claims to be: hashes detect change ([[What is SHA-2]]), HMAC and signatures prove change did not happen silently ([[What is HMAC]], [[What is RSA]]), authorization checks prevent forged writes. Failures: undetected tampering, MITM modification, malicious dependency updates.
- **Availability** - the service is up for legitimate users: redundancy, failover, backups, DDoS protection, rate limiting. Failures: outages, ransomware, resource-exhaustion attacks.

## How the triad is used

Engineers use it as a **classification grid**: for every threat, name the leg(s) it attacks; for every control, name the leg(s) it defends. A security review that says "this API change threatens confidentiality (missing authz) and availability (unbounded query)" is communicating faster than prose. Extensions exist - authenticity and non-repudiation are folded into integrity's orbit, and the Parkerian hexad adds possession and utility - but CIA remains the shared baseline.

> [!warning] "Availability is not security"
> The classic back-end blind spot: a DoS is a security incident, not just an ops problem, and "we do security later because we must ship uptime" picks one leg and ignores the others. The inverse error is equally common - gold-plating confidentiality while backups (the availability leg) were never tested; a restore that was never rehearsed is an availability control that exists only on paper.

> [!tip] Interview answer
> CIA is confidentiality, integrity, availability - the three properties security controls exist to protect: only-authorized-read, no-undetected-change, up-when-needed. I use it to classify threats and controls - TLS and least privilege for C, hashes and signatures for I, redundancy and backups for A - and most real incidents, like ransomware, hit all three legs at once.
