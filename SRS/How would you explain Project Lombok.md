<!--
reps: 0
priority: 0
-->
#Java/Library #SRS

# How would you explain Project Lombok?

> [!abstract] Short answer
> **Lombok is an annotation processor that deletes boilerplate at compile time: annotate a class with `@Getter`, `@Data`, `@Builder`, `@Slf4j`, and the generated getters, setters, `equals`, `hashCode`, `toString`, or builder methods appear in the bytecode — your source keeps only the annotations.**

## Compile-time AST surgery, not reflection

Lombok plugs into `javac` as a JSR 269 annotation processor, but unlike typical processors it does more than generate new files — it **edits the compiler's own abstract syntax tree** while compilation runs, so the generated methods are real members of the compiled class. The IDE needs the Lombok plugin to resolve them for code completion, because the source never contains them. `delombok` prints what the source would look like with all generated code inlined.

The flagship shortcut is `@Data`: it bundles `@ToString`, `@EqualsAndHashCode`, `@Getter` on all fields, `@Setter` on all **non-final** fields, and `@RequiredArgsConstructor` — a constructor for the final and `@NonNull` fields. `@Builder` generates a fluent builder (`Config.builder().host(...).build()`). `@Slf4j` adds a `log` field. Generation is polite: a method with the same name and parameter count that you already wrote suppresses generation silently — no warning ([[How do annotation processors differ from runtime reflection]]).

```java
import lombok.Builder;
import lombok.Data;

@Data
@Builder
class Config {
    private final String host; // final: getter, no setter
    private int port;          // non-final: getter and setter
}

public class LombokDemo {
    public static void main(String[] args) {
        Config cfg = Config.builder().host("localhost").port(8080).build();
        System.out.println("toString: " + cfg);
        // toString: Config(host=localhost, port=8080)
        Config same = new Config("localhost", 8080);
        System.out.println("equals: " + cfg.equals(same));
        // equals: true  (hashCode matches too; canEqual is generated as well)
    }
}
```

**Listing 1.** Verified on JDK 21 with Lombok 1.18.36: reflection found `builder`, `getHost`, `equals`, `canEqual`; a setter existed for `port` but **not** for the final `host`.

> [!warning] A compile-time hack with rules of its own
> Lombok mutates the compiler's internals, so each new JDK can break it until Lombok catches up — an upgrade risk plain Java does not have. Silent-skip behavior hides mistakes: write `equals(OtherType o)` yourself and `@Data` quietly generates nothing. And since Java 16, **records** cover the read-only case — accessors, `equals`, `hashCode`, `toString` — without any dependency, so the common reason for `@Data` on an immutable carrier is gone; Lombok stays interesting for builders, `@Slf4j`, and mutable beans ([[What is the difference between a Java record and Lombok Value]]).

```d2
direction: down
src: "Source with annotations\n@Data @Builder" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
proc: "javac + Lombok processor\nedits the AST" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
cls: "Bytecode with real methods\ngetters, builder, equals..." {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
ide: "IDE plugin\nmakes them resolvable" {
  width: 240
  height: 60
  style.fill: "#fff8e1"
}
src -> proc -> cls
proc -> ide
```

**Fig. 1.** Annotations enter compilation; the processor injects the members before bytecode is emitted.

> [!tip] Interview answer
> **Lombok generates boilerplate at compile time — `@Data` for getters/setters/equals/hashCode/toString plus a required-args constructor, `@Builder` for fluent construction — by editing the AST inside javac, so the bytecode has real methods while your source stays small.** Remember the rules: final fields get no setters, an existing same-signature method suppresses generation, the IDE needs the plugin — and records now cover most immutable-carrier cases without a library.

> [!example] Verified behavior
> Compiling with lombok 1.18.36 on JDK 21 produced `Config(host=localhost, port=8080)` from `@Data`'s `toString`, a working `builder()`, matching `equals`/`hashCode`, and `canEqual`; reflection confirmed a setter for non-final `port` and none for final `host`.
