<!--
reps: 0
priority: 0
-->
#Security/Cryptography #SRS

# What is HMAC

> [!abstract] Short answer
> HMAC (RFC 2104) is a keyed message authentication code built from any cryptographic hash: `HMAC(K, m) = H((K xor opad) || H((K xor ipad) || m))` with `ipad = 0x36...` and `opad = 0x5C...` repeated to the block size. It provides integrity and authenticity of a message between parties sharing the key, and unlike a raw `hash(key || message)` it resists length-extension and unknown key-derivation attacks.

## The construction

The double-hash with padded keys is the whole trick: the inner hash absorbs key and message, the outer hash re-hashes the result with the opad-masked key. The RFC specifies:

- Keys longer than the hash block size B (64 bytes for SHA-256) are first reduced by hashing; the minimal recommended key length equals the hash output length L.
- Truncating output is acceptable: `HMAC-SHA256-128` means the left 128 bits - MAC strength drops with the truncated length, not below.

```java
Mac mac = Mac.getInstance("HmacSHA256");
mac.init(new SecretKeySpec(key, "HmacSHA256"));
byte[] tag = mac.doFinal(message);
```

**Listing 1.** JCE HMAC-SHA256. The tag authenticates the message for anyone holding the same key.

```d2
direction: right
k1: "Key K\nxor ipad (0x36...)" { width: 210; height: 80; style.fill: "#e3f2fd" }
m: "Message m" { width: 150; height: 70; style.fill: "#e3f2fd" }
inner: "H(inner)" { width: 150; height: 70; style.fill: "#fff3e0" }
k2: "Key K\nxor opad (0x5C...)" { width: 210; height: 80; style.fill: "#e8f5e9" }
out: "HMAC tag" { width: 150; height: 70; style.fill: "#e8f5e9" }
k1 -> inner; m -> inner
inner -> k2 -> out
```

**Fig. 1.** Two nested hashes with the key XORed by different pads: the inner pass mixes key and message, the outer pass seals the result.

## Where HMAC is the answer

- **JWT HS256** = HMAC-SHA256 over the base64url header.payload ([[What is the difference between HS256 and RS256 in JWT]]).
- **TLS record layer** and webhook signatures (HMAC of the body with a shared secret) rely on it for tamper detection.
- **Key derivation**: HMAC in counter mode underlies HKDF.

## Where it is not

- **Password storage**: HMAC is fast by design; offline guessing runs at GPU speed - use a memory-hard KDF ([[How should you store and handle passwords securely]]).
- **Comparing tags with `==`** invites timing attacks; Java's `MessageDigest.isEqual` is the constant-time comparison.

> [!warning] Why not just hash the key and message together
> `H(key || message)` breaks for Merkle-Damgard hashes: knowing the digest of one message lets an attacker append data and compute a valid digest for the extended message without knowing the key (length extension). HMAC's outer pass closes that path - the same reason [[What is SHA-2]] alone is not a MAC.

> [!tip] Interview answer
> HMAC is RFC 2104's keyed MAC: hash the key-XOR-ipad with the message, then re-hash with the key-XOR-opad. That structure removes length-extension and padding weaknesses of naive hash-plus-key schemes. I use it for token and webhook signatures with constant-time tag comparison - and never for password storage, where a slow KDF is required.
