<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Final #Java/Lambdas #SRS

# How would you explain effectively final?

> [!abstract] Short answer
> A local variable or parameter that is **not** declared `final`, but **could be**: you never reassign it (`=` / `++` / `--`), so adding `final` would not introduce a compile-time error. Lambdas and inner classes may use a surrounding local only if it is `final` or effectively final, and it is definitely assigned before the body. Instance fields have no such rule. `final` itself: [[What does the final keyword mean in Java]]. Capture set: [[Which variables can a Java lambda expression capture]]. Not a constant variable: [[What is a compile-time constant in Java]].

## Assigned once, without writing `final`

`final` means assigned at most once. **Effectively final** is the same assignment pattern **without** the keyword. Parameters (method, constructor, lambda, exception) are treated as locals that already have an initializer: any later `=` or `++`/`--` kills effectively-final status.

If the declarator **has** an initializer, the variable is effectively final when it is never on the left of `=` and never incremented or decremented. If it **lacks** an initializer, it may still be effectively final when every `=` happens while it is definitely unassigned (one assignment per path, no second write) and there is still no `++`/`--`. A lambda also needs definite assignment **before** the lambda body: an effectively final blank local that is only assigned on some paths is still illegal to capture.

Why the capture rule: the language refuses access to **dynamically changing** locals (capture would be a concurrency hazard). Dropping the need to type `final` is only clerical. The same restriction applies in an inner class. A basic `for` index is one variable that is incremented, so it is not effectively final. An enhanced-`for` loop variable is a **new** variable per iteration and is effectively final. Lambdas: [[How would you explain lambda expressions in Java]].

`try`-with-resources resources and multi-`catch` parameters are **implicitly `final`**, not merely effectively final. A uni-`catch` parameter may be effectively final. A `final` **reference** still allows mutation of the object (or array components); only the variable’s own identity is frozen.

```java
class Capture {
    int field;

    void m1(int x) {
        int y = 1;
        Runnable r = () -> System.out.println(x + y + field);
        field++; // not a local; allowed
    }

    void m2(int x) {
        int y;
        y = 1; // still effectively final: assigned once
        Runnable r = () -> System.out.println(x + y);
    }

    void m5(int x) {
        int y = 1;
        y = 2; // not effectively final
        // Runnable r = () -> System.out.println(y);
    }

    void loops(String[] arr) {
        for (String s : arr) {
            Runnable r = () -> System.out.println(s); // s is a fresh variable
        }
        for (int i = 0; i < arr.length; i++) {
            // Runnable r = () -> System.out.println(arr[i]); // i is incremented
        }
    }
}
```

**Listing 1.** Locals must be effectively final to appear in the lambda. `field` does not. Enhanced-`for` `s` does; classic `i` does not.

```java
void mutateSlot() {
    int[] box = { 0 };
    Runnable r = () -> box[0]++; // box is effectively final; the array is not frozen
    r.run();
}
```

**Listing 2.** The variable `box` is assigned once. Mutating `box[0]` does not reassign `box`. That is not a way to capture a changing **local**.

```d2
direction: down
local: "local / parameter" {
  width: 200
  height: 40
  style.fill: "#fff8e1"
}
once: "assigned once\n(no ++ / --)" {
  width: 200
  height: 44
  style.fill: "#e8f5e9"
}
ef: "effectively final\n(or declared final)" {
  width: 220
  height: 48
  style.fill: "#e8f5e9"
}
cap: "lambda / inner class may read it" {
  width: 260
  height: 44
  style.fill: "#e3f2fd"
}
no: "reassigned → cannot capture" {
  width: 240
  height: 44
  style.fill: "#ffcdd2"
}
local -> once -> ef -> cap
local -> no: "second = or ++"
```

**Fig. 1.** Effectively final is an assignment property of the **variable**, not of the object it refers to.

> [!warning] Stale-copy folklore is not the rule
> The compiler does not “let you capture a snapshot, then complain it would go stale.” It **forbids** capturing a local that is assigned more than once. Implementation details (inlining a captured local) are not a license to reassign. `x++` after the lambda still makes the lambda illegal even if the increment is “later.”

> [!warning] Mutating a referent is not reassigning the local
> `list.add(...)`, `array[0] = …`, or `atomic.incrementAndGet()` keep the **variable** effectively final. That does not make the one-element array a supported “mutable local.” Instance fields can change under a lambda with no effectively-final check at all.

> [!tip] Interview answer
> Effectively final means a local or parameter is not declared final but is never reassigned, so you could add final and still compile. A lambda or inner class can use that local only then, and only if it is definitely assigned first. Fields are unrestricted. An enhanced-for variable is effectively final; a classic for index is not.
