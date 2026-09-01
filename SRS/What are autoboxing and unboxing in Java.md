<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers/Autoboxing #SRS

# What are autoboxing and unboxing in Java?

> [!abstract] Short answer
> **Boxing** converts a **primitive** to its **wrapper** (`int` → `Integer`). **Unboxing** is the reverse (`Integer` → `int`). **Autoboxing** is the compiler inserting those conversions — `Integer.valueOf` and `xxxValue` — so you do not write them. The eight primitive/wrapper pairs are a closed list. The feature arrived in Java 5. It is a conversion in assignment, invocation, and cast contexts — not a new numeric type. Unboxing `null` throws `NullPointerException`.

## Primitive value ↔ wrapper object

Each of the eight primitives has a matching wrapper (`boolean`/`Boolean`, `byte`/`Byte`, `short`/`Short`, `char`/`Character`, `int`/`Integer`, `long`/`Long`, `float`/`Float`, `double`/`Double` — [[What are the wrapper types for Java primitives]]). Boxing conversion builds a wrapper whose `xxxValue()` equals that primitive. Unboxing conversion *is* that method call, and throws `NullPointerException` if the reference is `null` ([[What method does the compiler insert when autoboxing an int]], [[What method does the compiler insert when unboxing an Integer]], [[What is unboxing]]).

**Auto**-boxing/unboxing means you do not write those calls: `Integer j = 5` and `int n = j` compile as `Integer.valueOf(5)` and `j.intValue()`, not `new Integer` ([[When does autoboxing occur in Java]], [[Why does autoboxing exist in Java]]).

```d2
direction: down
p: "int 5" {
  width: 100
  height: 40
}
box: "autoboxing\nInteger.valueOf" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
unbox: "unboxing\nintValue" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
p -> box -> unbox
```

**Fig. 1.** Boxing and unboxing are inverse conversions; “auto” means the compiler inserts them.

```java
int p = 5;
Integer boxed = p;           // boxing — Integer.valueOf(5)
int back = boxed;            // unboxing — boxed.intValue()

List<Integer> list = new ArrayList<>();
list.add(5);                 // boxing at the collection boundary
int n = list.get(0);         // unboxing
```

**Listing 1.** Conceptual: assignment and the collection boundary.

They exist because generics and collections store objects, not `int` ([[In which Java version were autoboxing and unboxing introduced]]). `List<int>` remains illegal. Matching is exact — a `byte` variable does not box to `Integer` or `Short`; assignment conversion details live in [[What are the autoboxing rules when assigning a primitive to a wrapper]]. Two wrappers compared with `==` test identity (cache for **-128..127** — [[Which wrapper types besides Integer cache boxed values]]). Loop `Integer` accumulators allocate; unboxing `null` throws.

> [!warning] Unboxing `null` is still a method call
> `int x = (Integer) null;` looks like a cast/assignment and throws `NullPointerException` from `intValue()`. Autoboxing did not make `int` nullable.

> [!tip] Interview answer
> **Boxing puts a primitive into its wrapper; unboxing takes it out.** Since Java 5 the compiler does that with `valueOf` and `intValue` (`Integer x = 5`, `int n = x`) so `List<Integer>` can take an `int`. It is not a third numeric type. Unboxing `null` throws, and `==` on two wrappers is identity.
