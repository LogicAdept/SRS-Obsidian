<!--
reps: 0
priority: 0
-->
#Java/Serialization/SerialVersionUID #SRS

# What is the role of serialVersionUID in Java serialization?

> [!abstract] Short answer
> **`serialVersionUID` is the class’s stream version stamp.** On deserialize, the runtime compares the UID in the stream’s class descriptor with the local class. A mismatch throws `InvalidClassException`. Declare `private static final long serialVersionUID` so compatible revisions keep the same number. It is not instance data: [[How do static and final fields affect Java serialization]]. Where it sits in the binary stream: [[How would you explain Java binary serialization]].

## Compatibility id, not a serial field

Each serializable class is associated with a 64-bit Stream Unique Identifier. Later compatible versions must keep the UID they can still read and write. The value is stored on `ObjectStreamClass` (`getSerialVersionUID`) and written with the class name in the descriptor — before field bytes.

If the class does not declare one, the runtime **computes** a default: a SHA-1 hash of the class name, modifiers, interfaces, fields, constructors, and methods. `private static` and `private transient` fields are omitted from that field list. Compilers differ in synthetic members, so two “same” sources can disagree — unexpected `InvalidClassException`. Declare it explicitly. `serialver` prints a copy-pasteable constant.

```java
import java.io.Serializable;

class Point implements Serializable {
    private static final long serialVersionUID = 1L;
    int x, y;
}
```

**Listing 1.** Required shape: `static`, `final`, `long`. Any access modifier works; `private` is advised because the field is not a useful inherited member. Adding `y` later stays compatible **if** this UID is unchanged and you only add a serial field.

```java
ANY-ACCESS-MODIFIER static final long serialVersionUID = 42L;
```

**Listing 2.** Conceptual — the signature `Serializable` documents. Not an interface member; the runtime looks it up by name.

Special cases: enum types and dynamic proxies are `0L` (declarations ignored for enums). Record default is `0L`; an explicit UID is allowed, but **matching is waived**. Array classes cannot declare one; matching is waived. Default protocol walk: [[How does serialization and deserialization with Serializable work]]. Records: [[How does Java serialization treat record classes]].

```d2
direction: down
stream: "class descriptor in the stream\nname + serialVersionUID" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
local: "local class UID\n(declared or computed)" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
ok: "same → restore fields" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
bad: "different → InvalidClassException" {
  width: 280
  height: 44
  style.fill: "#ffcdd2"
}
stream -> local
local -> ok
local -> bad
```

**Fig. 1.** Role: verify sender and receiver loaded **compatible** class versions. It does not version your `Externalizable` payload; that format is yours.

Bump the constant only when you **intend** incompatibility. Compatible field adds keep the same UID. What serialization is: [[What is serialization]].

> [!warning] Default UID tracks the compiler
> Adding a method, changing access, or a different `javac` can change the hash even when the serial fields did not. Then old files fail to load. Pin a literal.

> [!warning] Same UID does not mean the same bytes
> Matching UIDs only pass the version check. Incompatible layout changes (type of a primitive field, `Serializable` ↔ `Externalizable`) still break at restore. Records will not fail this check by default (`0L`, matching waived).

> [!tip] Interview answer
> serialVersionUID is a long stamped on the class descriptor so deserialization can reject an incompatible class revision with InvalidClassException. Declare private static final long serialVersionUID yourself; the default hash is too sensitive to compiler details. Enums are 0L; records default to 0L and skip the match.
