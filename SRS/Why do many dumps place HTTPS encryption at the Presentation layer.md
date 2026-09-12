<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS
# Why do many dumps place HTTPS encryption at the Presentation layer

> [!abstract] Short answer
> The habit comes from OSI's textbook mapping: Layer 6 (Presentation) owns data *representation and transformation*, which includes encryption — and TLS "encrypts the message", so dumps mechanically file HTTPS under Presentation. The honest version: OSI is a reference model, the Internet stack has no separate layer 6, and TLS is a real protocol that sits between TCP and HTTP, behaving partly like a session/presentation shim — while HTTP + TLS together are all "application layer" in TCP/IP terms.

## The reasoning chain (and where it bends)

1. **What OSI really says:** Presentation handles syntax — encodings, serialization, compression, encryption — so that peers exchange *meaningful* data regardless of local representations. That is why dumps say "encryption → layer 6".
2. **Why HTTPS fits neatly:** in the HTTP-over-TLS arrangement, HTTP's payload is transformed (encrypted) end-to-end without the transport knowing — exactly a presentation-style duty.
3. **Where it bends:** TLS is not a header convention inside HTTP; it is a separate protocol with its own handshake, record layer, and connection state. It encrypts *the channel*, not individual messages; it authenticates peers; and its session resumption is session-layer behavior. A single OSI slot fits poorly.

```d2
direction: down
http: "HTTP (L7 semantics)" { width: 240; height: 70; style.fill: "#e8f5e9" }
tls: "TLS record + handshake\nencrypts the channel (bytes)" { width: 300; height: 90; style.fill: "#fff3e0" }
tcp: "TCP (L4: segments, ports)" { width: 260; height: 70; style.fill: "#e3f2fd" }
http -> tls -> tcp
```

**Fig. 1.** The deployment truth: TLS is a shim between HTTP and TCP. Interview-safe wording: "TLS acts like a presentation/session layer", not "HTTPS is layer 6".

## How to answer without being wrong anywhere

- If the question is *about OSI as a model*: yes, by the textbook duty list, encryption of message representation is a Presentation concern.
- If the question is *about real stacks*: HTTPS = HTTP (application) + TLS (a security protocol riding TCP, which itself is transport); TCP/IP folds 5–6 into applications. TLS also spans concerns: record encryption (presentation-flavored), session resumption (session-flavored).
- If the question is a trick ("at which OSI layer does HTTPS work?"): the defensible one-liner is "application layer in practice, presentation by old textbook habit — and here is why".

> [!warning] The dump answer fails on follow-ups
> Saying only "layer 6" breaks the moment the interviewer asks "so which device strips it?" — nothing in a router or switch touches TLS; the endpoints' application stack does. If you know HTTP-over-TLS terminates at the reverse proxy (which re-encrypts to upstream), you have out-thought the dump; [[What is the difference between HTTP and HTTPS]] covers the protocol-level comparison and [[What is the function of the OSI Presentation layer]] the layer's own duties.

Also compare with [[What is the OSI model]] (why the model is vocabulary, not law) and [[What is the TCP IP protocol suite]] (what real stacks actually define).

> [!tip] Interview answer
> Dumps say Presentation because OSI's layer 6 owns data transformation, including encryption. The accurate story: TLS is a real protocol between TCP and HTTP — it encrypts a channel, authenticates peers, and even does session resumption, so it straddles session/presentation duties; in TCP/IP terms everything from HTTP upward is the application layer. I give both mappings and keep the model-versus-reality distinction explicit.
