<!--
reps: 0
priority: 0
-->
#Java/Serialization #SRS

# Why is Java object serialization used?

> [!abstract] Short answer
> **To store or send a live object graph and get an equivalent graph back** — files and blobs for persistence, sockets for another host or process, and marshaling of arguments in remote calls. The stream keeps types, field values, and sharing (including cycles). What it is: [[What is serialization]]. The binary protocol: [[How would you explain Java binary serialization]].

## Persistence, the wire, and remote arguments

Most applications need to save objects and restore them later. Serialization represents enough state to reconstruct the objects **and** the references between them. One stream format does that job.

Typical uses of `ObjectOutputStream` / `ObjectInputStream`:

- **Persistence** — pair with `FileOutputStream` / `FileInputStream` (or a database blob) so a graph survives the process.
- **Sockets** — pass objects to another host or JVM; the receiver reconstitutes a matching graph.
- **Remoting** — marshal and unmarshal arguments and return values for a remote communication system.

The protocol is meant to stay simple for the default case (opt in with `Serializable`, customize only when a class needs it) while still encoding Java types, not a raw heap dump. Handles preserve identity: two fields that pointed at the same instance still do after deserialize.

```java
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectOutputStream;
import java.time.LocalDateTime;

class Snapshot {
    static void save(String path) throws IOException {
        try (ObjectOutputStream oos =
                     new ObjectOutputStream(new FileOutputStream(path))) {
            oos.writeObject("Today");
            oos.writeObject(LocalDateTime.now());
        }
    }
}
```

**Listing 1.** Persistence of a small graph: a string and a `LocalDateTime`. The same pairing on a socket stream is the remoting case. How restore works: [[How does serialization and deserialization with Serializable work]].

```d2
direction: down
why: "need the same graph later or elsewhere" {
  width: 300
  height: 44
  style.fill: "#fff8e1"
}
file: "file / blob persistence" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
sock: "socket / process boundary" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
rmi: "marshal remote arguments" {
  width: 240
  height: 40
  style.fill: "#ffecb3"
}
why -> file
why -> sock
why -> rmi
```

**Fig. 1.** Java object serialization is used where a JVM must freeze or ship **typed object graphs**, not where you only need language-neutral JSON.

It is a poor default for **untrusted** input: deserialization can run `readObject`, `readResolve`, and class loading. Do not use it as an open interchange format with strangers — [[How do you prevent a Java class from being serialized]].

> [!warning] “Used for persistence” is not “safe checkpoint”
> The bytes name your classes and restore private fields. A file from an older, incompatible class fails (`serialVersionUID`) or comes back without constructors having run. Treat stored graphs as trusted, versioned data.

> [!warning] Not a general network schema
> Another language cannot consume `0xACED` class descriptors as a public API. For cross-language services, this protocol is the wrong tool.

> [!tip] Interview answer
> Java object serialization exists to persist object graphs and to send them across processes or as RMI-style arguments, keeping types and sharing intact. You opt in with Serializable so most classes need no extra code. Do not use it for untrusted bytes or as a language-neutral API.
