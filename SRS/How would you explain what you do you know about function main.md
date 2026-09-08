<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Static #SRS

# How would you explain what you do you know about function main?

> [!abstract] Short answer
> `main` is the **launch** method, not a compiler-required member. The usual declaration is `public static void main(String[] args)`. A project may have **many** classes with a `main`; `java com.example.App` chooses **one** initial type. A class **without** `main` **compiles**. Launch then fails. HotSpot prints `Error: Main method not found in class …, please define the main method as: public static void main(String[] args)`. Full launcher rules: [[How would you explain the Java main method entry point]]. Why `static`: [[Why is the main method static in Java]].

## What interviewers mean by “the `main` function”

It is a **method** named `main`, not a free function. After the initial class is loaded, linked, and initialized, the VM invokes a **candidate** `main` ([[How would you explain static methods in Java]]). Command-line tokens after the class name become the `String[]` (empty array if you passed none). `-jar` reads `Main-Class` from the manifest instead of a class name on the command line.

Several `main` methods in one application are normal: each type you might start has its own. That is not “one process, many entries at once.” One `java` invocation still starts **one** initial class. Inside that class, a `String[]` candidate is chosen over a no-arg `main` if both exist.

A missing candidate is **not** a javac error. Libraries ship without `main`. The launcher message is implementation text; JLS only says execution fails if there is no candidate. Uncaught exceptions from `main` go to the virtual machine ([[Can method main throw exception and if yes where will happens exception]]). `args` is still pass-by-value ([[Does Java pass arguments by reference or by value]]).

```d2
direction: down
src: "javac SomeClass.java\nno main required" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
run: "java SomeClass\nneeds a candidate main" {
  width: 260
  height: 55
  style.fill: "#fff3e0"
}
miss: "HotSpot: Main method not found" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}
src -> run
run -> miss: "none"
```

**Fig. 1.** Compilation and launch are different checks. `main` belongs to launch.

```java
public class App {
    public static void main(String[] args) {
        System.out.println(args.length);
    }
}

class Tools {
    public static void main(String[] args) { // another entry in the same app
        System.out.println("tools");
    }
}

// class Lib {}  // compiles; java Lib fails at launch
```

**Listing 1.** Everyday entry plus a second `main` on another class. `java App` does not run `Tools.main`.

From **Java SE 25** a candidate may be instance, no-arg, `protected`, or package-private — not `private`. Interview default remains `public static void main(String[] args)` ([[How would you explain method signatures in Java]]). Compact source can be just `void main() { … }`.

> [!warning] The dump truncates the launcher line
> The phrase is not only `` `Error: Main method not found` ``. OpenJDK’s `java` prints that the method was not found **in that class**, then shows `public static void main(String[] args)`, and mentions JavaFX. A different error is `Could not find or load main class` — wrong name or classpath, not a missing method. Instance `main` can instead fail on a missing no-arg constructor.

> [!warning] “No `main` means it will not compile” is false
> `javac` accepts ordinary classes with no entry point. Failure is `java` (or an IDE run configuration) choosing a type that has no candidate. Several `main` methods do not confuse the compiler; they confuse **you** if the run config points at the wrong class.

> [!tip] Interview answer
> **`main` is the JVM entry: `public static void main(String[] args)` on the class you name to `java`.** Many classes may each have a `main`; only the launched one runs. Missing `main` still compiles. At run you get a launcher error that the method was not found, not a javac error.
