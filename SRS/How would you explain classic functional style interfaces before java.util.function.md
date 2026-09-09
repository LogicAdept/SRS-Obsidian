<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #SRS

# How would you explain classic functional style interfaces before java.util.function

> [!abstract] Short answer
> **Before Java 8, functional-style behavior traveled as single-abstract-method (SAM) interfaces used with anonymous inner classes: `Runnable`, `Callable<V>`, `Comparator<T>`, `Comparable<T>`, event listeners like `ActionListener`.** Java 8 did not invent the pattern — it added lambdas, method references, and `java.util.function` to make it cheap, and retrofitted the existing interfaces with `@FunctionalInterface` and default methods.

## The pre-lambda SAM family

Each of these encodes one behavior behind one method, years before lambdas existed: `Runnable.run()` (a task, no result), `Callable<V>.call()` (a task with a result and exceptions — the concurrency sibling of Runnable), `Comparator<T>.compare(T,T)` (external ordering strategy), `Comparable<T>.compareTo(T)` (internal, natural ordering), and GUI listeners like `ActionListener.actionPerformed(ActionEvent)` (a reaction to an event).

```d2
direction: right
old: "Pre-Java 8\nclass implements SAM\nanonymous inner class" {
  width: 320
  height: 100
  style.fill: "#e3f2fd"
}
new: "Java 8+\nlambda or method reference\nsame interface as target" {
  width: 320
  height: 100
  style.fill: "#e8f5e9"
}
old2: "6+ lines of boilerplate\nper usage site" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}
new2: "One line\nsame behavior, same API" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
old -> old2
new -> new2
```

**Fig. 1.** Java 8 changed the *syntax of supplying* the behavior, not the behavior-carrying mechanism — the SAM interface stays the target type.

```java
Runnable oldStyle = new Runnable() {
    @Override
    public void run() {
        System.out.println("anonymous class task");
    }
};
Runnable newStyle = () -> System.out.println("lambda task");

List<String> names = new ArrayList<>(List.of("Kathy", "Ann", "Bob"));
names.sort(new Comparator<String>() {
    @Override
    public int compare(String a, String b) { return a.length() - b.length(); }
});
names.sort(Comparator.comparingInt(String::length));   // Java 8 helper API
```

**Listing 1.** The same two behaviors, before and after Java 8 — the interface (`Runnable`, `Comparator`) is unchanged; only how you hand over the implementation differs. (Comparator's `comparingInt` helper is itself a default/static method added in Java 8.)

> [!warning] "Lambda replaced anonymous classes" is only true for interfaces
> The boundaries of the story. First, lambdas only target *functional interfaces* — a lambda cannot implement an abstract class or an interface with two abstract methods; anonymous classes remain the tool there. Second, the pre-8 interfaces are NOT part of `java.util.function` and never moved: `Runnable`, `Callable`, `Comparator` live in `java.lang`/`java.util` and are still the right types for their domains — `java.util.function` added the *generic* shapes (`Function`, `Predicate`, `Consumer`, `Supplier`) for user code. Third, subtle runtime differences survive: `this` inside a lambda refers to the enclosing instance (not the lambda, as it does inside an anonymous class), and anonymous classes create a new class file per site while lambdas use `invokedynamic`. The SAM rule that unifies both eras: [[How would you explain requirements for a Java functional interface]]; the standard shapes that arrived with Java 8: [[What are the main functional interfaces in java.util.function]].

> [!tip] Interview answer
> **Functional style existed long before Java 8 through SAM interfaces: Runnable, Callable, Comparator, Comparable, event listeners — filled with anonymous inner classes. Java 8 made supplying the behavior one line via lambdas and method references, added @FunctionalInterface, default methods and the generic java.util.function shapes. The old interfaces stayed where they were — they are still functional interfaces today.**

