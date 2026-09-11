<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Behavioral/Strategy #SRS

# What is the Strategy pattern used for

> [!abstract] Short answer
> Strategy defines a **family of interchangeable algorithms**: each variant lives in its own class behind a common interface, and the context object delegates to whichever one the client injects — so behavior can be swapped at runtime without editing the context.

## The mechanism

The context keeps a reference typed to the strategy interface, normally set through the constructor or a setter, and calls exactly one method on it when it needs the algorithm's result. The client picks the concrete strategy because only it knows the differences between the variants; the context stays ignorant of which one is active. The classic use cases from the catalog: many near-duplicate classes that differ only in one algorithm — Strategy collapses them into one context plus a strategy hierarchy; a massive conditional that switches between variants of the same algorithm — Strategy replaces the `switch` with delegation; and any place where algorithm details should not leak into business logic, like a navigator that renders routes but delegates route computation to road, walking, or transit strategies.

```java
List<Order> orders = loadOrders();
orders.sort(Comparator.comparing(Order::total));        // by total
orders.sort(Comparator.comparing(Order::createdAt));    // by date
```

**Listing 1.** The JDK's most visible Strategy: `Comparator` is the algorithm interface, `sort` is the context, and the client passes the variant per call.

## The costs and the lambda shortcut

The catalog is honest about the price: with few algorithms that rarely change, extra interfaces and classes are overhead; clients must understand the variants to choose one; and in languages with function types, a set of lambdas can replace the whole class hierarchy — the same delegation with no boilerplate. That shortcut is itself one of the standard criticisms catalogued in [[What are downsides of design patterns]]. The pattern remains the right shape when strategies carry state, configuration, or several related methods, and when the set of algorithms grows or changes.

> [!warning] Strategy is not State
> Both are composition with delegation and their class diagrams are nearly identical, so "they are the same thing" is a common wrong answer. The distinguishing fact — who drives the switch and whether the helpers know each other — is laid out in [[What is the difference between the Strategy and State design patterns]].

> [!tip] Interview answer
> Strategy extracts each variant of an algorithm into its own class behind a common interface, and the context delegates to the injected one, so algorithms swap at runtime and the context stays closed to modification. Use it to kill duplicated near-identical classes and big conditionals; in modern Java a lambda or Comparator often plays the strategy.
