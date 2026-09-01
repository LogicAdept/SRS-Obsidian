<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# What are the storage sizes of Java primitive types?

> [!abstract] Short answer
> **Numeric primitives have fixed bit widths; `boolean` does not.** `byte` is 8 bits, `short` and `char` 16, `int` and `float` 32, `long` and `double` 64. Those are the **value** widths (`Byte.SIZE`, `Integer.SIZE`, …). The language does not give `boolean` a bit size, and there is no `Boolean.SIZE`.

## Width of the value, not the object

The integral types are two’s-complement `byte`, `short`, `int`, and `long` at **8 / 16 / 32 / 64** bits, plus `char` as a **16-bit** unsigned UTF-16 code unit. `float` and `double` are IEEE 754 **binary32** and **binary64**. Each numeric wrapper’s `SIZE` is that bit count; `BYTES` is `SIZE / 8` ([[How many bits are in one Java byte]]).

`boolean` has only `true` and `false`. It is **not** “1 bit” in the language, and JVM computational operations treat it as `int`. Layout of a `boolean` field or `boolean[]` is an implementation choice ([[What is the size of the Java boolean type]]).

These widths are **not** the size of a boxed `Integer` on the heap, and they are **not** “always one stack slot.” A `long` or `double` value is 64 bits; a local still lives in a frame, a field still lives in its object ([[How would you explain Java primitive data types]]).

| Type | Bits (`Type.SIZE`) | Bytes (`Type.BYTES`) |
| --- | ---: | ---: |
| `byte` | 8 | 1 |
| `short` | 16 | 2 |
| `int` | 32 | 4 |
| `long` | 64 | 8 |
| `char` | 16 | 2 |
| `float` | 32 | 4 |
| `double` | 64 | 8 |
| `boolean` | *(none)* | *(none)* |

```d2
direction: down
widths: "value width" {
  width: 160
  height: 40
}
b8: "byte 8" {
  width: 100
  height: 40
}
b16: "short / char 16" {
  width: 160
  height: 40
}
b32: "int / float 32" {
  width: 150
  height: 40
}
b64: "long / double 64" {
  width: 170
  height: 40
}
bo: "boolean unspecified" {
  width: 180
  height: 40
  style.fill: "#fff8e1"
}

widths -> b8
widths -> b16
widths -> b32
widths -> b64
widths -> bo
```

**Fig. 1.** Language value widths. `boolean` is the exception: two values, no `SIZE`.

```java
public final class PrimitiveStorageSizes {
    public static void main(String[] args) {
        System.out.println(Byte.SIZE);       // 8
        System.out.println(Short.SIZE);      // 16
        System.out.println(Integer.SIZE);    // 32
        System.out.println(Long.SIZE);       // 64
        System.out.println(Character.SIZE);  // 16
        System.out.println(Float.SIZE);      // 32
        System.out.println(Double.SIZE);     // 64
        System.out.println(Byte.BYTES);      // 1
        // Boolean.SIZE does not exist
    }
}
```

**Listing 1.** Numeric wrappers expose `SIZE` (bits) and `BYTES`. `Boolean` has neither.

> [!warning] Do not quote “`boolean` = 1 bit”
> Interview tables that put `boolean` at 1 bit (or 8 bits) are talking about **some JVM’s layout**, not a language rule. `SIZE` is the representation of the **primitive value**, not padding around a field or the size of a wrapper object.

> [!tip] Interview answer
> **Eight primitives; seven have fixed bit sizes; `boolean` does not.** Recite 8 / 16 / 32 / 64 for `byte` / `short`·`char` / `int`·`float` / `long`·`double`, and say `Boolean.SIZE` is not a thing. Those numbers are value widths, not heap object sizes.
