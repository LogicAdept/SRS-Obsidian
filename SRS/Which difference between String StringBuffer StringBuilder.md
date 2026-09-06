<!--
reps: 0
priority: 0
-->
#Java/String #Java/StringBuilder #Java/StringBuffer #SRS

# Which difference between String StringBuffer StringBuilder

> [!abstract] Short answer
> **`String` is immutable: any “edit” is a new object.** **`StringBuffer` and `StringBuilder` are mutable buffers** (`append` / `insert`, growing capacity, `toString()` snapshot). **Buffer (1.0) is thread-safe** (synchronized on that instance). **Builder (5) is the unsynchronized drop-in**, recommended for one thread and faster under most implementations because it does no synchronization. Same character API family; different mutation and locking.

## Immutable value vs two buffers

`String`: constant value, internable literals, language `+` (non-constant `+` allocates a new `String`). Share freely across threads. You cannot overwrite the characters ([[How would you explain java.lang.String]], [[What is the difference between String and StringBuilder]]).

`StringBuffer`: like a `String` that can be modified. Methods are synchronized where needed so concurrent calls on **one** instance serialize. It does **not** lock a shared source you append from.

`StringBuilder`: API-compatible with Buffer, **no** synchronization, **not** safe for multiple threads. Prefer it on a single thread ([[What is the difference between StringBuilder and StringBuffer]]). Java 5.

For many pieces, mutate **one** buffer then `toString()`; a loop of `s = s + x` recopies `String`s ([[What is the difference between StringBuilder and naive string concatenation]]). Neither buffer interns; intern the resulting `String` if you must.

```d2
direction: down
s: "String\nimmutable · intern literals · new object to change" {
  width: 340
  height: 50
}
pair: "Mutable buffers\nappend / insert / capacity / toString" {
  width: 320
  height: 50
}
buf: "StringBuffer\nsynchronized · Java 1.0" {
  width: 280
  height: 45
}
bld: "StringBuilder\nunsynchronized · Java 5 · prefer locally" {
  width: 320
  height: 45
}

s -> pair: "need mutation"
pair -> buf
pair -> bld
```

**Fig. 1.** First split: immutable vs buffer. Second split: synchronized Buffer vs Builder.

```java
public class ThreeStringTypesDemo {
    static String immutable(String a, String b) {
        return a + b; // new String
    }

    static String oneThread(String[] parts) {
        StringBuilder sb = new StringBuilder();
        for (String p : parts) {
            sb.append(p);
        }
        return sb.toString();
    }

    static void manyThreads(StringBuffer shared, String piece) {
        shared.append(piece); // serialized on shared
    }
}
```

**Listing 1.** `String` for values. Builder for local assembly. Buffer only if several threads mutate one instance.

> [!warning] “Identical except faster” skips the source lock
> Builder is not magically faster than Buffer on a single uncontended call in every JMH run — the spec’s claim is **no synchronization**. Concurrent Builder use is a data race. Buffer’s sync does not freeze a mutable `CharSequence` argument. Do not use Buffer as a faster `String`.

> [!tip] Interview answer
> **`String` cannot change; Buffer and Builder can.** **Buffer is synchronized; Builder (Java 5) is not, and is what you use on one thread.** For loops, append to one buffer rather than `s = s + x`.
