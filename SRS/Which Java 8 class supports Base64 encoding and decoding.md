<!--
reps: 0
priority: 0
-->
#Java/Library #Java/Versions/8 #SRS

# Which Java 8 class supports Base64 encoding and decoding?

> [!abstract] Short answer
> **`java.util.Base64` (`@since 1.8`).** Static factories return `Base64.Encoder` and `Base64.Decoder`. Basic: `getEncoder` / `getDecoder` (RFC 4648). URL-safe: `getUrlEncoder` / `getUrlDecoder`. MIME: `getMimeEncoder` / `getMimeDecoder` (RFC 2045). There is no public constructor. Encode **bytes**; decode back to bytes.

## Factories, not `new Base64()`

`java.util.Base64` only hands out encoders and decoders. You never construct it. Encode/decode run on the nested types: `encode` / `encodeToString` on `Encoder`; `decode` on `Decoder` (bytes, `ByteBuffer`, or wrapping streams). Encoder and Decoder instances are **safe for concurrent threads** — keep one and reuse it. `null` arguments throw `NullPointerException`. Invalid Basic/URL input throws `IllegalArgumentException`.

**Basic** (RFC 4648 Table 1): encoder emits no line feeds; decoder **rejects** non-alphabet characters. **URL and filename safe** (Table 2) uses `-` and `_`. **MIME** (RFC 2045) wraps at 76 with `\r\n`; MIME decode **ignores** non-alphabet characters. Optional `getMimeEncoder(int lineLength, byte[] lineSeparator)` customizes wrap.

Base64 encodes **bytes**. Strings must become bytes with an explicit charset first. `encodeToString` then builds the alphabet `String` with ISO-8859-1. `Decoder.decode(String)` is `decode(src.getBytes(StandardCharsets.ISO_8859_1))`. Padding `=` is accepted and means end-of-data, but is **not required**; if padding *is* present, the count must be correct. `withoutPadding()` returns an encoder that omits `=`. `wrap` gives an encoding `OutputStream` / decoding `InputStream`.

```d2
direction: down
enc: "Base64.getEncoder()\nBasic Encoder" {
  width: 260
  height: 60
  style.fill: "#e8f5e9"
}
dec: "Base64.getDecoder()\nBasic Decoder" {
  width: 260
  height: 60
  style.fill: "#e3f2fd"
}
url: "getUrlEncoder / getUrlDecoder\n- and _ instead of + and /" {
  width: 300
  height: 60
  style.fill: "#fff3e0"
}
mime: "getMimeEncoder / getMimeDecoder\n76-char lines, ignores junk" {
  width: 300
  height: 60
  style.fill: "#fff8e1"
}

enc -> dec: "same Basic alphabet"
enc -> url
enc -> mime
```

**Fig. 1.** Three pairs. Mixing a URL-safe payload with `getDecoder()` fails: `-` / `_` are outside the Basic alphabet.

```java
import java.nio.charset.StandardCharsets;
import java.util.Base64;

class Demo {
    static String encodeUtf8(String text) {
        return Base64.getEncoder()
                .encodeToString(text.getBytes(StandardCharsets.UTF_8));
    }

    static String decodeUtf8(String b64) {
        byte[] raw = Base64.getDecoder().decode(b64);
        return new String(raw, StandardCharsets.UTF_8);
    }
}
```

**Listing 1.** `encodeUtf8("input")` is `aW5wdXQ==`. Use `StandardCharsets.UTF_8` rather than `getBytes("utf-8")` (checked `UnsupportedEncodingException`).

> [!warning] Basic, URL-safe, MIME, Apache, and `sun.misc` are not interchangeable
> A Basic decoder rejects any character outside its alphabet. URL-safe output (`-`, `_`) will not decode with `getDecoder()`. MIME output with `\r\n` likewise fails on Basic. Pair encoder and decoder from the same scheme. Commons Codec `org.apache.commons.codec.binary.Base64` and `sun.misc.BASE64Encoder` are different types. This is encoding, not encryption.

> [!warning] Charset of the payload ≠ charset of the alphabet string
> `getBytes()` with no argument uses the platform default and will not round-trip on every JVM. `encodeToString` / `decode(String)` talk ISO-8859-1 for the **Base64 characters**, not for your original text. Decode still yields **bytes**; wrap them with the same charset you encoded.

> [!tip] Interview answer
> **Java 8 added `java.util.Base64` in `java.util`.** `getEncoder()` / `getDecoder()` for RFC 4648 Basic; `getUrl*` and `getMime*` for the other two. Nested `Encoder`/`Decoder` are thread-safe. Not `new Base64()`, not Apache, not `sun.misc`. Encode UTF-8 bytes with `encodeToString`, `decode` back to bytes, then `new String(..., UTF_8)`.
