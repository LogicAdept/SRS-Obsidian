<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Static #Java/OOP/Polymorphism #SRS

# Can an instance method overload a static method in Java?

> [!abstract] Short answer
> **Yes**, when the signatures are **not override-equivalent**. Overloading is same name, different parameter types. `static` is **not** part of a signature. An instance method and a class method may share a name in one class or across a superclass. The **same** signature is a compile-time error: an instance method cannot override a `static` method, and a `static` method cannot hide an instance method. Overloading: [[How would you explain method overloading in Java]]. Versus override: [[How would you explain Overload vs Override]].

## Signatures decide; `static` does not

Two methods of a class (both declared, both inherited, or one of each) overload a name when they have that name and signatures that are **not** override-equivalent. That fact is never itself a compile-time error. There is no rule that both must be instance methods or both `static`.

A signature is the name, type parameters, and formal parameter types. Return type, `throws`, and `static` versus instance do not create a new signature. `foo(int)` as a class method next to `foo(int)` as an instance method is the same signature twice — illegal in one class body.

Call sites pick a signature at **compile time** from the argument types. If the chosen method is an instance method, the JVM then looks up an override. If it is a class method, that is the last word: no runtime dispatch. Class methods: [[How would you explain static methods in Java]]. Instance vs static members: [[What is the difference between an instance member and a static member in Java]].

```d2
direction: down
name: "same name\ninstance + static" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
diff: "parameter types differ\noverload — legal" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
same: "override-equivalent\ncompile-time error" {
  width: 240
  height: 50
  style.fill: "#ffcdd2"
}
name -> diff
name -> same
```

**Fig. 1.** Mixing instance and `static` is overloading only when the parameter lists differ.

```java
class Counter {
    static int of(int n) {
        return n;
    }

    int of(String s) {
        return s.length();
    }
}

class Sub extends Counter {
    int of(long n) {
        return (int) n;
    }
}

class Demo {
    static int use() {
        Counter c = new Sub();
        int fromStatic = Counter.of(3); // class method
        int fromInst = c.of("ab");      // instance method
        int viaRef = c.of(3);           // still Counter.of(int) — class method
        int fromSub = ((Sub) c).of(4L); // Sub.of(long)
        return fromStatic + fromInst + viaRef + fromSub;
    }
}
```

**Listing 1.** `of(int)` is `static`; `of(String)` and `of(long)` are instance methods. All three overload. `c.of(3)` is **not** dispatched on `Sub`.

```java
// Conceptual: does not compile
class Counter {
    static int of(int n) { return n; }
    int of(int n) { return n; }       // same signature in one class
}

class Sub extends Counter {
    int of(int n) { return n; }       // instance cannot override static
}
```

**Listing 2.** Conceptual. Override-equivalent signatures are not overloads. The subclass form tries to override a `static` method. The reverse mix (`static` hiding an instance method) is also illegal: [[Can static method be override or]] and [[Can static methods be overridden in Java]].

A legal overload still binds the class-method alternative using the **compile-time** type of the qualifier. `Counter c = new Sub(); c.of(3)` does not look for `Sub.of(int)` even if `Sub` declared a hiding `static of(int)`.

> [!warning] Same parameters is not “overload with static as the difference”
> `static void f(int x)` and `void f(int x)` do not overload. Changing only the return type does not help. Add, remove, or change a parameter type.

> [!warning] `obj.staticMethod(args)` is still a class-method call
> The expression is evaluated (and NPE is **not** thrown for a class method declared on a **class** if the qualifier is null). It is not `this`, and it is not override dispatch. Prefer `ClassName.method(...)`.

> [!warning] A subclass instance method with the same signature is override, not overload
> That override is illegal when the superclass method is `static`. Different parameter list: overload. Same parameter list: error, not “instance version of the static method.”

> [!tip] Interview answer
> Yes. An instance method can overload a static method if the parameter lists differ, because static is not part of the signature. Same name and same parameters is a compile-time error, whether they sit in one class or a subclass tries to “override” the static method. Overload resolution is compile-time; only a chosen instance method is dispatched at run time.
