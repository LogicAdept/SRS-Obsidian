<!--
reps: 0
priority: 0
-->
#Java/Versions/18 #SRS

# What does UTF-8 by default mean in Java 18

> [!abstract] Short answer
> **JEP 400 (Java 18) made UTF-8 the default charset for the JDK's APIs on every platform: `Charset.defaultCharset()`, `file.encoding`, `InputStreamReader`/`OutputStreamWriter` without an explicit charset, `Files.newBufferedReader`, `Properties.load` — regardless of OS locale.** Before 18, a JVM on a Windows-1252 machine defaulted to Windows-1252; the same jar could produce different bytes on different machines. `native.encoding` was added to report the OS's own charset when you really need it.

## What changed and what deliberately did not

The JDK split "platform charset" from "JDK default charset": `file.encoding` defaults to `UTF-8` everywhere, while the new `native.encoding` property carries the old OS-derived value (on a Chinese-locale Windows it would be GBK, on POSIX/C Linux ANSI_X3.4-1968). APIs that never took a charset argument now mean UTF-8: `new FileReader(f)`, `new String(bytes)` (uses default charset), `System.out` (`stdout.encoding`), `Files.readString`. **Properties files stayed ISO-8859-1** for `Properties.load(InputStream)` — the legacy `Properties` contract is untouched (use `load(Reader)` with UTF-8 or `PropertyResourceBundle`'s UTF-8 handling from 9) — and `ByteArrayOutputStream.toString()` etc. that specify a charset explicitly behave as documented.

The migration reality: code that "worked" by matching file encoding to platform default on one box starts producing mojibake when that box is gone — the fix is passing explicit `Charset` arguments for durable artifacts ([[What was new in Java 11]]'s `Files.readString` is explicit UTF-8 by design).

```d2
direction: down
pre: "pre-18: default charset = OS locale\nWindows-1252 / GBK / POSIX -> mojibake roulette" {
  width: 460
  height: 70
  style.fill: "#ffcdd2"
}
j400: "JEP 400 (18): default charset = UTF-8 always" {
  width: 420
  height: 60
  style.fill: "#e8f5e9"
}
nat: "native.encoding = old OS value\n(kept for the rare real need)" {
  width: 380
  height: 60
  style.fill: "#e3f2fd"
}
prop: "Properties.load(InputStream) still ISO-8859-1" {
  width: 420
  height: 60
  style.fill: "#fff8e1"
}
pre -> j400
j400 -> nat
j400 -> prop
```

**Fig. 1.** One default to rule them all (UTF-8), an escape hatch to the old value (`native.encoding`), and one deliberate holdout (`Properties` streams).

```java
import java.nio.charset.Charset;

public class V22_Utf8Default {
    public static void main(String[] args) {
        System.out.println("file.encoding: " + System.getProperty("file.encoding"));
        System.out.println("defaultCharset: " + Charset.defaultCharset().name());
        System.out.println("native.encoding: " + System.getProperty("native.encoding"));
        System.out.println("stdout.encoding: " + System.getProperty("stdout.encoding"));
    }
}
```

**Listing 1.** Verified on JDK 21 (V22_Utf8Default in empirics): `file.encoding: UTF-8`, `defaultCharset: UTF-8`, `native.encoding: UTF-8`, `stdout.encoding: UTF-8` — on this Linux host the native locale is already UTF-8, so the values coincide; on a Windows-1252 host pre-18 the first two would have read `windows-1252` (out/V22_Utf8Default.txt).

> [!warning] The default moved — explicit charsets are still the answer
> The trap: code that wrote files via `new FileWriter(f)` "suddenly changes encoding" across an 8→18 upgrade **on Windows** — that is the point of JEP 400, and blaming the jar is wrong; also possible in reverse: legacy files written in a platform charset now get read as UTF-8 and mojibake appears in the other direction. Second: `Properties.load(InputStream)` did **not** switch to UTF-8 — assuming it did corrupts non-Latin-1 keys. Third: `System.out` uses `stdout.encoding`, which redirects/capture layers can override — "UTF-8 by default" does not guarantee your console pipe ([[What was new in Java 11]]).

> [!tip] Interview answer
> **JEP 400 in Java 18 fixed the default charset to UTF-8 on all platforms — defaultCharset(), FileReader, Files APIs all agree now — and added native.encoding for the OS's old value.** Properties stream loading stays ISO-8859-1 by contract. Upgrades shift the mojibake direction on Windows boxes; explicit charsets remain the durable fix.
