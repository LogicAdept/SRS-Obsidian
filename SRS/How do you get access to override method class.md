<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Access #Java/OOP/Polymorphism #SRS

# How do you get access to override method class?

> [!abstract] Short answer
> Use **`super.method(...)`** (and **`super.field`**) in an **instance** context of the subclass. That names the **direct superclass** member on **this** object, **without** virtual dispatch. It works only if that member is **accessible** — not `private`, and not package-access from **another** package. `super` is not a key to “any” parent member. Call form: [[How do you call an overridden superclass method in Java]]. All superclass calls: [[How do you call superclass methods from a subclass in Java]]. `private`: [[How would you explain private]].

## `super` is access + non-virtual invoke

Overriding replaces the inherited instance method for **virtual** calls (`this.m()`, `((Parent) this).m()`). To run the **overridden** declaration, write `super.m()`. Invocation mode `super` **does not allow further overriding**. Overriding: [[How would you explain method overriding in Java]]. Access rules: [[How do Java access modifiers work]].

**Fields** use the same keyword: `super.f` is `this` viewed as the superclass, so a field **hidden** by the subclass is still the parent’s `f` if it is accessible.

**What `super` cannot reach**

- A `private` method or field of the parent — it is **not inherited** and is not accessible from the subclass body. Same-class `private` is a different rule ([[Can one object access another class private fields in Java]]).
- A package-access member if the subclass is in **another package**.
- An `abstract` superclass method (`super.m()` would have no body).
- Anything from a **static** context (`static` method, static initializer).
- A **grandparent** method skipped with `super.super`.
- A **constructor** as `super.Parent(...)` — that is `super(...)`, not a method.

Default methods of an interface use **`Interface.super.m()`**, not unqualified `super`.

```d2
direction: down
want: "run Parent's overridden m / hidden f" {
  width: 300
  height: 40
  style.fill: "#e3f2fd"
}
ok: "super.m() / super.f\nif accessible" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
no: "private, other-package package-access,\nstatic context, super.super" {
  width: 320
  height: 55
  style.fill: "#fff3e0"
}
want -> ok
want -> no
```

**Fig. 1.** `super` names an accessible superclass instance member on this object. Access control still applies.

```java
class Parent {
    int hidden = 1;

    public void pub() {}
    protected void prot() {}
    void pack() {}
    private void priv() {}
}

class Child extends Parent {
    int hidden = 2;

    @Override
    public void pub() {
        super.pub();
    }

    @Override
    protected void prot() {
        super.prot();
    }

    @Override
    void pack() {
        super.pack(); // same package
    }

    int parentHidden() {
        return super.hidden; // 1
    }

    // void x() { super.priv(); } // compile-time error
}
```

**Listing 1.** Accessible overridden methods and a hidden field go through `super`. `priv` does not.

> [!warning] “`super` sees everything except `private`” is too wide
> Package-access members are invisible across packages. `protected` is for subclasses (and the package), not for arbitrary code. `super` does not bypass access control; it only chooses **which** accessible inherited instance member you mean.

> [!warning] `((Parent) this).m()` does not restore the parent method
> The cast is still a **virtual** call. If `Child` overrides `m`, you get `Child.m`. Access to the override is `super.m()`, not a cast.

> [!warning] `super()` is not access to an overridden method
> `super(args)` invokes a **constructor**. Constructors are not members and are not overridden. There is no `super` form that calls a `private` parent constructor from the subclass either, unless that constructor is accessible (`protected`/`public`/package).

> [!tip] Interview answer
> Use super.method() in an instance method of the subclass to invoke the overridden superclass method without virtual dispatch. The same super.field form reads a hidden instance field. super does not unlock private members, package-access members in another package, or a static context. A cast to the parent type still calls the override.
