<!--
reps: 0
priority: 0
-->
#Java/IO/Streams #SRS

# What is the difference between Scanner and BufferedReader in Java?

> [!abstract] Short answer
> **`BufferedReader` is a char-stream decorator: `readLine()` returns raw strings, no parsing, fast and dumb. `Scanner` (java.util) is a tokenizing reader: it splits input with a regex — "the default whitespace delimiter used by a scanner is as recognized by `Character.isWhitespace()`" — and hands you `nextInt()` / `nextDouble()` / `next()` values directly, from strings, files, `Path`s, streams and channels (charset-aware constructors exist).** Scanner pays for parsing with regex machinery and is slower; `BufferedReader` needs manual parsing but keeps the raw lines and lets you control buffering and charset ([[What are common concrete InputStream and OutputStream implementations]], [[How does file reading work in Java]]).

## Parsing vs raw lines

`Scanner` owns a cursor and throws `NoSuchElementException` when tokens run out; `hasNext()` **blocks** on an interactive stream like `System.in`. `BufferedReader.readLine()` returns `null` at end of input and throws `IOException` on failures. Scanner reads from `String`, `File`, `Path`, `InputStream`, `Readable`, `ReadableByteChannel`; `BufferedReader` wraps any `Reader` (typically an `InputStreamReader` bridge with an explicit charset).

| | `BufferedReader` | `Scanner` |
| --- | --- | --- |
| Unit | line (`String`) | token (regex-delimited) |
| Parsing | manual (`Integer.parseInt`) | built-in `nextInt`/`nextDouble`/`useDelimiter` |
| EOF signal | `null` | `NoSuchElementException` / `hasNext` false |
| Failure model | `IOException` | `IllegalStateException` / unchecked |
| Raw speed | higher (no regex) | lower (tokenizing) |
| Sources | any `Reader` | strings, files, streams, channels, `Path` |

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;

class TwoReaders {
    public static void main(String[] args) throws IOException {
        String data = "42 7.5 done\nnext line\n";

        BufferedReader br = new BufferedReader(new InputStreamReader(
                new java.io.ByteArrayInputStream(data.getBytes(StandardCharsets.UTF_8)),
                StandardCharsets.UTF_8));
        String first = br.readLine();
        System.out.println("br: [" + first + "] second=[" + br.readLine() + "]");
        br.close();

        Scanner sc = new Scanner(data);
        int i = sc.nextInt();
        double d = sc.nextDouble();
        String word = sc.next();
        System.out.println("sc: i=" + (i * 2) + " d=" + d + " word=" + word);
        sc.close();
    }
}
```

**Listing 1.** The same input through both lenses: raw lines versus parsed tokens:

```text
br: [42 7.5 done] second=[next line]
sc: i=84 d=7.5 word=done
```

**Listing 2.** Raw lines versus typed tokens over identical input.

```d2
direction: right
src: "input text" {
  width: 150
  height: 45
  style.fill: "#e8f5e9"
}
br: "BufferedReader\nlines, no parsing, fast" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
sc: "Scanner\nregex tokens, typed nextXxx" {
  width: 270
  height: 55
  style.fill: "#fff8e1"
}
src -> br
src -> sc
```

**Fig. 1.** Same source, two contracts: strings versus typed tokens ([[Which class reads primitive values from a Java InputStream]]).

> [!warning] Two classic traps
> Mixing `nextInt()` with `nextLine()` on one `Scanner` leaves the newline in the buffer, so the following `nextLine()` returns an empty string — consume the leftover token explicitly. `Scanner.hasNext()` on `System.in` blocks forever waiting for input, which freezes batch scripts that expected EOF. On the `BufferedReader` side, `readLine()` strips the terminator and returns `null` at EOF — calling methods on it without the check throws `NullPointerException`, not `IOException`.

> [!tip] Interview answer
> `BufferedReader` gives fast raw lines and needs manual parsing; `Scanner` tokenizes with regex and hands over typed values from many sources at the cost of speed. EOF is `null` versus `NoSuchElementException`, failures are checked versus unchecked, and the newline-after-`nextInt` trap belongs to `Scanner`.

