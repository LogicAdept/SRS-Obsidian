<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Java/Generics #SRS

# What is a self type and how do recursive generics emulate one in Java?

> [!abstract] Short answer
> A **self type** would type `this` as *"the class of whoever is running this code"*. Java lacks it: inside `Caller`, `this` is typed `Caller`, so an inherited fluent method returns `Caller` and chains lose subclass members ([[How would you explain the Builder design pattern]]). The standard emulation is **recursive generics** (the CRTP idiom): `abstract class Caller<B extends Caller<B>>` with an abstract `B self()` that each subclass answers with `this`. The JDK itself is built this way: `Enum<E extends Enum<E>>`, `Comparable<T>`.

## The chaining problem

Fluent APIs return `this` so calls chain. The moment a fluent method is **inherited**, its declared return type is the *base* class: `new HttpCaller().timeout(250)` is a `Caller`, and `.path("/api")` no longer compiles — `path` exists only on `HttpCaller`. The chain breaks exactly at the inherited link, which is why hand-rolled builders either re-declare every method in the subclass or accept the truncation.

## The CRTP emulation

Declare the base with a type parameter bounded by itself and route every fluent return through it: `B timeout(int ms) { ...; return self(); }`. Each subclass extends `Caller<HttpCaller>` and implements `self()` to return `this` — now statically `HttpCaller`. The inherited method's declared return type in the subclass view is `HttpCaller`, so the chain keeps every subclass method. The sandbox run executes exactly that chain: `timeout(250).path("/api").run()` ([[What is the difference between subtyping and inheritance]] for why `B` is a parameter, not a magic keyword).

## Limits and JDK precedents

The idiom is a convention, not a true self type: nothing structural forces `class X extends Caller<X>` to pass itself — `X extends Caller<Y>` compiles until the abstract `self()` and the overridden return types make the lie expensive. `final` subclasses close the escape hatch and make the parametrization honest. The JDK uses the same shape for `Enum<E extends Enum<E>>` (`compareTo` against one's own kind) and `Comparable<T>`; builder hierarchies and fluent DSLs are the everyday application ([[How would you explain covariance of generic and return types in Java]] covers the related return-narrowing story).

```d2
direction: down
base: "Caller<B extends Caller<B>>\nB timeout(int) { return self(); }\nabstract B self()" {
  width: 320
  height: 84
  style.fill: "#e3f2fd"
}
sub: "HttpCaller extends Caller<HttpCaller>\nself() { return this; }\nHttpCaller path(String)" {
  width: 320
  height: 84
  style.fill: "#e8f5e9"
}
base -> sub: "B = HttpCaller"
sub -> sub: "timeout() returns HttpCaller"
```

**Fig. 1.** The subclass feeds itself as `B`, so inherited fluent methods return the subclass type.

```java
abstract class Caller<B extends Caller<B>> {
    int timeoutMs = 1000;
    public B timeout(int ms) { this.timeoutMs = ms; return self(); }
    protected abstract B self();
    public String run() { return "call timeout=" + timeoutMs; }
}
final class HttpCaller extends Caller<HttpCaller> {
    String path = "/";
    public HttpCaller path(String p) { this.path = p; return this; }
    @Override protected HttpCaller self() { return this; }
    @Override public String run() { return super.run() + " path=" + path; }
}
```

**Listing 1.** The idiom: self-bounded parameter, abstract `self()`, `final` subclass.

```text
call timeout=250 path=/api
```

**Listing 2.** Verbatim run (JDK 21.0.12.1, sandbox `oop_14`): the inherited `timeout` returned an `HttpCaller`, so `path` stayed chainable — `timeout(250).path("/api").run()` compiles and runs.

> [!warning] "Recursive generics are true self types" is false
> They are an emulation with known holes: `B` is an arbitrary type parameter, so a class can extend `Caller<Other>` and still compile; and `this` inside the base remains typed `Caller<B>`, not `B`. The idiom works because `self()` and `final` subclasses make the honest parametrization the easy one — not because the compiler enforces it ([[How would you explain the Builder design pattern]]).

> [!tip] Interview answer
> A self type types `this` as the concrete runtime class; Java does not have one, so inherited fluent methods return the base type and chains break. The recursive-generics idiom — `class B extends Caller<B>` plus abstract `self()` returning `this` — emulates it; that is how `Enum<E extends Enum<E>>` and builder hierarchies keep chains typed to the subclass.
