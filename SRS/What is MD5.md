<!--
reps: 0
priority: 0
-->
#Security/Cryptography #SRS

# What is MD5

> [!abstract] Short answer
> MD5 is a 128-bit cryptographic hash function (Rivest, 1992) that processes 512-bit message blocks through four rounds of mixing and produces a 16-byte digest. It is **broken as a collision-resistant hash**: attackers can craft two different inputs with the same MD5 in seconds on a laptop, so it must not be used for signatures, certificates, or password storage.

## How the algorithm works

The input is padded so its length is 64 bits short of a multiple of 512, then the length is appended. Processing starts from four fixed 32-bit registers (A, B, C, D) and each 512-bit block goes through **four rounds of 16 steps** (64 operations total), where each step mixes a message word, a constant derived from sine, and a shift amount into one register.

```d2
direction: right
msg: "Message\n(any length)" { width: 200; height: 80; style.fill: "#e3f2fd" }
pad: "Padding\n+ 64-bit length" { width: 220; height: 80; style.fill: "#e3f2fd" }
blocks: "512-bit blocks\nprocessed in order" { width: 240; height: 80; style.fill: "#fff3e0" }
state: "4 x 32-bit registers\nA B C D\n64 steps per block" { width: 260; height: 100; style.fill: "#fff3e0" }
out: "128-bit digest\n(16 bytes)" { width: 200; height: 80; style.fill: "#e8f5e9" }
msg -> pad -> blocks -> state -> out
```

**Fig. 1.** MD5 pads the message to a 512-bit multiple and compresses block by block into the four-register state; the final registers concatenated are the 128-bit digest.

```java
MessageDigest md = MessageDigest.getInstance("MD5");
byte[] digest = md.digest("hello".getBytes(StandardCharsets.UTF_8));
new HexBinaryAdapter().marshal(digest); // 5D41402ABC4B2A76B9719D911017C592
```

**Listing 1.** The JCE still offers MD5 via `MessageDigest`; nothing stops you from compiling it - the restriction is policy, not the API.

## Why it is considered broken

- **Collisions are practical.** Chosen-prefix collisions let an attacker build two different files (or two different certificates) with the same MD5 - demonstrated in real certificate forgery a decade and a half ago.
- **No collision resistance means no digital signatures.** A signer cannot tell which of the two colliding documents it is committing to.
- **Second-preimage and preimage attacks** are still expensive, which is why MD5 sometimes survives as a checksum for *accidental* corruption - but an adversary controls that too.

> [!warning] "MD5 is fine for checksums"
> Fine only when nobody adversarial touches the input. For downloaded files the attacker chooses the content, and a collision means the malicious file and the published "safe" file share the digest. Use SHA-256 ([[What is SHA-2]]) or a modern hash ([[What is BLAKE2]]).

MD5 is also a Merkle-Damgard construction, so it inherits the **length-extension** property - a MAC built as `MD5(key || message)` can be extended by an attacker who knows the digest. That is exactly the gap [[What is HMAC]] was designed to close.

> [!tip] Interview answer
> MD5 is a legacy 128-bit Merkle-Damgard hash. Its collision resistance is dead - practical chosen-prefix collisions were used to forge certificates - so it is banned for signatures, certificates, and password storage. It survives only as a non-adversarial checksum, and even there SHA-256 costs nothing and removes the argument.
