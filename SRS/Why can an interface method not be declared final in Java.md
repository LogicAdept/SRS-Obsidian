<!--
reps: 0
priority: 0
-->
#Java/OOP #Java/Language/Modifiers/Final #SRS

# Why can an interface method not be declared final in Java?

> [!abstract] Short answer
> **`final` is not a legal modifier on any interface method.** Implicitly `abstract` methods **must** be implemented (overridden) by a concrete class; `final` would forbid that override. **`default`** methods exist to supply a body that implementing classes **may still replace**. `static` and `private` interface methods are not inherited, but the grammar still does not allow `final` on them. Contrast a class, where `final` is legal: [[What does the final keyword mean in Java]]. Abstract vs complete: [[How would you explain the abstract keyword in Java]]. Interface method kinds: [[How would you explain default modifiers for fields and methods inside interfaces]].

## Abstract demands an implementation; `final` forbids it

A method in an interface that is not `private`, `default`, or `static` is implicitly `abstract`. Its body is a semicolon. A concrete class that implements the interface **must** provide an instance method that overrides it. `final` on a method means no override (and, for `static` in a **class**, no hide). Those two requirements cannot hold together, which is why `abstract` and `final` are also illegal as a pair on class methods.

| Kind | Has a body? | Why `final` is still illegal |
| --- | --- | --- |
| Implicit `abstract` | no | implementors **must** override |
| `default` | yes | implementors **may** override; that is the point |
| `static` / `private` | yes | not inherited — and `final` is **not** an interface-method modifier anyway |

`default` methods have a body, but they are still **instance** methods meant to be inherited and optionally overridden. Locking them with `final` would take away the feature. `static` interface methods are not inherited and are not overridden; `private` interface methods are neither inherited nor overridden. Even so, you cannot write `final` on them: it is simply not an interface-method modifier (`public`, `private`, `abstract`, `default`, `static`, and obsolete `strictfp` are).

`synchronized` and `native` are likewise illegal on interface methods. An **interface type** cannot be `final` either (it may be `sealed`).

A **class** method may be `final`. That includes a `final static` class method, which only blocks hiding: [[How would you explain the final modifier on a static method in Java]]. Interface `static` methods are a different rule set: [[How would you explain static methods on Java interfaces]].

```java
interface Named {
    String name();                 // implicit abstract — must be implemented
    default String label() { return name(); } // may be overridden
    static Named of(String n) { return () -> n; }
}

class Person implements Named {
    public String name() { return "p"; }           // required
    @Override public String label() { return "P"; } // allowed
}
```

**Listing 1.** Nothing here can be marked `final`. `Person` must override `name()` and may override `label()`.

```d2
direction: down
abs: "interface instance method\n(implicit abstract or default)" {
  width: 260
  height: 48
  style.fill: "#e3f2fd"
}
need: "implementors may / must\nsupply their own method" {
  width: 240
  height: 48
  style.fill: "#e8f5e9"
}
fin: "final would forbid\noverride" {
  width: 180
  height: 48
  style.fill: "#ffcdd2"
}
abs -> need
need -> fin: "conflict"
```

**Fig. 1.** The contract of an interface method is that classes can complete or replace it. `final` would close that door.

> [!warning] “All interface methods are abstract” is outdated
> `default`, `static`, and `private` methods are not abstract. They still cannot be `final`. An answer that only cites implicit `abstract` is incomplete, not wrong for `void m();`.

> [!warning] Not because the method is `public`
> Class methods can be `public` and `final` at once. The ban is specific to **interface** method declarations, not to public API in general.

> [!warning] `default` does not mean “closed”
> A default method is a fallback, not a final implementation. If you need a method that subclasses cannot replace, put it on a **class** (and mark that class method `final`), not on an interface.

> [!tip] Interview answer
> Implicitly abstract interface methods have to be overridden by a concrete implementor, and `final` forbids override, so the combination is illegal. Default methods are also overridable by design. `final` is not in the list of interface method modifiers at all, including on `static` and `private` methods. Use `final` on class methods when you need that lock.
