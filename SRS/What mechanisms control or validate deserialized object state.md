<!--
reps: 0
priority: 0
-->
#Java/Serialization/Validation #Java/Security #SRS

# What mechanisms control or validate deserialized object state?

> [!abstract] Short answer
> **Class hooks restore and check state; a late callback checks the whole graph.** In `readObject` (after `defaultReadObject`) you assign and reject bad fields. `readObjectNoData` initializes when this class is missing from the stream. `readResolve` can replace the instance. `registerValidation` runs `ObjectInputValidation.validateObject` **after the graph is complete**. Records run the canonical constructor instead. For confidentiality wrap in `SealedObject`; for integrity wrap in `SignedObject`. Process: [[How does serialization and deserialization with Serializable work]]. Hook catalog: [[How do you customize Java serialization and deserialization]].

## Restore, then prove the object is legal

Serializable-class constructors do not run, so invariants that lived in `new` must be enforced on the way in.

| When | Mechanism |
| --- | --- |
| Per class, while reading this class’s data | `readObject` — restore fields, recompute `transient`s, throw `InvalidObjectException` / `IOException` |
| This class absent from the stream (evolution or a hostile stream) | `readObjectNoData` |
| You own every byte | `readExternal` — same duty, after the public no-arg constructor |
| After this object is built, before it is returned | `readResolve` — substitute a known instance ([[What is the singleton serialization problem]]) |
| After **every** object in the graph is restored | `in.registerValidation(this, prio)` → `validateObject()` |
| Record | Canonical constructor with component values ([[How does Java serialization treat record classes]]) |

`registerValidation` is legal only from `readObject` (`NotActiveException` otherwise). Higher `prio` runs first; `0` is the usual default. `validateObject` throws `InvalidObjectException` if the object cannot be made valid — that aborts validation and the `readObject` call. Use it for checks that need **other** graph nodes already restored. Single-object field checks can stay in `readObject`.

```java
import java.io.IOException;
import java.io.InvalidObjectException;
import java.io.ObjectInputStream;
import java.io.ObjectInputValidation;
import java.io.Serializable;

class Range implements Serializable, ObjectInputValidation {
    private static final long serialVersionUID = 1L;
    int lo, hi;

    private void readObject(ObjectInputStream in)
            throws IOException, ClassNotFoundException {
        in.defaultReadObject();
        in.registerValidation(this, 0);
    }

    @Override
    public void validateObject() throws InvalidObjectException {
        if (lo > hi) {
            throw new InvalidObjectException("lo > hi");
        }
    }
}
```

**Listing 1.** `defaultReadObject` fills `lo` and `hi`. The constructor that would have rejected `lo > hi` never ran. Validation runs after the full graph is reconstituted.

```d2
direction: down
read: "readObject / readExternal\nrestore fields" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
rr: "readResolve\n(optional substitute)" {
  width: 240
  height: 44
  style.fill: "#fff8e1"
}
graph: "entire graph complete" {
  width: 220
  height: 40
  style.fill: "#ffe0b2"
}
val: "validateObject callbacks\nby priority" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
read -> rr -> graph -> val
```

**Fig. 1.** Control the bytes first, then validate. `resolveObject` on a stream subclass is substitution, not `validateObject`.

`ObjectInputFilter` (stream or JVM-wide) can reject **classes**, array lengths, depth, reference counts, and bytes — it does not check `lo <= hi`. It is a gate on what may be instantiated, not a replacement for `validateObject`.

Cryptographic wrappers sit **outside** those class hooks. `javax.crypto.SealedObject` serializes any `Serializable`, then encrypts with a fully initialized `Cipher`; `getObject(Key)` or `getObject(Cipher)` decrypts and deserializes — confidentiality, with the key kept off the stream. `java.security.SignedObject` is a deep copy in serialized form plus a signature from a `PrivateKey` and a `Signature` engine; `verify(PublicKey, Signature)` must succeed before you trust `getObject()` — integrity / authenticity, not secrecy. Nested signed objects are allowed. Field restore: [[How do you customize default Java serialization behavior]].

Do not call overridable instance methods from `readObject` / `readObjectNoData`: dispatch uses the real type, so a subclass method can run before that subclass’s state is restored.

> [!warning] Field defaults are not validated for you
> Missing stream fields become `0` / `null` / `false`. A `transient` cache stays `null`. If that state is illegal, `readObject` or `validateObject` must fail the object.

> [!warning] `readObject` is too early for some invariants
> Cross-object rules (this node’s `parent` must already point back) belong in `validateObject` after the graph exists. Registering outside `readObject` throws `NotActiveException`. A class that only implements `ObjectInputValidation` is never called.

> [!warning] `SignedObject` is not a symmetric key
> Signing uses a **private** key; verification uses the matching **public** key. A malicious custom `Signature` engine can always return `true` — use a real provider. `SealedObject` is encryption (`Cipher`); it does not replace a signature.

> [!tip] Interview answer
> After deserialize, constructors of a serializable class have not run, so you validate in readObject, readObjectNoData, or readExternal, and you can registerValidation so validateObject runs once the whole graph is up. readResolve can swap in a known instance. Filters limit which classes load; they do not check your fields. Wrap in SealedObject for confidentiality or SignedObject for integrity, and keep the keys off the stream.
