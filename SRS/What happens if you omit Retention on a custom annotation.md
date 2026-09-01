<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS

# What happens if you omit Retention on a custom annotation?

> [!abstract] Short answer
> The policy is **`RetentionPolicy.CLASS`**. The annotation is **written into the class file** but **need not** be kept by the VM, so `getAnnotation` / `isAnnotationPresent` return **`null` / false**. It is **not** `SOURCE` (discarded) and **not** `RUNTIME` (reflectable).

## CLASS is the language default

If `@Retention` is absent on the `@interface`, the compiler treats it as `@Retention(CLASS)`. That is independent of how frameworks use annotations.

```java
@Target(ElementType.TYPE)
public @interface Audited {}   // no @Retention → CLASS

@Audited
class Job {}

// Job.class.getAnnotation(Audited.class) == null
// Job.class.isAnnotationPresent(Audited.class) == false
```

**Listing 1.** Compiles and the class file still carries `@Audited`. Core reflection does not see it. Fix: `@Retention(RetentionPolicy.RUNTIME)` when a runtime reader, test runner, or container must call `getAnnotation`. Lookup: [[How do you retrieve annotations at runtime]]. The three policies: [[How do Java annotation retention policies work]].

Processors still see CLASS (and SOURCE) from **source**. They cannot recover SOURCE from a `.class`; CLASS is in the binary for class-file readers: [[How do annotation processors differ from runtime reflection]].

```d2
direction: right
omit: "no @Retention" {
  width: 170
  height: 60
  style.fill: "#fff3e0"
}
klass: "CLASS\nin .class" {
  width: 160
  height: 70
  style.fill: "#e3f2fd"
}
refl: "getAnnotation\nnull" {
  width: 170
  height: 70
  style.fill: "#ffebee"
}

omit -> klass: "default"
klass -> refl: "not RUNTIME"
```

**Fig. 1.** Omitting `@Retention` is CLASS, not “visible at runtime.”

> [!warning] CLASS is not a cheaper RUNTIME
> Popular line: “annotations are always available at runtime.” Only **`RUNTIME`** is. Omitting `@Retention` is also **not** `SOURCE`: you still pay class-file space. A Spring/JPA-style marker that compiles but “does nothing” at runtime is usually this default, not a broken scan.

> [!tip] Interview answer
> If you omit @Retention, the default is CLASS: the annotation is in the class file but getAnnotation returns null. Set RUNTIME when anything reflects on it. SOURCE would drop it from bytecode entirely; forgetting Retention is the CLASS middle ground, not runtime visibility.
