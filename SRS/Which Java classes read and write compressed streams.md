<!--
reps: 0
priority: 0
-->
#Java/IO/Streams #SRS

# Which Java classes read and write compressed streams?

> [!abstract] Short answer
> **`java.util.zip` filters on `java.io` byte streams (since 1.1).** Write: `DeflaterOutputStream` compresses **deflate** (`FilterOutputStream`); `GZIPOutputStream` and `ZipOutputStream` subclass it (GZIP file format; ZIP **entries**, compressed or `STORED`). Read: `InflaterInputStream` inflates deflate (`FilterInputStream`); `GZIPInputStream` and `ZipInputStream` subclass it. `Deflater` / `Inflater` are ZLIB **engines** (`setInput` / `deflate` / `inflate` / `end()`), not streams — wrap them in the `*Stream` filters when you want a stream ([[What kinds of input and output streams exist in Java]], [[What are common concrete InputStream and OutputStream implementations]]).

## Deflate filters, then ZIP and GZIP

`DeflaterOutputStream(out)` uses a default compressor; you can pass a `Deflater`. `finish()` ends compressed data **without** closing `out` (chain more filters on the same sink). `close()` writes remaining compressed bytes and closes the underlying stream. `GZIPOutputStream` writes GZIP. `ZipOutputStream` writes **entries** (`putNextEntry` / `closeEntry`); default method is `DEFLATED`. `JarOutputStream` subclasses `ZipOutputStream`.

`InflaterInputStream` inflates deflate; `read()` blocks until a byte can be decompressed; `-1` at end of compressed input. `GZIPInputStream` / `ZipInputStream` subclass it (`ZipInputStream.getNextEntry()` walks LOC headers). `available()` on `InflaterInputStream` is **1 before EOF and 0 after**, not a byte count. `markSupported()` is `false` ([[What kinds of input and output streams exist in Java]], [[What are buffered streams in Java]]).

These are **byte** filters. For text, wrap with `InputStreamReader` / `OutputStreamWriter` after inflate or before deflate ([[Which classes convert between Java byte streams and character streams]], [[What are buffered streams in Java]]).

| Write | Read | Format |
| --- | --- | --- |
| `DeflaterOutputStream` | `InflaterInputStream` | raw deflate |
| `GZIPOutputStream` | `GZIPInputStream` | GZIP |
| `ZipOutputStream` | `ZipInputStream` | ZIP entries |
| `Deflater` | `Inflater` | ZLIB engine, not a stream |

```java
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.zip.GZIPInputStream;
import java.util.zip.GZIPOutputStream;

class GzipFiles {
    static void compress(String from, String to) throws IOException {
        try (FileInputStream in = new FileInputStream(from);
             GZIPOutputStream out = new GZIPOutputStream(new FileOutputStream(to))) {
            in.transferTo(out);
        }
    }

    static void decompress(String from, String to) throws IOException {
        try (GZIPInputStream in = new GZIPInputStream(new FileInputStream(from));
             FileOutputStream out = new FileOutputStream(to)) {
            in.transferTo(out);
        }
    }
}
```

**Listing 1.** GZIP write/read as `Filter*` on file streams. Try-with-resources on `GZIPOutputStream` so `close()` finishes compressed bytes. Use `finish()` if `out` must stay open.

```d2
direction: down
def: "DeflaterOutputStream / InflaterInputStream\ndeflate" {
  width: 340
  height: 50
  style.fill: "#e8f5e9"
}
gz: "GZIP*Stream" {
  width: 160
  height: 40
  style.fill: "#e3f2fd"
}
zip: "Zip*Stream\nentries" {
  width: 160
  height: 40
  style.fill: "#fff8e1"
}
def -> gz
def -> zip
```

**Fig. 1.** Interview set: deflate pair, then GZIP and ZIP subclasses. Engines `Deflater`/`Inflater` sit inside, not in the `InputStream` tree ([[Which subclasses class InputStream you do you know for what they intended]]).

> [!warning] `ZipOutputStream` is not a raw deflate blob, and `available()` is not length
> ZIP needs `putNextEntry`. `InflaterInputStream.available()` is 0 or 1. `Deflater`/`Inflater` need `end()`; they are not `Closeable` streams. Unsupported store or missing privileges are not these types — they are still `java.io` filters when the platform supports zip.

> [!tip] Interview answer
> Compressed streams live in `java.util.zip`: `DeflaterOutputStream` and `InflaterInputStream` for deflate, with GZIP and ZIP subclasses. `Deflater` and `Inflater` are the ZLIB engines underneath, not stream classes. Close the filter so remaining compressed bytes are written.
