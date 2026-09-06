<!--
reps: 0
priority: 0
-->
#Java/Serialization #SRS

# How do you customize Java serialization and deserialization?

> [!abstract] Short answer
> **Pair a write-side hook with its read-side counterpart.** On the class: `writeObject`/`readObject` (optional `readObjectNoData`) wrap default fields; `writeExternal`/`readExternal` own the payload; `writeReplace`/`readResolve` swap the instance. On a **trusted stream subclass**: `replaceObject`/`resolveObject` after `enableReplaceObject`/`enableResolveObject`. Default-field details: [[How do you customize default Java serialization behavior]]. Full payload protocol: [[How do you implement a custom serialization protocol in Java]].

## Three layers, always in pairs

Java object serialization does not have a single “customize” API. The runtime looks up **matching** hooks.

**1. Default field protocol (`Serializable`).** `writeObject` runs instead of automatic `defaultWriteObject`; `readObject` instead of automatic `defaultReadObject`. Each must call `defaultWriteObject`/`putFields` or `defaultReadObject`/`readFields` **once** before extra bytes. `transient` and `serialPersistentFields` change which fields that default step sees. `readObjectNoData` is the deserialize-only sibling when this class is absent from the stream’s superclass list.

**2. Externalizable payload.** The stream checks `Externalizable` first. Only class identity is written by the container; `writeExternal` / `readExternal` save and restore **all** state (including coordinating with supertypes) and **supersede** `writeObject` / `readObject`. Deserialize: **public** no-arg constructor (it **does** run), then `readExternal`. Same types, same order. Inner classes that capture an enclosing instance cannot supply that constructor. Ordinary `Serializable` deserialization runs only the first **non-serializable** supertype’s no-arg constructor.

**3. Substitution.** Class-level `writeReplace` (before the object is written) and `readResolve` (after it is fully built, before return) nominate a substitute — [[What is the singleton serialization problem]]. Stream-level `ObjectOutputStream.replaceObject` / `ObjectInputStream.resolveObject` do the same for **every** object the first time it is written or returned, but only after the subclass enables replacement. `writeObject(Object)` takes `Object` so a non-serializable original can be replaced by a serializable stand-in.

```java
private void writeObject(java.io.ObjectOutputStream out)
        throws java.io.IOException { /* … */ }
private void readObject(java.io.ObjectInputStream in)
        throws java.io.IOException, ClassNotFoundException { /* … */ }
private void readObjectNoData()
        throws java.io.ObjectStreamException { /* … */ }
ANY-ACCESS-MODIFIER Object writeReplace()
        throws java.io.ObjectStreamException { /* … */ }
ANY-ACCESS-MODIFIER Object readResolve()
        throws java.io.ObjectStreamException { /* … */ }
public void writeExternal(java.io.ObjectOutput out)
        throws java.io.IOException { /* … */ }
public void readExternal(java.io.ObjectInput in)
        throws java.io.IOException, ClassNotFoundException { /* … */ }
```

**Listing 1.** Conceptual. Class hooks are magic signatures, not `Serializable` methods. `Externalizable` methods are real interface methods.

```java
import java.io.IOException;
import java.io.ObjectOutputStream;
import java.io.OutputStream;

final class SubstitutingOutput extends ObjectOutputStream {
    SubstitutingOutput(OutputStream out) throws IOException {
        super(out);
        enableReplaceObject(true);
    }

    @Override
    protected Object replaceObject(Object obj) throws IOException {
        return obj;
    }
}
```

**Listing 2.** Stream-level write-side substitute. Pair with `ObjectInputStream.enableResolveObject(true)` and `resolveObject`. Replacement is off until enabled; the enable check is for trusted streams (`SerializablePermission "enableSubstitution"` when not in the system domain).

```d2
direction: down
ser: "serialize" {
  width: 200
  height: 36
  style.fill: "#e3f2fd"
}
de: "deserialize" {
  width: 200
  height: 36
  style.fill: "#e8f5e9"
}
ser -> de: "writeObject ↔ readObject"
ser -> de: "writeExternal ↔ readExternal"
ser -> de: "writeReplace ↔ readResolve"
ser -> de: "replaceObject ↔ resolveObject"
```

**Fig. 1.** Customization is a pair. Unmatched extra bytes on write become `OptionalDataException` / EOF on read.

Enums ignore class-level `writeObject` / `readObject` / `readObjectNoData` / `writeReplace` / `readResolve`. Records ignore `writeObject` / `readObject` / `readExternal` but still honor `writeReplace` / `readResolve` — [[How does Java serialization treat record classes]]. `replaceObject` is not invoked for `Class` or `ObjectStreamClass`; `resolveObject` is not invoked for `Class`, `ObjectStreamClass`, `String`, or arrays.

`serialPersistentFields` is a narrower knob: it replaces the **default field list** without changing the protocol. `static` / `final` still follow the usual rules: [[How do static and final fields affect Java serialization]]. `transient`: [[How would you explain the transient field modifier in Java]].

> [!warning] Class hooks do not customize the stream
> `writeReplace` is the object nominating a stand-in. `replaceObject` is the **stream** nominating one, and it is disabled by default. Mixing them: `writeReplace` runs first; if enabled, `replaceObject` is then called with that replacement.

> [!warning] `writeObject` does not write fields by itself
> Defining it **replaces** the automatic `defaultWriteObject` call. If you omit `defaultWriteObject` / `writeFields`, the matching `readObject` has no default field data. Extra `writeInt` / `writeObject` bytes are optional data, not serial fields. Unmatched extra bytes on write become `OptionalDataException` / EOF on read.

> [!warning] `readResolve` does not rewrite the graph
> It runs only after the object is fully constructed. Handles already pointing at the pre-resolve instance stay there. `writeReplace` *does* rewrite references in the replacement’s graph to the substitute.

> [!tip] Interview answer
> Customize Java serialization and deserialization in pairs: writeObject with readObject on Serializable, writeExternal with readExternal on Externalizable, writeReplace with readResolve to swap instances. A trusted ObjectOutputStream subclass can also replaceObject if you enable it, matched by resolveObject on the way in. Enums cannot use the class hooks; records keep only the replace/resolve pair.
