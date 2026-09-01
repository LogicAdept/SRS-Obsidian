<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #Java/Serialization #SRS

# How does Java serialization treat enum constants?

> [!abstract] Short answer
> **By name, not by fields.** `Enum` already implements `Serializable`; you do not declare it on the enum. The stream stores `name()` only. Deserialization calls `Enum.valueOf(type, name)` and returns the live constant, so identity is kept. Extra instance fields, `writeObject` / `readObject` / `readResolve`, and a declared `serialVersionUID` are ignored. Every enum type’s UID is `0L`.

## Name out, `valueOf` in

Ordinary objects serialize field values. An enum constant does not. `ObjectOutputStream` writes the string from `name()` (the declaration identifier, not `toString()` — [[Can you override toString on a Java enum]]). `ObjectInputStream` reads that string and obtains the constant with `Enum.valueOf` ([[How do you convert a String to a Java enum]]). If that name does not exist on the local enum, `valueOf` throws `IllegalArgumentException` and deserialization fails with `InvalidObjectException`.

That lookup is why `deserialize(Holder.INSTANCE) == Holder.INSTANCE` ([[How does an enum provide a Singleton]]). The stream may later use a back reference to the same constant, like any other object handle.

```d2
direction: down
c: "Status.ON\nlabel = \"running\"" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
wire: "stream: name \"ON\"\n(no fields)" {
  width: 240
  height: 60
  style.fill: "#fff3e0"
}
live: "Enum.valueOf(Status, \"ON\")\nsame Status.ON" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

c -> wire -> live
```

**Fig. 1.** The wire form is the identifier. Field state on the constant is not in the stream and is not restored.

```java
enum Status {
    ON("running"), OFF("stopped");

    final String label;
    Status(String label) { this.label = label; }
}

// serialized form of Status.ON is the name "ON"
// after deserialize: the object is Status.ON (identity)
// label is whatever the local Status.ON was initialized with — not a streamed field
```

**Listing 1.** Extra fields live only in the local class initialization of that constant. They do not round-trip.

You still do not write `implements Serializable` on `Status`. `java.lang.Enum` already does. Class-specific `writeObject`, `readObject`, `readObjectNoData`, `writeReplace`, `readResolve`, and `serialPersistentFields` on an enum type are **ignored**. Declaring `serialVersionUID` is ignored too; the UID is fixed at `0L`.

`toString` overrides, labels, and mutable instance fields are display or local heap state. Changing a constant’s identifier, or deleting it, breaks old streams ([[Can you add constants to a Java enum at runtime]]). Adding a constant is usually fine: old names still `valueOf`.

> [!warning] Fields do not survive Java serialization
> Dumps that say “name-only” are right. After deserialize you see the local constant’s constructor-initialized fields, not what another JVM stored in those fields before `writeObject`. Do not use extra enum fields as a serialized document.

> [!warning] You cannot `readResolve` your way out
> On a normal class, `readResolve` is how a singleton repairs `readObject`. On an enum those hooks are skipped; `valueOf` *is* the repair. A `readObject` on `Enum` that throws `InvalidObjectException` is a backstop against default field deserialization, not a customization point.

> [!warning] `name()`, not `toString()`
> A friendlier `toString` does not change the stream. The identifier `valueOf` expects is `name()`. Rename `ON` to `RUNNING` and old bytes that say `ON` will not resolve.

> [!tip] Interview answer
> **Enum constants serialize as their `name()`; deserialize is `Enum.valueOf`, so you get the same JVM constant back.** Fields and custom serialization methods are ignored, and `serialVersionUID` is always `0L`. You do not implement `Serializable` yourself — `Enum` already does.
