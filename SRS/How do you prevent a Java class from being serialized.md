<!--
reps: 0
priority: 0
-->
#Java/Serialization/NotSerializable #SRS

# How do you prevent a Java class from being serialized?

> [!abstract] Short answer
> **Do not implement `java.io.Serializable` or `java.io.Externalizable`.** The runtime will throw `NotSerializableException` if that instance is reached from a graph. You cannot drop the interface in a subclass: every subtype of a serializable class is serializable. Then refuse with `writeObject` / `readObject` that throw `NotSerializableException`. Dropping a field is `transient`, not this: [[How do you exclude fields from Java serialization]]. Graph reachability is a different cue: [[How do you prevent Java object serialization]].

## Stay off the protocol, or abort it

`Serializable` is a marker. Classes that do not implement it have none of their state written. Spec-level advice for sensitive types: implement neither `Serializable` nor `Externalizable`.

```java
final class Credentials {
    private final char[] secret;

    Credentials(char[] secret) {
        this.secret = secret.clone();
    }
}
```

**Listing 1.** Not serializable. A `writeObject` of a graph that reaches a `Credentials` instance fails with `NotSerializableException`. No magic methods required.

If a **superclass** already implements `Serializable`, this class is serializable whether it repeats the interface or not. Then the class-side abort documented on `ObjectOutputStream` is to define the magic methods and throw:

```java
import java.io.IOException;
import java.io.NotSerializableException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

class LocalHandle extends SharedHandle {
    private void writeObject(ObjectOutputStream out) throws IOException {
        throw new NotSerializableException(LocalHandle.class.getName());
    }

    private void readObject(ObjectInputStream in)
            throws IOException, ClassNotFoundException {
        throw new NotSerializableException(LocalHandle.class.getName());
    }
}
```

**Listing 2.** Conceptual (`SharedHandle` is serializable). The exception’s argument should be the class name. `readObject` must declare `ClassNotFoundException` or this is not the serialization hook. For `Externalizable`, throw from `writeExternal` / `readExternal` instead — [[How do you customize default Java serialization behavior]].

```d2
direction: down
cls: "the class" {
  width: 180
  height: 36
  style.fill: "#fff8e1"
}
root: "Serializable in the type?" {
  width: 240
  height: 44
  style.fill: "#ffe0b2"
}
off: "omit both markers" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
on: "writeObject / readObject\nthrow NotSerializableException" {
  width: 280
  height: 55
  style.fill: "#ffcdd2"
}
cls -> root
root -> off: "no — this is enough"
root -> on: "yes — cannot un-implement"
```

**Fig. 1.** Preventing a **class** from being serialized is an interface decision first. The throw is only for types already on the protocol.

Enums are serializable by definition (name only); class hooks are ignored. Record `writeObject` is ignored — a serializable record cannot be blocked this way: [[How does Java serialization treat record classes]]. `writeReplace` runs before `writeObject` and can still emit a substitute.

> [!warning] `implements Serializable` is inherited
> A subclass cannot “turn off” a serializable superclass by omitting the interface. Private constructors, `final`, and package-private types do not stop `ObjectOutputStream` once the type is serializable.

> [!warning] Wrong `writeObject` shape is silent
> Public or package-private methods, a different parameter type, or `readObject` without `ClassNotFoundException` are unused. Default field serialization still runs.

> [!tip] Interview answer
> Prevent a class from being serialized by not implementing Serializable or Externalizable. If a superclass already is serializable, you cannot undo that — throw NotSerializableException from private writeObject and readObject with the exact signatures. Transient only excludes fields; records ignore writeObject entirely.
