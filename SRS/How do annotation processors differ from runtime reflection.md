<!--
reps: 0
priority: 0
-->
#Java/Annotations #Java/Language/Reflection #SRS

# How do annotation processors differ from runtime reflection?

> [!abstract] Short answer
> **A processor runs during compilation on a language model of source (and of class files from earlier rounds). Core reflection runs later on types already loaded in this VM, and only `RUNTIME` retention is visible.** The processor can create files through `Filer` and fail the compile through `Messager`. `Class` / `AnnotatedElement` can only read metadata the VM kept and then run your own code.

## Two consumers, two times

An annotation is a marker with **no effect at run time** until some consumer acts ([[Why do annotations have no direct effect on annotated code]]). The two consumers interviewers mean are not interchangeable:

| | Annotation processor | Core reflection |
| --- | --- | --- |
| When | Rounds inside `javac` (JSR 269 / Java 6+) | After the class is loaded |
| Types you see | `javax.lang.model` `Element`s, not live objects | `Class`, `Method`, `Field` — loaded types |
| Typical API | `Processor` / `AbstractProcessor`, `ProcessingEnvironment` | `AnnotatedElement` (`isAnnotationPresent`, `getAnnotation`) |
| SOURCE | Visible while the model is built **from source** | Never — discarded from the binary |
| CLASS | In the class file; the language model can still show it | Not returned by reflective APIs |
| RUNTIME | Visible | Visible |
| What you can do | Generate source/class/resource files; raise a compile error | Read the annotation and act on **live** instances |

Processors implement `javax.annotation.processing.Processor` (usually by extending `AbstractProcessor`). The tool constructs the processor, calls `init` with a `ProcessingEnvironment`, then `process` on each round. `getFiler()` creates new files that later rounds will see; `getMessager()` reports diagnostics. `Diagnostic.Kind.ERROR` is a problem that **prevents the tool's normal completion**.

Default discovery: a service file `META-INF/services/javax.annotation.processing.Processor` listing the processor class (one name per line) on the processor path or class path. `-processor` names classes explicitly and **bypasses** that lookup. Reflection has no equivalent registry: your code (or a framework) calls `getAnnotation` after load ([[How do you retrieve annotations at runtime]], [[What is reflection in Java]]).

```d2
direction: down
src: "source with @Foo" {
  width: 220
  height: 45
}
apt: "Processor rounds\nFiler / Messager" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
cls: ".class" {
  width: 220
  height: 40
}
load: "VM loads the type" {
  width: 220
  height: 45
}
refl: "AnnotatedElement\nRUNTIME only" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
src -> apt
apt -> cls: "compile + generated files"
cls -> load
load -> refl
```

**Fig. 1.** Processors sit in the compiler. Reflection sits after load. SOURCE never reaches the class file; CLASS is in the file as a run-time-invisible attribute and is ignored by `getAnnotation`.

Retention is the switch ([[How do Java annotation retention policies work]], [[What happens if you omit Retention on a custom annotation]]):

- **SOURCE** — the compiler must not put the annotation in the binary. A processor still sees it on **source** elements. A model built from a `.class` cannot recover it.
- **CLASS** (the default if `@Retention` is omitted) — written to the class file (`RuntimeInvisibleAnnotations`). Reflective APIs must **not** return it (unless an implementation-specific VM flag keeps those attributes). Class-file readers can still parse the attribute.
- **RUNTIME** — written to the class file (`RuntimeVisibleAnnotations`) and kept so `getAnnotation` can return it.

```java
@SupportedAnnotationTypes("com.example.Generate")
@SupportedSourceVersion(SourceVersion.RELEASE_21)
public class GenerateProcessor extends AbstractProcessor {
    @Override
    public boolean process(Set<? extends TypeElement> unused, RoundEnvironment round) {
        TypeElement generate = processingEnv.getElementUtils()
            .getTypeElement("com.example.Generate");
        if (generate == null) {
            return false;
        }
        for (Element e : round.getElementsAnnotatedWith(generate)) {
            processingEnv.getMessager()
                .printMessage(Diagnostic.Kind.ERROR, "illegal @Generate target", e);
            // processingEnv.getFiler().createSourceFile("com.example.JobGenerated", e)
            // writes a *new* compilation unit; it cannot replace Job.java.
        }
        return true;
    }
}
```

**Listing 1.** Compile-time only: fail the build, or (commented) emit another file through `Filer`. This does not rewrite `e`'s body and does not run when `e`'s class is later loaded.

```java
@Retention(RetentionPolicy.RUNTIME)
@interface Generate {}

@Generate
class Job {}

class ReadGenerate {
    static Generate marker() {
        if (!Job.class.isAnnotationPresent(Generate.class)) {
            return null;
        }
        return Job.class.getAnnotation(Generate.class);
    }
}
```

**Listing 2.** After load, `getAnnotation` / `isAnnotationPresent` see `Generate` only because it is `RUNTIME`. `isAnnotationPresent` is `getAnnotation(...) != null`. Drop `@Retention` (CLASS) or use SOURCE, and both calls miss it.

A processor that supports `"*"` and returns `true` **claims every annotation interface**, so later processors never see those types. Validators that only check should return `false`.

> [!warning] SOURCE is gone from the `.class`; CLASS is still not `getAnnotation`
> A runtime reader cannot recover SOURCE: the compiler discarded it. CLASS is in the class file, so a bytecode parser can see it, and `Class.getAnnotation` still returns `null`. A Spring- or JPA-style marker that “does nothing” at runtime is usually CLASS (or a missing consumer), not a broken processor. The inverse mistake: a processor that is only given `.class` inputs will not see SOURCE annotations that existed in the original source.

> [!warning] `Filer` will not overwrite the type you annotated
> Initial inputs are the zeroth round. `createSourceFile` for a name that is already an input throws `FilerException`. Processors generate **other** files (or fail the compile). They do not patch the annotated method in place. If you need the original body rewritten, that is a bytecode tool, not `Processor`.

> [!tip] Interview answer
> **Processors run in the compiler on the language model; reflection runs on loaded classes.** Processors can see SOURCE from source, generate files with `Filer`, and fail the build with `Messager`. `getAnnotation` only sees `RUNTIME`. CLASS sits in the class file for class-file readers and is invisible to core reflection. Register a processor with `META-INF/services/javax.annotation.processing.Processor` (or `-processor`); reflection is just code that calls the API.
