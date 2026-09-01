<!--
reps: 0
priority: 0
-->
#Java/Language/Records #Java/Bytecode #SRS

# How does the JVM represent a Java record?

> [!abstract] Short answer
> A record compiles to an ordinary `class` file, not a new JVM type. The file is `ACC_FINAL`, its direct superclass is `java/lang/Record`, and a single `Record` attribute (class-file 60.0 / Java 16) lists each component’s name, descriptor, and optional annotations. There is **no** `ACC_RECORD` bit in JVMS Table 4.1-B. Dumps that name a `RecordComponents` attribute are using the wrong name.

## Class file, not a new JVM kind

```d2
direction: down
src: "record Point(int x, int y)" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
cf: "ClassFile\nACC_FINAL (+ ACC_SUPER)\nsuper_class = java/lang/Record" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
attr: "Record attribute (at most one)\nrecord_component_info[] in header order" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
src -> cf
cf -> attr
```

**Fig. 1.** Record-ness is class-file metadata. The VM still executes ordinary `new`, field loads, and accessor `invokevirtual` / `invokeinterface` — there is no record bytecode.

JVMS §4.7.30: the `Record` attribute sits on the `ClassFile` attributes table and **indicates that the current class is a record class**. At most one such attribute. Each `record_component_info` has `name_index`, a field `descriptor_index`, and an attributes table. Table 4.7-C allows `Signature`, `RuntimeVisibleAnnotations` / `RuntimeInvisibleAnnotations`, and the type-annotation attributes on a component — that is how [[Where do annotations on Java record components apply]] and generic components show up. Introduced as major version **60.0**, Java 16.

```
Record_attribute {
    u2 attribute_name_index;   // Utf8 "Record"
    u4 attribute_length;
    u2 components_count;
    record_component_info components[components_count];
}
```

**Listing 1.** The predefined attribute name is `Record`. Reflection’s `Class.getRecordComponents()` is the library view of this table ([[How do you inspect a Java record with reflection]]).

JLS §8.10: a record class is **implicitly `final`** (`final record` is redundant) and its direct superclass type is `Record`. A record declaration has **no `extends` clause**, so you cannot write `extends Record` even though that is the superclass. JLS §8.1.4: a normal class that names `Record` in `extends` is a compile-time error — only a record class may extend it, same pattern as `Enum`. `java.lang.Record` is an `abstract` class (since 16) with a `protected` constructor and abstract `equals` / `hashCode` / `toString`; `Record.class.isRecord()` is **false**.

```java
public record Point(int x, int y) {}

// javap-style picture of Point.class:
//   flags: ACC_PUBLIC, ACC_FINAL, ACC_SUPER
//   super_class: java/lang/Record
//   Record:
//     Component: int x
//     Component: int y
```

**Listing 2.** `javap -v` shows `ACC_FINAL` and a `Record:` section. It does **not** show an `ACC_RECORD` access flag, because Table 4.1-B never defined one. (Sealed classes are the same idea: `PermittedSubclasses`, not `ACC_SEALED`.)

The rest of the class is ordinary: `private final` component fields ([[Are Java record fields final]]), the canonical constructor, accessors, and the implicit `equals` / `hashCode` / `toString` ([[What methods does the compiler generate for a Java record]]). Those members are **not** marked `Synthetic`; JVMS §4.7.8 excepts implicitly declared members of enum and record classes.

Why subclassing is banned: the class is `final`, so JVMS §4.1 already forbids any `class` file whose `super_class` names a type with `ACC_FINAL`. That is the JVM rule. Language-level reasons are the copy-equals invariant and a stable component list for pattern matching — not a Valhalla value-class encoding and not a special JIT bit in the spec.

> [!warning] `ACC_RECORD` is dump wording, not Table 4.1-B
> `access_flags` for classes lists `ACC_PUBLIC`, `ACC_FINAL`, `ACC_SUPER`, `ACC_INTERFACE`, `ACC_ABSTRACT`, `ACC_SYNTHETIC`, `ACC_ANNOTATION`, `ACC_ENUM`, `ACC_MODULE`. Record identity is the **`Record` attribute**. Tooling (ASM, some compiler internals) may expose a convenience `ACC_RECORD` **outside** that `u2` table; do not claim the class file stores `ACC_RECORD | ACC_FINAL` as two JVMS flags.

> [!warning] Direct superclass is `Record`, not `Object`
> A record’s **direct** superclass is `java.lang.Record`. `Record` itself extends `Object`, so `instanceof Object` is still true. “Records inherit Object” is a sloppy **direct**-vs-transitive mix-up, not a second hierarchy. You still cannot write `class C extends Record`.

> [!warning] The VM does not freeze instances
> `ACC_FINAL` on the **class** blocks subclasses. Component fields are `private final`, which is the usual Java `final` — not a JVM guarantee against `setAccessible`, `Unsafe`, or a hand-written `class` file. “Bytecode cannot change a record” is not a spec claim.

> [!tip] Interview answer
> **A record is a normal class file: `final`, superclass `java.lang.Record`, plus a `Record` attribute that lists components in header order (class-file 60 / Java 16).** That metadata is what `isRecord()` / `getRecordComponents()` read. There is no `ACC_RECORD` flag in the JVMS class-flag table and no record-specific instruction — dumps that treat records as a new VM type or as Valhalla values are mixing layers.
