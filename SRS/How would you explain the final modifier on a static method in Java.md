<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Final #Java/Language/Modifiers/Static #Java/OOP #SRS

# How would you explain the final modifier on a static method in Java?

> [!abstract] Short answer
> **`final` on a class method forbids hiding.** A `static` method is never overridden; a subclass `static` method with an override-equivalent signature **hides** the superclass one. If the superclass method is `final`, that hiding is a **compile-time error**. The subclass still **inherits** the class method and may **overload** it with a different signature. `final` in general: [[What does the final keyword mean in Java]]. Hiding vs override: [[Can static method be override or]]. Class methods: [[How would you explain static methods in Java]].

## Stop hiding, not dispatch

A method declared `final` may not be overridden **or hidden**. For `static`, only hiding is in play. Invocation of a class method is compile-time: the qualifier’s type picks the method. `final` does not change that mode; it only locks the name-plus-signature so a subclass cannot declare another class method that would hide it.

`private` methods and methods declared in a `final` class already behave as if `final` (nothing can override or hide them from outside that constraint). Interface methods — including `static` ones — **cannot** be declared `final`. `abstract` cannot combine with `static` or `final`.

A subclass may still call `Super.greet()` or, if it does not declare a hider, `Sub.greet()` as the inherited class method. A different parameter list is overloading, which `final` does not forbid.

```java
class Super {
    static final void greet() {
        System.out.println("super");
    }

    static void greet(int n) {
        System.out.println(n);
    }
}

class Sub extends Super {
    // static void greet() {}     // compile-time error: cannot hide final
    static void greet(String s) { // overload, not a hide
        System.out.println(s);
    }
}

class Demo {
    static void run() {
        Super.greet();
        Sub.greet();       // inherited Super.greet
        Sub.greet("hi");   // Sub's overload
        Super s = new Sub();
        s.greet();         // still Super.greet — compile-time type Super
    }
}
```

**Listing 1.** `final` blocks the zero-arg hider. Other signatures and inherited calls remain legal.

```d2
direction: down
sm: "static method in Super" {
  width: 220
  height: 40
  style.fill: "#fff8e1"
}
fin: "also final?" {
  width: 160
  height: 36
  style.fill: "#e3f2fd"
}
hide: "subclass static same signature\n= hiding" {
  width: 260
  height: 48
  style.fill: "#ffcdd2"
}
ok: "subclass may inherit / overload" {
  width: 260
  height: 44
  style.fill: "#e8f5e9"
}
sm -> fin
fin -> hide: "yes → compile error"
fin -> ok: "yes → no hider"
sm -> hide: "no final → legal hide"
```

**Fig. 1.** `static` + `final` is a hiding lock. It is not runtime polymorphism.

> [!warning] `Sub.greet()` is not “the subclass version”
> With `final`, there is no subclass version. `Sub.greet()` is still `Super`’s class method. Writing `s.greet()` on a `Super` variable never dispatched on `s`’s run-time class anyway.

> [!warning] `final static` is not a substitute for `private`
> Other classes can still call a `public static final` method. `final` only stops **subclasses** from hiding it. Interface `static` methods cannot take `final` at all.

> [!tip] Interview answer
> Final on a static method means a subclass cannot hide it with another static method of the same signature. Static methods are not overridden, so final is not about virtual dispatch. The subclass can still inherit the method and can overload other signatures.
