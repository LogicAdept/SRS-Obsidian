<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# What is the size of the Java `boolean` type?

> [!abstract] Short answer
> **The language does not define one.** `boolean` has two values, `true` and `false` — not a bit width. Cheat sheets that say “1 bit” are not a storage guarantee. The numeric primitives have fixed widths (`byte` 8, `int` 32, …); `boolean` does not. `Boolean` has no `SIZE` / `BYTES` constants.

## Two values, not a width

`byte`, `short`, `char`, `int`, `long`, `float`, and `double` each have a specified range and format ([[What are the storage sizes of Java primitive types]], [[Why does the Java int type have a fixed size]]). `boolean` is specified only as a logical type with literals `true` and `false`. There are no conversions between `boolean` and the numeric types except via expressions such as `x != 0`.

Where the value actually sits is a **JVM** question, and it is not one number:

- **Computation.** There are no `boolean` arithmetic/load opcodes. Compilers map `boolean` to the JVM `int` computational type (category 1). A local `boolean` occupies **one local-variable slot**, the same kind of slot as `int` — 32-bit `int` encoding, `1` for `true` and `0` for `false`.
- **`boolean[]`.** The VM accesses components with `baload` / `bastore`. In Oracle’s JVM, those arrays are encoded as `byte` arrays: **8 bits per element**, not 1. That is an implementation note in the VM spec, not a JLS field-layout rule.
- **Object fields.** Layout, padding, and whether a `boolean` field is a byte or packed with neighbors are **not specified**. Do not treat “1 byte in HotSpot” as a language fact.

```d2
direction: down
lang: "boolean\ntrue / false only" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
comp: "bytecode ops use int\n1 slot, 1 or 0" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
arr: "Oracle boolean[]\n8 bits per element" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
no: "not a 1-bit JLS size" {
  width: 220
  height: 55
  style.fill: "#ffebee"
}

lang -> comp
lang -> arr
lang -> no
```

**Fig. 1.** The type is two values. Storage is a JVM encoding, and it is not “1 bit” everywhere.

```java
public final class BooleanHasNoSize {
    public static void main(String[] args) {
        System.out.println(Byte.SIZE);     // 8
        System.out.println(Integer.SIZE);  // 32
        // Boolean.SIZE  — does not exist (unlike Byte, Integer, …)

        boolean flag = true;               // compiles to int 1 on the JVM
        boolean[] bits = new boolean[8];   // not 1 byte total on Oracle’s VM
        bits[0] = flag;
        System.out.println(bits.length);   // 8 elements
    }
}
```

**Listing 1.** Numeric wrappers publish `SIZE`. `Boolean` does not. An eight-element `boolean[]` is eight array components, not eight packed bits.

> [!warning] “1 bit” is a table myth, not packed storage
> A `boolean[]` is not a bitset. Oracle’s VM uses a **byte per element**. Locals and expression values are `int` slots, not 1-bit flags. If you need packed bits, that is a different data structure, not the `boolean` type. [[How many bits are in one Java byte]] is a real width; `boolean` is not.

> [!tip] Interview answer
> **`boolean` has no specified size — only `true` and `false`.** Tables that list 1 bit are not JLS storage. The JVM compiles `boolean` operations to `int` (`1`/`0`), and Oracle’s VM stores `boolean[]` as one byte per element. `Boolean.SIZE` does not exist.
