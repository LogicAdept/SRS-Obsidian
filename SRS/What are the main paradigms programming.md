<!--
reps: 0
priority: 0
-->
#Java/OOP #Paradigms/OOP #SRS

# What are the main paradigms programming?

> [!abstract] Short answer
> Common interview families: **imperative** (how: statements, assignment, loops), **declarative** / **functional** (what: expressions, transformations), and sometimes **reactive** (values over time). **Java** is specified as a **general-purpose, concurrent, class-based, object-oriented** language: objects + `this`, one superclass, interfaces, static typing ([[What does it mean that Java is object oriented]]; [[How would you explain static typing in Java]]). You still write **imperative** statements. Lambdas and `Stream` are a **functional style** on that VM ([[Which programming paradigm does the Streams API follow]]; [[How would you explain the functional programming paradigm]]). OOP principles: [[What are the main oop principles]].

## Families, then where Java sits

**Imperative.** The program is a sequence of commands that **change state**. Java’s blocks and statements (assignment, `if`, `for`, method bodies) are this style. Textbooks often put **procedural**, **structured**, and **OOP** under this umbrella because objects still execute statements. OOP in Java is **class-based**: instance methods run with a current object `this`.

**Declarative / functional.** You describe the result; evaluation details stay implicit. **SQL** is the usual non-Java example. **Functional** programming emphasizes immutable values, functions as values, and expressions ([[What ideas sit at the center of the functional programming paradigm]]). The dump’s “declarative programs have no variables or assignment” is **too strong**—even FP languages bind names. Java is **not** a functional language first; `stream().map(...).sum()` is still bytecode that mutates an accumulator inside the library.

**Reactive.** Dataflow: when an upstream value changes, downstream updates. Not in the JLS’s one-line language definition. In Java interviews it means libraries on top of threads/`Flow`, not a third way to write `class`.

**Java mix.** Imperative OO is the default. `static` methods and primitives are not “objects all the way down.” Concurrency (`synchronized`, threads) is specified separately from “paradigm.” Tradeoffs of OO: [[What are the advantages and disadvantages of object oriented programming]].

There is no JLS table of “the main paradigms.” Name the families, then pin Java to **class-based OO + imperative statements + optional functional style**.

```d2
direction: down
imp: "imperative\nstatements, state" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
oo: "class-based OOP\nthis, types, dispatch" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}
fn: "functional style\nlambdas, Stream" {
  width: 240
  height: 45
  style.fill: "#fff8e1"
}
imp -> oo: "Java default"
oo -> fn: "Java 8+"
```

**Fig. 1.** Java’s spec identity is class-based OO. Imperative statements are how methods run. Streams are an extra style.

```java
class Total {
    static int loop(int[] a) {
        int s = 0;
        for (int n : a) {
            s += n;
        }
        return s;
    }

    static int stream(java.util.List<Integer> a) {
        return a.stream().mapToInt(Integer::intValue).sum();
    }
}
```

**Listing 1.** `loop` is imperative. `stream` is a functional pipeline that still runs on the same class-based language. Both can live in one class.

> [!warning] “OOP ⊂ imperative” is a textbook split, not a law
> Some schools treat OOP as message passing and contrast it with both imperative and FP. In a **Java** interview, OOP means classes, interfaces, and dispatch, implemented with imperative method bodies.

> [!warning] Declarative does not mean “no state in the JVM”
> A stream pipeline is easier to read as “what.” The JDK implementation is loops and arrays. Lambdas can capture and mutate locals if they are effectively final—or mutate heap objects they refer to.

> [!warning] Do not list ten paradigms
> Imperative vs declarative/FP, plus OOP as Java’s organizing model, is enough. Logic (Prolog), array (APL), and reactive get a sentence only if asked.

> [!tip] Interview answer
> The main families are imperative programming, object-oriented programming, and functional or declarative style; reactive is an extra dataflow model. Java is a class-based object-oriented language with imperative statements and, since Java 8, lambdas and streams. It is not a pure functional language. Say how those styles show up in Java rather than reciting a taxonomy with no types or `this`.
