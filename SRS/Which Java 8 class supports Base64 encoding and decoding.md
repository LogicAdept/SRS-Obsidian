<!--
reps: 0
priority: 0
-->
#Java/Library #Java/Versions/8 #SRS

# Which Java 8 class supports Base64 encoding and decoding

> [!abstract] Short answer
> **`java.util.Base64` (`@since 1.8`).** Static factories return `Base64.Encoder` and `Base64.Decoder`. Basic: `getEncoder` / `getDecoder` (RFC 4648). URL-safe: `getUrlEncoder` / `getUrlDecoder`. MIME: `getMimeEncoder` / `getMimeDecoder` (RFC 2045). There is no public constructor.

## `Base64` is the factory; Encoder/Decoder do the work

`java.util.Base64` exists only to hand out encoders and decoders for the Base64 schemes in RFC 4648 and RFC 2045. You never instantiate it. Encode/decode run on the nested types: `encode` / `encodeToString` on `Encoder`; `decode` on `Decoder` (bytes, `ByteBuffer`, or wrapping streams). Encoder and Decoder instances are safe for concurrent threads — keep one and reuse it ([[How do you create a Base64 encoder and decoder in Java 8]]).

**Basic** (RFC 4648 Table 1, same alphabet as RFC 2045): encoder emits no line feeds; decoder **rejects** non-alphabet characters. **URL and filename safe** (RFC 4648 Table 2) uses `-` and `_`. **MIME** (RFC 2045) wraps at 76 with CRLF; MIME decode skips non-alphabet. Optional `getMimeEncoder(int lineLength, byte[] lineSeparator)` customizes wrap. `null` → `NullPointerException`. Bad Basic/URL input → `IllegalArgumentException`. Alphabet `String` conversions use ISO-8859-1; your payload still needs its own charset to become `byte[]` first.

```d2
cls: "java.util.Base64" {
  shape: rectangle
}
enc: "Base64.Encoder\nencode / encodeToString / wrap" {
  shape: rectangle
}
dec: "Base64.Decoder\ndecode / wrap" {
  shape: rectangle
}
cls -> enc: "getEncoder\ngetUrlEncoder\ngetMimeEncoder"
cls -> dec: "getDecoder\ngetUrlDecoder\ngetMimeDecoder"
```

**Fig. 1.** The Java 8 class is `Base64`. The objects you call are the nested encoder and decoder.

```java
Base64.Encoder encoder = Base64.getEncoder();
Base64.Decoder decoder = Base64.getDecoder();
String text = encoder.encodeToString(new byte[] {1, 2, 3});
byte[] back = decoder.decode(text);
```

**Listing 1.** Obtain the Basic pair from `java.util.Base64`. URL-safe and MIME are the other factory names on the same class.

> [!warning] Same name, three incompatible dialects
>
> Commons Codec `org.apache.commons.codec.binary.Base64` and `sun.misc.BASE64Encoder` are different types. Mixing Basic, URL-safe, and MIME alphabets corrupts data. Padding `=` ends a block but is not required; a wrong pad count still fails. This is encoding, not encryption.

> [!tip] Interview answer
>
> **`java.util.Base64`, Java 8, `java.util` package.** `getEncoder()` / `getDecoder()` for standard RFC 4648; `getUrl*` and `getMime*` for the other two. Nested `Encoder`/`Decoder` are thread-safe. Not `new Base64()`, not Apache, not `sun.misc`. Encodes **bytes**, not `Optional` / `LocalDateTime`.
