<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Collections/Iteration #SRS

# Which functional interface does `Iterable.forEach` use?

> [!abstract] Short answer
> **`java.util.function.Consumer<? super T>`.** `Iterable<T>.forEach` takes that consumer and calls `accept` on each element. `Consumer` is a Java 8 functional interface: one abstract method `void accept(T t)`, expected to work by side effects. The default body is enhanced `for` over `this`. `Map.forEach` is **`BiConsumer`**, not `Consumer`.

## `Consumer.accept`, not a second loop API

`default void forEach(Consumer<? super T> action)` has been on `Iterable` since Java 8. A `null` action is rejected (`NullPointerException`). The default implementation is specified as:

`for (T t : this) action.accept(t);`

So it still goes through `iterator()` (or an override that does not). Overriding `forEach` does **not** change enhanced `for` [[What is the Iterable interface in Java]], [[How are Iterable Iterator and for-each related in Java]], [[What language feature enables the enhanced for each loop]].

`Consumer<T>`’s functional method is `accept`. Lambdas and method references (`System.out::println`) work because it is `@FunctionalInterface`. `andThen` composes two consumers; `forEach` does not call `andThen` for you [[How would you explain Consumer DoubleConsumer IntConsumer and LongConsumer]], [[How does Supplier differ from Consumer in Java]].

`? super T` is PECS: a `Consumer<Object>` can accept `String` elements. Primitive specializations (`IntConsumer`, …) are for primitive streams, not `Iterable.forEach`.

**Same `Consumer`, different type:** `Iterator.forEachRemaining(Consumer)` drains **that cursor**. `Collection` inherits `Iterable.forEach` unless a concrete class overrides it.

**Not `Consumer`:** `Map.forEach` is `BiConsumer<? super K, ? super V>` — `(k, v) -> …` [[How would you explain the BiConsumer functional interface]]. Passing a one-arg `Consumer` to a `Map` does not compile. Walk `keySet()` / `values()` / `entrySet()` if you want `Iterable.forEach`.

```d2
direction: down
itb: "Iterable<T>\nforEach" {
  width: 200
  height: 55
  style.fill: "#e3f2fd"
}
con: "Consumer<? super T>" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
acc: "accept(t)" {
  width: 150
  height: 40
}
map: "Map.forEach" {
  width: 160
  height: 45
}
bi: "BiConsumer<K,V>" {
  width: 200
  height: 45
  style.fill: "#ffebee"
}

itb -> con -> acc
map -> bi
```

**Fig. 1.** `Iterable.forEach` is one argument per element. `Map.forEach` is key **and** value.

```java
static void printAll(java.lang.Iterable<String> source) {
    java.util.function.Consumer<String> printer = s -> System.out.println(s);
    source.forEach(printer);
    source.forEach(System.out::println);
}
```

**Listing 1.** Both arguments are `Consumer<? super String>`. `Map` would need `(k, v) -> …` instead.

> [!warning] `Map.forEach` is `BiConsumer`
> `map.forEach(e -> …)` does not compile. Use `map.forEach((k, v) -> …)` or `map.entrySet().forEach(...)`. Do not treat “forEach” as one signature.

> [!warning] `forEach` is not the enhanced `for` statement
> `iterable.forEach(action)` is a **method**. `for (T t : iterable)` is the **language** loop and does not take a `Consumer`. Changing `forEach` does not change enhanced `for`. The default `forEach` still uses enhanced `for` internally, so fail-fast iterators still see structural modifications.

> [!tip] Interview answer
> **`Iterable.forEach` takes `Consumer<? super T>` and calls `accept` on each element.** `Consumer` is the Java 8 one-arg, void, side-effect interface. The default method is enhanced `for` over `this`. `Map.forEach` uses `BiConsumer`, not `Consumer`.
