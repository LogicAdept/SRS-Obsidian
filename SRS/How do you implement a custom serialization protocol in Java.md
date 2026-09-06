<!--
reps: 0
priority: 0
-->
#Java/Serialization/Externalizable #SRS

# How do you implement a custom serialization protocol in Java?

> [!abstract] Short answer
> **Implement `java.io.Externalizable`:** a **public no-arg constructor**, `writeExternal(ObjectOutput)`, and `readExternal(ObjectInput)` that consume the **same types in the same order**. `ObjectOutputStream.writeObject` still writes the class identity; you write every value, including supertype state. Format design (version tags, named fields vs private bytes): [[How do you design a custom Java serialization format]]. Hook catalog: [[How do you customize Java serialization and deserialization]].

## The Externalizable contract

The stream tests `Externalizable` before ordinary `Serializable`. If the class implements it, `writeObject` / `readObject` are **superseded**. You do not get the default serial-field list or `transient` filtering.

Implementation checklist:

1. `implements Externalizable` (it already extends `Serializable`).
2. **Public** no-arg constructor — used on deserialize **before** `readExternal`. Inner classes that capture an enclosing instance cannot provide one.
3. `writeExternal` — `DataOutput` for primitives, `writeObject` for objects, strings, and arrays. Coordinate with the supertype explicitly; the container will not walk its serial fields for you.
4. `readExternal` — mirror that sequence. Wrong order or type is a corrupt object or an `IOException` / `ClassNotFoundException`.
5. Optional `writeReplace` / `readResolve` still apply. Pin `serialVersionUID` if you need a stable class id. A leading format `int` in the payload is how **you** version the bytes; that is not `serialVersionUID`.

Enums never take this path (name only). Records ignore `writeExternal` / `readExternal`. Pairing with the other hooks: [[How do you customize Java serialization and deserialization]].

```java
import java.io.Externalizable;
import java.io.IOException;
import java.io.ObjectInput;
import java.io.ObjectOutput;

public class Packet implements Externalizable {
    private String type;
    private byte[] payload;

    public Packet() {}

    public Packet(String type, byte[] payload) {
        this.type = type;
        this.payload = payload.clone();
    }

    @Override
    public void writeExternal(ObjectOutput out) throws IOException {
        out.writeUTF(type);
        out.writeInt(payload.length);
        out.write(payload);
    }

    @Override
    public void readExternal(ObjectInput in)
            throws IOException, ClassNotFoundException {
        type = in.readUTF();
        int n = in.readInt();
        payload = new byte[n];
        in.readFully(payload);
    }
}
```

**Listing 1.** Length-prefixed custom payload. `readFully` is on `DataInput` (`ObjectInput` extends it). Use `writeObject` / `readObject` when a field is a graph, not a primitive.

```d2
direction: down
call: "ObjectOutputStream.writeObject(packet)" {
  width: 300
  height: 44
  style.fill: "#e3f2fd"
}
id: "class descriptor" {
  width: 220
  height: 40
  style.fill: "#fff8e1"
}
w: "packet.writeExternal" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
ctor: "new Packet()  // public no-arg" {
  width: 260
  height: 44
  style.fill: "#ffecb3"
}
r: "packet.readExternal" {
  width: 220
  height: 40
  style.fill: "#c8e6c9"
}
call -> id -> w
w -> ctor: "deserialize"
ctor -> r
```

**Fig. 1.** You implement the content protocol. The stream still supplies the class descriptor and, on the way in, the public no-arg constructor. This is not a new magic header, and it is not `DataOutputStream` or JSON used alone.

`writeObject` on `Serializable` is not this protocol: it still sits on named serial fields plus optional data — [[How do you customize default Java serialization behavior]].

> [!warning] Public constructor, public methods
> Anyone who can reach an `ObjectOutput` / `ObjectInput` can call `writeExternal` / `readExternal`. The no-arg constructor cannot enforce invariants — check them again in `readExternal`. Negative length or a truncated `readFully` must fail the object, not allocate blindly.

> [!warning] `transient` does not apply
> Default field serialization looks at `transient` and `static`. `writeExternal` does not. If you write a secret, it is in the stream. Skipping a field is your code’s job: [[How would you explain the transient field modifier in Java]].

> [!warning] Superclass fields are not automatic
> If the superclass has state, `writeExternal` must persist it (call `super.writeExternal` when the super is Externalizable, or write accessible fields). Switching a class from `Serializable` to `Externalizable` is an incompatible stream change.

> [!tip] Interview answer
> Implement Externalizable: public no-arg constructor, writeExternal, and a matching readExternal. ObjectOutputStream still records the class; you record the data, including superclass state, in a fixed order. That replaces writeObject, which only customizes the default field protocol.
