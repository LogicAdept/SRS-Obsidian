<!--
reps: 0
priority: 0
-->
#Java/Serialization #SRS

# How would you explain Java binary serialization?

> [!abstract] Short answer
> **Java binary serialization is the `java.io` object-stream protocol:** `ObjectOutputStream` / `ObjectInputStream` encode a graph of `Serializable` objects as typed binary tokens, not as JSON or field-only bytes. Every stream starts with magic `0xACED` and version `5`, then class descriptors (`serialVersionUID`, flags, field names and types) and values, with handles for repeats. How that walk works: [[How does serialization and deserialization with Serializable work]]. What “serialization” means in general: [[What is serialization]].

## A typed binary graph, not a dump of fields

The protocol is designed to be compact, skippable from structure alone, and usable with only stream access. Terminals live in `ObjectStreamConstants`: `TC_OBJECT`, `TC_STRING`, `TC_ARRAY`, `TC_NULL`, `TC_REFERENCE`, `TC_ENUM`, block-data markers, and so on. Strings are modified UTF-8. Primitive data is wrapped in block-data records (JDK 1.2+ `PROTOCOL_VERSION_2`, up to 1024-byte chunks).

That is heavier than `DataOutput.writeInt`: the stream must identify **which class** wrote the bytes so a later VM can bind fields by name. `Externalizable` still uses this wrapper; only the payload after the descriptor is yours — [[How do you implement a custom serialization protocol in Java]].

```java
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.nio.file.Files;
import java.nio.file.Path;

class Node implements Serializable {
    private static final long serialVersionUID = 1L;
    int value;
    Node next;

    static void writeGraph(Path path, Node head) throws java.io.IOException {
        try (ObjectOutputStream out =
                     new ObjectOutputStream(Files.newOutputStream(path))) {
            out.writeObject(head);
        }
    }
}
```

**Listing 1.** The file begins `AC ED 00 05` (`STREAM_MAGIC`, `STREAM_VERSION`), then a `TC_OBJECT` / `TC_CLASSDESC` for `Node`, then `value` and `next`. A second reference to the same node is `TC_REFERENCE` plus a handle (base `0x7E0000`), not a second copy.

```d2
direction: down
hdr: "STREAM_MAGIC 0xACED\nSTREAM_VERSION 5" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
tok: "TC_* tokens\nclassDesc + values + handles" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
graph: "Serializable object graph" {
  width: 240
  height: 44
  style.fill: "#e8f5e9"
}
hdr -> tok -> graph: "readObject reconstitutes"
```

**Fig. 1.** Binary serialization is this grammar, not “whatever bytes the object occupies in the heap.” Layout and identity handles are protocol-defined.

Deserialization reconstructs **new** objects of the local classes, matching `serialVersionUID`. Untrusted streams are unsafe: the `Serializable` API warns that deserialization of untrusted data is inherently dangerous. Blocking a type: [[How do you prevent a Java class from being serialized]].

This is not JSON, XML, or a custom `byte[]` layout you invented with `DataOutputStream` alone. Those can store Java objects too; they are not Java object serialization.

> [!warning] The bytes name your classes
> The stream carries class names and field signatures. A reader with a gadget class on the classpath can instantiate it. Do not deserialize untrusted data; this protocol is for trusted peers and persistence you control.

> [!warning] Opaque and version-brittle
> You cannot usefully edit the file as text. Compatible field adds work for default `Serializable`; swapping `Serializable`/`Externalizable` or changing a primitive field type does not. Hex `AC ED` is a sniff test, not a parser.

> [!tip] Interview answer
> Java binary serialization is ObjectOutputStream’s binary protocol for Serializable object graphs: magic 0xACED, version 5, then class descriptors and field values with handles for sharing and cycles. It is not JSON and not a raw memory dump. Treat incoming streams as untrusted by default.
