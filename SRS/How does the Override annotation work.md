<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS

# How does the Override annotation work?

> [!abstract] Short answer
> `@Override` is a **marker** (`@Target(METHOD)`, **SOURCE** retention) that forces a **compile-time** check: the method must actually **override** (or implement) a supertype method, be override-equivalent to a **public** `Object` method, or — on a **record** — be a component **accessor**. If none of those hold, compilation **fails**. It does **not** change dispatch and is **not** in the class file.

## What the compiler accepts

Without `@Override`, `equals(Foo)` **overloads** `equals(Object)` and still compiles — the inherited `Object.equals` stays in play. `@Override` is how you make that a hard error.

```java
class Foo {
    @Override
    public boolean equals(Foo that) { // compile-time error
        return true;
    }
}
```

**Listing 1.** Classic miss: the signature is not a subsignature of `Object.equals(Object)`. Drop `@Override` and this **overloads** instead of overriding.

A method annotated `@Override` is legal only if one of these is true:

1. It **overrides** from its declaring class or interface a method in a **supertype** (including implementing a superinterface method).
2. Its signature is **override-equivalent** to a **public** method of `Object` (`equals`, `hashCode`, `toString`, …) — so an interface may write `@Override int hashCode();`.
3. It is a **record** component accessor (`record Roo(int x) { @Override public int x() { … } }`).

```java
interface Bar {
    @Override int hashCode();     // legal — public Object method
    @Override Object clone();     // error — Object.clone is not public
}

class Beep {
    @Override
    protected Object clone() throws CloneNotSupportedException {
        return super.clone();
    }
}
```

**Listing 2.** Interfaces only “override” the public `Object` methods they already implicitly declare. A class **can** `@Override` `clone()` because it really overrides `Object.clone`.

`@Override` has **no elements**. Retention is **SOURCE**: discarded by the compiler, absent from bytecode, invisible to `getAnnotation`. See [[How do Java annotation retention policies work]] and [[Why do annotations have no direct effect on annotated code]]. It may appear only on **methods**: [[How does the Target meta-annotation restrict annotation placement]]. Marker vs members: [[What is the difference between marker single-member and multi-member annotations]].

```d2
direction: right
src: "@Override m()" {
  width: 160
  height: 70
  style.fill: "#e3f2fd"
}
check: "overrides / public Object\n/ record accessor?" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
ok: "compile" {
  width: 120
  height: 60
  style.fill: "#e8f5e9"
}
err: "compile-time error" {
  width: 170
  height: 60
  style.fill: "#ffebee"
}

src -> check
check -> ok: "yes"
check -> err: "no"
```

**Fig. 1.** The annotation is a compiler assertion. After a successful compile it is gone (SOURCE); vtables are unchanged.

> [!warning] Private and static do not override
> `private` members are **not inherited**, so a subclass `private` method with the same name never overrides — `@Override` is an error. A `static` method **hides** another class method; hiding is not overriding, so `@Override` on `static` fails (and a `static` method cannot override an instance method). `@Override` also does nothing to runtime dispatch: it only rejects a declaration that is not an override.

> [!tip] Interview answer
> @Override asks the compiler to prove this method overrides a supertype method, matches a public Object method, or is a record accessor — otherwise you get a compile error, which is how you catch equals(Foo) and typos. It is a SOURCE marker: not in the class file, no effect on dispatch. Private methods are not inherited and static methods hide, so @Override is illegal on those.
