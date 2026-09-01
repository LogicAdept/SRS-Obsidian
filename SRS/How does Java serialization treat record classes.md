<!--
reps: 0
priority: 0
-->
#Java/Language/Records #Java/Serialization #SRS

# How does Java serialization treat record classes?

> [!abstract] Short answer
> A record implements `Serializable` like any class, but the **stream is only the component values**, and **deserialization always calls the canonical constructor**. `writeObject` / `readObject` / `readObjectNoData` / `writeExternal` / `readExternal` are ignored. Default `serialVersionUID` is `0L` and matching is **waived**. This shipped with records (Java 16 / JEP 395), not JEP 445.

## Components out, canonical constructor in

```d2
direction: down
ser: "serialize: component values only" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}
stream: "ObjectOutputStream / ObjectInputStream" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
de: "deserialize: new R(c1, c2, …)\ncanonical constructor" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
ser -> stream
stream -> de
```

**Fig. 1.** Ordinary serializable classes can be reconstituted by allocating an object and setting fields, skipping constructors. A record cannot.

JLS §8.10: a record object is deserialized using the canonical constructor. Java Object Serialization Spec §1.13 (and the Java SE records tutorial): the serialized form is the sequence of component values; then the implementation locates the canonical constructor from `getRecordComponents()` and invokes it (missing stream fields get the default for the type). Compact-constructor validation therefore **runs** on deserialize — [[What is a canonical constructor in a Java record]] / [[What is a compact constructor in a Java record]].

```java
public record RangeRecord(int lo, int hi) implements Serializable {
    public RangeRecord {
        if (lo > hi)
            throw new IllegalArgumentException("lo > hi");
    }
}
```

**Listing 1.** `implements Serializable` is enough. No `serialVersionUID` required. A stream with `lo=100, hi=1` fails in the compact body; an ordinary class with the same invariant often **succeeds** because its constructor never ran.

```java
public record Point(int x, int y) implements Serializable {}
```

**Listing 2.** Minimal serializable record. Default `serialVersionUID` is `0L`. Declare one only when migrating a legacy serializable class to a record (Serialization Spec §5.6.2).

Ignored on records: `writeObject`, `readObject`, `readObjectNoData`, `writeExternal`, `readExternal`, and `serialPersistentFields`. Allowed: `writeReplace` / `readResolve` (unlike enums, which ignore those too). That is how a well-known instance can survive the stream — [[What is the singleton serialization problem]].

Cycles: components are deserialized **before** the constructor runs, so a cycle in which the record is reachable from one of its own components is **not** preserved (Spec §1.13 / §1.14).

This is `java.io` object serialization. JSON via Jackson is a different mapper: [[How do you serialize a Java record with Jackson]].

> [!warning] Ordinary class deserialization can skip your constructor
> `ObjectInputStream` may allocate via a superclass no-arg constructor and then set fields. That can yield an object no `new` expression could create. Records close that hole: the only construction path is the canonical constructor.

> [!warning] `writeObject` on a record is dead code
> It will not run. You cannot reshape the serial form; it is the components, in header order. `serialVersionUID` mismatch is also not the usual failure mode — matching is waived, default `0L`.

> [!tip] Interview answer
> **Serializable records write only their components and always come back through the canonical constructor, so compact-constructor checks apply.** `readObject`/`writeObject` are ignored; `serialVersionUID` defaults to `0L` and need not match. That is Java 16 record serialization (JEP 395), not JEP 445.
