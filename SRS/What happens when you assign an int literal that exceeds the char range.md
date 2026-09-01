<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives/Conversions #SRS

# What happens when you assign an `int` literal that exceeds the `char` range?

> [!abstract] Short answer
> **The assignment does not compile.** An `int` constant may narrow into `char` only when the value is representable as `char`: **0…65535**. `char ch = 66000;` is a compile-time error. `(char) 66000` compiles and **wraps** to the low 16 bits (464), with no exception.

## Constant narrowing, then the unsigned 16-bit box

`char` is a 16-bit **unsigned** integral type: `'\u0000'`…`'\uffff'`, which is 0…65535. `Character.MIN_VALUE` / `Character.MAX_VALUE` are those endpoints. It is not signed `short`. [[What is the value range of the Java char type]] and [[Is the Java char type signed or unsigned]] are that box.

Integer literals are `int`. Assignment does not apply general narrowing, so `char c = someInt;` would normally need a cast. There is one exception: a **constant** `byte`/`short`/`char`/`int` expression whose value **already fits** in the variable’s type. That is why `char a = 97;` (`'a'`) and `char letterB = 66;` (`'B'`) compile — the same rule as `byte b = 42`. `66000` is still a legal `int` literal; it simply does not fit in `char`, so the exception does not apply. [[Why does assigning 128 to a byte without a cast fail to compile]] is the signed 8-bit twin; [[What is a compile-time constant in Java]] is what “constant” means.

A **variable** of type `int` never gets that exception, even if the runtime value would fit: `int n = 97; char c = n;` does not compile. Write `(char) n`.

With an explicit cast, narrowing **discards all but the low 16 bits**. `66000` is `0x101D0`; the low half is `0x01D0` = 464. Negative constants are also out of range (`char c = -1;` fails); `(char) -1` is 65535.

```d2
direction: down
lit: "int literal 66000" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
fit: "0 … 65535?\nCharacter.MAX_VALUE" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
err: "char ch = 66000\ncompile error" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
ok: "(char) 66000 → 464\nlow 16 bits" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

lit -> fit
fit -> err: "no"
fit -> ok: "cast anyway"
```

**Fig. 1.** Out-of-range `int` constants are rejected on assignment. A cast wraps; it does not clamp or throw.

```java
public final class IntLiteralToChar {
    public static void main(String[] args) {
        char a = 97;          // 'a' — constant fits
        char letterB = 66;    // 'B'
        char max = 65535;     // Character.MAX_VALUE
        System.out.println(a);
        System.out.println(letterB);
        System.out.println((int) max);

        // char ch1 = 66000;  // compile error: 66000 > 65535
        // char neg = -1;     // compile error: below 0
        char wrapped = (char) 66000;  // 464
        System.out.println((int) wrapped);

        int n = 97;
        // char fromVar = n;  // compile error: not a constant
        char fromVar = (char) n;
        System.out.println(fromVar);
    }
}
```

**Listing 1.** In-range `int` constants assign to `char`. `66000` needs `(char)` and becomes 464. A non-constant `int` always needs the cast.

> [!warning] The cast does not clamp, and a variable is not a literal
> `(char) 66000` is 464, not 65535. Out of range is a **compile** error only when the cast is missing. `int n = 97; char c = n;` fails even though 97 would fit — the implicit narrowing is for constants, not for any `int` that happens to look small. `char` is unsigned: `-1` is out of range the same way `66000` is.

> [!tip] Interview answer
> **`char ch = 66000;` does not compile.** Implicit narrowing of an `int` constant into `char` is allowed only for 0…65535. Above `Character.MAX_VALUE` you need `(char)`, which keeps the low 16 bits and does not throw. A non-constant `int` always needs that cast, even if the value would fit.
