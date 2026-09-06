<!--
reps: 0
priority: 0
-->
#Java/Serialization/NotSerializable #SRS

# How do you prevent Java object serialization?

> [!abstract] Short answer
> **Keep the object off the serial graph, or make its class refuse the protocol.** `ObjectOutputStream` writes an object when `writeObject` is called on it or when a **non-transient, non-static** field reaches it. A non-serializable type yields `NotSerializableException`. A serializable type that must not go out throws from `writeObject` / `readObject`, or nominates a substitute with `writeReplace`. Class-level refusal: [[How do you prevent a Java class from being serialized]]. Cutting a field: [[How do you exclude fields from Java serialization]].

## Reachability, then the type

Serialization walks the object graph. Prevention is whichever of these actually stops that walk for **this** instance:

1. **Do not write it.** Never pass it to `writeObject`. Nothing else runs.
2. **Do not reach it.** Mark every field that would point at it `transient` (or omit the name from `serialPersistentFields`). References in `transient` or `static` fields are not followed. Another live serial field that still points at the same instance will serialize it anyway.
3. **Do not implement `Serializable` / `Externalizable`.** The runtime throws `NotSerializableException` (argument: class name) when that instance is required to be serializable.
4. **Refuse after the type is already serializable** (serializable superclass). Magic `writeObject` / `readObject` throw `NotSerializableException` — [[How do you prevent a Java class from being serialized]]. `writeReplace` can emit a stand-in instead of aborting.
5. **Stream policy.** A trusted `ObjectOutputStream` subclass may `enableReplaceObject` and swap the instance in `replaceObject` — [[How do you customize Java serialization and deserialization]].

```java
import java.io.Serializable;

class Envelope implements Serializable {
    private static final long serialVersionUID = 1L;
    String label;
    transient Object attachment;
}
```

**Listing 1.** `attachment` is not followed. A later `writeObject(envelope.attachment)` still serializes that object if it is reachable some other way.

```java
private void writeObject(java.io.ObjectOutputStream out)
        throws java.io.IOException {
    throw new java.io.NotSerializableException(getClass().getName());
}
```

**Listing 2.** Conceptual. Aborts this object when its class is already `Serializable`. Exact private signature required; `writeReplace` runs **before** this and can bypass it. Records and enums ignore it.

```d2
direction: down
root: "writeObject(root)" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
edge: "non-transient field?" {
  width: 220
  height: 40
  style.fill: "#fff8e1"
}
ser: "obj Serializable?" {
  width: 200
  height: 40
  style.fill: "#ffe0b2"
}
skip: "not written" {
  width: 160
  height: 36
  style.fill: "#c8e6c9"
}
nse: "NotSerializableException" {
  width: 220
  height: 40
  style.fill: "#ffcdd2"
}
bytes: "instance in the stream" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
root -> edge
edge -> skip: "no"
edge -> ser: "yes"
ser -> nse: "no"
ser -> bytes: "yes, unless writeObject throws"
```

**Fig. 1.** An object is serialized only if the graph reaches it and its type (or a substitute) participates. Blocking the class is not enough if a replacement is written.

> [!warning] `transient` hides a field, not an identity
> The same instance behind a non-transient field, or passed directly to `writeObject`, is still written. Handles then share that copy for later references.

> [!warning] Filters do not stop serialization
> `ObjectInputFilter` constrains **deserialization**. It does not keep an object from being written.

> [!tip] Interview answer
> Prevent Java object serialization by keeping the instance off the graph — don’t write it, and don’t let a non-transient field reach it — or by making its class non-serializable. If a superclass already implements Serializable, throw NotSerializableException from writeObject. Transient on one field is not enough when another path still points at the object.
