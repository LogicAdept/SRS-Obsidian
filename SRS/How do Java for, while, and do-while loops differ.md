<!--
reps: 0
priority: 0
-->
#Java/Language/Loops #SRS

# How do Java for, while, and do-while loops differ?

> [!abstract] Short answer
> `while` evaluates a `boolean`/`Boolean` condition **before** the body, so the body may run **zero** times. `do`-`while` runs the body **first**, then tests, so if the statement is reached the body runs **at least once**. Basic `for` is a pre-test loop that also owns a one-shot `ForInit` and a post-body `ForUpdate`; omit the condition and it repeats until `break`.

## When the test runs

```d2
direction: right
while_: "while\ntest → body" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
do_: "do-while\nbody → test" {
  width: 200
  height: 80
  style.fill: "#fff3e0"
}
for_: "for\ninit; test → body → update" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Same iteration idea; the difference is **when** the condition runs and whether `for` owns init and update.

When a condition is present, it must be `boolean` or `Boolean`. An `int` such as `while (1)` is a compile-time error. A `Boolean` that is `null` fails on unboxing with `NullPointerException`. Basic `for` may omit the condition; that is not a `while (1)` substitute, it is “always true until `break`.”

## `while`: test, then body

A `while` statement evaluates the expression first. If that value is `false` the first time, the body is not executed. If it is `true`, the body runs; when the body completes normally, the whole `while` starts again at the test. `while (true) { ... }` is the explicit infinite form.

```java
class WhileDemo {
    public static void main(String[] args) {
        int count = 1;
        while (count < 11) {
            System.out.println("Count is: " + count);
            count++;
        }
    }
}
```

**Listing 1.** Prints `Count is: 1` through `10`. If `count` started at `11`, the body would not run.

`continue` in a `while` jumps back to the test. If the increment lives only in the body, `continue` skips it and can spin forever.

## `do`: body, then test

A `do` statement executes the body first, then evaluates the condition. Once the statement is entered, the body runs at least once — even when the condition is already `false`. That is the right shape when the first pass is required: at least one hex digit, at least one read of a prompt, and similar.

```java
class HexOnce {
    static String toHexString(int i) {
        StringBuilder buf = new StringBuilder(8);
        do {
            buf.append(Character.forDigit(i & 0xF, 16));
            i >>>= 4;
        } while (i != 0);
        return buf.reverse().toString();
    }

    public static void main(String[] args) {
        System.out.println(toHexString(0));
        System.out.println(toHexString(255));
    }
}
```

**Listing 2.** `toHexString(0)` still appends `'0'` because `do` runs before the test. A `while (i != 0)` here would return empty for `0`. Output: `0` then `ff`.

`continue` in a `do` evaluates the condition next (it does not skip that test). The semicolon after `while (expression)` belongs to `do`; see the warning below for the empty-`while` trap.

## Basic `for`: init, test, body, update

A basic `for` runs `ForInit` **once** (a local-variable declaration or a list of statement expressions), then each iteration: evaluate the condition, run the body, run `ForUpdate`. Each of the three header slots may be omitted. A missing condition behaves as `true`; the loop can then complete normally only with `break`.

If the condition is `false` the first time it is evaluated, the body is skipped — but `ForInit` has already run. A variable declared in `ForInit` is in scope for the condition, the update, and the body, and not after the statement.

```java
class ForDemo {
    public static void main(String[] args) {
        for (int i = 1; i < 11; i++) {
            System.out.println("Count is: " + i);
        }
        // i is not in scope here

        int seeded = 0;
        for (seeded = 99; seeded < 0; seeded++) {
            seeded = -1;
        }
        System.out.println(seeded); // 99: init ran, body did not

        for (;;) {
            break;
        }
    }
}
```

**Listing 3.** Header `int i` dies with the loop. `for (;;)` is infinite until `break`. `ForInit` still runs when the first test is `false`.

`continue` in a `for` still executes `ForUpdate`, then the next test. That is **not** the same as a `while` whose increment sits at the bottom of the body: rewriting a `for` that way, then using `continue`, skips the increment and can loop forever.

```java
class ContinueFor {
    public static void main(String[] args) {
        for (int i = 0; i < 3; i++) {
            if (i == 1) {
                continue;
            }
            System.out.print(i);
        }
    }
}
```

**Listing 4.** Prints `02`. The update `i++` still ran when `i == 1`.

`for` also has an enhanced for-each form over an array or `Iterable`. That is translation into a basic `for` plus an iterator or index, not a fourth condition-test style: [[How would you explain the enhanced for each loop in Java]], [[What language feature enables the enhanced for each loop]]. Catalog of loop kinds: [[How would you explain kinds of loops in Java]].

## Constant-`false` body

If a `while` or basic `for` condition is the constant `false`, the body is unreachable and compilation fails. A `do` body is reachable whenever the `do` statement is, so `do { x = 3; } while (false);` is legal and assigns once. `if (false) { x = 3; }` is also legal (conditional compilation). Do not treat `if` and `while` as the same reachability rule.

```java
class DoFalse {
    public static void main(String[] args) {
        int x;
        do {
            x = 3;
        } while (false);
        System.out.println(x);
        // while (false) { x = 3; }     // compile-time error: unreachable
        // for (; false; ) { x = 3; }   // compile-time error: unreachable
    }
}
```

**Listing 5.** Compiles and prints `3`. Uncomment either commented loop and `javac` rejects the body.

> [!warning] `do` is not a `while` written backwards
> If the condition is already `false`, `while` and `for` skip the body; `do` still runs it. Empty input, a failed precondition, and “retry until success” that should no-op are the usual misuses. `toHexString(0)` in Listing 2 is the case where that extra run is the point.

> [!warning] A semicolon can eat the loop
> `while (n-- > 0);` and `for (int i = 0; i < n; i++);` are loops whose body is the empty statement. The next block is not the loop body. `do { ... } while (n > 0);` **does** need that semicolon; the other two usually do not.

> [!tip] Interview answer
> **`while` tests before the body and may run zero times; `do-while` runs the body first, so it always runs at least once; basic `for` is a pre-test loop that also owns initialization and update.** `continue` in `for` still executes the update. `while (false) { ... }` does not compile; `do { ... } while (false);` does.
