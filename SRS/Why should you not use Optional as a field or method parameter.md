<!--
reps: 0
priority: 0
-->
#Java/Language/Optional/Usage #SRS

# Why should you not use `Optional` as a field or method parameter?

> [!abstract] Short answer
> **`Optional` is documented as a method *return* type for “no result,” not a general maybe-type for fields or parameters.** A field is an extra identity wrapper per instance and is not `Serializable`. A parameter forces callers to box, can still be `null` (defeating the type), and makes overloads clumsier than `greet()` / `greet(String)`.

## Return type, not a stored or incoming maybe

The class API note says `Optional` is **primarily intended for use as a method return type** where there is a clear need to represent “no result,” and that a variable of type `Optional` should never itself be `null` ([[What is Optional]], [[Why should a method that returns Optional never return null]]). Holding the return in a local while you `map` / `orElse` is normal. Storing `Optional` in a field, passing it as a parameter, or taking it as a constructor argument is using it as a general `T | absent` container — the job the note does not give it.

**Fields.** Each present `Optional` is a heap object around the value ([[What is the performance cost of Optional]]). `java.util.Optional` does not implement `Serializable`, so a non-transient `Optional` field in a serializable bean throws `NotSerializableException` when the box is written — including `Optional.empty()` ([[Is Optional serializable]]). Keep a nullable `String` (or whatever the payload is) and expose `Optional.ofNullable(nickname)` from the getter.

**Parameters.** The caller must write `Optional.of` / `ofNullable` at every call site. Nothing stops `greet(null)`: the parameter is still a reference, so the method must null-check the `Optional` itself — the failure mode `Optional` was meant to remove. Two overloads (`greet()` and `greet(String name)`) or a nullable `String` keep absence in the type system you already have, without a wrapper argument.

```d2
direction: down
ret: "return Optional<T>\n(documented use)" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
field: "field Optional<T>" {
  width: 260
  height: 50
  style.fill: "#ffebee"
}
param: "parameter Optional<T>" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}
ser: "not Serializable\nextra wrapper" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
npe: "caller can pass null\nmust box at every site" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
field -> ser
param -> npe
```

**Fig. 1.** Return is the intended slot. Field and parameter reintroduce wrapping, serialization, and a nullable `Optional`.

```java
import java.io.Serializable;
import java.util.Optional;

class UserAvoid {
    Optional<String> nickname;
}

class UserOk implements Serializable {
    private static final long serialVersionUID = 1L;
    private String nickname;

    Optional<String> nickname() {
        return Optional.ofNullable(nickname);
    }
}

class Greeter {
    void greetAvoid(Optional<String> name) {
        name.ifPresent(System.out::println);
    }

    void greet() {
        System.out.println("friend");
    }

    void greet(String name) {
        System.out.println(name);
    }
}
```

**Listing 1.** `UserAvoid.nickname` is the field anti-pattern. `UserOk` persists a `String` and returns `Optional`. `greetAvoid(null)` throws before `ifPresent`; `greet()` / `greet(String)` do not need a box. `UserAvoid` inside a `Serializable` graph fails once `nickname` holds an `Optional` instance.

> [!warning] The compiler will not save you
> `private Optional<String> nickname` and `void f(Optional<String> x)` compile. The API note is guidance plus the serialization and null-reference holes. “Primarily return type” is not a language error.

> [!warning] Locals from a return are not this anti-pattern
> `Optional<User> u = find(id);` is holding a return value. The discouraged uses are *storing* Optional in the object model and *requiring* callers to pass Optional in. Constructor arguments count as parameters.

> [!tip] Interview answer
> **Use `Optional` as a return type for “no result,” not as a field or a method parameter.** Fields add a non-serializable wrapper; parameters can still be null and force `of`/`ofNullable` at every call. Store a nullable value and return `Optional` from the getter; prefer overloads over an `Optional` argument.
