<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #Patterns/GoF/Creational #SRS

# How does an enum provide a Singleton?

> [!abstract] Short answer
> **Give the enum exactly one constant.** That constant is the only instance the type will ever have: the language forbids `new`, `clone`, and extra reflective construction, and deserialization looks the constant up by `name()` via `Enum.valueOf` instead of allocating a copy. Class initialization is synchronized, so you do not write double-checked locking to publish `INSTANCE`.

## One constant, then the instance set is closed

An enum class has no instances other than its constants. `enum Holder { INSTANCE }` therefore has a single instance, created when the enum class initializes and the implicit `public static final` field `INSTANCE` is set ([[Can you create a Java enum instance with new]]). Zero constants is a different trick ([[How do you create a Java enum with no instances]]); two constants is not a singleton.

```java
enum Holder {
    INSTANCE;

    void ping() { /* … */ }
}

Holder x = Holder.INSTANCE;
// new Holder() does not compile
```

**Listing 1.** The singleton *is* the constant. Callers use `Holder.INSTANCE`; they never construct.

```d2
direction: down
decl: "enum Holder { INSTANCE }" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
one: "one instance\nclass-init, synchronized" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
blocked: "new / clone / extra reflection\nextra deserialize" {
  width: 280
  height: 70
  style.fill: "#ffcdd2"
}

decl -> one -> blocked
```

**Fig. 1.** The JVM makes `INSTANCE` once. The rest of the enum rules keep it unique.

`Enum.clone` is `final` and throws. `Constructor.newInstance` rejects enum constructors. Those are the same locks as “cannot add constants at runtime.”

## Serialization returns the same constant

Ordinary serializable singletons need `readResolve` so `readObject` does not mint a second instance. Enum constants skip that protocol. The stream stores the constant’s `name()` only; extra instance fields are **not** in the form. On the way back, `ObjectInputStream` calls `Enum.valueOf(type, name)` and you get the live constant ([[How does Java serialization treat enum constants]]). `writeObject` / `readObject` / `readResolve` on the enum type are ignored.

That is why deserialize(`INSTANCE`) `==` `Holder.INSTANCE`. It is also why you must not keep mutable “singleton state” in instance fields if you round-trip through Java serialization — those fields are not restored from the stream.

## Why you skip DCL

Initializing a class uses a per-class initialization lock: other threads wait until the class is fully initialized. The enum constructor for `INSTANCE` runs as part of that procedure, on first active use of `Holder`. You do not need `volatile` + double-checked locking to publish the instance. You also do not get per-constant laziness: **every** constant is created when the enum class initializes.

A record is not this. Records are ordinary instantiable classes; their serialization may even use `writeReplace` / `readResolve`. They do not get the enum instance freeze. Enum singleton is still a singleton, with the usual design cost of a global instance ([[Why is the singleton pattern often labeled an anti pattern]]).

> [!warning] One constant means singleton; two means a set
> `enum Role { ADMIN, USER }` is a closed set of two instances, not a singleton. Adding a second name is a source change that ends the singleton property ([[Can you add constants to a Java enum at runtime]]).

> [!warning] Serialized form is the name, not your fields
> `readResolve` cannot save extra field state on an enum — those methods are ignored. If the singleton must carry durable mutable state, that state does not ride along with Java serialization of `INSTANCE`.

> [!tip] Interview answer
> **A one-constant enum is a singleton because that constant is the type’s only instance, and the language plus serialization `valueOf` lookup refuse to make another.** Class initialization is already synchronized, so you do not hand-roll DCL. It is not the same as a record or a private-constructor class that still has to defend `readObject` and `clone`.
