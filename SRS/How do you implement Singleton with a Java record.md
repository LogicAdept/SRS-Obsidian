<!--
reps: 0
priority: 0
-->
#Java/Language/Records #Java/Language/Enum #Patterns/GoF/Creational #SRS

# How do you implement Singleton with a Java record?

> [!abstract] Short answer
> You can put a `static final INSTANCE` on a record — static members are allowed — but that is only a **well-known instance**, not a language-enforced singleton. A **public** record’s canonical constructor **must be public**, so `new Config(...)` remains legal. For a true single instance, use a **one-constant enum**: the JVM forbids extra instances, cloning, reflective construction, and serialization duplicates.

## A record can hold `INSTANCE`; it cannot hide `new`

```d2
direction: down
rec: "public record Config(...)" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
ctor: "canonical constructor must be public" {
  width: 300
  height: 55
  style.fill: "#ffebee"
}
inst: "static final Config INSTANCE = new Config(...)" {
  width: 340
  height: 55
  style.fill: "#e8f5e9"
}
rec -> ctor
rec -> inst
```

**Fig. 1.** Static `INSTANCE` is a convenience field. The public canonical constructor is still part of the API.

JLS §8.10.4: an explicit canonical constructor (normal or compact) must be **at least as accessible as the record**. If the record is `public`, the constructor **must be `public`**. Package-private records still cannot make it `private`. Only a **private** record may declare a private canonical constructor.

So this compact constructor **does not compile** on a public record:

```java
public record Config(String url) {
    private static final Config INSTANCE = new Config("default");
    // private Config {}  // compile-time error: canonical ctor must be public
    public static Config getInstance() { return INSTANCE; }
}
```

**Listing 1.** Illegal attempt to hide construction. Extra constructors must still `this(...)` into that public canonical constructor — [[Can a Java record declare additional constructors]].

What *does* compile is a published instance plus an unavoidable public constructor:

```java
public record Config(String databaseUrl, int maxConnections) {
    public static final Config INSTANCE =
        new Config("jdbc:postgresql://localhost:5432/mydb", 10);
}
```

**Listing 2.** Legal static member ([[Can a Java record declare static members and instance methods]]). `Config.INSTANCE` is one object; `new Config("other", 1)` is another. Record `equals` compares components, so two configs with the same URL and pool size compare equal even when they are not the same instance.

Class initialization of `INSTANCE` is synchronized by the JVM (JLS §12.4.2). That makes **this field** safe to publish; it does not stop other threads from calling `new`. A nested holder class only delays initialization until that nested type is first used (JLS §12.4.1) — still not a singleton.

## Enum is the singleton the language actually guarantees

```java
public enum Config {
    INSTANCE;

    public String databaseUrl() { return "jdbc:postgresql://localhost:5432/mydb"; }
    public int maxConnections() { return 10; }
}
```

**Listing 3.** JLS §8.9: an enum class has **no instances other than its constants**; `new Config()` is a compile-time error. `Enum.clone` is `final`; reflective instantiation is prohibited; serialization is required **not** to create duplicates. See [[How does an enum provide a Singleton]].

If a record implements `Serializable`, deserialization **invokes the canonical constructor** and returns a **new** object (Java Object Serialization Spec; records ignore `readObject` / `writeObject`). Records **may** declare `readResolve` / `writeReplace` to substitute `INSTANCE` after that construction. Enums ignore those methods and still restore the constant. Default record deserialization is the opposite of “serialization-safe singleton.” [[What is the singleton serialization problem]] · [[How does Java serialization treat record classes]]

JEP 445 (unnamed classes / instance main) is unrelated to this.

> [!warning] Do not say a record “guarantees a single instance”
> `static final INSTANCE` is a naming convention. The public canonical constructor is a factory anyone can call. Identity (`==`) is not unique; component `equals` may still treat two separately constructed values as equal.

> [!warning] `private` compact constructor is illegal on a public record
> Accessibility is tied to the record type, not to a wish for Singleton. Reflection is not the interesting bypass: on a public record, `new` already works. Serialization creates another instance through the same canonical constructor unless you add `readResolve`.

> [!tip] Interview answer
> **A record can expose `static final INSTANCE`, but a public record cannot have a private canonical constructor, so it is not a real singleton.** Use a one-constant enum when you need the JVM to forbid extra instances, including via clone, reflection, and serialization. Treat a record `INSTANCE` as a well-known immutable value, not as “the only object of this type.”
