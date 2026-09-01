<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives/Conversions #Career/Interview/Exercises #SRS

# What happens when this primitive assignment snippet runs?

> [!abstract] Short answer
> **It does not run: `c = b` fails to compile.** `byte` → `char` is not a widening assignment. After `s = b` the first print is `1`; `'a' - 2` is `95`. The dump’s last line `1.0` is what you get only after an explicit `(char) b`, which then widens through `int` into `double`.

## The dump’s trace, with the illegal line called out

```java
byte b = 1;
int i = 3;
char c = 'a';
short s = 0;
double d = 4d;

s = b;                      // widening; s is 1
System.out.println(s);      // 1
System.out.println(c - 2);  // 95  ('a' is 97; both operands become int)
c = b;                      // compile error: byte → char
i = c;
d = i;
System.out.println(d);
```

**Listing 1.** Dump snippet. Conceptual — `c = b` is not assignment-convertible. (Not a complete compilation unit.)

`byte` widens to `short`, `int`, `long`, `float`, or `double` — not to `char`. `byte` → `char` is a **widening-and-narrowing** conversion: `char` is 16-bit unsigned, `byte` is signed. Assignment will not do that silently unless the right-hand side is a **constant** that fits. `b` is a variable, so you need `(char) b` ([[How would you explain widening and narrowing casts between Java primitive types]]).

`c - 2` is a numeric operator, not an assignment. `char` and `int` are promoted to `int`; `'a'` is 97, so the print is `95` — an `int`, not a `char`.

If you insert the cast, the rest of the dump is ordinary widening: `(char) 1` is `'\u0001'`, `i = c` copies 1, `d = i` is `1.0` ([[Can a byte be assigned to a double without a cast in Java]]). The leftover `4d` is overwritten.

```d2
direction: down
ok1: "byte → short" {
  width: 140
  height: 40
  style.fill: "#e8f5e9"
}
ok2: "char - int → int 95" {
  width: 180
  height: 40
  style.fill: "#e8f5e9"
}
bad: "byte → char" {
  width: 140
  height: 40
  style.fill: "#ffebee"
}
cast: "(char) then → int → double" {
  width: 240
  height: 40
}

ok1 -> ok2: "prints 1 then 95"
ok2 -> bad: "assignment"
bad -> cast: "needs a cast"
```

**Fig. 1.** Two prints are real. The assignment `c = b` is the stop.

```java
public final class LineByLinePrimitives {
    public static void main(String[] args) {
        byte b = 1;
        int i = 3;
        char c = 'a';
        short s = 0;
        double d = 4d;

        s = b;
        System.out.println(s);           // 1
        System.out.println(c - 2);       // 95
        c = (char) b;
        i = c;
        d = i;
        System.out.println(d);           // 1.0
    }
}
```

**Listing 2.** Same trace as the dump after the required cast. `c = b` without `(char)` does not compile.

> [!warning] “Smaller type into bigger type” fails for `byte` → `char`
> `char` is not a wider **signed** integer; it is unsigned 16-bit. A non-constant `byte` needs a cast. A constant `byte`/`int` that fits can narrow into `char` without a cast (`char ch = 1`), which is a different rule ([[Why does assigning 128 to a byte without a cast fail to compile]]).

> [!tip] Interview answer
> **Compile error at `c = b`.** Before that, `s` prints `1` and `'a' - 2` prints `95`. With `(char) b`, `c` becomes code point 1, then `i` and `d` become `1` and `1.0`. Do not recite the dump as if the raw snippet ran.
