<!--
reps: 0
priority: 0
-->
#Java/NIO/Charset #Java/IO/Streams #SRS

# How does Java handle character encoding when reading and writing files?

> [!abstract] Short answer
> **A `Charset` is "a named mapping between sequences of sixteen-bit Unicode code units and sequences of bytes" (`java.nio.charset`).** Files store bytes; Java strings are UTF-16; every reader/writer crossing that border decodes or encodes through one. The bridges are `InputStreamReader` / `OutputStreamWriter` (always pass an explicit charset), `Files.readString(path, cs)` and friends. Error policy matters: `Charset.decode`/`encode` convenience methods silently **replace** malformed input; build a `CharsetDecoder` with `CodingErrorAction.REPORT` to detect it. The **default** charset is UTF-8 since JDK 18 (JEP 400) — before that it followed the OS and locale, which is why portable code never relies on the default ([[Which classes convert between Java byte streams and character streams]], [[What is a Buffer in Java NIO and how do position limit and capacity work]]).

## Bridges and the error policy

A reader wraps bytes and a charset: `new BufferedReader(new InputStreamReader(in, StandardCharsets.UTF_8))`. Underneath, `CharsetDecoder` converts byte buffers to char buffers and answers the three questions for broken input: replace (U+FFFD), ignore, or report (`CodingErrorAction.REPORT` → `CharacterCodingException`). The `Charset.encode`/`decode` convenience methods choose replace — convenient, and the reason silently corrupted text passes CI. Byte-order issues belong to the charset too: UTF-16 maps may expect a BOM; UTF-8 files with a BOM get the `\uFEFF` character in Java unless you strip it.

| Tool | Chooses the charset how | Broken input |
| --- | --- | --- |
| `Charset.decode(bb)` | named charset | replaces silently |
| `CharsetDecoder` + `onMalformedInput` | explicit action | replace / ignore / report |
| `InputStreamReader(in, cs)` | explicit | decoder policy (replace by default) |
| `Files.readString(path)` | default charset (UTF-8, JDK 18+) | per decoder |

## The default-charset story

`file.encoding` used to differ per platform — Windows gave `windows-1251`/`cp1252`-style defaults, Linux often UTF-8 — so the same jar produced different files. **JEP 400 (JDK 18)** fixed the default: "UTF-8 by Default" for APIs that depend on the default charset (`Files.readString(path)`, `PrintStream`, `toLocaleString`-style conversions). The console can still use a native encoding on Windows, and `System.out` may be reconfigured — the lesson is not "UTF-8 everywhere now", but "never let the default decide".

```java
import java.nio.ByteBuffer;
import java.nio.charset.CharacterCodingException;
import java.nio.charset.CodingErrorAction;
import java.nio.charset.StandardCharsets;

class Decode {
    public static void main(String[] args) {
        byte[] bad = {(byte) 0xD0, (byte) 0x9, (byte) 0xFF};   // broken UTF-8 tail
        ByteBuffer bb = ByteBuffer.wrap(bad);
        String lenient = StandardCharsets.UTF_8.decode(bb.duplicate()).toString();
        System.out.println("replace: codepoints=" + lenient.length());
        try {
            StandardCharsets.UTF_8.newDecoder()
                    .onMalformedInput(CodingErrorAction.REPORT)
                    .onUnmappableCharacter(CodingErrorAction.REPORT)
                    .decode(bb.duplicate());
            System.out.println("report: clean");
        } catch (CharacterCodingException e) {
            System.out.println("report: rejected (" + e.getMessage() + ")");
        }
    }
}
```

**Listing 1.** The same bytes through the lenient convenience API and the strict decoder:

```text
replace: codepoints=3
report: rejected (Input length = 1)
```

**Listing 2.** Lenient decode invents replacement codepoints; the strict decoder refuses.

```d2
direction: right
bytes: "file bytes\nUTF-8 / UTF-16 / cp1251..." {
  width: 250
  height: 55
  style.fill: "#fff8e1"
}
dec: "CharsetDecoder\nreplace / ignore / report" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
str: "String (UTF-16)\nthen encode back" {
  width: 230
  height: 50
  style.fill: "#e8f5e9"
}
bytes -> dec -> str
```

**Fig. 1.** One charset object, two directions, one error policy ([[What notable features does Java NIO offer]]).

> [!warning] The default charset is a portability bug with a history
> Code that reads with `new FileReader(path)` or `Charset.defaultCharset()` changes meaning between JDK versions and OS locales — the exact problem JEP 400 names. Corrupt input through the lenient path looks like ordinary text (every bad byte becomes U+FFFD), so corruption is discovered by users, not tests. Do not assume UTF-8 file contents just because the JDK defaults to UTF-8 for API defaults — the file's own encoding is a property of its producer. And `Charset.forName("utf8")`-style lookups throw for unknown names; `StandardCharsets` constants cannot fail.

> [!tip] Interview answer
> Java separates chars (UTF-16 in memory) from bytes (files, network); a `Charset` is the named mapping between them, realized by encoder/decoder objects with a policy for malformed input — convenience methods replace, a configured `CharsetDecoder` can report. Bridges (readers/writers, `Files.readString`) take the charset explicitly; since JDK 18 the default is UTF-8 (JEP 400), before that it was OS-locale dependent — so production code names its charsets.

