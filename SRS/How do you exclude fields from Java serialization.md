<!--
reps: 0
priority: 0
-->
#Java/Serialization/Transient #Java/Language/Modifiers #SRS

# How do you exclude fields from Java serialization?

> [!abstract] Short answer
> **For default `Serializable` serialization, mark the instance field `transient`.** Default serializable fields are the non-`transient` and non-`static` ones. To omit a field that is not `transient`, declare `serialPersistentFields` without that name, or switch to `Externalizable` and never write it. `final` does not exclude a field: [[How do static and final fields affect Java serialization]]. What `transient` means: [[How would you explain the transient field modifier in Java]].

## Three ways to keep a value out of the stream

**1. `transient` (usual).** The language marks the field as not persistent. `ObjectOutputStream` skips it; `ObjectInputStream` does not assign it. After deserialize the slot is the type default (`0` / `null` / `false`) because constructors and instance initializers of a serializable class **do not run**. Restore derived state in `readObject`. Sensitive data is often `private transient` so it cannot reappear from the stream.

**2. `serialPersistentFields`.** A `private static final ObjectStreamField[]` **replaces** the default list. Leave a live field off that array and it is not a serial field, even without `transient`. Name a `transient` field in the array and it **is** written. Wrong modifiers, or a null array, and the declaration is ignored — every default field is written again. Inner classes cannot declare this array.

**3. You write the bytes.** `writeObject` still emits every default serial field if you call `defaultWriteObject`. Exclusion there means reshaping the list (above) or not using the default list: `PutField` only for declared serial names, or `Externalizable.writeExternal` that simply does not output the value — [[How do you implement a custom serialization protocol in Java]].

`static` fields are already omitted (class state, not instance serial fields). Do not make a field `static` in order to hide it.

Records ignore `transient` / `serialPersistentFields` / `writeObject`: every **component** is in the form. Enums write only the constant name.

```java
import java.io.Serializable;

class Session implements Serializable {
    private static final long serialVersionUID = 1L;
    String user;
    transient char[] password;
    transient int cachedHash;
}
```

**Listing 1.** `user` is a default serial field. `password` and `cachedHash` are excluded. After default deserialization they are `null` and `0`.

```java
import java.io.ObjectStreamField;
import java.io.Serializable;

class Account implements Serializable {
    private static final long serialVersionUID = 1L;
    String id;
    String secret;

    private static final ObjectStreamField[] serialPersistentFields = {
        new ObjectStreamField("id", String.class)
    };
}
```

**Listing 2.** `secret` is a live instance field but not a serial field. Same stream effect as `transient` on `secret`, without that modifier.

```d2
direction: down
live: "live instance fields" {
  width: 220
  height: 40
  style.fill: "#fff8e1"
}
keep: "non-static, non-transient\nin serialPersistentFields if declared" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
drop: "transient / static\nor omitted from serialPersistentFields" {
  width: 280
  height: 55
  style.fill: "#ffcdd2"
}
live -> keep: "instance bytes"
live -> drop: "not in the stream"
```

**Fig. 1.** Exclusion is a property of the **serial field list**, not of `final`. Customizing that list: [[How do you customize default Java serialization behavior]].

> [!warning] Excluded is not “re-initialized”
> `transient List<String> cache = new ArrayList<>();` becomes `null` on the way back. Re-create it in `readObject` (or lazily). A `transient final` field cannot be assigned there at all.

> [!warning] Records cannot drop a component
> The serialized form is the component values. `writeObject` and `serialPersistentFields` are ignored. If a value must not hit the stream, do not make it a component — wrap it, or use `writeReplace`.

> [!tip] Interview answer
> Exclude a field from default Java serialization by marking it transient, or by listing serialPersistentFields without it. Static fields are skipped anyway because they are not instance serial fields. After deserialize, excluded fields are type defaults; restore anything you still need in readObject.
