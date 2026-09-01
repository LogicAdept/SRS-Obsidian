<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS

# What is the difference between SOURCE, CLASS, and RUNTIME retention?

> [!abstract] Short answer
> **All three exist in source.** **SOURCE** never reaches the class file. **CLASS** and **RUNTIME** both do; the interview split is **reflection**: only **RUNTIME** is visible to `getAnnotation`. **CLASS is the default** if you omit `@Retention`.

## Same `@interface`, three lifetimes

`RetentionPolicy` is the `value` of `@Retention` ([[How do Java annotation retention policies work]]). Javadoc:

| Policy | Compiler | VM / `AnnotatedElement` |
| --- | --- | --- |
| `SOURCE` | Discarded — **not** in the `.class` | No |
| `CLASS` | Recorded in the class file | **Need not** be retained at run time — `getAnnotation` misses it |
| `RUNTIME` | Recorded in the class file | Retained so it **may be read reflectively** |

Flattening the table to “in the class file or not” **collapses CLASS and RUNTIME**. Both are in the binary; only RUNTIME is a reflective lookup. SOURCE is the one that never appears in bytecode.

Platform examples: `@Override` / `@SuppressWarnings` are **SOURCE**; `@Deprecated` is **RUNTIME**. A forgotten `@Retention` is **CLASS**, not SOURCE and not runtime-visible ([[What happens if you omit Retention on a custom annotation]]).

```d2
direction: down
src: "source text\nall three" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
source: "SOURCE\nnot in .class" {
  width: 180
  height: 50
  style.fill: "#ffebee"
}
klass: "CLASS\n.class, no getAnnotation" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
rt: "RUNTIME\n.class + getAnnotation" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}

src -> source
src -> klass
src -> rt
```

**Fig. 1.** CLASS vs RUNTIME is not “bytecode vs not.” It is “bytecode the VM may drop from reflection” vs “bytecode `AnnotatedElement` can read.”

> [!warning] CLASS is the language default, not RUNTIME
> Frameworks that call `getAnnotation` need **RUNTIME**. Dumps that treat “on the class” as “visible at runtime” miss CLASS.

> [!tip] Interview answer
> SOURCE is compile-only. CLASS and RUNTIME are both in the class file; only RUNTIME shows up in getAnnotation. The default if you omit @Retention is CLASS. Do not describe CLASS as “almost SOURCE” or “almost RUNTIME.”
