<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# When should you use the Java `byte` type?

> [!abstract] Short answer
> **Use it for 8-bit cells — `byte[]` buffers and large arrays — not as a mini-`int`.** `byte` is a signed integer −128…127 (`Byte.MIN_VALUE`…`MAX_VALUE`). Binary I/O speaks `byte[]`. Arithmetic still promotes to `int`, so a local `byte` does not make `a + b` smaller or faster.

## Arrays and streams, not arithmetic

`byte` is the 8-bit signed two’s-complement integer ([[What is the value range of the Java byte type]], [[How many bits are in one Java byte]]). `Byte.SIZE` / `Byte.BYTES` are that width. A field or array component defaults to `(byte) 0` ([[What default values do Java fields receive when not explicitly initialized]]).

That compactness matters when you store **many** of them: a `byte[]` of length *n* is *n* 8-bit components. The I/O APIs are built on that: `InputStream.read(byte[])` fills a buffer; `read()` returns the next octet as an `int` in **0…255**, or `-1` at EOF — because a Java `byte` cannot hold 255. [[Which classes convert between Java byte streams and character streams]] is the byte vs char stream split.

Do **not** pick `byte` to “save space” on a counter or a loop index. In a numeric arithmetic context the promoted type is `int`: `byte a + byte b` is `int`, and assigning it back needs `(byte)` ([[Why does adding two byte values not compile as a byte in Java]], [[How does numeric promotion work in Java arithmetic expressions]]). Locals used in arithmetic are `int` on the JVM anyway.

For a 0…255 **view** of the same bits, `Byte.toUnsignedInt` / `compareUnsigned` exist. The variable is still a signed `byte`. Values 128…255 need a cast and wrap ([[Why does assigning 128 to a byte without a cast fail to compile]]).

```d2
direction: down
use: "byte / byte[]" {
  width: 180
  height: 50
  style.fill: "#e8f5e9"
}
io: "binary buffers\nInputStream, files" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
arr: "large arrays\nvalues in −128…127" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
not: "not a + b as byte\npromotes to int" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}

use -> io
use -> arr
use -> not
```

**Fig. 1.** `byte` is an 8-bit cell type. It is not an 8-bit ALU type.

```java
public final class WhenToUseByte {
    public static void main(String[] args) throws java.io.IOException {
        byte[] buf = new byte[1024];      // 1024 eight-bit cells, default 0

        byte a = 10;
        byte b = 20;
        int sum = a + b;                  // 30 — type int
        // byte compact = a + b;          // compile error

        java.io.InputStream in =
            new java.io.ByteArrayInputStream(new byte[] { (byte) 0xFF });
        int octet = in.read();            // 255, not a signed byte
        byte cell = (byte) octet;         // -1
        System.out.println(sum);
        System.out.println(octet);
        System.out.println(cell);
        System.out.println(Byte.toUnsignedInt(cell)); // 255
        System.out.println(buf.length);
    }
}
```

**Listing 1.** Store and move octets in `byte[]`. Add with `int`. `read()` is 0…255 so EOF `-1` is distinct from data.

> [!warning] `byte` is signed, and `read()` is not a `byte`
> `128` does not fit; `(byte) 128` is `-128`. High bit set means negative, not “octet 128”. `InputStream.read()` is an `int` precisely so 255 and EOF `-1` do not collide. Writing `byte b = (byte) in.read();` without checking `-1` first will turn EOF into a data byte `-1` (`0xFF`).

> [!tip] Interview answer
> **Use `byte` for 8-bit storage — especially `byte[]` and I/O buffers — when the value is in −128…127 or you are holding raw octets.** Do not use it to shrink arithmetic: `byte + byte` is `int`. It is signed; for 0…255 use `int` from `read()` or `Byte.toUnsignedInt`.
