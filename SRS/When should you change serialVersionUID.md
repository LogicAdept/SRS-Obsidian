<!--
reps: 0
priority: 0
-->
#Java/Serialization/SerialVersionUID #SRS

# When should you change serialVersionUID?

> [!abstract] Short answer
> **Change it when the serial form is intentionally incompatible** and you want old streams to fail immediately with `InvalidClassException`. **Keep it unchanged** for compatible evolution (adding a field, `static`→instance, `transient`→non-`transient`, adding `writeObject` that still writes default field data). Role of the stamp: [[What is the role of serialVersionUID in Java serialization]]. Compatible vs incompatible lists: [[How do you design a custom Java serialization format]].

## Same UID means “I still read your stream”

Compatible versions of a class **must** declare the SUID they can still read and write. The value is fixed across those versions. Deserialization compares the descriptor in the stream with the local class; a different `long` aborts before field restore.

Bump the constant when you **break** that contract on purpose, for example:

- changing the declared type of a primitive serial field
- switching `Serializable` ↔ `Externalizable`
- dropping default field data from `writeObject` / `readObject` after it used to appear (or the reverse)
- moving the class up or down the hierarchy
- deleting a serial field that older readers still need to fulfill their contract

Then old files and new class (or new files and old class) fail fast instead of restoring defaults and limping.

Do **not** bump when you only add a serial field (missing values become type defaults), add a class in the hierarchy, or add `readObject` that still calls `defaultReadObject`. Those are compatible if the UID stays put.

```java
import java.io.Serializable;

class Point implements Serializable {
    private static final long serialVersionUID = 1L;
    int x;
    int y; // added later — keep 1L
}
```

**Listing 1.** Adding `y` is a compatible change. Leave `serialVersionUID` at `1L` so streams written with only `x` still load (`y` becomes `0`).

```java
class Point implements Serializable {
    private static final long serialVersionUID = 2L; // was 1L
    long x; // was int — incompatible
}
```

**Listing 2.** Conceptual (renamed in place). A new UID makes `InvalidClassException` the result, rather than a type mismatch inside field data. Process: [[How does serialization and deserialization with Serializable work]].

```d2
direction: down
chg: "class change" {
  width: 180
  height: 36
  style.fill: "#fff8e1"
}
ok: "compatible\nkeep the same UID" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
bad: "incompatible form\nnew serialVersionUID" {
  width: 260
  height: 50
  style.fill: "#ffcdd2"
}
chg -> ok
chg -> bad
```

**Fig. 1.** The UID is a compatibility **gate**, not a changelog. `Externalizable` payload versions still belong in your bytes; the UID only identifies the class descriptor.

Enums ignore a declared UID (`0L`). Records default to `0L` and **waive matching**, so bumping a record UID is not the usual failure mode. Arrays cannot declare one. What serialization is: [[What is serialization]].

> [!warning] Bumping on every source edit breaks readers
> Adding a method or a `transient` cache is not an incompatible serial-form change. If you also rely on a **computed** default UID, that hash *will* move and old files will fail — pin a literal and leave it.

> [!warning] Not bumping after a real layout break is not “kind”
> Deleting a serial field without a new UID is still incompatible: the new writer omits the value, and an older class restores `0` / `null` / `false` instead of failing. Older readers may also see type errors or a stream they cannot skip. A new UID makes that failure an `InvalidClassException`.

> [!tip] Interview answer
> Change serialVersionUID only when you intentionally break the serialized form and want InvalidClassException instead of a corrupt restore. Keep the same value when you add fields or other compatible changes. Never leave it to the default compiler hash if you care about old streams.
