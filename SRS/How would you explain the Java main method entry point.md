<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Static #SRS

# How would you explain the Java main method entry point?

> [!abstract] Short answer
> The virtual machine **starts a program** by invoking a **candidate `main`** on a specified class or interface, after that type is loaded, linked, and **initialized**. The everyday form is `public static void main(String[] args)`: `args` is the command-line strings after the class name. From **Java SE 25** a candidate may also be an **instance** method, take **no** parameters, and be package-private or `protected` — not `private`. Why `static`: [[Why is the main method static in Java]].

## Launch is load → link → initialize → invoke `main`

Startup is not “the compiler looks for `main`.” A class **without** `main` **compiles**. Launch fails if the initial type has **no candidate** (the implementation then reports something like a missing main method; that wording is a launcher message, not a compile error).

Command line `java Test reboot Bob` typically loads `Test`, then calls a `main` with `args` `{ "reboot", "Bob" }`. Compact source `void main() { … }` in `HelloWorld.java` launches the **implicitly declared** class named from the file.

A method is a **candidate** `main` when it has a `void` result, is not `private`, and either:

- has one parameter of type `String[]` (written `String[]` or `String...`), or
- has **no** parameters.

It may be `static` or instance, and it may declare `throws`. If **both** a `String[]` candidate and a no-arg candidate exist, the launcher **invokes the `String[]` form**. `static` `main` is invoked on the type. Instance `main` is `new InitialClass()` with no arguments, then `main` on that object. You cannot declare both a `static` and an instance `main` with the **same** signature in one class ([[How would you explain method signatures in Java]], [[How would you explain static methods in Java]]). Inherited methods count: a `default void main()` on an interface can be the candidate of an implementing class.

```d2
direction: down
load: "load the initial class" {
  width: 240
  height: 45
  style.fill: "#fff8e1"
}
link: "link: verify, prepare" {
  width: 240
  height: 45
  style.fill: "#fff3e0"
}
init: "initialize\nstatic initializers" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
run: "invoke candidate main\nString[] preferred over no-arg" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
load -> link
link -> init
init -> run
```

**Fig. 1.** Class initialization (including the superclass chain) finishes **before** `main` runs. `main` is not a special compilation rule.

```java
public class App {
    public static void main(String[] args) {
        System.out.println(args.length);
    }
}

class Compact {
    void main() { // SE 25: launcher does new Compact(), then main()
        System.out.println("hi");
    }
}

interface Entry {
    default void main(String... args) {} // inherited candidate
}
```

**Listing 1.** Interview default remains `public static void main(String[] args)`. SE 25 also launches instance / no-arg / non-`public` (non-`private`) candidates. `String...` is the same parameter type as `String[]`.

Before SE 25 the only launch shape was `public static` with a single `String[]` / `String...` parameter. `throws` on `main` has always been allowed; an uncaught exception ends the **main thread** and is handled by the virtual machine ([[Can method main throw exception and if yes where will happens exception]]). Parameters are still pass-by-value: `args` is a copied reference to the array ([[Does Java pass arguments by reference or by value]]).

> [!warning] No `main` is a launch failure, not a javac error
> Libraries compile without `main`. `java SomeClass` then fails because there is no candidate. Several classes in one application may each have a `main`; the **command** chooses the initial class. The dump phrase “the program will not compile without `main`” is false.

> [!warning] SE 25 relaxed the launcher, not the interview default
> `protected` / package-private `main` can launch. `private main` cannot. Instance `main` needs an accessible no-arg constructor. Prefer `public static void main(String[] args)` unless the question is explicitly about compact source or SE 25. A `String[]` candidate wins over a no-arg `main` in the same type.

> [!tip] Interview answer
> **The JVM loads the named class, initializes it, then calls `main`. The form everyone still writes is `public static void main(String[] args)` so it can run with no instance and receive command-line strings.** Missing `main` does not fail compilation. Java 25 also accepts instance and no-arg candidates; `String[]` is chosen if both exist.
