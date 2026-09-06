<!--
reps: 0
priority: 0
-->
#Java/Serialization #SRS

# What is serialization?

> [!abstract] Short answer
> **Serialization is turning object state into a stream of bytes so it can be stored or sent, then rebuilt (deserialized) into live objects.** In Java, `java.io` object serialization does that for graphs of `Serializable` instances: default field protocol, or `Externalizable` if you own the payload. Binary layout: [[How would you explain Java binary serialization]]. The default walk: [[How does serialization and deserialization with Serializable work]].

## Store the graph, not the heap

The serialized form must identify the class and carry enough state to reconstruct instances and their relationships (sharing and cycles). `ObjectOutputStream` writes primitives and objects; `ObjectInputStream` reads them back as **new** objects. The type opts in with a marker:

```java
import java.io.Serializable;

class Point implements Serializable {
    private static final long serialVersionUID = 1L;
    int x, y;
}
```

**Listing 1.** Default serialization: non-`static`, non-`transient` fields. `Externalizable` is the other standard protocol — class identity in the stream, contents from `writeExternal` / `readExternal`: [[How do you implement a custom serialization protocol in Java]].

Two kinds of data per serializable class: **required** field values (bound by name) and **optional** data from `writeObject`. Compatible evolution the default protocol handles without custom methods includes adding fields, and changing a field from `static` to non-`static` or from `transient` to non-`transient` (equivalent to adding a serial field). Deleting a field, or the reverse modifier changes, are **incompatible** for older readers. Designing that contract: [[How do you design a custom Java serialization format]].

```d2
direction: down
live: "object graph in the VM" {
  width: 220
  height: 44
  style.fill: "#fff8e1"
}
ser: "serialize → byte stream" {
  width: 240
  height: 44
  style.fill: "#e3f2fd"
}
de: "deserialize → new graph" {
  width: 240
  height: 44
  style.fill: "#e8f5e9"
}
live -> ser -> de
```

**Fig. 1.** Serialization is the encode/decode pair. Identity in the stream is handles, not heap addresses.

This is specifically Java object serialization (`java.io`). JSON mappers and `DataOutputStream` alone are different encodings.

> [!warning] Untrusted bytes are not “just data”
> Deserialization can run class constructors, `readObject`, `readResolve`, and `readExternal`. Do not deserialize untrusted streams.

> [!warning] “We added a field” is not the same as “we deleted one”
> New fields on read get type defaults. A field missing from a newer writer leaves older readers at defaults and can break their contract. Flipping `Serializable` ↔ `Externalizable` is incompatible.

> [!tip] Interview answer
> Serialization converts an object graph to bytes for storage or the wire, and deserialization rebuilds objects from that stream. In Java the standard mechanisms are Serializable, which writes default serial fields, and Externalizable, where you write the contents. The format can tolerate adding fields; deleting fields or swapping those two interfaces does not.
