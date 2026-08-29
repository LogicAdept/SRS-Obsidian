<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS

# What did Java 14 change about `NullPointerException` messages?

> [!abstract] Short answer
> **The JVM can attach a null-detail message that names the expression that was `null`.** Instead of a bare `NullPointerException` plus a line number, you can see text such as `Cannot invoke "String.length()" because "s" is null`. That does **not** change *when* NPE is thrown — only what `getMessage()` can say.

## Bytecode analysis, not a new throw site

Before Java 14, a JVM-generated NPE usually had **no** detail message: only the stack frame (method, file, line). On a line with several dereferences (`a.b.c.i = 99`), that line number does not tell you whether `a`, `b`, or `c` was null ([[What is NullPointerException]]).

From Java 14, the JVM can walk the bytecode that popped `null` and build a two-part message: what could not be done, and which access path was null. Examples from that design:

- `Cannot assign field "i" because "a" is null`
- `Cannot read field "c" because "a.b" is null`
- `Cannot invoke "String.length()" because "s" is null`

`NullPointerException.getMessage()` computes that text on demand when no constructor message was supplied. The extra detail is **off** unless the HotSpot flag `-XX:+ShowCodeDetailsInExceptionMessages` is on. In Java 14 the flag defaulted to **off**; from Java 15 it is **on** by default (still on in current JDKs). `-XX:-ShowCodeDetailsInExceptionMessages` turns it off.

```d2
direction: down
npe: "JVM throws NPE\n(same moment as before)" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
old: "line number only" {
  width: 280
  height: 50
  style.fill: "#eceff1"
}
neu: "Cannot invoke \"String.length()\"\nbecause \"s\" is null" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}
npe -> old
npe -> neu
```

**Fig. 1.** Helpful messages diagnose the consumer of `null`. They do not move the throw.

```java
class Demo {
    static int len(String s) {
        return s.length();
    }

    static void explicit() {
        throw new NullPointerException("my message");
    }
}
```

**Listing 1.** `len(null)` is a JVM-raised NPE and can get a null-detail message. `explicit` is not analyzed: you supplied the message. Unboxing a null wrapper is still NPE at the same point; the message may mention `intValue()` rather than “unbox” ([[How do you avoid NullPointerException when unboxing a Map value]], [[What happens when a ternary operator unboxes a null Integer in Java]]).

Only NPEs **created and thrown by the JVM** get this analysis. `throw new NullPointerException()` and `Objects.requireNonNull` (which constructs the exception in Java code) do not ([[Should you throw NullPointerException or IllegalArgumentException for a null argument]], [[How do you prevent a NullPointerException]]).

> [!warning] Serialization drops the verbose text
> The detail is rebuilt from internal JVM state. After deserialize (for example RMI), that state is gone, so `getMessage()` may be `null` again. Method redefinition can also discard the original bytecode needed for the message.

> [!warning] The flag can leak source-shaped names
> With debug info (`javac -g`), local variable names appear in the message. That can show up in logs or HTTP error pages. Java 15’s default-on change called this out: disable the flag if those snippets must not leave the process.

> [!tip] Interview answer
> **Java 14 added helpful NPE messages that name which expression was null, via bytecode analysis.** They do not change when NPE is thrown. The feature is `-XX:+ShowCodeDetailsInExceptionMessages` (off by default in 14, on from 15). `new NullPointerException(...)` and deserialized NPEs do not get that JVM text.
