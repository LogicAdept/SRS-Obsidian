<!--
reps: 0
priority: 0
-->
#Java/Serialization #Java/Language/Modifiers/Static #Java/Language/Modifiers/Final #SRS

# How do static and final fields affect Java serialization?

> [!abstract] Short answer
> **`static` fields are not default serializable fields** — they belong to the class, not the instance. **`final` instance fields are serialized** unless they are also `static` or `transient`. Two special names, `serialVersionUID` and `serialPersistentFields`, are themselves `static final` metadata, not instance bytes. Exclude with `transient`: [[How would you explain the transient field modifier in Java]]. Version stamp: [[What is the role of serialVersionUID in Java serialization]].

## Default serial fields ignore `static`, not `final`

Default serializable fields are the **non-transient and non-static** fields. `ObjectOutputStream` writes those values; `ObjectInputStream` restores them. `final` is not an exclusion modifier.

A `static` field has one incarnation for the class. The instance stream never carries that slot, so after deserialize you see whatever the **receiving** class currently holds — not the value from the writer. `writeObject` may still emit extra bytes of your choosing; that is optional data, not a default serial field.

`final` instance fields **are** in that default list. Serializable-class constructors and field initializers **do not run** on deserialize. Memory is zeroed, then `defaultReadObject` (or the equivalent default path) assigns matching stream fields, including `final` ones, through the serialization runtime. Ordinary assignment in `readObject` cannot touch a `final` field; the compiler rejects it.

Two `static final` declarations are special, not instance state:

- `serialVersionUID` — `static final long`; lives in the class descriptor used for compatibility.
- `serialPersistentFields` — must be `private static final ObjectStreamField[]`; **replaces** the default field list. Inner classes cannot declare it (they may only have compile-time constant `static` fields).

Enums do not transmit field values at all. Records serialize component values (those components are implicit `final`) and reconstruct through the canonical constructor — [[How does Java serialization treat record classes]].

```java
import java.io.Serializable;

class Account implements Serializable {
    private static final long serialVersionUID = 1L;

    static int opened;
    final String id;
    transient final String secret;

    Account(String id, String secret) {
        this.id = id;
        this.secret = secret;
        opened++;
    }
}
```

**Listing 1.** `opened` is a class variable: not in the instance stream. `id` is a `final` instance field: default-serialized. `secret` is `transient final`: omitted, then left at `null` because constructors do not run.

```d2
direction: down
cls: "Serializable class fields" {
  width: 240
  height: 44
  style.fill: "#fff8e1"
}
keep: "non-static, non-transient\n(including instance final)" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
drop: "static (any) / transient" {
  width: 240
  height: 44
  style.fill: "#ffcdd2"
}
meta: "serialVersionUID\nserialPersistentFields" {
  width: 240
  height: 55
  style.fill: "#e3f2fd"
}
cls -> keep: "instance bytes"
cls -> drop: "not default serial fields"
cls -> meta: "class descriptor / field list"
```

**Fig. 1.** Default instance data is selected by `static` and `transient`. `final` does not drop a field. The two well-known `static final` names are protocol metadata.

```java
private void readObject(java.io.ObjectInputStream in)
        throws java.io.IOException, ClassNotFoundException {
    in.defaultReadObject();
    // secret = "";  // compile error: cannot assign to final
}
```

**Listing 2.** Conceptual (inside `Account`). `defaultReadObject` restores `id`. It cannot restore `secret`, and you cannot assign a `final` field here.

`Externalizable` reconstruction is a **public no-arg constructor**, then `readExternal`. A blank `final` must be definitely assigned in that constructor. Afterward `this.id = in.readUTF()` does not compile — there is no `defaultReadObject` on this path. Reflection can still write a non-static `final` during deserialization; ordinary assignment cannot. You *can* write a `static` from `writeExternal` and assign a **non-final** `static` in `readExternal`; that mutates class state for every instance in the VM. Protocol: [[How do you implement a custom serialization protocol in Java]].

```java
import java.io.Externalizable;
import java.io.IOException;
import java.io.ObjectInput;
import java.io.ObjectOutput;

public class ExtId implements Externalizable {
    private final String id;

    public ExtId() {
        this.id = "";
    }

    @Override
    public void writeExternal(ObjectOutput out) throws IOException {
        out.writeUTF(id);
    }

    @Override
    public void readExternal(ObjectInput in)
            throws IOException, ClassNotFoundException {
        in.readUTF();
        // this.id = in.readUTF();  // compile error: final, already assigned
    }
}
```

**Listing 3.** The UTF on the stream cannot land in `id`. Default `Serializable` can restore that `final`; this protocol cannot without special (reflective) assignment.

> [!warning] `final` is not “skip this field”
> A common interview slip is “static and final fields are not serialized.” Only **`static` and `transient`** are omitted from the default list. A `final String id` round-trips like any other instance field.

> [!warning] `transient final` stays at the type default
> After default deserialization the field is `0` / `null` / `false`. `readObject` cannot assign it. If the declaration used a constant expression (`final int n = 7`), even a later reflective write may be invisible because uses were inlined at compile time.

> [!warning] `readExternal` into a `static` is a class-wide write
> Every instance sees the new value. Two objects deserialized in one VM do not get two copies of a `static`.

> [!tip] Interview answer
> Static fields are class state, so default Java serialization skips them; the deserialized object sees the receiving JVM’s current statics. Final instance fields are still written unless they are also static or transient. serialVersionUID is a special static final long in the class descriptor, not an instance field. Externalizable is the exception for finals: the no-arg constructor must initialize them, and readExternal cannot assign them again.
