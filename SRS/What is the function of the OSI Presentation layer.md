<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS
# What is the function of the OSI Presentation layer

> [!abstract] Short answer
> The Presentation layer (Layer 6) makes sure both sides interpret the same bytes the same way: character encodings, number formats, media formats, serialization, compression, and message-level encryption/decryption. Its job is translation between the application's view of data and the wire's bytes.

## What belongs to Layer 6

- **Character and number representation:** ASCII vs EBCDIC historically, UTF-8 today; big-endian vs little-endian integer order.
- **Media and serialization formats:** JPEG, PNG, MPEG; JSON/Protobuf/ASN.1 style encodings are presentation-layer decisions in OSI terms.
- **Compression:** gzip/deflate applied to the message content.
- **Encryption/decryption (conceptually):** OSI places message transformation here, which is why TLS is popularly (and imprecisely) called a layer-6 technology.

```d2
direction: right
a: "App object\n{\"price\": 99}" { width: 230; height: 80; style.fill: "#e8f5e9" }
p: "Presentation\nserialize to UTF-8 JSON\ncompress, encrypt" { width: 300; height: 100; style.fill: "#fff3e0" }
w: "Bytes for lower layers" { width: 220; height: 70; style.fill: "#e3f2fd" }
a -> p -> w
```

**Fig. 1.** Layer 6 is the adapter between structured application data and raw bytes, including privacy transformations of the message itself.

## The modern reality

TCP/IP has no separate layer-6 protocol; the responsibilities live in libraries and protocols above TCP. The practical mapping: HTTP content negotiation and `Content-Type` headers, `Content-Encoding: gzip`, charset declarations, and serialization formats are all presentation-layer duties performed by application protocols. TLS is the frequent example in interviews — record-layer encryption behaves like a layer-6 function while session resumption is layer-5 flavored; see [[Why do many dumps place HTTPS encryption at the Presentation layer]] for the honest version of that argument.

> [!warning] "Encryption is layer 6" is a simplification
> OSI *conceptually* puts data transformation here, but on the Internet encryption is done by TLS sitting between TCP and HTTP (layers 4–5.5 in practice), or by IPsec below TCP. Saying "encryption is always layer 6" fails as an implementation claim; frame it as: presentation is *where OSI put the responsibility*, TLS is *where the Internet actually does it*.

Neighboring layers: [[What is the function of the OSI Session layer]] above the payload question and [[What PDU is associated with each OSI layer]] for the unit vocabulary; the full ladder is in [[What is the purpose of each OSI layer]].

> [!tip] Interview answer
> Presentation defines common data representation: encodings like UTF-8, media formats, serialization, compression, and message-level encryption — the layer that guarantees the receiver's interpretation of bytes matches the sender's. On TCP/IP stacks there is no separate layer-6 protocol; these duties live in Content-Type/Content-Encoding headers, serialization libraries, and TLS, which is why people loosely call TLS a presentation-layer mechanism.
