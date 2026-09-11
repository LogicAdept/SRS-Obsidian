<!--
reps: 0
priority: 0
-->
#Methodologies/Principles/SOLID #SRS

# How would you explain the Dependency Inversion Principle in SOLID?

> [!abstract] Short answer
> DIP says high-level policy modules should not depend on low-level detail modules - both should depend on abstractions, and the abstraction should be OWNED by the high-level side. Robert Martin stated it in 1996: "High-level modules should not depend upon low-level modules. Both should depend upon abstractions. Abstractions should not depend upon details. Details should depend upon abstractions." Inverting the classic top-down dependency arrow is what makes policy reusable across details and details replaceable without touching policy.

## The inversion in the dependency arrows

Naive layering points dependencies downward: `OrderService` (policy) imports `PostgresOrderRepository` (detail), so the business rule is welded to one storage technology. DIP redraws it: the high-level module declares the interface it needs - `OrderRepository` in the POLICY's package, phrased in the policy's vocabulary - and the detail module implements it. Source-code dependencies now point toward the abstraction; the runtime call still reaches the database, but the compile-time dependency of policy-on-detail is gone. That is the "inversion": details conform to the policy's contract, not the reverse ([[What is layered architecture]]).

```d2
direction: right
naiveA: "OrderService" {
  width: 200
  height: 55
}
naiveB: "PostgresOrderRepository" {
  width: 250
  height: 55
  style.fill: "#fde8e8"
}
naiveA -> naiveB: "naive: policy -> detail"
dipA: "OrderService" {
  width: 200
  height: 55
}
abs: "<< OrderRepository >>\nowned by policy" {
  width: 250
  height: 65
  style.fill: "#e8f5e9"
}
dipB: "PostgresOrderRepository" {
  width: 250
  height: 55
}
dipA -> abs
dipB -> abs: "inverted: detail -> abstraction"
```

**Fig. 1.** Same runtime flow, different source dependencies: the interface lives with the policy, and the detail implements it.

## What changes in practice

The policy defines the contract it wishes existed; adapters implement it with real technologies (Postgres, Kafka, HTTP). Wiring the implementation in is a separate concern - constructor injection, a factory, or a container - which is where Dependency Injection, the MECHANISM, meets DIP, the PRINCIPLE; they are neither identical nor interchangeable ([[What is the difference between dependency injection and dependency inversion]]). Testability is the free win: the policy runs against in-memory fakes with no infrastructure. Plugin architectures are DIP at application scale - the core defines ports, plug-ins implement them ([[How would you explain dependency injection]], [[What is the difference between inversion of control and a service locator]]).

> [!warning] "DIP = inject an interface" misses the ownership rule
> Creating an interface that MIRRORS the concrete class and injecting it still leaves the policy coupled to detail's vocabulary - the abstraction must be phrased by and for the high-level side, or it is ceremony with an arrow drawn backwards. The second trap: abstractions depending on details (an interface whose signatures leak `HttpServletRequest` or a JDBC type), which inverts nothing. And like all of SOLID, DIP is selective: a small tool with one storage does not owe the world a repository interface ([[What is the Strategy pattern used for]]).

> [!tip] Interview answer
> DIP: high-level policy and low-level detail both depend on abstractions, and the abstraction is owned by the policy side - so source dependencies point toward stable contracts while details plug in from below. I phrase the interface in the policy's language, implement it with adapters, and wire at the edge. It is the principle; dependency injection is just the mechanism that hands the implementation over.
