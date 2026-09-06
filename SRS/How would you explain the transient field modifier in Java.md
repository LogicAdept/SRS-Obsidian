<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers #Java/Serialization/Transient #SRS

# How would you explain the transient field modifier in Java?

> [!abstract] Short answer
> **`transient` marks a field as not part of an object’s persistent state.** It is a **field** modifier only. For `java.io.Serializable` default serialization, the serializable fields are the **non-`transient` and non-`static`** instance fields — unless the class lists them in `serialPersistentFields`. After deserialization, a `transient` field is left at the **type’s default** (`0` / `null` / `false`) unless `readObject` assigns it. Exclude fields: [[How do you exclude fields from Java serialization]]. `static` / `final` vs the stream: [[How do static and final fields affect Java serialization]]. Default protocol: [[How does serialization and deserialization with Serializable work]].

## Not in the default serial form

The language does not define a persistence service; it only labels the field. Java object serialization is the usual service: `ObjectOutputStream` writes non-`transient`, non-`static` field values (and follows references in those fields). `defaultWriteObject` / `defaultReadObject` do the same for the current class. `Externalizable` classes supply their own bytes; they do not use that default field list.

On the way in, a serializable object’s fields are first set to defaults; constructors and instance field initializers of the serializable class **do not run**. Then `readObject` or `defaultReadObject` restores matching stream fields. A `transient` field never appears in that stream, so it stays at the default unless you restore it yourself. Typical uses: derived or cached values, secrets, and references that must not pull a non-serializable helper into the graph. Sensitive data is often `private transient` so it cannot reappear from the stream.

`serialPersistentFields` (a `private static final ObjectStreamField[]`) **overrides** the default list: a field can be serialized without a matching live field, or omitted even if it is not `transient`. Inner classes cannot declare that array (they cannot hold a suitable `static` field), and they contain an implicit **non-`transient`** reference to the enclosing instance — serializing the inner object serializes the outer one too.

```java
class Point implements java.io.Serializable {
    int x, y;
    transient float rho, theta;

    Point(int x, int y) {
        this.x = x;
        this.y = y;
        this.rho = (float) Math.hypot(x, y);
    }
}
```

**Listing 1.** A persistence service saves `x` and `y`. `rho` and `theta` are derived; after default deserialization they are `0.0f` until you recompute them in `readObject`.

```java
private void readObject(java.io.ObjectInputStream in)
        throws java.io.IOException, ClassNotFoundException {
    in.defaultReadObject();
    rho = (float) Math.hypot(x, y);
}
```

**Listing 2.** Conceptual (inside `Point`). Restore anything `transient` that should not stay at the default.

```d2
direction: down
obj: "Serializable instance" {
  width: 200
  height: 40
  style.fill: "#fff8e1"
}
keep: "non-static, non-transient fields" {
  width: 260
  height: 44
  style.fill: "#e8f5e9"
}
drop: "transient / static" {
  width: 200
  height: 40
  style.fill: "#ffcdd2"
}
stream: "ObjectOutputStream" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
obj -> keep -> stream
obj -> drop: "not default serial fields"
```

**Fig. 1.** Default serializable fields are computed from modifiers. `serialPersistentFields` can replace that computation.

> [!warning] Field initializers do not run on deserialize
> `transient List<T> cache = new ArrayList<>();` becomes `null` after default deserialization, not a fresh list. Re-create it in `readObject` (or lazy-init on first use).

> [!warning] `transient` is not “non-static”
> `static` fields are omitted too, because they are not instance serial fields. Marking a class variable `transient` does not change that. `final` instance fields **are** serialized under the default mechanism.

> [!warning] `transient` is not a lock on the bytes
> `writeExternal` can still emit the value. A `serialPersistentFields` entry can put the name in the stream even if the live field is `transient`. Records serialize every component.

> [!tip] Interview answer
> Transient means this instance field is not part of persistent state. Default Java serialization writes every non-static, non-transient field and, on the way back, leaves transient fields at default values because constructors do not run. Use it for caches, derived data, secrets, and non-serializable references; restore what you still need in readObject.
