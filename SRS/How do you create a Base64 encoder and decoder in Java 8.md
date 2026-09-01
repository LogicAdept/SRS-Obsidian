<!--
reps: 0
priority: 0
-->
#Java/Library #Java/Versions/8 #SRS

# How do you create a Base64 encoder and decoder in Java 8?

> [!abstract] Short answer
> **`java.util.Base64` (`@since 1.8`).** `Base64.getEncoder()` / `Base64.getDecoder()` return the **Basic** RFC 4648 pair. Encode bytes with `encodeToString`; decode a string with `decode`. URL-safe and MIME are different factories (`getUrlEncoder` / `getMimeEncoder` and matching decoders).

## Factories, not `new Base64()`

`Base64` is a holder of static factories. You never construct it. `getEncoder()` returns a `Base64.Encoder` for the Basic alphabet (Table 1 of RFC 4648 / RFC 2045): no line feeds, decoder **rejects** characters outside that alphabet. `getDecoder()` is the matching Basic decoder ([[Which Java 8 class supports Base64 encoding and decoding]]).

Encoder and Decoder instances are **safe for concurrent threads**. Reuse them. `null` arguments throw `NullPointerException`.

Base64 encodes **bytes**. Strings must be turned into bytes with an explicit charset first. `encodeToString` then builds the alphabet `String` with ISO-8859-1 (same as `new String(encode(src), StandardCharsets.ISO_8859_1)`). `Decoder.decode(String)` is `decode(src.getBytes(StandardCharsets.ISO_8859_1))`. Invalid input throws `IllegalArgumentException`. Padding `=` is accepted and means end-of-data, but is **not required**; if padding *is* present, the count must be correct.

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

**Listing 1.** `encodeUtf8("input")` is `aW5wdXQ==`. Use `StandardCharsets.UTF_8` rather than `getBytes("utf-8")` (checked `UnsupportedEncodingException`). `withoutPadding()` returns an encoder that omits `=`. `wrap` gives an encoding `OutputStream` / decoding `InputStream`.

URL and filename safe: `getUrlEncoder()` / `getUrlDecoder()` use RFC 4648 Table 2 (`-` and `_`). MIME: `getMimeEncoder()` wraps at 76 characters with `\r\n`; `getMimeDecoder()` **ignores** line separators and other non-alphabet characters. That is the opposite of Basic’s reject policy ([[When should you use HTTP Basic versus form login]]).

> [!warning] Basic, URL-safe, and MIME are not interchangeable
> A Basic decoder rejects any character outside its alphabet. URL-safe output (`-`, `_`) will not decode with `getDecoder()`. MIME output with `\r\n` likewise fails on Basic. Pair encoder and decoder from the same scheme.

> [!warning] Charset of the payload ≠ charset of the alphabet string
> `getBytes()` with no argument uses the platform default and will not round-trip on every JVM. `encodeToString` / `decode(String)` talk ISO-8859-1 for the **Base64 characters**, not for your original text. Decode still yields **bytes**; wrap them with the same charset you encoded.

> [!tip] Interview answer
> **Java 8 added `java.util.Base64`: `getEncoder()` and `getDecoder()` for the Basic alphabet.** `encodeToString` on UTF-8 bytes, `decode` back to bytes, then `new String(..., UTF_8)`. Mention URL-safe and MIME as separate factories, thread-safe instances, and `IllegalArgumentException` on junk — Base64 is encoding, not encryption.
