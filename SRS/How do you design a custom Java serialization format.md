<!--
reps: 0
priority: 0
-->
#Java/Serialization #SRS

# How do you design a custom Java serialization format?

> [!abstract] Short answer
> **Decide the bytes before you write code.** Either freeze a named field list (`serialPersistentFields` / default serial fields plus optional data) or own a private layout with `Externalizable`. Document it (`@serial` / `@serialField` / `@serialData`). Pin `serialVersionUID`. Default serialization versions field addition for you; Externalizable versioning is **your** format tag. How to implement the payload: [[How do you implement a custom serialization protocol in Java]]. How to wrap the default list: [[How do you customize default Java serialization behavior]].

## Two serial-form designs

The stream always carries a class descriptor (`serialVersionUID`, flags, field names and types). What you design is the **content contract**.

**Named fields (default protocol).** Required data is the serializable fields, in canonical order: primitives sorted by name, then object fields sorted by name — **not** source order. Optional data is whatever `writeObject` writes after `defaultWriteObject` / `writeFields`; that class is responsible for its length, types, and versions. `serialPersistentFields` (`private static final ObjectStreamField[]`) is how you freeze names and types while live fields move. Missing stream fields become type defaults; extra stream fields are discarded.

**Private layout (`Externalizable`).** Only class identity is written for you. You specify the order, types, and meaning of every datum, including **where superclass state sits**. The evolved class must keep the contract with older writers/readers; there is no automatic field matching. A leading format `int` (or equivalent) is the usual way to branch.

Incompatible with either design: switching `Serializable` ↔ `Externalizable`; deleting a field that older readers still need; changing a primitive’s declared type; moving the class in the hierarchy; dropping `defaultWriteObject` after older streams already contain required field data.

```java
import java.io.ObjectStreamField;
import java.io.Serializable;

class Employee implements Serializable {
    private static final long serialVersionUID = 1L;
    private String name;
    private String title;

    /**
     * @serialField name String employee name
     */
    private static final ObjectStreamField[] serialPersistentFields = {
        new ObjectStreamField("name", String.class)
    };
}
```

**Listing 1.** Designed form: one `String` named `name`. `title` can appear later in the class without entering the stream. Canonical order would have put `name` then `title` if both were default serial fields.

```java
import java.io.Externalizable;
import java.io.IOException;
import java.io.ObjectInput;
import java.io.ObjectOutput;

public class Box implements Externalizable {
    private static final int FORMAT = 1;
    private int width, height;

    public Box() {}

    /**
     * @serialData format {@code int}, then width {@code int}, then height {@code int}
     */
    @Override
    public void writeExternal(ObjectOutput out) throws IOException {
        out.writeInt(FORMAT);
        out.writeInt(width);
        out.writeInt(height);
    }

    @Override
    public void readExternal(ObjectInput in)
            throws IOException, ClassNotFoundException {
        int format = in.readInt();
        if (format != FORMAT) {
            throw new IOException("unknown format " + format);
        }
        width = in.readInt();
        height = in.readInt();
    }
}
```

**Listing 2.** Private content protocol. `readExternal` must use the same sequence. Superclass: none (`Object` is not serializable). Pin `serialVersionUID` if you need a stable class id — [[What is the role of serialVersionUID in Java serialization]].

```d2
direction: down
choice: "design the serial form" {
  width: 240
  height: 40
  style.fill: "#fff8e1"
}
named: "named fields\nSUID + serialPersistentFields\noptional data in writeObject" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
priv: "private layout\nExternalizable + format tag\nyou version the bytes" {
  width: 280
  height: 70
  style.fill: "#ffecb3"
}
choice -> named
choice -> priv
```

**Fig. 1.** Pick one contract and keep it. Flipping from named fields to Externalizable is an incompatible stream change.

Records cannot choose either custom form (components only). Enums cannot (name only). Catalog of hooks: [[How do you customize Java serialization and deserialization]].

> [!warning] Declaration order is not stream order
> Default required data is primitives by name, then references by name. If layout or packing matters, do not rely on field declaration order — use `Externalizable` or accept the canonical field order.

> [!warning] Externalizable gets no free evolution
> Adding a field to a `Serializable` class is compatible (old streams leave it at the default). Adding a datum in the middle of `writeExternal` without a format tag breaks every older reader. Version the payload yourself.

> [!tip] Interview answer
> Design the serialized form first: either a frozen named field list with serialPersistentFields and a stable serialVersionUID, or an Externalizable byte layout you version yourself. Document it with the serial javadoc tags. Do not switch Serializable and Externalizable later, and do not assume source field order is the stream order.
