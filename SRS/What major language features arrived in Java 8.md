<!--
reps: 0
priority: 0
-->
#Java/Language #Java/Versions/8 #SRS

# What major language features arrived in Java 8

> [!abstract] Short answer
> **Java SE 8’s language changes are lambda expressions, method references, default and `static` methods on interfaces, richer target-type inference, type-use annotations, and repeating annotations.** Oracle also lists method-parameter names via `javac -parameters` and `Executable.getParameters`. Streams, `Optional`, `java.time`, and Nashorn are **libraries**, not syntax. Diamond, `String` `switch`, and try-with-resources are **Java 7**.

## Syntax that shipped with 8

Oracle’s Java SE 8 language-enhancements list is the catalog. **Lambdas** package one unit of behavior to pass around (per-element work, completion, error). **Method references** are compact lambdas for an already-named method (`System.out::println`). Lambdas target a **functional interface** (one abstract method besides public `Object` methods) ([[How would you explain lambda expressions in Java]], [[What is method reference]], [[What is functional interface]]).

**Default methods** are interface methods with a body and the `default` keyword, so libraries can add API without breaking binaries. The same bullet adds **`static` methods on interfaces**. You still cannot write a `default` that overrides `Object` ([[How would you explain default interface methods since Java 8]]).

**Improved type inference:** Java 8 uses the **target type** in more places, including inferring generic method **arguments**. `stringList.addAll(Arrays.asList())` can infer `String`; Java 7 needed a type witness `Arrays.<String>asList()`.

**Annotations on types** (JSR 308): an annotation may appear anywhere a type is used, for pluggable checkers. **Repeating annotations:** the same annotation type may appear more than once on one declaration or type use (`@Repeatable` plus a container) ([[How do you create a repeatable annotation in Java]]).

**Parameter names:** `.class` files omit them unless you compile with `-parameters`; then `Executable.getParameters` can read them. That is compiler + reflection, not a new keyword.

```d2
lang: "Java 8 language" {
  shape: rectangle
  lam: "lambdas + method refs"
  iface: "default / static on interfaces"
  infer: "target typing (args)"
  ann: "type-use + repeating annotations"
}
lib: "Java 8 libraries (not language)" {
  shape: rectangle
  st: "Stream / Optional"
  time: "java.time"
  nash: "Nashorn / jjs"
}
not8: "Already in 7 (not 8)" {
  shape: rectangle
  d: "diamond <>"
  sw: "String switch"
  twr: "try-with-resources"
}
```

**Fig. 1.** Interview trap: naming Stream or `LocalDateTime` as a *language* feature. They rode in with 8’s JDK, not with new grammar.

```java
interface Greeter {
    default String greet() { return "hi"; }
    static Greeter noop() { return new Greeter() {}; }
}

List<String> names = new ArrayList<>();
names.add("A");
names.addAll(Arrays.asList()); // 8 infers String; 7 wanted Arrays.<String>asList()
names.forEach(System.out::println);
names.forEach(s -> System.out.println(s));
```

**Listing 1.** Default/`static` on an interface, method reference, lambda, and the `addAll(Arrays.asList())` target-typing example from the Java SE 8 language-enhancements page.

> [!warning] Language ≠ JDK 8 brochure
>
> `Stream`, `Optional`, `java.time`, `CompletableFuture`, and Nashorn are APIs. `var` is **10**. Records are **16**. Pattern `switch` is **21**. Diamond, binary literals, `String` in `switch`, and try-with-resources are **7**. Do not put those on a “Java 8 language” list. Repeating annotations need `@Repeatable` and a container — two of the same annotation without that do not compile.

> [!tip] Interview answer
>
> **Language in 8: lambdas, method references, default and static interface methods, better target typing, type annotations, repeating annotations** (and `-parameters` for names). Then say Streams/`java.time` are the famous *libraries*. Name default methods as the tool that let `Collection` grow `stream()` without breaking implementors.
