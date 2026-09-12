<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS
# What is the function of the OSI Application layer

> [!abstract] Short answer
> The Application layer (Layer 7) is where actual software requests network work: it defines the semantics of the exchange — "resolve this name", "fetch this document", "lease this address" — through concrete protocols like HTTP, DNS, DHCP, FTP, SMTP and SSH. It does not mean the browser or the database itself; it means the network-facing protocol those programs speak.

## What Layer 7 provides

1. **Resource semantics.** Methods and payloads: HTTP defines what GET/POST mean, FTP defines retrieve/store, SMTP defines mail transactions.
2. **Addressing of services.** Well-known ports (80/443, 53, 25, 21) let the transport hand a message to the right service; URLs name resources within it.
3. **Protocol-level metadata.** Headers, status codes, cookies, MIME types — the vocabulary applications and intermediaries (proxies, caches) agree on.
4. **Human-facing services.** Name resolution (DNS), mail transfer, remote shells, file transfer, web APIs.

```d2
direction: down
browser: "Browser wants page on example.com" { width: 340; height: 70; style.fill: "#e8f5e9" }
dns: "L7 DNS: resolve example.com" { width: 340; height: 70; style.fill: "#fff3e0" }
http: "L7 HTTP: GET /page over TCP+TLS" { width: 340; height: 70; style.fill: "#fff3e0" }
stack: "Transport/Network/Data Link/Physical move the bytes" { width: 380; height: 80; style.fill: "#e3f2fd" }
browser -> dns -> http -> stack
```

**Fig. 1.** Two different layer-7 protocols cooperate inside one page load: DNS to get the address, HTTP to fetch the document.

## What is *not* layer 7

The application *program* is not the layer — the protocol it speaks is. Chrome is an application; HTTP is the layer-7 protocol. Similarly "user authentication in the app" is not an OSI concern: layer 7 authentication happens via protocol mechanisms (HTTP auth, TLS client certs) while account logic is above networking entirely.

> [!warning] DNS is not layer 4, and "HTTP runs on port 443" is imprecise
> A common exam lie places DNS in transport because it "uses UDP 53"; DNS is an application-layer protocol that *may* use UDP or TCP as transport (and HTTP/3-style transports). Also, TLS termination means the server's HTTP stack often runs on a plain port behind a proxy — ports identify services, they do not define layers.

Layer 7 leans on every layer below; good cross-checks: [[What is HTTP]], [[What is DNS and how does DNS resolution work]], [[What is FTP]], and the ladder in [[What is the purpose of each OSI layer]].

> [!tip] Interview answer
> Layer 7 defines what applications ask the network to do, through protocols like HTTP, DNS, DHCP and SMTP — semantics, headers, status codes, well-known ports. The distinction I draw: the browser is a program, HTTP is the layer-7 protocol; and on TCP/IP stacks this is exactly where everything above transport got folded into one "application" tier.
