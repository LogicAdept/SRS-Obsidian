<!--
reps: 0
priority: 0
-->
#Java/IO/Streams #SRS

# What is `SequenceInputStream`?

> [!abstract] Short answer
> **Logical concatenation of `InputStream`s — read the first to EOF, then the next, and so on.** Constructors: two streams (`s1` then `s2`), or an `Enumeration<InputStream>`. When a substream hits EOF, that substream is **closed** and reading continues on the next. `close()` on the sequence closes the current stream and every **remaining** stream from the enumeration. This is `java.io` (since 1.0), not `java.util.stream`.

## One logical byte stream from several

`SequenceInputStream` extends `InputStream` (not `FilterInputStream`). It starts with an ordered collection of streams and reads from the first until EOF, then the second, until EOF on the last ([[Which subclasses class InputStream you do you know for what they intended]], [[What are common concrete InputStream and OutputStream implementations]]).

`SequenceInputStream(s1, s2)` reads `s1` then `s2`. `SequenceInputStream(Enumeration<? extends InputStream> e)` reads whatever the enumeration yields, in order. A `null` element from the enumeration is a `NullPointerException` (OpenJDK `peekNextStream`).

`read()` / `read(byte[],int,int)` try the **current** substream. On EOF they `close` that substream and switch. The enumeration constructor’s JavaDoc states that explicitly; `read()` documents the same switch-and-close for the current substream in general. OpenJDK’s two-arg constructor is `Collections.enumeration(List.of(s1, s2))`, so both shapes share that machinery.

`close()`: a closed sequence cannot be reopened. If it was created from an enumeration, **all remaining** elements are taken from the enumeration and closed before `close` returns (exceptions can be suppressed onto the first `IOException`).

`available()` is only the **current** substream’s `available()` — not the sum of everything still concatenated ([[What kinds of input and output streams exist in Java]], [[What is the difference between and what InputStream OutputStream Reader Writer]]).

```d2
direction: right
s1: "InputStream A" {
  width: 140
  height: 40
  style.fill: "#e3f2fd"
}
s2: "InputStream B" {
  width: 140
  height: 40
  style.fill: "#e3f2fd"
}
seq: "SequenceInputStream" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
s1 -> seq
s2 -> seq
```

**Fig. 1.** Bytes of A, then bytes of B, as one `InputStream`. Exhausted A is closed before B is read.

```java
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.SequenceInputStream;

class Demo {
    static byte[] concat(byte[] a, byte[] b) throws IOException {
        try (SequenceInputStream in = new SequenceInputStream(
                new ByteArrayInputStream(a),
                new ByteArrayInputStream(b))) {
            return in.readAllBytes();
        }
    }
}
```

**Listing 1.** Two-arg constructor: `s1` then `s2`. Closing `in` closes whichever substream is still open and any not yet started.

> [!warning] Substreams are closed for you — and `available()` is not the total length
> Do not keep using a substream after the sequence has moved past it; it is already closed. `available()` can be `0` between streams even when more data remains. Closing the sequence does not un-close anything you already exhausted. This class is **not** `java.util.stream.Stream`, and not a database `SEQUENCE` / `SERIAL` / `AUTO_INCREMENT`.

> [!tip] Interview answer
> **`SequenceInputStream` is concatenate-as-one-`InputStream`: two streams or an `Enumeration`.** It reads each to EOF, closes that one, continues. `close()` on the wrapper closes remaining members. Name that it is `java.io` concatenation, not Stream API `concat`.
