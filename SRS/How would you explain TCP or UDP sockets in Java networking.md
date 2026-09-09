<!--
reps: 0
priority: 0
-->
#Java/Networking #Networking/TCP #Networking/UDP #SRS

# How would you explain TCP or UDP sockets in Java networking

> [!abstract] Short answer
> **Java splits them by type: TCP = `Socket` (client) and `ServerSocket` (acceptor) giving byte streams over a connection; UDP = `DatagramSocket` sending/receiving `DatagramPacket`s — connectionless, no delivery guarantee.** Both wrap the OS socket; you choose by whether the application needs ordered reliable streams (TCP) or low-latency fire-and-forget datagrams (UDP).

## The two APIs

TCP is a connection: `ServerSocket.bind + accept()` yields a `Socket` per client; both ends read/write plain streams (`InputStream`/`OutputStream`), and the stack guarantees order and delivery. UDP is datagrams: every `DatagramPacket` carries address+port and travels independently; packets may arrive out of order, duplicated, or not at all.

```d2
direction: right
tcp: "TCP\nServerSocket.accept() -> Socket\nInputStream / OutputStream" {
  width: 340
  height: 110
  style.fill: "#e3f2fd"
}
tcpf: "Connected, ordered,\nreliable, flow-controlled" {
  width: 320
  height: 100
  style.fill: "#e3f2fd"
}
udp: "UDP\nDatagramSocket.send / receive\nDatagramPacket(addr, port, data)" {
  width: 360
  height: 110
  style.fill: "#fff3e0"
}
udpf: "Connectionless datagrams:\nlost / reordered / duplicated" {
  width: 330
  height: 100
  style.fill: "#fff3e0"
}
tcp -> tcpf
udp -> udpf
```

**Fig. 1.** Same OS sockets, two Java APIs: stream-based for TCP, packet-based for UDP.

```java
// TCP: ServerSocket accepts, Socket connects, streams exchange bytes
try (ServerSocket server = new ServerSocket(0)) {
    int port = server.getLocalPort();
    new Thread(() -> {
        try (Socket c = new Socket("localhost", port)) {
            c.getOutputStream().write("ping-over-tcp".getBytes(StandardCharsets.UTF_8));
            c.getOutputStream().flush();
        } catch (Exception e) { }
    }).start();
    try (Socket peer = server.accept()) {
        byte[] buf = peer.getInputStream().readNBytes(13);
        System.out.println("TCP received: " + new String(buf, StandardCharsets.UTF_8));
    }
}

// UDP: connectionless datagrams
try (DatagramSocket receiver = new DatagramSocket(0);
     DatagramSocket sender = new DatagramSocket()) {
    byte[] rx = new byte[64];
    DatagramPacket in = new DatagramPacket(rx, rx.length);
    new Thread(() -> {
        try {
            byte[] msg = "ping-over-udp".getBytes(StandardCharsets.UTF_8);
            sender.send(new DatagramPacket(msg, msg.length,
                    InetAddress.getByName("localhost"), receiver.getLocalPort()));
        } catch (Exception e) { }
    }).start();
    receiver.setSoTimeout(5000);
    receiver.receive(in);
    System.out.println("UDP received: " + new String(in.getData(), 0, in.getLength(), StandardCharsets.UTF_8));
}
```

**Listing 1.** Both transports on localhost, verified on JDK 21:

```java
TCP received: ping-over-tcp
UDP received: ping-over-udp
```

**Listing 2.** The TCP side read exactly 13 ordered bytes from a stream; the UDP side received one self-addressed datagram and had to know its length — the receiver sizes the buffer and reads `getLength()`, because datagrams have no stream position.

> [!warning] A TCP stream is not a message protocol — and UDP loss is your code's problem
> The two interview traps. First, TCP gives a byte stream, not messages: two `write()` calls may arrive as one read or split across reads (Nagle coalescing, MTU segmentation) — protocols frame data themselves (length-prefix, delimiter); code that assumes "one write = one read" breaks under load. Second, UDP in Java is bare datagrams: no ordering, no retransmission, and a `receive()` blocks until a packet or timeout — real systems build ACK/retry on top or accept loss (games, telemetry, DNS). Also mind `DatagramPacket` capacity: a receive buffer smaller than the datagram silently truncates it. On the Java side, both APIs have non-blocking and asynchronous NIO variants (`SocketChannel`, `DatagramChannel` with a `Selector` — [[How does NIO provide non-blocking access to resources]]), and neither API encrypts anything: TLS is a separate layer ([[How do you enable HTTPS in a Spring Boot application]]).

> [!tip] Interview answer
> **TCP in Java is Socket and ServerSocket: accept a connection, then read and write ordered reliable byte streams. UDP is DatagramSocket and DatagramPacket: every packet carries its own address, packets can be lost or reordered, no connection. Choose TCP when correctness of ordering matters, UDP for latency or broadcast-style traffic. Streams are bytes, not messages — framing is your job — and both have NIO channel variants for non-blocking I/O.**

