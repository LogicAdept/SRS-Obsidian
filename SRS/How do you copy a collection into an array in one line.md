<!--
reps: 0
priority: 0
-->
#Java/Collections #Java/Arrays #SRS

# How do you copy a collection into an array in one line?

> [!abstract] Short answer
> One line, three spellings: `c.toArray()` for `Object[]`, `c.toArray(new String[0])` when you want a typed array — the classic idiom, "identical in function to `toArray()`" per the Javadoc API note — and since Java 11 the generator form `c.toArray(String[]::new)`. Every element is copied in iterator order into a fresh array the caller owns.

## The three overloads of `toArray`

`Collection` declares all three. `toArray()` always produces `Object[]` — the runtime component type is fixed, so no cast can turn it into `String[]`. `toArray(T[] a)` uses the argument's runtime type: if the collection fits, it fills the passed array and returns it (adding a `null` terminator if there is room to spare); otherwise it allocates a new array of the same runtime type — that is why you must reassign the result. The generator overload `toArray(IntFunction<T[]>)` allocates exactly one array of the requested type ([[What is collection]]).

```d2
direction: down
need: "Need a typed array?" {
  width: 240
  height: 64
  style.fill: "#e3f2fd"
}
obj: "No → toArray()\nObject[], caller-owned copy" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
typed: "Yes → Java 11+\ntoArray(String[]::new)" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
legacy: "Legacy codebase\ntoArray(new String[0])" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
need -> obj: no
need -> typed: yes
typed -> legacy: "equivalent,\nolder idiom"
```

**Fig. 1.** Same copy semantics in all branches; only the array's runtime type and the spelling differ.

```java
Collection<String> c = List.of("x", "y");

Object[] a1 = c.toArray();
String[] a2 = c.toArray(new String[0]);     // idiomatic one-liner
String[] a3 = c.toArray(String[]::new);     // Java 11+
System.out.println(Arrays.toString(a2) + " " + a2.getClass().getSimpleName());

String[] broken = (String[]) c.toArray();   // Object[] at runtime
```

**Listing 1.** The typed one-liners work; the cast fails. Verified on JDK 21 — output: `[x, y] String[]`, then `ClassCastException: class [Ljava.lang.Object; cannot be cast to class [Ljava.lang.String;`.

> [!warning] The cast of `toArray()` is the classic interview trap
> `(String[]) c.toArray()` throws `ClassCastException` at runtime because the array's actual type is `Object[]` — the compile-time cast lies. Also remember `toArray(T[])` reuses the passed array when it is big enough: an oversized guess like `toArray(new String[c.size() + 2])` leaves trailing `null` elements in the returned array ([[Can you turn a Java array into a stream]]).

> [!tip] Interview answer
> **`c.toArray(new String[0])` is the one-line answer — the collection copies its elements, in iterator order, into a typed array it allocates; Java 11+ offers the same thing as `c.toArray(String[]::new)`.** Plain `toArray()` gives `Object[]` and cannot be cast to a typed array; the `T[]` variant returns either the array you passed (if it fit) or a new one, so always use the return value.
