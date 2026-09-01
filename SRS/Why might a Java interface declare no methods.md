<!--
reps: 0
priority: 0
-->
#Java/Annotations #Java/OOP/Interfaces #SRS

# Why might a Java interface declare no methods?

> [!abstract] Short answer
> To be a **marker**: an empty **type** whose meaning is **membership**, not a list of operations. Code (or the runtime) tests **`instanceof`**, takes the type as a parameter, or special-cases it — `Object.clone` and **`Cloneable`**, serialization and **`Serializable`**, list algorithms and **`RandomAccess`**. `Cloneable` still declares **no** `clone()`. Markers: [[How would you explain marker interfaces and why annotations largely replaced them]]. `clone`: [[Why is clone declared on Object rather than on Cloneable]].

## Empty body, still a type

An interface may declare **no members**. Classes `implement` it. That is enough for:

- **`instanceof` / casts / generic bounds**
- **API parameters** (`void accept(Tag t)`)
- **hooks that already exist elsewhere** (`clone` on `Object`, the serialization stream)

You omit methods when there is **no operation** for implementors to write. The behavior lives in the JVM or in callers that branch on the type ([[How would you explain marker interfaces and why annotations largely replaced them]]).

**New tags.** If the tag need not be a **type**, a **marker annotation** (`@interface` with no elements) is the usual Java 5+ tool. Keep an empty **interface** when `instanceof` or a parameter type is the contract.

If callers should invoke behavior, declare the methods ([[What kinds of methods can a Java interface declare]]).

```d2
direction: down
empty: "interface with no methods" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
hook: "instanceof / clone / serialize" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}
empty -> hook: "type tag"
```

**Fig. 1.** No methods means “treat this type specially,” not “call these operations.”

```java
import java.io.Serializable;

class Packet implements Serializable {
    int n;
}

class Demo {
    static boolean serializable(Object o) {
        return o instanceof Serializable;
    }
}
```

**Listing 1.** `Serializable` has no methods. `Packet` is tagged so the stream (and `instanceof`) can see the type.

> [!warning] `Cloneable` is not a `clone()` contract
> Implementing it allows `Object.clone` to copy fields; otherwise `CloneNotSupportedException`. There is no `clone()` on the interface.

> [!warning] Empty is not an unfinished interface
> A marker without any code that tests the type does nothing. Do not ship a barren interface “for later methods.”

> [!warning] Do not replace `Serializable` with an annotation
> The stream looks for the **interface**. Prefer annotations for new metadata that is not a type.

> [!tip] Interview answer
> An interface with no methods is a marker type: it only classifies instances. `Cloneable`, `Serializable`, and `RandomAccess` are the usual JDK examples. `Cloneable` does not declare `clone()`. For new metadata that need not be a type, use a marker annotation.
