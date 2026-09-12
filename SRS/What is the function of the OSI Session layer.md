<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS
# What is the function of the OSI Session layer

> [!abstract] Short answer
> The Session layer (Layer 5) establishes, manages and terminates dialogs between applications: it decides who may transmit when (dialog control), keeps long exchanges structured (synchronization/checkpointing), and lets an interrupted dialog resume instead of restarting. In the TCP/IP world its duties are mostly absorbed by TLS sessions, RPC sessions and application code.

## The three classic functions

1. **Dialog establishment, maintenance, termination.** A session is the lifetime of an ongoing exchange between two endpoints (a login, a long file transfer), distinct from a physical or transport connection that may outlive it.
2. **Dialog control.** Who sends when: full-duplex, half-duplex turn-taking, or simplex — the session layer arbitrates.
3. **Synchronization and recovery.** The layer inserts sync points/checkpoints into a stream so that after a failure the parties agree on the last confirmed state and resume from there instead of from zero.

```d2
direction: right
app1: "Application A" { width: 200; height: 70; style.fill: "#e8f5e9" }
sess: "Session layer\nestablish dialog -> checkpoints -> resume/teardown" { width: 340; height: 100; style.fill: "#fff3e0" }
app2: "Application B" { width: 200; height: 70; style.fill: "#e8f5e9" }
app1 -> sess
sess -> app2
```

**Fig. 1.** Layer 5 sits between application semantics and transport pipes, structuring *when* and *in what state* the parties talk.

## Where it went on the modern Internet

The Internet suite has no dedicated session protocol under TCP; the work moved up:

- **TLS** does session establishment and resumption (session tickets, PSK in TLS 1.3) right above the transport — a session-layer duty, even though the encryption itself is presentation-like.
- **HTTP cookies + server session stores** implement dialog state for stateless HTTP.
- **RPC/ORM connection pools, SIP, SMB** and database drivers keep explicit session state (SIP is the textbook "session" protocol — it sets up and tears down multimedia dialogs).

> [!warning] Session (5) is not connection (4)
> A TCP connection is a transport-level pipe; a session spans logic above it. One session can survive several TCP connections (session resumption, connection pools), and one connection can carry many sessions (multiplexing in HTTP/2). Equating "session" with "connection" is the standard trap in this question; [[Which OSI layer provides end-to-end delivery flow control and error recovery]] shows the transport-side counterpart.

Related: [[What is an HTTP session]] for the web-practice version, [[What is the function of the OSI Presentation layer]] for the neighboring layer, and [[What is the purpose of each OSI layer]] for the whole ladder.

> [!tip] Interview answer
> Layer 5 manages dialogs: establish/terminate sessions, control turn-taking, and add checkpoints so an interrupted exchange resumes. On the real Internet there is no separate session protocol — TLS resumption, HTTP cookie sessions and RPC/SIP sessions carry these duties. The one-line distinction I make: transport gives a pipe; session gives a managed, resumable conversation on top of it.
