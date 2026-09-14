<!--
reps: 0
priority: 0
-->
#Java/OOP/Initialization #SRS

# What triggers class initialization in Java

> [!abstract] Short answer
> A closed list: an instance of the class is created, a static method declared by it is invoked, a static field declared by it is assigned, or a non-constant static field declared by it is used; plus certain reflective calls and the initialization of a subclass. Superclasses initialize first. Everything else stays lazy — `T.class`, declaring a variable of the type, or reading a compile-time constant never initializes.

## The closed list

The language spec states that a class or interface T will be initialized immediately before the first occurrence of any one of the following: T is a class and an instance of T is created; a static method declared by T is invoked; a static field declared by T is assigned; a static field declared by T is used and the field is not a constant variable. Invocation of certain reflective methods in class `Class` and in `java.lang.reflect` also causes initialization — one-arg `Class.forName` is the deliberate one ([[What is the difference between loadClass and Class.forName in Java]]). The virtual machine states the same list through bytecode: the `new`, `getstatic`, `putstatic`, and `invokestatic` instructions referencing the class, plus a subclass's initialization. A class or interface will not be initialized under any other circumstance. What serializes the run itself under concurrent first use: [[How does the JVM guarantee thread safety during class initialization]].

## What stays lazy

Reading a static field that is a constant variable does nothing at runtime: its value was folded into the calling code at compile time. A class literal `T.class` only loads, and creating an array of `T` does not initialize `T` itself. A reference to a static field causes initialization of only the class or interface that actually declares it, even though it might be referred to through the name of a subclass — inheritance in the source does not drag the subclass into initialization.

```java
class Config {
    static final int LIMIT = 10;          // constant variable
    static final String NAME = "app";     // constant variable
    static int version = 2;               // not a constant variable
    static { System.out.println("Config ready"); }
}

int limit = Config.LIMIT;      // no output: compile-time constant, folded in
int v = Config.version;        // prints "Config ready": getstatic on non-constant
Class<?> c = Config.class;     // no output: class literal only loads
Config[] arr = new Config[3];  // no output: array creation does not initialize Config
```

**Listing 1.** Constant reads, class literals and array creation all skip `<clinit>`; a non-constant static read is the classic trigger.

## The superclass rule

When a class is initialized, its superclasses are initialized first, as well as any superinterfaces that declare default methods. The superclass's static state is therefore fully built before the subclass's `<clinit>` runs ([[How would you explain static initialization order in Java]]). Initialization of an interface does not, of itself, cause initialization of its superinterfaces, and initializing a class does not touch interfaces unless they declare default methods.

```d2
direction: down
use: "Code touches T somehow" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
active: "Active use?\nnew · static method · assign ·\nread non-constant static ·\nreflective opt-in · subclass init" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
passive: "Passive?\nT.class · constant read ·\nvariable declaration ·\narray creation" {
  width: 240
  height: 90
  style.fill: "#ffebee"
}
init: "initialize T\n(superclass first)" {
  width: 180
  height: 55
  style.fill: "#e8f5e9"
}
done: "no <clinit>" {
  width: 130
  height: 50
  style.fill: "#e8f5e9"
}
use -> active
use -> passive
active -> init
passive -> done
```

**Fig. 1.** Every kind of reference to T lands on one of the two branches; only the active branch reaches `<clinit>`, and the list of active forms is closed.

> [!note] Synthetic default methods count
> The compiler may generate synthetic default methods in an interface — default methods that are neither explicitly nor implicitly declared in the source. Such methods will trigger the interface's initialization despite the source code giving no indication that the interface should be initialized.

> [!warning] Constants hide your side effects
> A "constants holder" class whose fields are all `static final` primitives or strings never runs its static block on use — every read was folded at compile time. If you put logging or registration inside `<clinit>` of such a class, it will silently never execute on constant reads; the same list explains why a failed initialization is also terminal: the class is marked erroneous and later uses fail with `NoClassDefFoundError` ([[What happens if you use a class after ExceptionInInitializerError]]).

> [!tip] Interview answer
> **Initialization runs on first active use: `new`, a static method, writing a static field, reading a non-constant static field, certain reflective calls, or a subclass being initialized — superclasses first. Class literals, constant reads, variable declarations and array creation do not initialize. The list is closed, and `Class.forName` is the one reflective call that opts in deliberately.**

