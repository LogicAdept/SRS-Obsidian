<!--
reps: 0
priority: 0
-->
#Career/Interview/Exercises #Java/Collections/List/Vector #Java/Language/Parameters #SRS

# What does this code snippet print to the console?

> [!abstract] Short answer
> **`[100] []`** — `push` mutates the stack `s1` points to; `x2 = x1` only rebinds the **parameter** `x2`, so `s2` stays empty.

## Trace

`Stack()` starts empty. `processStacks` receives **copies of the two references**. `x1.push(...)` is `Vector.addElement` on that shared `s1` object, so `s1` holds `Integer` 100. `x2 = x1` makes the local `x2` point at `s1`'s stack; `s2` is never assigned.

`println(s1 + " " + s2)` converts each stack with `Vector.toString`, which delegates to the collection format: elements in iterator order, square brackets, comma-space between items. One element whose `toString` is `100`, plus an empty stack, with a space between the two conversions.

```java
import java.util.Stack;

public class Snippet1 {
    public static void main(String[] args) {
        Stack s1 = new Stack();
        Stack s2 = new Stack();
        processStacks(s1, s2);
        System.out.println(s1 + " " + s2);
    }

    public static void processStacks(Stack x1, Stack x2) {
        x1.push(new Integer("100"));
        x2 = x1;
    }
}
```

**Listing 1.** Interview snippet (raw `Stack`, deprecated `Integer(String)`). Output is `[100] []` ([[Does Java pass arguments by reference or by value]], [[What does pass by value mean for Java parameters]]).

```d2
direction: right
s1: "s1 → Stack\nafter push: [100]" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
s2: "s2 → Stack\nstill empty: []" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
x2: "x2 after x2=x1\nnow points at s1's stack" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
x2 -> s1
```

**Fig. 1.** Mutation follows the copied pointer. Rebinding `x2` does not retarget `s2`.

The other common picks fail for one reason each: `[] []` ignores `push`; `[100] [100]` treats `x2 = x1` as pass-by-reference into `s2`; `[] [100]` swaps which stack was mutated. `java.util.Stack` is a `Vector` subclass; prefer `Deque` / `ArrayDeque` in new code ([[Why is java.util.Stack discouraged and what should you use instead]], [[How are parameters passed in Java]]).

> [!warning] `[100] [100]` is the pass-by-reference trap
> `x2 = x1` never writes the caller's `s2`. If the method did `x2.push(100)` *before* reassigning `x2`, `s2` would change; after `x2 = x1`, further `x2.push` would hit `s1`'s stack instead. This snippet pushes only on `x1`.

> [!tip] Interview answer
> It prints `[100] []`. `push` changes the object `s1` and `x1` both point to. Assigning `x2 = x1` only updates the method's copy of the reference, so `s2` is still empty. Collection `toString` is `[elements]`, which is why you see those brackets.
