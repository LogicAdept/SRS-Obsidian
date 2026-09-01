<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS

# How does Inherited annotation inheritance work?

> [!abstract] Short answer
> **Only for class annotations, and only if you opt in.** By default a subclass does **not** see annotations declared on its superclass. Meta-annotate the annotation interface with `@Inherited`, query the **class** with `getAnnotation` / `getAnnotations` / `getAnnotationsByType`, and the lookup walks **superclasses** up to `Object` until it finds a directly present annotation of that type. It does **not** walk interfaces, and it does **not** apply to methods, fields, constructors, or parameters.

## Opt-in superclass lookup

`@Inherited` is a meta-annotation on the **annotation interface**, not on each use. Reflective “present” / “associated” queries on a **class** then mean:

1. If the class has that annotation **directly**, return it (no merge with a superclass).
2. Otherwise, if the type is `@Inherited`, repeat on the **superclass**.
3. Stop at `Object` or when there is no superclass.

```java
import java.lang.annotation.Inherited;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import java.lang.annotation.ElementType;

@Inherited
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface Audited {
    String value() default "";
}

@Audited("base")
class Base {}

class Child extends Base {}

// Child.class.getAnnotation(Audited.class).value() → "base"
```

**Listing 1.** `Child` does not declare `@Audited`; `getAnnotation` still returns the superclass instance. Runtime queries still need **RUNTIME** retention: [[How do Java annotation retention policies work]], [[How do you retrieve annotations at runtime]].

```java
@Audited("base")
class Base {}

@Audited("child")
class Child extends Base {}

// Child.class.getAnnotation(Audited.class).value() → "child"
// Child.class.getDeclaredAnnotation(Audited.class) → "child"
// Base's value is not merged
```

**Listing 2.** A directly present annotation on the subclass **replaces** the inherited one. `getDeclaredAnnotation` never walks superclasses, even when the type is `@Inherited`.

If a repeatable type is `@Inherited`, its **container** must be `@Inherited` too (the reverse is allowed). Container unwrap is `getAnnotationsByType`, not `getAnnotation`: [[How are repeating annotations stored for compatibility]].

```d2
direction: right
child: "Child.getAnnotation(A)" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
direct: "A directly on Child?" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
super: "query superclass\nuntil Object" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}

child -> direct
direct -> super: "no and @Inherited"
```

**Fig. 1.** Inheritance is a reflective walk of the class line, not a copy of the annotation onto the subclass bytecode as a second declaration.

> [!warning] Interfaces and members are never part of this walk
> `@Inherited` has **no effect** if the annotation is used on anything other than a **class**. A class does **not** inherit annotations from an interface it implements (or from superinterfaces of that interface). Method/field/parameter annotations are not inherited this way even if the type is `@Inherited`. Read those sites on the actual declaring `Method` / `Field` / `Class` of the interface.

> [!tip] Interview answer
> Annotations are not inherited unless the annotation type is meta-annotated with @Inherited. Then getAnnotation on a class walks superclasses until it finds that annotation or hits Object; a declaration on the subclass wins and values are not merged. It never follows implements, and it never copies method or field annotations.
