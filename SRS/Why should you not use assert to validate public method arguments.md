<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #Java/Exceptions/Unchecked #Java/Exceptions/Error #SRS

# Why should you not use `assert` to validate public method arguments?

> [!abstract] Short answer
> **Public argument checks are part of the method’s contract and must run even when assertions are disabled.** `assert` is off by default (`-ea` to enable). A failed assert throws `AssertionError`, not `IllegalArgumentException` or `NullPointerException`. It is not illegal — `javac` still accepts it — but it is generally inappropriate.

## The contract must hold without `-ea`

A disabled `assert` does **nothing**. Callers of a public method cannot know whether the library’s JVM was started with `-ea`. The published precondition (non-null, range, and so on) still has to be enforced ([[What happens when a Java assert statement fails]], [[What does Objects.requireNonNull do]]).

A failed assertion throws `AssertionError` (`Error`), not the exception the API documents. Public failures should be `IllegalArgumentException`, `NullPointerException`, or `IndexOutOfBoundsException` ([[Should you throw NullPointerException or IllegalArgumentException for a null argument]], [[What is the difference between IllegalArgumentException and IllegalStateException]], [[Is AssertionError a subclass of Exception]], [[Should you catch AssertionError]]).

`public static void main(String[] args)` is a public method. Do not `assert args.length > 0`; throw or handle like any other public argument.

**Nonpublic** helpers may `assert` preconditions you believe always hold if clients only use the public API. That documents an internal invariant, not the published contract.

```d2
direction: down
pub: "public method argument" {
  width: 280
  height: 50
}
iae: "if (...) throw IAE / NPE\n(always runs)" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
as: "assert cond\n(off unless -ea)" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
pub -> iae
pub -> as
```

**Fig. 1.** Public preconditions must not depend on assertion status.

```java
class Demo {
    static void setRate(int rate) {
        if (rate <= 0) {
            throw new IllegalArgumentException("rate");
        }
    }

    private static void helper(int interval) {
        assert interval > 0 : interval;
    }
}
```

**Listing 1.** `setRate` always rejects a bad public argument. `helper` may assert an internal precondition. `assert rate > 0` inside `setRate` would vanish in production without `-ea`, and a failure would be `AssertionError`, not `IllegalArgumentException`.

> [!warning] Inappropriate ≠ a compile error
> `assert` on public parameters compiles. The check simply may never run, and the throw type is wrong for the API.

> [!warning] `AssertionError` is not an `IllegalArgumentException`
> Clients catching IAE will miss it. `AssertionError` is an `Error` and is not meant to be caught ([[Should you catch AssertionError]]).

> [!tip] Interview answer
> **Do not `assert` public method arguments because the contract must hold whether assertions are on or off, and a failure must be IAE or NPE, not `AssertionError`.** Assertions default to off. Private helpers may assert internal preconditions. `main`’s `args` are public arguments too.
