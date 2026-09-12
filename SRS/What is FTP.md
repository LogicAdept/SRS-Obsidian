<!--
reps: 0
priority: 0
-->
#Networking/Web/Protocols/FTP #SRS
# What is FTP

> [!abstract] Short answer
> FTP (File Transfer Protocol, RFC 959) is the classic client-server protocol for transferring files between hosts: it keeps *two* channels — a control connection for commands/replies and a separate data connection for actual transfers — and supports authentication, directory navigation, and text/binary modes. Invented when trust and NAT did not exist; today it survives in legacy automation, largely replaced by SFTP/SCP (over SSH) and HTTPS uploads.

## The two-channel architecture (its defining trait)

1. **Control connection** (TCP 21): login (USER/PASS), commands (LIST, RETR, STOR, CWD), status replies (3-digit codes like 220, 530).
2. **Data connection** — a *second* TCP connection per transfer:
   - **Active mode:** the *client* opens a port (PORT command) and the *server* connects back — breaks through NAT/firewalls at the client side.
   - **Passive mode (PASV):** the server opens a port and the client connects out — the NAT-friendly default today.
3. **Transfer modes:** ASCII (line-ending conversion — corrupts binaries if wrongly chosen) vs image/binary (raw bytes); structured file types defined by the spec.

```d2
direction: down
c: "Client" { width: 160; height: 55; style.fill: "#e3f2fd" }
ctrl: "Control connection\nTCP 21: commands, replies" { width: 300; height: 70; style.fill: "#fff3e0" }
pasv: "Passive data connection\nclient -> server:P (PASV)" { width: 330; height: 80; style.fill: "#e8f5e9" }
act: "Active data connection\nserver -> client:port (PORT)\ndies behind NAT" { width: 330; height: 80; style.fill: "#ffebee" }
c -> ctrl -> pasv
ctrl -> act
```

**Fig. 1.** One conversation, two sockets: control persists, data opens per transfer — and the direction of the data connection decides NAT survival.

## Why it is a legacy story now

- **No encryption:** credentials and data are plaintext; **FTPS** (FTP over TLS, explicit AUTH TLS) patches that while keeping the two-channel model; **SFTP** is a different protocol entirely (SSH File Transfer Protocol over SSH's port 22, one connection).
- **NAT-hostility** is native (the PORT callback problem) — [[What is NAT and how does it work]] explains why active mode needed NAT ALG hacks to survive at all.
- **HTTPS uploads and object storage APIs** replaced most human use; anonymous FTP mirrors faded.

> [!warning] FTP vs SFTP vs FTPS — the naming trap
> SFTP is *not* "secure FTP" in the FTP family — it is the SSH subsystem with a completely different command set and a single connection. FTPS is real FTP with TLS. Saying "we use SFTP, port 21 with SSL" mixes all three. Second trap: FTP's ASCII mode silently rewrites line endings — a CSV may survive while a JPEG corrupts; binary mode is the default you insist on. And the control connection carries credentials in cleartext unless FTPS — password policy on legacy FTP is still a finding auditors write.

Contrast with HTTP file serving: [[What is HTTP]] (single-channel, stateless request/response vs FTP's stateful control session), and [[What is the TCP IP protocol suite]] for where it sits.

> [!tip] Interview answer
> FTP is the RFC 959 file-transfer protocol with two channels: a persistent control connection (port 21) and a per-transfer data connection — active mode has the server connect back to the client (NAT-hostile), passive mode has the client connect out. I flag its decline: plaintext credentials, the ASCII/binary trap, and the naming mess — FTPS is FTP+TLS, SFTP is a different SSH protocol — then note modern stacks use SFTP/SCP or HTTPS.
