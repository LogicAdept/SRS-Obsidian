<!--
reps: 0
priority: 0
-->
#Java/Language/Optional/Usage #Java/Serialization #SRS

# Is `Optional` serializable?

> [!abstract] Short answer
> **No. `java.util.Optional` does not implement `java.io.Serializable`.** Writing an `Optional` instance with `ObjectOutputStream` throws `NotSerializableException`. Keep a nullable field (or `transient` plus custom write/read) and return `Optional` from the getter.

## The class is not `Serializable`; the graph still walks it

Serializability is opt-in: a class is serializable only if it implements `Serializable` ([[What is Optional]]). `Optional` is `public final class Optional<T> extends Object` — no `Serializable`. It is a value-based type whose documented job is a **method return type**, not a stored field.

When the serialization runtime walks an object graph and hits an instance that is not `Serializable`, it throws `NotSerializableException` and names that class. A non-null, non-`transient` `Optional` field is such an instance — including `Optional.empty()`. Empty is an object, not `null`. A `null` field writes a null token and does not require the field type to be `Serializable`; that is not a present `Optional`, and a variable of type `Optional` is not supposed to be `null`.

`transient` skips the field on default write, then deserialization leaves it `null` (the default for a reference), which again contradicts “never `null`.” If you must persist absence, store the inner value (`String`, `Long`, …) and expose `Optional.ofNullable` from the accessor ([[What are Optional.ofNullable and Optional.empty]], [[Why should you not use Optional as a field or method parameter]], [[Why should a method that returns Optional never return null]]). Custom `writeObject` / `readObject` can do the same: write the unwrapped value, not the box.

```d2
direction: down
opt: "Optional instance\n(empty or present)" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
nse: "NotSerializableException\njava.util.Optional" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
ok: "nullable String field\ngetter returns Optional" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
write: "ObjectOutputStream" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
opt -> nse
ok -> write
```

**Fig. 1.** Default Java serialization fails on a live `Optional`. Persist the nullable value; return the box.

```java
import java.io.Serializable;
import java.util.Optional;

class AccountBroken implements Serializable {
    private static final long serialVersionUID = 1L;
    Optional<String> email;
}

class AccountOk implements Serializable {
    private static final long serialVersionUID = 1L;
    private final String email;

    AccountOk(String email) {
        this.email = email;
    }

    Optional<String> getEmail() {
        return Optional.ofNullable(email);
    }
}
```

**Listing 1.** `AccountBroken` compiles: `Serializable` is not checked against field types by the compiler. `ObjectOutputStream.writeObject` throws `NotSerializableException` once `email` holds `Optional.empty()` or `Optional.of(...)`. `AccountOk` serializes a `String` (null means absent) and still returns `Optional` from the getter.

> [!warning] `Optional.empty()` is not a free pass
> Empty still serializes as an `Optional` object. Only a `null` reference, a `transient` field, or custom write/read avoids writing that object — and `null` / default-deserialized `transient` is a null `Optional` field, which the API tells you not to have.

> [!warning] This is `java.io.Serializable`, not “any mapper”
> JSON, JPA, or DTO libraries have their own rules. The Java SE answer is: `Optional` is not `Serializable`; default Java serialization of a boxed field fails. Do not treat a working JSON getter as proof the type is serializable.

> [!tip] Interview answer
> **`Optional` is not `Serializable`.** Putting one in a serializable bean throws `NotSerializableException` at write time, even for `Optional.empty()`. Store the nullable value and return `Optional` from the method; that matches how the type is meant to be used.
