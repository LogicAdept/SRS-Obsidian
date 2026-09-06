<!--
reps: 0
priority: 0
-->
#Java/IO/Streams #SRS

# Which class reads primitive values from a Java `InputStream`?

> [!abstract] Short answer
> **`DataInputStream` (Java 1.0).** It extends `FilterInputStream` and implements `DataInput`, so it reconstructs `boolean`, `byte`, `char`, `short`, `int`, `long`, `float`, `double`, and modified-UTF-8 `String`s from an underlying byte stream, high byte first. Pair it with `DataOutputStream` (`DataOutput`) so `writeInt` matches `readInt`. Primitive reads throw **`EOFException`** if the stream ends mid-value — not `InputStream.read()`’s `-1`. `readUTF` is **modified UTF-8**, not UTF-8 ([[What are common concrete InputStream and OutputStream implementations]], [[What kinds of input and output streams exist in Java]]).

## A `DataInput` filter, not a source

Constructor: `DataInputStream(InputStream in)`. Wrap a file, socket, or `ByteArrayInputStream`. `RandomAccessFile` also implements `DataInput` but is not an `InputStream` wrapper ([[What is RandomAccessFile in Java]], [[Which subclasses class InputStream you do you know for what they intended]]). `ObjectInputStream` can read primitives during **deserialization** — wrong class for this cue.

| Read | Width | Writer twin |
| --- | --- | --- |
| `readBoolean` | 1 byte (zero / nonzero) | `writeBoolean` |
| `readByte` / `readUnsignedByte` | 1 | `writeByte` |
| `readShort` / `readChar` / `readUnsignedShort` | 2, high byte first | `writeShort` / `writeChar` |
| `readInt` / `readFloat` | 4 | `writeInt` / `writeFloat` |
| `readLong` / `readDouble` | 8 | `writeLong` / `writeDouble` |
| `readUTF` | 2-byte length + modified UTF-8 | `writeUTF` |
| `readFully` | exact `len` or `EOFException` | `write(byte[])` |

`readLine()` on `DataInputStream` is **deprecated** (bytes as Latin `char`s). Use `BufferedReader` for text ([[What are buffered streams in Java]], [[What kinds of input and output streams exist in Java]]). `skipBytes` never throws `EOFException`. `DataOutputStream` is not safe for unsynchronized concurrent writers.

```java
import java.io.ByteArrayInputStream;
import java.io.DataInputStream;
import java.io.IOException;

class ReadPrimitives {
    static int firstInt(byte[] bigEndian) throws IOException {
        try (DataInputStream in = new DataInputStream(new ByteArrayInputStream(bigEndian))) {
            return in.readInt();
        }
    }
}
```

**Listing 1.** The class that answers the cue: wrap any `InputStream`, call `readInt()`. Need four bytes or `EOFException`.

```d2
direction: down
in: "InputStream" {
  width: 160
  height: 40
  style.fill: "#e3f2fd"
}
dis: "DataInputStream\nDataInput" {
  width: 200
  height: 45
  style.fill: "#e8f5e9"
}
prim: "readInt / readUTF" {
  width: 180
  height: 40
  style.fill: "#fff8e1"
}
in -> dis -> prim
```

**Fig. 1.** Primitives from a byte `InputStream` go through `DataInputStream`, not `Scanner` and not `Reader` ([[What is the difference between and what InputStream OutputStream Reader Writer]], [[Which classes convert between Java byte streams and character streams]]).

> [!warning] `read()` EOF is not `readInt()` EOF
> `InputStream.read()` returns `-1` at end. `DataInput.readInt()` throws `EOFException`. `readUTF` rejects standard UTF-8 that uses 4-byte sequences or a 1-byte NUL. Do not use this class to **write** — that is `DataOutputStream`.

> [!tip] Interview answer
> `DataInputStream` wraps an `InputStream` and implements `DataInput` so you can read portable primitives and modified UTF-8 strings. Match it with `DataOutputStream`. If the stream ends in the middle of an `int`, you get `EOFException`, not `-1`.
