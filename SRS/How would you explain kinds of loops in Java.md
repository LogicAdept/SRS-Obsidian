<!--
reps: 0
priority: 0
-->
#Java/Language/Loops #SRS

# How would you explain kinds of loops in Java?

> [!abstract] Short answer
> Java has **three** iteration statements: `while`, `do`, and `for`. `for` itself has **two** forms — basic (`init; condition; update`) and enhanced (for-each over an array or `Iterable`). That is four syntactic shapes, not four statement kinds. Choose by **when** the condition runs and whether you need an **index** or only **elements**.

## The map

```d2
direction: down
stmts: "Iteration statements" {
  width: 280
  height: 50
  style.fill: "#eceff1"
}
while_: "while\npre-test, 0..n" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
do_: "do-while\npost-test, 1..n" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
for_: "for (two forms)" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
basic: "basic for\ninit + pre-test + update" {
  width: 240
  height: 70
  style.fill: "#c8e6c9"
}
each: "enhanced for\narray or Iterable" {
  width: 240
  height: 70
  style.fill: "#a5d6a7"
}
stmts -> while_
stmts -> do_
stmts -> for_
for_ -> basic
for_ -> each
```

**Fig. 1.** Three statements. `for` splits into a counted header and a for-each header. Infinite loops are a **use** of `while (true)` or `for (;;)`, not a fifth kind.

`continue` is legal only in these iteration statements. `break` can also leave a `switch`. None of that adds a new loop kind.

Mechanics of the three condition-test forms: [[How do Java for, while, and do-while loops differ]].

## `while` — unknown count, test first

Use when the number of trips is not a range you can write in a header: read until sentinel, wait for a flag, walk an `Iterator` by hand. The body may run zero times. The increment, if any, lives in the body, so `continue` skips it unless you increment before `continue`.

## `do` — at least once, test last

Use when the first pass is required even if the later test would already be false (emit at least one digit, show a prompt once). If the `do` statement is reached, the body runs at least once. It is the **only** post-test loop.

## Basic `for` — index, range, or compact header

Use when you own initialization, a pre-test, and an update: `for (int i = 0; i < n; i++)`. All three slots are optional. A missing condition is “true until `break`.” A variable declared in the header is not in scope after the loop. Prefer this when you need the **index**, two sequences in lockstep, or a non-`Iterable` countdown.

## Enhanced `for` — elements only

Use when the source is an array or a subtype of `Iterable` and each trip needs the **element**, not the index. The language translates it into a basic `for` over `iterator()` / `hasNext()` / `next()`, or over `0 .. length` for arrays. The loop variable is a **fresh local** each trip (`x = #a[i]` or `x = it.next()`), so assigning to `x` does not write the array or the collection. The iterator itself is a generated name; you cannot call `remove()` on it.

Details: [[How would you explain the enhanced for each loop in Java]], [[What language feature enables the enhanced for each loop]], [[What must a class implement to support enhanced for each iteration]].

```java
class LoopKinds {
    static int sumWhile(int n) {
        int s = 0, i = 1;
        while (i <= n) {
            s += i;
            i++;
        }
        return s;
    }

    static String atLeastOneDigit(int i) {
        StringBuilder buf = new StringBuilder();
        do {
            buf.append(Character.forDigit(i & 0xF, 16));
            i >>>= 4;
        } while (i != 0);
        return buf.reverse().toString();
    }

    static int sumIndexed(int[] a) {
        int s = 0;
        for (int i = 0; i < a.length; i++) {
            s += a[i];
        }
        return s;
    }

    static int sumEach(int[] a) {
        int s = 0;
        for (int x : a) {
            s += x;
        }
        return s;
    }

    public static void main(String[] args) {
        int[] a = {1, 2, 3};
        System.out.println(sumWhile(3));         // 6
        System.out.println(atLeastOneDigit(0));  // 0
        System.out.println(sumIndexed(a));       // 6
        System.out.println(sumEach(a));          // 6
    }
}
```

**Listing 1.** Four shapes, same language: two `for` forms, plus `while` and `do`. `atLeastOneDigit(0)` still produces `"0"` because `do` is post-test.

A handwritten `while (it.hasNext()) { it.next(); }` is still a `while`. It is the pattern enhanced `for` desugars to, not a separate statement.

> [!warning] For-each is not a drop-in for every `for`
> You still need a basic `for` (or a `while`) when you need the index, a reverse walk, two arrays in lockstep, or an iterator you can `remove()` from. `x = 0` in `for (int x : a)` does not write `a`. Mutation of a collection during for-each is a separate contract: [[Can you modify a collection while iterating with a for-each loop]].

> [!warning] Do not invent a fifth kind
> `while (true)` and `for (;;)` are infinite **uses** of existing statements. Labeled `break`/`continue` change which loop they affect, they do not add a kind. A `boolean`/`Boolean` condition is required when the condition is present; `while (1)` does not compile.

> [!tip] Interview answer
> **Three iteration statements: `while`, `do-while`, and `for`; `for` has a basic header and an enhanced for-each over arrays or `Iterable`.** `while` and basic `for` test first and may run zero times; `do-while` tests last and runs at least once. Pick enhanced `for` for elements, basic `for` when you need the index or the update.
