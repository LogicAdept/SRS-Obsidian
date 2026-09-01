<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #DataAndState/ValueSemantics #SRS

# How would you explain Java primitive data types?

> [!abstract] Short answer
> **Eight predefined value types, not objects.** `boolean` plus seven numeric types: `byte`, `short`, `int`, `long`, `char`, `float`, `double`. They have fixed widths, default field values, and no `null`. Primitive values do not share state. Wrappers (`Integer`, `Boolean`, …) are reference types built *around* them.

## The eight, with language widths

Primitives are named by keywords. Numeric types split into integral and floating-point. Values are copied; two `int` variables never alias the same cell ([[How would you explain Java data types primitives and references]]).

| Type | What it is | Width |
| --- | --- | --- |
| `byte` | signed two’s-complement integer | 8-bit (−128…127) |
| `short` | signed two’s-complement integer | 16-bit |
| `int` | signed two’s-complement integer | 32-bit |
| `long` | signed two’s-complement integer | 64-bit |
| `char` | unsigned UTF-16 code unit | 16-bit (0…65535) |
| `float` | IEEE 754 binary32 | 32-bit |
| `double` | IEEE 754 binary64 | 64-bit |
| `boolean` | `true` / `false` only | **not specified** |

`char` is the unsigned exception among the integers ([[Is the Java char type signed or unsigned]]). `boolean` is not “1 bit” in the spec ([[What is the size of the Java boolean type]]). `Byte.SIZE` / `Integer.SIZE` / … publish the numeric widths; `Boolean` has no `SIZE`. The catalog of sizes is [[What are the storage sizes of Java primitive types]]; the roster is [[Which primitives are there in Java]].

Fields and array components get defaults: `0`, `0L`, `0.0f`, `0.0d`, `'\u0000'`, `false` ([[What default values do Java fields receive when not explicitly initialized]]). Locals do not. Arithmetic on `byte`/`short`/`char` promotes to `int`.

Each primitive has a wrapper class (`Byte`, `Short`, `Integer`, `Long`, `Float`, `Double`, `Character`, `Boolean`) so the value can be an object ([[Why are wrapper classes needed in Java]]). That pairing is not a ninth primitive.

```d2
direction: down
p: "primitive types" {
  width: 180
  height: 45
  style.fill: "#fff3e0"
}
num: "numeric\nbyte short int long char\nfloat double" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
bool: "boolean\ntrue / false" {
  width: 200
  height: 60
  style.fill: "#e8f5e9"
}

p -> num
p -> bool
```

**Fig. 1.** Eight types: seven numeric plus `boolean`. None of them is a class.

```java
public final class PrimitiveTypes {
    public static void main(String[] args) {
        System.out.println(Byte.SIZE);       // 8
        System.out.println(Integer.SIZE);    // 32
        System.out.println(Character.SIZE);  // 16 — unsigned
        // Boolean.SIZE — does not exist

        byte b = 1;
        int copy = b;        // widening copy; b unchanged
        System.out.println(copy);
    }
}
```

**Listing 1.** Numeric wrappers publish `SIZE` in bits (`Character.SIZE` is 16). `boolean` has no width constant. Assignment copies a primitive value.

> [!warning] Cheat sheets that give `boolean` as 1 bit are not the language
> `byte` is 8 bits, not “1 byte” as a C `char` that might be larger. `char` is 16-bit unsigned, not a signed C `char`. `int` is always 32 bits. Listing 1-bit `boolean` next to those fixed widths mixes a JVM encoding rumor with JLS sizes.

> [!tip] Interview answer
> **Eight primitives: `byte`, `short`, `int`, `long`, `char`, `float`, `double`, `boolean`.** They are values with fixed numeric widths — except `boolean`, which is only `true`/`false`. They are not objects, cannot be `null`, and assignment copies bits. Wrappers are separate reference types, not extra primitives.
