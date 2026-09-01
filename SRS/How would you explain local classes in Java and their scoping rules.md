<!--
reps: 0
priority: 0
-->
#Java/OOP #Java/Language/NestedClasses #SRS

# How would you explain local classes in Java and their scoping rules?

> [!abstract] Short answer
> **A local class is a nested class declared in a block** (usually a method). Its **simple name** is in scope for the **rest of that block, including the declaration itself**. You cannot `public` / `private` it, cannot write `static` on the class, and you refer to it only by that simple name. It captures enclosing members and **effectively final** locals.

## Declared in a block, named, not a member

A local class’s declaration is **immediately contained by a block** — method or constructor body, initializer, `if` / `for` body, or a nested `{ }`. It may be mixed with statements. Unlike an anonymous class, it has a **simple name**. Like an anonymous class, it is **not** a member of a package or type, so it has no access modifier ([[How would you explain categories of Java classes such as nested and anonymous]], [[What are anonymous classes and where are they used]]).

`public`, `protected`, `private`, `static`, `sealed`, and `non-sealed` on the local class are compile-time errors. A local **normal** class is an **inner** class. A local **enum** or **record** is implicitly `static` (not inner). A local **interface** is allowed and is implicitly `static` (Java SE 16+).

If the surrounding method is `static`, the local class is in a **static context**: no enclosing instance, so unqualified instance members of the enclosing type are illegal ([[How do you from class get access to field outer class]]).

## Scope is “the rest of this block, including me”

Scope is the region where the **simple name** denotes that class (unless shadowed). For a local class declared in a block, that region is **the remainder of the immediately enclosing block, including the local class declaration itself**. In a `switch` group, the same idea applies to the rest of that group.

Because the name is in scope **on its own header**, `class Cyclic extends Cyclic` is a **self-extension**, not an extension of a member class also named `Cyclic`. A `new Cyclic()` that appears **above** the local declaration still means the member class — the local name is not in scope yet.

The name is usable only as a **simple** name. A local class has **no** fully qualified or canonical name, so `Host.Local` from outside the block does not exist.

You cannot declare another local class (or local interface) with the same name **in that remaining block**. You **can** declare one inside a **nested class or interface** that itself sits in that scope (a new nested type is a new naming level). After the block ends, the name is free again.

```java
class Host {
    class Member { }

    void foo() {
        new Member();

        class Local extends Member {
            int value() {
                return 1;
            }
        }

        Local x = new Local();
        x.value();
        {
            // class Local { }              // compile-time error: still in scope
            class Nested {
                void inner() {
                    class Local { }         // OK: nested type
                }
            }
        }
    }

    void bar() {
        class Local { }                     // OK: different block
    }
}
```

**Listing 1.** `prior` is `Host.Member`. After `class Local`, the simple name `Local` means that local class until `foo`’s block ends. A nested `Local` inside `Nested` is a different declaration.

Captured locals and parameters must be **final or effectively final** (unchanged after initialization). Assigning to the local, even later in the method, makes a use **inside** the local class illegal. Members of the enclosing type stay accessible under the usual inner-class rules ([[How would you explain nested classes in Java and when to use each kind]]).

```java
class Host {
    void print(int n) {
        class Printer {
            void show() {
                System.out.println(n);
            }
        }
        new Printer().show();
        // n = 2;  // would make n not effectively final
    }
}
```

**Listing 2.** `n` is captured. The method’s return type cannot be `Printer` — that name is not in scope on the method header, only from the local declaration downward in the body.

```d2
direction: down
block: "enclosing block" {
  width: 280
  height: 40
}
before: "above the declaration\nname not in scope" {
  width: 300
  height: 55
  style.fill: "#fff3e0"
}
decl: "class Local { ... }\nscope includes this header" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
rest: "rest of the block\nsimple name Local" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
end: "after the block\nname gone" {
  width: 260
  height: 50
  style.fill: "#ffebee"
}
block -> before
before -> decl
decl -> rest
rest -> end
```

**Fig. 1.** Use-before-declaration sees an enclosing member of the same name, if any. The local name starts at its own header and dies with the block.

> [!warning] `extends Cyclic` is yourself
> The scope includes the declaration. `class Cyclic extends Cyclic` does not pick the member class `Host.Cyclic`. Write `extends Host.Cyclic` if that is what you meant. `new Cyclic()` **before** the local declaration is the member class.

> [!warning] Same simple name twice in the remaining block
> A second `class Local` in a nested `{ }` still sits in the outer Local’s scope and fails. Moving it into a nested class’s method is the allowed hole. Locals, parameters, and local classes are **simple-name only** — there is no `this.Local` escape.

> [!warning] JDK 8 “no interfaces, no static members” is stale
> Since **Java SE 16**, a local **interface** is legal (implicitly `static`), and a local inner class may declare static members and static initializers, not only constant variables. The class itself still cannot be marked `static`. Capture of locals still requires effectively final (since **Java SE 8**).

> [!tip] Interview answer
> **A local class is a named nested class written inside a block. Its name is in scope from its own declaration to the end of that block — including the header, so it can accidentally extend itself.** You cannot give it `public` or `private`, and you cannot redeclare that name in the same remaining block except inside another nested type. **It captures enclosing members and effectively final locals; in a static method there is no enclosing instance.**
