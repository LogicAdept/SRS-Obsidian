<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# Which primitives are there in Java?

> [!abstract] Short answer
> **Eight: `byte`, `short`, `int`, `long`, `char`, `float`, `double`, and `boolean`.** That is the full set. `void` is not a primitive. `String`, wrappers, and arrays are reference types.

## The eight, and what is not on the list

Integral types: `byte`, `short`, `int`, `long` (signed two’s complement) and `char` (unsigned 16-bit UTF-16 code unit). Floating-point: `float` and `double` (IEEE 754 binary32 / binary64). Boolean: `boolean`, whose only values are `true` and `false` ([[How would you explain Java primitive data types]]).

`void` is a method result that means “returns no value.” You cannot declare a `void` variable. `String`, `Integer`, and `int[]` are references ([[What is the difference between primitive and reference types in Java]], [[Is a Java array a primitive or an object]]).

Widths: 8 / 16 / 32 / 64 bits for `byte` / `short`·`char` / `int`·`float` / `long`·`double`. The language does **not** give `boolean` a bit size ([[What are the storage sizes of Java primitive types]]). Field defaults (`0`, `false`, `'\u0000'`) apply to fields and array cells, not to locals.

```d2
direction: down
eight: "8 primitives" {
  width: 140
  height: 40
}
intg: "byte short int long char" {
  width: 220
  height: 40
}
fp: "float double" {
  width: 140
  height: 40
}
bo: "boolean" {
  width: 100
  height: 40
}
not: "not: void, String, Integer, arrays" {
  width: 280
  height: 40
  style.fill: "#ffebee"
}

eight -> intg
eight -> fp
eight -> bo
eight -> not: "exclude"
```

**Fig. 1.** Recite the eight. Drop `void` and every object type.

```java
public final class WhichPrimitives {
    public static void main(String[] args) {
        byte b = 1;
        short s = 1;
        int i = 1;
        long n = 1L;
        char c = 'A';
        float f = 1.0f;
        double d = 1.0d;
        boolean flag = true;
        System.out.println(b + s + i + n + c);
        System.out.println(f + d);
        System.out.println(flag);
        // void v = null;   // does not compile: void is not a type for variables
    }
}
```

**Listing 1.** One local of each primitive. `void` cannot appear here.

> [!warning] Dump traps: `void`, “`boolean` = 1 bit”, `char` max
> `void` is not a primitive. `boolean` is not 1 bit in the language, and there is no `Boolean.MIN_VALUE`. `char`’s maximum is `'\uFFFF'` (65535), not `'\uFFFF' - 1`. Typos like `bolean` / `ture` are not types.

> [!tip] Interview answer
> **Eight primitives: `byte`, `short`, `int`, `long`, `char`, `float`, `double`, `boolean`.** No `void`, no `String`. If they want sizes, give the bit widths and say `boolean` has none.
