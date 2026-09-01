<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Java/OOP/Interfaces #SRS

# Why are interfaces important in object oriented design?

> [!abstract] Short answer
> They let you **depend on a type** without locking a **class, constructor, or fields**. A class **`extends` one** superclass and **`implements` many** interfaces, so an interface is how Java shares **contracts** across unrelated implementations. Calls on an interface variable are **polymorphic**. That is the usual “program to a type, not a concrete class.” Types: [[How would you explain main concepts OOP class object interface]]. vs class: [[What is the difference between a Java interface and an abstract class]]. Many types: [[How does Java model multiple inheritance with interfaces]].

## A contract other types can keep

**Abstraction.** An interface is a **reference type**: methods, constants, nested types — not instance fields, not constructors ([[Can a Java interface declare a constructor]]; [[What is abstraction]]). Clients write `List<String>` or `AutoCloseable` and do not construct `ArrayList` or a particular stream class unless they choose to. The JDK collections API is built this way ([[What is the List interface in Java]]).

**Multiple inheritance of type.** Two libraries cannot both be your superclass. They can both be interfaces you `implement`. Design can slice behavior (`Closeable`, `Iterable`, `Comparable`) instead of forcing a single abstract class tree.

**Polymorphism.** A variable of interface type accepts any implementing object; instance calls dispatch to that class ([[What is polymorphism]]; [[What mechanisms implement polymorphism in Java]]). Tests and alternate implementations plug in without changing the caller.

**Evolution and extras.** `default` / `static` / `private` methods let an interface grow without breaking every implementor ([[How would you explain default interface methods since Java 8]]; [[What kinds of methods can a Java interface declare]]). A **functional** interface is a lambda target type. A **small** interface beats a fat one ([[How would you explain the Interface Segregation Principle in SOLID]]).

Prefer an **abstract class** when you must share **state or constructor** policy ([[When should you use an abstract class versus an interface]]).

```d2
direction: down
client: "caller (Job)" {
  width: 200
  height: 40
  style.fill: "#fff8e1"
}
iface: "interface Sink" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
impl: "Printer, mock, lambda" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
client -> iface: "depends on type"
impl -> iface: "implements"
```

**Fig. 1.** The caller is coupled to the interface. Implementations stay replaceable.

```java
interface Sink {
    void accept(String s);
}

class Printer implements Sink {
    public void accept(String s) {}
}

class Job {
    static void run(Sink out) {
        out.accept("ok");
    }
}
```

**Listing 1.** `Job.run` takes `Sink`, not `Printer`. A test or a lambda can satisfy `Sink` without a `Printer` subclass.

> [!warning] An interface is not automatically good design
> A large interface that every client only half-uses still couples them. Split by what callers need. Putting `default` methods everywhere can smuggle a hidden abstract class into the API.

> [!warning] Not a substitute for a class
> If instances share fields or a construction sequence, an abstract class (or a concrete type) is the honest tool. `new I(...)` is never legal.

> [!warning] Do not wrap every class “for OOP”
> A package-private type with one implementation does not need a public interface. Add an interface when you have **two implementations**, an **API boundary**, or a **JDK/callback** type to implement.

> [!tip] Interview answer
> Interfaces matter because they are types you can depend on without sharing a class or instance state, and a class may implement many of them. That gives multiple inheritance of contracts and polymorphic callers. Use an abstract class instead when the parent must own fields or constructors; keep interfaces small for the clients that use them.
