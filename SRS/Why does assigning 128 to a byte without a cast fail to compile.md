<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives/Conversions #SRS

# Why does assigning 128 to a `byte` without a cast fail to compile?

> [!abstract] Short answer
> **128 is an `int` constant that does not fit in `byte`.** The range is −128…127. Assignment may narrow a constant `int` into `byte` only when the value is representable. `byte large = 128;` is a compile-time error. `(byte) 128` compiles and wraps to **−128**.

## Constant narrowing, then the signed 8-bit box

Integer literals without `L`/`l` are type `int`. `byte` is signed 8-bit: `Byte.MIN_VALUE` is −128, `Byte.MAX_VALUE` is 127 ([[What is the value range of the Java byte type]]). Assignment does not apply general narrowing, so `byte b = someInt;` would need a cast.

The exception: a **constant** `byte`/`short`/`char`/`int` expression whose value **already fits**. That is why `byte b = 5;` and `byte max = 127;` compile — the same rule as `char ch = 97` ([[What happens when you assign an int literal that exceeds the char range]], [[What is a compile-time constant in Java]]). 128 is a perfectly legal `int`; it is simply not a `byte`.

A **variable** never gets that exception: `int n = 5; byte b = n;` does not compile even though 5 would fit. Write `(byte) n`.

With an explicit cast, narrowing keeps the **low 8 bits**. 128 is `0x80`, which as a signed `byte` is −128 (`Byte.MIN_VALUE`). No exception ([[What happens when you cast 280 to a Java byte]]). `byte b = b + 1` is a different failure: the `+` is `int`, and that expression is not a fitting constant ([[Why does a byte plus-equals compile when byte plus one does not]]).

```d2
direction: down
lit: "int literal 128" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
fit: "−128 … 127?\nByte.MAX_VALUE is 127" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
err: "byte large = 128\ncompile error" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
ok: "(byte) 128 → -128\nlow 8 bits" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

lit -> fit
fit -> err: "no"
fit -> ok: "cast anyway"
```

**Fig. 1.** Out-of-range `int` constants are rejected on assignment. A cast wraps; it does not clamp to 127.

```java
public final class Assign128ToByte {
    public static void main(String[] args) {
        byte inRange = 5;         // constant fits
        byte max = 127;           // Byte.MAX_VALUE
        System.out.println(inRange);
        System.out.println(max);

        // byte large = 128;      // compile error: 128 > 127
        byte wrapped = (byte) 128; // -128
        System.out.println(wrapped);

        int n = 5;
        // byte fromVar = n;      // compile error: not a constant
        byte fromVar = (byte) n;
        System.out.println(fromVar);
    }
}
```

**Listing 1.** 5 and 127 assign. 128 needs `(byte)` and becomes `MIN_VALUE`. A non-constant `int` always needs the cast.

> [!warning] The cast does not clamp, and a variable is not a literal
> `(byte) 128` is −128, not 127. Out of range is a **compile** error only when the cast is missing. `int n = 5; byte b = n;` fails even though 5 fits — implicit narrowing is for constants assigned to `byte`/`short`/`char`, not for any `int` that happens to look small. `byte` is signed: 128 is one past `MAX_VALUE`, not an unsigned octet.

> [!tip] Interview answer
> **`byte large = 128;` does not compile because 128 is an `int` outside −128…127.** Implicit narrowing of an `int` constant is allowed only when the value already fits. With `(byte) 128` you get −128 — the low 8 bits, no exception. A non-constant `int` always needs that cast.
