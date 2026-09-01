<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS

# Why do annotations have no direct effect on annotated code?

> [!abstract] Short answer
> An annotation is **metadata**: it **names** extra information on a program element. The language does **not** run it, and it does **not** rewrite the annotated body. Anything that “happens” — a compile error, generated source, a proxy, a transaction — comes from a **consumer** (compiler, processor, bytecode tool, or runtime reflection), not from the `@` token itself.

## Metadata, not a statement

The `@` form denotes an instance of an annotation interface and binds it to a declaration or type use. That instance is **not** an expression the JVM evaluates when the method runs. At run time an annotation has **no effect** unless some library **reads** it (`AnnotatedElement`, a framework index, a generated class).

Consumers, not the annotation, do the work:

- **Compiler** — `@Override` fails the build if you did not override; `@SuppressWarnings` quiets diagnostics. The method body is unchanged. [[How does the Override annotation work]]
- **Processors / bytecode tools** — generate or rewrite *other* files. The original method still does what you wrote until that extra code is compiled in. [[How do annotation processors differ from runtime reflection]]
- **Runtime** — only `RUNTIME` retention is visible to reflection; even then **your** code (or a proxy) must call `getAnnotation` and act. [[How do Java annotation retention policies work]]

A homemade `@LogExecutionTime` on `void save()` does not start a timer. An aspect, processor, or wrapper that **looks for** that type does.

```java
@LogExecutionTime          // inert by itself
void save() { persist(); }

// A framework might do this later — that code has the effect:
LogExecutionTime a = method.getAnnotation(LogExecutionTime.class);
if (a != null) { long t = System.nanoTime(); persist(); }
```

**Listing 1.** The annotation is data; the `if` is behavior. Related: [[What is a Java annotation]].

```d2
direction: right
ann: "@Foo on method" {
  width: 140
  height: 55
}
who: "compiler / apt /\nreflection / proxy" {
  width: 180
  height: 70
}
fx: "error, codegen,\nor wrapper logic" {
  width: 170
  height: 70
}
ann -> who: "read"
who -> fx: "act"
```

**Fig. 1.** No consumer → no operational change.

> [!warning] The JVM does not “honor” your annotation
> `@LogExecutionTime` does not alter the bytecode of the method **because it is present**. If the aspect, processor, or wrapper is missing, the method runs as written — often a silent production bug. Predefined types like `@Override` only change **diagnostics**, not the instruction stream of the method.

> [!tip] Interview answer
> Annotations are metadata bound to program elements; they are not executed and have no direct effect on how that code runs. The compiler, an annotation processor, or a runtime that uses reflection may react to them. If nothing reads the annotation, it is as inert as a comment that survived into the class file.
