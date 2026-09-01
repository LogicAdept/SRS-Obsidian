<!--
reps: 0
priority: 0
-->
#Java/String #Java/JVM #Java/Versions/9 #SRS

# Is it accurate to say String is backed by a character array internally

> [!abstract] Short answer
> **Not as a contract, and not on a Java 9+ HotSpot `String`.** The language type is an immutable sequence of Unicode code points. The public API is UTF-16 `char`s (`charAt`, `toCharArray`). Through Java 8 the usual JDK store was a `char[]`. **Java 9 compact strings (JEP 254)** switched that store to a **`byte[]` plus a coder flag** (Latin-1 or UTF-16). `toCharArray()` still **copies** into a new `char[]`.

## API vs heap layout

`String` objects have a constant value and represent Unicode code points. That is the language model. It does **not** name a field type. Callers never get the backing store: `toCharArray()` allocates a **new** `char[]` ([[How do you turn a Java string into a char array]]). Mutating that copy does not change the `String`.

Until compact strings, the JDK implementation stored characters in a UTF-16 `char` array (two bytes per `char`). Heap studies showed most strings were Latin-1, so half of that array was unused.

Java 9 changed **only the implementation**: `byte[]` plus an encoding flag. Contents are ISO-8859-1/Latin-1 (one byte per char) or UTF-16 (two bytes per char). The flag says which. `StringBuilder` / `StringBuffer` / HotSpot string intrinsics follow the same layout. **No public API changed.** It is **not** UTF-8 internally (explicitly out of scope).

A JDK 6 “compressed strings” `-XX` experiment used an `Object` that pointed at either `byte[]` or `char[]`. That design was not the mainline, and it was removed. Do not confuse it with JEP 254 ([[What does the String intern method do in Java]]).

So the interview line “`String` is a `char[]` underneath” is a **pre-9 implementation rumor**. The accurate line is: **UTF-16 in the API; compact `byte[]` in the 9+ JDK.**

```d2
direction: down
api: "Public String\ncharAt / toCharArray (copy)" {
  width: 300
  height: 50
  style.fill: "#fff8e1"
}
j8: "≤8 JDK store\nUTF-16 char[]" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
j9: "9+ compact store\nbyte[] + Latin-1 / UTF-16 coder" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}

api -> j8: "old HotSpot"
api -> j9: "JEP 254"
```

**Fig. 1.** Language and API stay UTF-16 `char`. The array type in the object is an implementation choice and changed in 9.

```java
class Demo {
    static void copyNotBacking(String s) {
        char[] a = s.toCharArray(); // new array; not the internal store
        a[0] = 'x';
        s.charAt(0); // unchanged
    }
}
```

**Listing 1.** `toCharArray()` is a copy. There is no supported way to obtain “the” internal array, `char[]` or `byte[]`.

> [!warning] Do not treat `char[]` as the `String` contract
> Reflection on `String.value` is not an API, breaks across JDK 8 vs 9, and is the wrong answer in an interview. Compact strings are always the 9+ representation — not a JDK 6-style optional flag. The API is still `char`; Latin-1 is only the **compressed** internal encoding.

> [!tip] Interview answer
> **Half-true for old JDKs, false as a spec, false for Java 9+.** `String` is an immutable Unicode sequence. Callers see UTF-16 `char`s. Java 9 stores a `byte[]` plus a Latin-1 vs UTF-16 coder. `toCharArray()` copies. It is not UTF-8 inside.
