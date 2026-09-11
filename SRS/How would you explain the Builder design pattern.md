<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Creational #SRS

# How would you explain the Builder design pattern

> [!abstract] Short answer
> Builder is a creational pattern that constructs **complex objects step by step**: construction moves out of the target class into a separate builder, and the same construction code can produce different representations. Its everyday motivation is killing the telescoping constructor.

## The mechanism

The pattern organizes construction into named steps — `setSeats`, `setEngine`, and so on. A builder interface declares the steps, concrete builders implement them, and the client calls only the steps the target configuration needs; nobody can observe the product while it is being assembled. An optional director class knows the order of steps for popular configurations, while the builder owns the implementation of each step — director decides "how to sequence", builder decides "how to perform". The product is fetched from the builder itself, via a `getProduct`-style method, not from the director: different builders can produce products that share no interface at all, like a car and its manual, so a statically typed language cannot put a common return type in the director. A builder is typically reset after handing over the product so it can build the next one.

```java
HttpRequest req = new HttpRequest.Builder("https", "api.example.com")
        .header("Accept", "application/json")
        .timeout(Duration.ofSeconds(5))
        .build();
```

**Listing 1.** The fluent shape most Java APIs use: chain the optional steps, then `build()` hands over the finished product.

## Why it pays and when it does not

The pattern removes constructor overloads like `Pizza(int size)`, `Pizza(int size, boolean cheese)`, `Pizza(int size, boolean cheese, boolean pepperoni)` — each feeding defaults into the next — and replaces them with readable, order-independent steps. It also lets the same construction code drive different representations: car versus car manual, or an HTML and a plain-text renderer over the same document. The cost is extra classes, which is why the classic advice is that Builder is justified only for genuinely complex products. The practical Java form and its advantages over constructors are compared in [[What are the advantages of the Builder pattern over constructors]], and the boundary against Facade is drawn in [[What is the difference between the Builder and Facade design patterns]].

> [!warning] Builder is not Abstract Factory
> An Abstract Factory returns a product immediately from a creation call, while Builder defers the result until the steps finish — mixing these up is a standard trap. A second trap: calling Lombok's `@Builder` "the Builder pattern" — the annotation generates the fluent shape, but the interview question is about the construction concept behind it.

> [!tip] Interview answer
> Builder extracts object construction into a separate builder with named steps, so complex objects are built step by step and only the needed steps are called. A director can fix the step order for standard configurations, and the product comes back from the builder via a build or getProduct method. Use it for telescoping constructors and for producing different representations from the same construction code.
