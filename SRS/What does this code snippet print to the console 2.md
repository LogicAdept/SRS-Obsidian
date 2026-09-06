<!--
reps: 0
priority: 0
-->
#Career/Interview/Exercises #Java/Lambdas #Java/FunctionalInterfaces #Java/Language/Modifiers/Final #SRS

# What does this code snippet print to the console 2?

> [!abstract] Short answer
> **`40`.** `se.get()` is what runs the lambda body. That body sets `p.age = 40` and returns `p`. The earlier `p.age = 50` is overwritten. Creating the `Supplier` at `// 1` does **not** execute the body.

## The body runs at `get()`, not at `() ->`

`p` is assigned once, so it is effectively final and legal to capture. The lambda mutates **`p.age`**, the field of that object, not the variable `p` ([[How would you explain effectively final]], [[Which variables can a Java lambda expression capture]]).

Evaluating `() -> { … }` produces a `Supplier<Person>` instance. That evaluation does not run the block ([[How would you explain lambda expressions in Java]], [[How does Supplier differ from Consumer in Java]]). After `// 1`, the lambda has not written `age`. `// 2` writes `50`. Then `se.get()` invokes `Supplier.get()`, which **does** run the body: write `40`, return the same `Person`, print `age`.

```d2
direction: down
c1: "1. Supplier created\nbody not run" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}
c2: "2. p.age = 50" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}
c3: "3. get() runs body\nage = 40; print 40" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
c1 -> c2
c2 -> c3
```

**Fig. 1.** Line numbers match the snippet. The `50` is live only until `get()`. A nearby print drill: [[What does this code snippet print to the console 3]].

```java
import java.util.function.Supplier;

class Demo {
    static class Person {
        int age;
    }

    public static void main(String[] args) {
        Person p = new Person();
        Supplier<Person> se = () -> {
            p.age = 40;
            return p;
        }; // 1
        p.age = 50; // 2
        System.out.println(se.get().age); // 3  → 40
    }
}
```

**Listing 1.** Same three steps as the prompt. `se.get()` is the only call that executes the block. A second `se.get()` would print `40` again (the body writes `40` every time).

> [!warning] Predicting `50` treats the lambda as eager
> If the body ran at `// 1`, then `// 2` would win and the console would show `50`. It does not run then. `Supplier.get()` is a later invocation. `System.out.println(se)` would print the supplier object, not `age`.

> [!warning] Reassigning `p` would not compile; mutating `p.age` does
> `p = new Person();` after the lambda makes `p` not effectively final. Writing `p.age = 40` inside the lambda is ordinary field assignment on the captured instance. Two `Person` objects would print whatever object `get()` returns — here it always returns the one `p` referred to at capture.

> [!tip] Interview answer
> **It prints `40`.** The lambda is not run when you assign `se`; `get()` runs it, sets `age` to `40`, and returns that same `Person`. The `50` is written in between and then overwritten. `p` is effectively final as a reference; the field is not frozen.
