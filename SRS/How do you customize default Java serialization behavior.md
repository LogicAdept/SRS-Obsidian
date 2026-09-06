<!--
reps: 0
priority: 0
-->
#Java/Serialization #SRS

# How do you customize default Java serialization behavior?

> [!abstract] Short answer
> **Stay on `Serializable` and intercept the default field protocol.** Declare `writeObject` / `readObject` with the exact private signatures and call `defaultWriteObject` / `defaultReadObject` (or `putFields` / `readFields`) once. Narrow the field list with `transient` or replace it with `serialPersistentFields`. That is not `Externalizable`, which throws the default list away: [[How do you implement a custom serialization protocol in Java]].

## Intercept, don’t abandon, the default list

For an ordinary serializable class, each class from the first serializable supertype downward either:

- has no `writeObject` — then `defaultWriteObject` writes the **non-static, non-transient** fields, or
- defines `writeObject` — then **that** method runs instead of the automatic call. It must still invoke `defaultWriteObject` or `putFields`+`writeFields` **once** before any extra bytes (even if it writes none). The same pairing holds for `readObject` with `defaultReadObject` / `readFields`.

Extra `writeInt` / `writeObject` after that call is **optional data** for the matching `readObject`, not a serial field. Superclasses are still handled by the stream; you do not walk them yourself.

```java
private void writeObject(java.io.ObjectOutputStream out)
        throws java.io.IOException { /* … */ }
private void readObject(java.io.ObjectInputStream in)
        throws java.io.IOException, ClassNotFoundException { /* … */ }
```

**Listing 1.** Conceptual. Not interface methods. Wrong modifiers, name, or throws clause means the runtime never calls them and you get silent default serialization.

```java
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;

class Range implements Serializable {
    private static final long serialVersionUID = 1L;
    int lo, hi;
    transient int width;

    Range(int lo, int hi) {
        this.lo = lo;
        this.hi = hi;
        this.width = hi - lo;
    }

    private void writeObject(ObjectOutputStream out) throws IOException {
        out.defaultWriteObject();
    }

    private void readObject(ObjectInputStream in)
            throws IOException, ClassNotFoundException {
        in.defaultReadObject();
        width = hi - lo;
    }
}
```

**Listing 2.** Default bytes are `lo` and `hi`. `width` is `transient`, so it is omitted and recomputed. Constructors of a serializable class do not run on deserialize: [[How would you explain the transient field modifier in Java]].

To **rename, drop, or invent** serial fields without matching live fields, declare

`private static final ObjectStreamField[] serialPersistentFields`

and map values with `PutField` / `GetField`. The array must actually be `private static final` and a non-null `ObjectStreamField[]`, or it is ignored. Inner classes cannot declare it. `static` / `final` still follow the usual default-list rules: [[How do static and final fields affect Java serialization]].

Object substitution (`writeReplace` / `readResolve`) and `readObjectNoData` are further hooks on the same protocol — catalog: [[How do you customize Java serialization and deserialization]]. Enums ignore these methods. Records ignore `writeObject` / `readObject` / `serialPersistentFields`.

```d2
direction: down
def: "default serial fields\nnon-static, non-transient" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
cut: "transient\nserialPersistentFields" {
  width: 240
  height: 50
  style.fill: "#ffcdd2"
}
hook: "writeObject / readObject\ndefaultWriteObject or PutField" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
opt: "optional data" {
  width: 180
  height: 40
  style.fill: "#e3f2fd"
}
def -> cut: "reshape the list"
def -> hook: "or intercept"
hook -> opt: "after the one required call"
```

**Fig. 1.** Customizing default serialization means reshaping or wrapping the field protocol. Switching to `Externalizable` is a different protocol.

> [!warning] Skip `defaultWriteObject` and the pair breaks
> Defining `writeObject` **replaces** the automatic field write. If you only emit ad-hoc bytes, `defaultReadObject` has nothing to assign. If you write optional data without that required call first, deserialization is undefined when the class cannot be resolved.

> [!warning] Exact signature or you customized nothing
> A `protected` / `public` `writeObject`, a different parameter type, or a missing `throws` list is just an unused method. The stream still writes every default serial field.

> [!tip] Interview answer
> Customize default Java serialization on Serializable: implement private writeObject and readObject, call defaultWriteObject and defaultReadObject, then write any extra data. Use transient or serialPersistentFields to change which fields are in that default list. Externalizable is not a customization of that list — it replaces it.
