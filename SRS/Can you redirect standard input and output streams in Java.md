<!--
reps: 0
priority: 0
-->
#Java/IO/Streams #Java/Runtime #SRS

# Can you redirect standard input and output streams in Java?

> [!abstract] Short answer
> **Yes, with `System.setIn`, `System.setOut`, and `System.setErr` (Java 1.1).** `System.in` is a `public static final InputStream`; `out` and `err` are `public static final PrintStream`. Application code cannot assign those fields. The setters reassign them. `setIn` takes an `InputStream`; `setOut` / `setErr` take a `PrintStream` (wrap a file, socket, or `ByteArrayOutputStream`). `out` and `err` are independent: redirecting one does not move the other.

## Three fields, three setters

`System` exposes the process standard streams and the only supported way to replace them ([[What is the purpose of the Runtime class and the System class]], [[What is the difference between and what InputStream OutputStream Reader Writer]]):

| Field | Type | Setter (since 1.1) |
| --- | --- | --- |
| `System.in` | `InputStream` | `setIn(InputStream)` |
| `System.out` | `PrintStream` | `setOut(PrintStream)` |
| `System.err` | `PrintStream` | `setErr(PrintStream)` |

The fields start already open. Typically they are the host keyboard and display, or whatever the environment attached to the process. OpenJDK fills them in VM init from `FileDescriptor.in` / `out` / `err` (`BufferedInputStream` on stdin; `PrintStream` on stdout/stderr with `stdout.encoding` / `stderr.encoding`).

`err` exists so diagnostics still reach a watched destination when `out` is sent to a file. `setOut` does not reassign `err`.

`PrintStream` is a byte `OutputStream` that prints; `setOut` will not take a raw `OutputStream` or a `Writer`. Wrap first: `new PrintStream(out, autoFlush, charset)` or a file-name constructor ([[What is the difference between PrintWriter and PrintStream]], [[Which subclasses class InputStream you do you know for what they intended]]). The two-arg `PrintStream(OutputStream, boolean)` encodes with the default charset and, if `autoFlush` is true, flushes after a byte-array write, a `println`, or a `'\n'`.

Java 21 still documents a security-manager gate: if one is installed, each setter calls `checkPermission` with `RuntimePermission("setIO")` and throws `SecurityException` on denial. `SecurityManager` has been deprecated for removal since 17; with none installed, the check is a no-op.

## Why `final` still moves

`in`, `out`, and `err` are `static final`, so `System.out = ps` does not compile. They are write-protected, not ordinary finals: only `System.setIn` / `setOut` / `setErr` may change them. A compiler must treat those reads as normal field reads (later stores are visible; a lock or volatile read can affect them). User code is not allowed to write them ([[Can you change the value of a final field using reflection]]).

OpenJDK’s setters call `checkIO()` then native `setIn0` / `setOut0` / `setErr0`. Native code stores into the write-protected fields; Java source cannot.

```d2
direction: down
fields: "System.in / out / err\nstatic final, write-protected" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
set: "setIn / setOut / setErr\ncheckIO, then native *0" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
new: "your InputStream\nor PrintStream" {
  width: 240
  height: 70
  style.fill: "#fff8e1"
}
cache: "saved local copy\nor Scanner / Reader wrap" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
fields -> set
set -> new
fields -> cache
```

**Fig. 1.** The setters replace the `System` fields. A reference you already copied, or a wrapper built around the old stream, is unchanged.

```java
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;

class RedirectDemo {
    static String captureLine() {
        PrintStream original = System.out;
        ByteArrayOutputStream buf = new ByteArrayOutputStream();
        PrintStream replacement = new PrintStream(buf, true, StandardCharsets.UTF_8);
        System.setOut(replacement);
        try {
            System.out.println("hello");
            replacement.flush();
            return buf.toString(StandardCharsets.UTF_8);
        } finally {
            System.setOut(original);
        }
    }

    static int readFedByte() throws java.io.IOException {
        InputStream original = System.in;
        System.setIn(new ByteArrayInputStream(new byte[] { 42 }));
        try {
            return System.in.read();
        } finally {
            System.setIn(original);
        }
    }
}
```

**Listing 1.** Temporary redirect: save, `setOut` / `setIn`, use `System.out` / `System.in`, restore in `finally`. Autoflush plus an explicit `flush` makes the capture complete before restore. Do not close `original`.

> [!warning] A saved reference still writes to the old destination
> `PrintStream out = System.out;` then `System.setOut(other)` leaves `out` bound to the previous stream. A `Scanner` or `BufferedReader` constructed on `System.in` before `setIn` keeps reading the old `InputStream`. `try-with-resources` on the replacement while it is installed as `System.out` closes that `PrintStream` at the end of the block; `System.out` still points at the closed stream. Restore first, then close the replacement if you own it. Closing the original `System.out` / `System.err` shuts the process streams.

> [!tip] Interview answer
> Yes: call `System.setIn`, `setOut`, and `setErr`. The fields are `final`, so you cannot assign them; `setIn` takes an `InputStream`, `setOut` and `setErr` take a `PrintStream`. Save and restore around tests, because a local copy or a wrapper built before the call still uses the old stream, and redirecting `out` does not redirect `err`.
