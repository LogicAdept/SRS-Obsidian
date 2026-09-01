<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Static #SRS

# Why is the main method static in Java?

> [!abstract] Short answer
> The virtual machine **starts on a type**, not on an object: it loads and **initializes** the initial class, then **invokes** a `main` method. A **`static`** `main` can be called as `TypeName.main(...)` with **no instance**. That is why the traditional entry point is `public static void main(String[] args)`. Since **Java SE 25**, an **instance** `main` is also a legal launch candidate; the launcher then does `new InitialClass()` and calls `main` on that object. Why `static` means “no `this`”: [[What does the static keyword mean in Java]]. Class vs instance: [[What is the difference between an instance member and a static member in Java]]. Methods: [[How would you explain static methods in Java]].

## The launcher has a class, not an object

Startup is: load the initial class or interface, link it, **run class initializers**, then invoke a candidate `main` declared in or inherited by that type.

If that `main` is `static`, it is invoked **directly** (passing the `String[]` argument array when the method has that parameter). No constructor runs for the sake of launch. That matches a type that should not be constructed (private constructor, abstract class with only a static entry, or an interface with a `static` `main`).

If that `main` is an **instance** method, the launcher must first evaluate `new InitialClass()` with **no arguments**, then call `main` on the result. Construction can fail (no accessible no-arg constructor, abstract class, checked exceptions from the constructor). `static` avoids that extra object and those failure modes.

A candidate `main` has `void` result, is not `private`, and either takes `String[]` / `String...` or takes no parameters. A method with a `String[]` parameter is chosen over a no-arg `main`. You cannot declare both a `static` and an instance `main` with the **same** signature in one class.

```java
public class App {
    public static void main(String[] args) {
        System.out.println(args.length);
    }
}

class Compact {
    void main() {                 // SE 25: launcher does new Compact()
        System.out.println("hi");
    }
}
```

**Listing 1.** The usual entry is `static` and needs no instance. An instance `main` is legal at launch only if the launcher can construct the class.

```d2
direction: down
start: "VM has the initial class\n(initialized)" {
  width: 240
  height: 48
  style.fill: "#fff8e1"
}
st: "static main\ninvoke on the type" {
  width: 200
  height: 48
  style.fill: "#e3f2fd"
}
inst: "instance main\nnew C() then c.main()" {
  width: 220
  height: 48
  style.fill: "#e8f5e9"
}
start -> st
start -> inst
```

**Fig. 1.** `static` is the launch path that never asks for an object. Instance `main` adds a no-arg construction step.

> [!warning] “It must be static or the program will not compile” is false
> `main` is an ordinary method to the compiler. A non-`static` `main` compiles. What used to fail was **launch** (no candidate). As of SE 25, instance `main` can launch. Interviewers still expect `public static void main(String[] args)` as the standard form.

> [!warning] Instance `main` needs a constructible class
> The launcher uses a no-arg `new`. A private-only constructor, a missing no-arg constructor, or an abstract class will not start that way. `static` `main` still runs after class initialization alone.

> [!tip] Interview answer
> `main` is `static` so the virtual machine can call it after loading the class, without constructing an object. You get a `this` only if you `new` something inside `main` (or, since SE 25, if you use instance `main` and the launcher constructs the class for you). The conventional signature remains `public static void main(String[] args)`.
