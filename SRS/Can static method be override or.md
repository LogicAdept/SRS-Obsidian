<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Static #Java/OOP #SRS

# Can static method be override or?

> [!abstract] Short answer
> **Overloaded: yes. Overridden: no.** Two class methods may share a name when their signatures are **not override-equivalent** — that is ordinary overloading. A subclass `static` method with an override-equivalent signature **hides** the superclass class method; it does **not** override it. There is no runtime dispatch on the class method. Overloading: [[How would you explain method overloading in Java]]. Versus override: [[How would you explain Overload vs Override]]. Hiding vs override: [[Can static methods be overridden in Java]].

## Hide at compile time, overload by signature

A method declared `static` is a **class method**. It is invoked without a particular object as `this`. An instance method is invoked with respect to an object and, if overridden, is selected at run time. Overload resolution itself is always compile-time: the argument types pick a signature. If that signature is an instance method, the JVM then looks up an override. If it is a class method, the compile-time type of the target (or the class named in a qualified call) is the last word.

Hiding: a class that declares or inherits a `static` method `m` hides an accessible superclass class method when the signature of `m` is a subsignature of that method’s signature. **It is a compile-time error if a `static` method hides an instance method.** The other mix is also illegal: an instance method cannot override a `static` method. Instance-on-static with a **different** signature is overloading, not hiding: [[Can instance methods overload]].

A hidden class method is still callable through a name or receiver whose **compile-time type** is the class that declares it, or through `super`. `@Override` does not apply to hiding: that annotation is legal only when the method actually overrides a supertype method (or a few special `Object` / record-accessor cases), so putting it on a hiding `static` method is a compile-time error. A `final` class method cannot be hidden.

```java
class Super {
    static String greeting() { return "Goodnight"; }
    String name() { return "Richard"; }
}

class Sub extends Super {
    static String greeting() { return "Hello"; } // hides Super.greeting
    String name() { return "Dick"; }             // overrides Super.name
}

class Demo {
    public static void main(String[] args) {
        Super s = new Sub();
        System.out.println(s.greeting() + ", " + s.name());
        System.out.println(Sub.greeting());
    }
}
```

**Listing 1.** Prints `Goodnight, Dick` then `Hello`. `s.greeting()` uses the compile-time type `Super`. `s.name()` uses the run-time class `Sub`.

```java
class Util {
    static int max(int a, int b) {
        return a >= b ? a : b;
    }

    static int max(int a, int b, int c) {
        return max(max(a, b), c);
    }

    // static long max(int a, int b) { return a; } // illegal: same signature
}
```

**Listing 2.** Two `static` `max` methods overload each other. A different return type alone would not.

```d2
direction: down
sameName: "same name as a superclass method" {
  width: 260
  height: 40
  style.fill: "#fff8e1"
}
kind: "both static, override-equivalent?" {
  width: 260
  height: 44
  style.fill: "#e3f2fd"
}
hide: "hiding\ncompile-time type wins" {
  width: 240
  height: 48
  style.fill: "#e8f5e9"
}
overload: "overloading\n(different signature)" {
  width: 240
  height: 48
  style.fill: "#e8f5e9"
}
illegal: "compile error\nstatic vs instance mix" {
  width: 240
  height: 48
  style.fill: "#ffcdd2"
}
sameName -> kind
kind -> hide: "yes, static on static"
kind -> overload: "no, signatures differ"
kind -> illegal: "yes, one is instance"
```

**Fig. 1.** Same name in a subclass is hiding, overloading, or illegal — never overriding of a class method.

> [!warning] The superclass class method does not “always run”
> Hiding is legal. `Sub.greeting()` and a `Sub`-typed receiver call `Sub`’s class method. A `Super`-typed receiver calls `Super`’s, even when the object is a `Sub`. That is why a call written on an instance is easy to misread.

> [!warning] `@Override` will not save a hiding `static` method
> The method does not override, so `@Override` is a compile-time error. Mixing `static` and instance on an override-equivalent signature is also a compile-time error, not a cute overload.

> [!tip] Interview answer
> A static method can be overloaded like any other method if the parameter lists differ. It cannot be overridden: a subclass static method with the same signature hides the parent, and the compiler picks it from the compile-time type. An instance method cannot override a static method, and a static method cannot hide an instance method.
