<!--
reps: 0
priority: 0
-->
#Java/StringBuilder #Java/StringBuffer #SRS

# What is the difference between StringBuilder and StringBuffer

> [!abstract] Short answer
> **Same mutable-buffer API (`append` / `insert`, capacity, `toString` snapshot). The difference is threads.** `StringBuffer` (1.0) is **thread-safe**: methods are synchronized where needed so operations on **one** instance serialize. `StringBuilder` (5) is the unsynchronized drop-in for a **single thread**; the API says use it in preference and that it is faster under most implementations because it does **no** synchronization. Buffer still does **not** lock a shared *source* you append from.

## Synchronization, not a different alphabet

Both are mutable character sequences with a growing internal buffer (default capacity 16). `append(x)` is `insert(length(), x)`. Overflow enlarges the buffer. `toString()` allocates a new `String`; later edits do not change it. `null` `String` / `CharSequence` appends `"null"`. Both implement `Comparable` and do **not** override `equals` ([[How would you explain java.lang.StringBuilder]]).

`StringBuffer`: safe for multiple threads on **that instance**. The monitor is the buffer performing the operation, **not** the source sequence. If you `append` a `CharSequence` shared across threads, the caller must keep that source stable (lock it, pass an immutable `String`, or do not share it).

`StringBuilder`: **not** safe for multiple threads. If you need that, use `StringBuffer`. Since JDK 5, Builder is the recommended default for local assembly ([[Is StringBuilder faster than StringBuffer without synchronization]]). Neither makes `String` mutable; a loop of `s = s + x` is a different problem ([[What is the difference between String and StringBuilder]]).

```d2
direction: down
api: "Same API\nappend / insert / capacity / toString" {
  width: 300
  height: 50
}
buf: "StringBuffer\nsynchronized on this instance · Java 1.0" {
  width: 320
  height: 50
}
bld: "StringBuilder\nno synchronization · Java 5 · prefer on one thread" {
  width: 340
  height: 50
}

api -> buf
api -> bld
```

**Fig. 1.** Mutability is shared. The split is whether each public mutation takes the instance’s monitor.

```java
public class BuilderVsBufferDemo {
    static String localJoin(String[] parts) {
        StringBuilder sb = new StringBuilder(); // one thread
        for (String p : parts) {
            sb.append(p);
        }
        return sb.toString();
    }

    static void appendShared(StringBuffer shared, String piece) {
        shared.append(piece); // safe for concurrent calls on shared
    }
}
```

**Listing 1.** Local concatenation: `StringBuilder`. A buffer published to several threads: `StringBuffer` (still protect a mutable source).

> [!warning] Sync on the buffer is not sync on the source
> Concurrent `append` on one `StringBuffer` serializes. `append(sharedMutableCharSequence)` does **not** lock that source. `StringBuilder` shared across threads is a data race. Do not pick Buffer “for speed” — the spec’s speed claim runs the other way. `compareTo` without `equals` still applies to both.

> [!tip] Interview answer
> **Both are mutable string buffers with the same operations.** **`StringBuffer` is synchronized; `StringBuilder` is not, and is the Java 5 single-thread replacement.** Prefer Builder unless multiple threads mutate one instance. Buffer does not lock the sequence you copy from.
