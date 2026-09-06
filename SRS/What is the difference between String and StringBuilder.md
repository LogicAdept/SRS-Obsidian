<!--
reps: 0
priority: 0
-->
#Java/String #Java/StringBuilder #SRS

# What is the difference between String and StringBuilder

> [!abstract] Short answer
> **`String` is an immutable sequence of Unicode code points; `StringBuilder` is a mutable character buffer.** Changing text with `String` means a **new** `String` (`+` unless it is a constant expression). `StringBuilder` mutates one buffer with `append` / `insert`; `toString()` copies out a new `String`. Builder is unsynchronized (Java 5); prefer it on one thread over `StringBuffer`. It is not the GoF “builder()” for domain objects.

## Immutable value vs growing buffer

`String` has a constant value. Literals are interned instances of that class. Indexes are UTF-16 `char`s. `equals` compares character sequences. Because the value cannot change, instances can be shared ([[How would you explain java.lang.String]]).

`StringBuilder` is a drop-in unsynchronized `StringBuffer`: `append` at the end (`append(x)` ≡ `insert(length(), x)`), capacity starting at 16, automatic growth, `toString()` a snapshot that later edits do not change. `null` appends `"null"`. Not safe for multiple threads ([[How would you explain java.lang.StringBuilder]], [[How would you explain the StringBuilder append method]]).

`+` on non-constants always creates a new `String`. A loop of `s = s + piece` recopies the prefix; one `StringBuilder` plus `append` is the fix ([[How would you explain performance pitfalls of naive string concatenation]]). A compiler may rewrite a **single** `a + b + c` expression with a builder or `StringConcatFactory`; that is still not “`String` is mutable.”

`StringBuilder` implements `Comparable` but not `equals`; `String.compareTo` is consistent with `equals`. Do not intern a builder; intern the `String` from `toString()` if you must.

```d2
direction: down
s: "String\nimmutable · internable literals · new object on +" {
  width: 340
  height: 50
}
sb: "StringBuilder\nmutable buffer · append/insert · toString snapshot" {
  width: 340
  height: 50
}
use: "Few pieces / constants → String\nMany pieces / loop → one StringBuilder" {
  width: 320
  height: 50
}

s -> use
sb -> use
```

**Fig. 1.** Same characters on the API (`CharSequence`); different mutation and allocation stories.

```java
public class StringVsBuilderDemo {
    static String withPlus(String a, String b) {
        return a + b; // new String (if not a compile-time constant)
    }

    static String withBuilder(String a, String b) {
        return new StringBuilder(a).append(b).toString();
    }
}
```

**Listing 1.** Two pieces: either is fine. In a loop, keep **one** builder; do not concatenate `String`s each iteration.

> [!warning] Not `User.builder()`, and `+` does not mutate `String`
> `StringBuilder` is not a fluent factory for types with many fields. `s = s + x` leaves the old `s` unchanged and assigns a new object. Sharing one `StringBuilder` across threads is unsafe. `toString()` is a copy; keep mutating the builder and the snapshot stays put.

> [!tip] Interview answer
> **`String` is immutable; any “change” is a new object.** **`StringBuilder` is a mutable buffer: `append`, then `toString`.** Use `String` for values and interned literals; use one builder when you assemble many pieces. It is not the Builder pattern for `User`.
