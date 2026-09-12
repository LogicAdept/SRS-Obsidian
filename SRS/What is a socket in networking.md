<!--
reps: 0
priority: 0
-->
#Networking/TCP #SRS
# What is a socket in networking

> [!abstract] Short answer
> A socket is the endpoint of a communication inside a running process — the OS object an application reads and writes, identified for TCP/UDP by the 4-tuple (local IP, local port, remote IP, remote port) and exposed to the program as a file descriptor. It is the interface where the transport layer's machinery becomes read()/write() calls.

## The three things "socket" means (keep them apart)

1. **The API (Berkeley/POSIX sockets):** `socket()`, `bind()`, `listen()`, `accept()`, `connect()`, `read()/recv()`, `write()/send()`, `close()` — the standard interface on Linux/Unix; Java wraps it in `ServerSocket`/`Socket`, which is what interviews really probe ([[How would you explain TCP or UDP sockets in Java networking]]).
2. **The kernel object:** protocol state — buffers, sequence numbers, timers for TCP; address and queue for UDP — living in the OS, not the app.
3. **The address pair:** TCP connections are unique by 4-tuple, which is why one server socket on port 443 can serve thousands of concurrent connections — each has a different remote endpoint.

```java
// Conceptual: the classic TCP server skeleton (Java)
ServerSocket server = new ServerSocket(8080);      // bind + listen
while (true) {
    Socket conn = server.accept();                  // one socket per client 4-tuple
    handle(conn.getInputStream(), conn.getOutputStream()); // byte stream, TCP semantics
}
```

**Listing 1.** `accept()` returns a *new* socket per connection while the listening socket keeps accepting — the two roles are distinct objects.

```d2
direction: right
app1: "Client process\nSocket fd" { width: 220; height: 80; style.fill: "#e3f2fd" }
t: "TCP: 4-tuple\n10.0.0.1:53422 <-> 93.1.2.3:443" { width: 320; height: 90; style.fill: "#fff3e0" }
app2: "Server process\nlistening socket + per-conn sockets" { width: 300; height: 90; style.fill: "#e8f5e9" }
app1 -> t -> app2
```

**Fig. 1.** The 4-tuple is what lets a single listening port multiplex thousands of clients.

## TCP socket vs UDP socket

- **TCP:** `connect()` performs the three-way handshake; the socket *is* the connection; read/write see a byte stream (no message borders).
- **UDP:** no connect in the connection sense — `connect()` optionally pins the default peer; each `send()` is one datagram; one socket can talk to many peers via `sendto/recvfrom`. Loss and ordering are the app's problem ([[What is the difference between TCP and UDP]]).

> [!warning] A socket is not a port
> A port is a 16-bit number in headers; a socket is the kernel endpoint object. Multiple sockets share one local port (every connection to a server), and one TCP socket is uniquely identified only by the full 4-tuple — "the server socket and the accepted socket have the same local port" surprises people who conflate the two. On file-descriptor semantics: sockets are pollable and closable like files, which is what makes `epoll`-style multiplexing work ([[What is TCP]]).

Deeper transport context: [[What is the TCP three-way handshake]] for what `connect()` actually does, [[What is UDP]] for datagram socket behavior, and the Java-level treatment in [[How would you explain TCP or UDP sockets in Java networking]].

> [!tip] Interview answer
> A socket is the OS endpoint a process uses to communicate — a file descriptor backed by transport state, identified by the 4-tuple of IPs and ports. Server flow: socket, bind, listen, accept — and each accepted connection gets its own socket while the listener keeps going. TCP sockets are connected byte streams; UDP sockets send independent datagrams. The distinction I always draw: port is the address component, socket is the endpoint object — one port, many sockets.
