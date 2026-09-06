<!--
reps: 0
priority: 0
-->
#Java/Serialization/SingletonSerializationProblem #SRS

# What is the singleton serialization problem?

> [!abstract] Short answer
> **`readObject` always allocates a new instance**, so a serializable singleton comes back as a **second object** and uniqueness is gone. Prevent that by not implementing `Serializable`, by throwing `NotSerializableException`, or by `readResolve` returning the canonical instance. Enum constants do not have this bug: they reconstitute with `Enum.valueOf`, not a extra allocation. Hooks: [[How do you customize Java serialization and deserialization]]. Enums: [[How does Java serialization treat enum constants]].

## A new object, not the old `INSTANCE`

Deserialization is not “fill the existing singleton.” Memory is allocated, fields are restored, **new objects are always allocated**. If `Config.INSTANCE` was written, the stream produces another `Config` with the same field values. `==` against `INSTANCE` fails; two “singletons” exist in the VM.

```java
import java.io.ObjectStreamException;
import java.io.Serializable;

class Config implements Serializable {
    private static final long serialVersionUID = 1L;
    static final Config INSTANCE = new Config();

    private Config() {}

    private Object readResolve() throws ObjectStreamException {
        return INSTANCE;
    }
}
```

**Listing 1.** `readResolve` runs after the extra instance is fully built, just before `readObject` returns it. The method may be private, package, protected, or public. Returning `INSTANCE` discards the duplicate for the caller.

```java
enum ConfigEnum {
    INSTANCE
}
```

**Listing 2.** Enums are serializable. The stream stores the constant **name**; the live object is `Enum.valueOf`. Class `readResolve` / `writeReplace` on an enum type are ignored — they are unnecessary here.

Forbidding serialization (`writeObject` throws `NotSerializableException`, or no `Serializable` at all) also preserves uniqueness — [[How do you prevent a Java class from being serialized]].

```d2
direction: down
stream: "bytes for the singleton" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
alloc: "new Config() via the stream\n(not INSTANCE)" {
  width: 260
  height: 50
  style.fill: "#ffcdd2"
}
rr: "readResolve → INSTANCE" {
  width: 240
  height: 44
  style.fill: "#e8f5e9"
}
stream -> alloc -> rr
```

**Fig. 1.** The problem is the extra allocation. `readResolve` replaces what the caller receives. Graph handles already pointing at the extra object are **not** rewritten.

`writeReplace` can emit a proxy instead of the singleton; still pair it with `readResolve` on the way in. Process: [[How does serialization and deserialization with Serializable work]].

> [!warning] `readResolve` does not patch the graph
> It runs only when the object is complete. If a field of the deserialized graph already references that extra instance, that field still points at the duplicate, not at `INSTANCE`.

> [!warning] Exact signature, or you still have two instances
> Wrong name, extra parameters, or a missing `Object` return and the runtime never calls it. Default field deserialization then returns the extra object. Records *do* honor `readResolve`; they still allocate through the canonical constructor first.

> [!tip] Interview answer
> The singleton serialization problem is that deserialization always creates a new object, so you get a second singleton. Fix it with readResolve that returns the canonical INSTANCE, or use an enum constant, which is restored by name. Forbidding serialization also works; do not rely on a private constructor alone.
