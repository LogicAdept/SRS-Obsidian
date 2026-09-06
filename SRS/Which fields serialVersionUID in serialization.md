<!--
reps: 0
priority: 0
-->
#Java/Serialization/SerialVersionUID #SRS

# Which fields serialVersionUID in serialization?

> [!abstract] Short answer
> **`serialVersionUID` is the class’s stream-compatibility stamp**, not a version of the payload bytes. If you omit it, the runtime **hashes** the class: name, modifiers, interfaces, fields, constructors, and methods. Field-wise, every field counts **except `private static` and `private transient`**. Declare `private static final long serialVersionUID` yourself so adding a method cannot throw `InvalidClassException`. Role: [[What is the role of serialVersionUID in Java serialization]].

## Stamp vs default hash

On deserialize, the UID in the class descriptor must match the local class or you get `InvalidClassException`. It does not version `writeExternal` contents; that is your format tag.

**Declared.** Looked up by name. Shape: `static final long`. `private` is recommended. This field is `private static`, so it is **not** one of the hashed fields.

**Computed (when absent).** SHA-1 over, in order: class name; class modifiers; interface names; then each field (name, modifiers, descriptor) **except `private static` and `private transient`**; `<clinit>` if present; non-private constructors; non-private methods. Compilers inject synthetics, so two builds can disagree.

```java
import java.io.Serializable;

class Account implements Serializable {
    private static final long serialVersionUID = 1L;
    String id;
    private transient char[] secret;
    private static int opened;
}
```

**Listing 1.** The literal `1L` is used. If this UID were omitted, `id` would enter the hash; `secret` (`private transient`) and `opened` (`private static`) would not. A package-private `static` *would* count.

```d2
direction: down
uid: "serialVersionUID" {
  width: 200
  height: 36
  style.fill: "#e3f2fd"
}
dec: "declared literal\nused as-is" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}
hash: "else SHA-1 of class\nfields except private static\nand private transient" {
  width: 280
  height: 70
  style.fill: "#fff8e1"
}
uid -> dec
uid -> hash
```

**Fig. 1.** “Which fields” for a **computed** UID is that hash input list, not the default serializable-field list (`transient` instance fields still hash unless they are `private transient`). When to bump a declared value: [[When should you change serialVersionUID]]. `static`/`final` vs instance bytes: [[How do static and final fields affect Java serialization]].

Enums and proxies are `0L`. Records default to `0L` and waive matching. Arrays cannot declare a UID. Binary descriptor: [[How would you explain Java binary serialization]].

> [!warning] Serial fields and hashed fields are different sets
> A public `transient` cache is omitted from the **stream** but still affects a **computed** UID. A `private static` counter is omitted from both the stream and the hash.

> [!warning] Adding a public method changes the default UID
> Serial fields can be unchanged and old files still fail. That is why the UID should be an explicit literal, not “whatever javac hashed.”

> [!tip] Interview answer
> serialVersionUID labels the class version in the stream so incompatible revisions throw InvalidClassException. Declare private static final long serialVersionUID; if you don’t, Java hashes almost every field except private static and private transient, plus methods and interfaces, which is far too brittle.
