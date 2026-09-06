<!--
reps: 0
priority: 0
-->
#Java/Serialization #SRS

# How does serialization and deserialization with Serializable work?

> [!abstract] Short answer
> **`ObjectOutputStream.writeObject` walks the serializable classes of the instance from the highest serializable supertype down, writing each class descriptor and its non-`static`, non-`transient` field values.** Object-typed fields recurse; a handle is reused for an object already in the stream, so cycles survive. **`ObjectInputStream.readObject` allocates zeroed memory, runs the first non-serializable supertype’s no-arg constructor, then restores fields in the same class order** — serializable-class constructors and instance initializers do not run. Customize that path: [[How do you customize default Java serialization behavior]]. Skip a field: [[How would you explain the transient field modifier in Java]].

## Write: descriptors, then fields, then the graph

Only types that implement `Serializable` (and are not `Externalizable`) use this protocol. The stream records, for each serializable class in the hierarchy:

- class name, `serialVersionUID`, flags, and the serial field names/types (the class descriptor)
- required field data in canonical order (primitives by name, then references by name)
- optional data if `writeObject` wrote any after `defaultWriteObject` / `writeFields`

The **highest serializable class** is written first, then each subclass. Fields of a **non-serializable** superclass are not written; that class must expose an accessible no-arg constructor for the way back. `java.lang.Object` is not serializable and is not a descriptor in this chain.

A first encounter with an object writes its bytes and assigns a handle. Later references write the handle only. That is why a cycle (`a.next == a`) reconstitutes with the same identity.

If the class defines `writeObject`, that method runs instead of automatic `defaultWriteObject` for that class (it should still call `defaultWriteObject` or `writeFields` once). `writeReplace` may substitute a different object **before** this layout is emitted.

```java
import java.io.Serializable;

class Named {
    String name;

    Named() {
        this.name = "anon";
    }
}

class Person extends Named implements Serializable {
    private static final long serialVersionUID = 1L;
    int age;

    Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
}
```

**Listing 1.** Stream content for a `Person`: `Person`’s descriptor and `age`. `Named.name` is not a serial field. After deserialize, `age` comes from the stream; `name` is `"anon"` from `Named()`.

## Read: allocate, super constructor, then assign

Memory is allocated and zeroed. The no-arg constructor of the first non-serializable supertype runs (here `Named()`). Then each serializable class restores fields — `defaultReadObject` / `readObject` — from that highest serializable type down to the most specific class. Missing stream fields become type defaults; extra stream fields are discarded. `serialVersionUID` mismatch throws `InvalidClassException`.

There is no `new Person(...)`. Instance initializers and `Person` constructors do not run. `final` instance fields are still assigned by this machinery: [[How do static and final fields affect Java serialization]].

Enums restore by name (`Enum.valueOf`). Records restore through the canonical constructor — [[How does Java serialization treat record classes]]. `Externalizable` is a different payload protocol.

```d2
direction: down
w: "writeObject(person)" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
desc: "class descriptors\n(serializable types only)" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
fields: "non-static, non-transient fields\nhighest serializable class first" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
h: "handles for repeats / cycles" {
  width: 240
  height: 40
  style.fill: "#c8e6c9"
}
alloc: "allocate + zero\nnon-serializable super() " {
  width: 260
  height: 50
  style.fill: "#ffecb3"
}
r: "restore serial fields" {
  width: 220
  height: 40
  style.fill: "#ffe0b2"
}
w -> desc -> fields -> h -> alloc -> r
```

**Fig. 1.** Default `Serializable` protocol. Non-serializable superclasses contribute a constructor on read, not field bytes on write.

> [!warning] Invariants in a serializable constructor do not run
> A `Person` constructor that rejects negative `age` is skipped. The stream can produce an instance no `new` expression would. Validate in `readObject` / `readResolve`, or use a record (canonical constructor runs).

> [!warning] Missing super no-arg constructor fails at read
> The first non-serializable supertype’s no-arg constructor must be accessible to the serializable subclass. If it is missing or inaccessible, deserialization throws `InvalidClassException`. `NotSerializableException` is the other failure: some reachable object is not `Serializable` — [[How do you prevent a Java class from being serialized]].

> [!tip] Interview answer
> Serializable default serialization writes each serializable class’s descriptor and its non-static, non-transient fields, from the highest serializable supertype down, and uses handles for repeated objects. Deserialization allocates the object, calls only the first non-serializable superclass’s no-arg constructor, then fills fields from the stream — the serializable class’s own constructors never run.
