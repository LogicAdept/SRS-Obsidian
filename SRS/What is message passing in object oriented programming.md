<!--
reps: 0
priority: 0
-->
#Java/OOP #Paradigms/OOP #SRS

# What is message passing in object oriented programming?

> [!abstract] Short answer
> In OOP textbooks, **message passing** means: ask an **object** to **do something**, with **arguments**; the object’s **method** of that name runs. In **Java** that is a **method invocation** (`ball.bounce()`), not a separate language feature. For **instance** methods the JVM still **looks up** the body on the **run-time class** ([[What is polymorphism]]; [[How would you explain dynamic runtime polymorphism in Java]]). The compiler already chose the **signature** ([[How would you explain Overload vs Override]]). Java OO: [[What does it mean that Java is object oriented]]. Principles: [[What are the main oop principles]].

## Smalltalk word, Java method call

**Dump (the bounce story).** Procedural code: `bounce(id, …)` and a table of ball data. OO: each ball is an object that **contains** its state **and** `bounce()`. You send **that object** the bounce **message** instead of passing a ball number into a global procedure.

**Java.** `b.bounce()` is a method invocation expression. Compile time: name, argument types, accessibility → one **signature**. Run time (virtual/interface instance call): start from the **class of the target object**, find the method that **overrides** that signature ([[How would you explain method overriding in Java]]). `null` → `NullPointerException`. `static` calls (`Type.m()` or even `obj.m()` when `m` is static) do **not** look up on the object; they are not message passing in the Kay sense.

**“Only way to transfer control.”** False in Java. Field access, `new`, `this()`/`super()`, and `static` methods all transfer control without an instance message. You can read `b.x` with no method. Encapsulation **asks** you not to; the language still allows `public` fields.

**“Extreme late binding.”** Overstated. Java is **statically typed** ([[How would you explain static typing in Java]]): the compiler must see `bounce` on the **compile-time** type. Late binding is **which body** of that signature runs. Smalltalk can send a name the compiler never checked.

The dump’s first block (Object’s `equals` / `hashCode` / …) is a **different** question. Root type: [[How would you explain java.lang.Object as the root of the class hierarchy]].

```d2
direction: down
msg: "b.bounce()\nmessage / invocation" {
  width: 240
  height: 45
  style.fill: "#e3f2fd"
}
ct: "compile time\nsignature bounce()" {
  width: 220
  height: 45
  style.fill: "#fff8e1"
}
rt: "run time\nbody in b's class" {
  width: 220
  height: 45
  style.fill: "#e8f5e9"
}
msg -> ct
ct -> rt: "if instance"
```

**Fig. 1.** A “message” in Java is an invocation. Signature first, then (for instance methods) the run-time class.

```java
class Ball {
    int x;

    void bounce() {
        x = -x;
    }
}

class Use {
    static void go(Ball b) {
        b.bounce();
    }
}
```

**Listing 1.** `go` sends bounce to `b`. A `HeavyBall extends Ball` that overrides `bounce` still compiles as `Ball`; the extra body is chosen at run time. `bounce(b)` as a static helper would be the procedural style the dump contrasts.

> [!warning] Not a Java keyword and not `Object`’s method list
> There is no `send`. Do not answer this cue with `equals`/`wait`/`finalize`. Those are members of `Object`, not the definition of messaging.

> [!warning] Overload resolution is not a message lookup
> `f(Shape)` vs `f(Ball)` is chosen from the **variable’s type**. Only `b.bounce()` on an instance method is polymorphic. `static void bounce(Ball b)` is a procedure with an object argument.

> [!warning] Field access is not a message
> `b.x = 1` mutates without calling a method. Message-passing style in Java is **methods as the API** (encapsulation), which you choose; it is not enforced.

> [!tip] Interview answer
> Message passing is the OOP name for asking an object to run a method with arguments. In Java that is `obj.method(args)`: the compiler picks a signature, then instance methods dispatch on the run-time class. It is not extreme late binding of unchecked names, and it is not the only way two pieces of code interact. Contrast it with a global `bounce(id)` that reaches into a data table.
