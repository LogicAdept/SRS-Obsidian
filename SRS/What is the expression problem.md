<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Paradigms/Functional #SRS

# What is the expression problem?

> [!abstract] Short answer
> Wadler's formulation: define a datatype and a set of operations over it so that you can add **new cases** and **new operations** without modifying (or recompiling) existing code, while keeping static type safety. Classical OOP adds cases easily (a new class implements the interface) but new operations mean editing every class — or a Visitor, which flips the asymmetry. Closed sums with pattern matching add operations client-side but new cases touch every match. Java 17+ **sealed interfaces + exhaustive `switch`** give a checked middle ground ([[What are switch expressions]]).

## The matrix

Put data variants in rows and operations in columns. Subtype-and-override grows **rows** cheaply — a new class adds itself to the family, no existing code changes — but a new **column** means touching every row (or accepting a central `if`-chain). A closed sum with an exhaustive matcher grows **columns** cheaply — write a new `switch` in client code — but a new row means editing every switch. The expression problem is the demand for both axes at once without losing exhaustiveness checking.

## Java's answer: sealed + exhaustive switch

`sealed interface Expr permits Num, Neg, Add` fixes the row set while keeping the hierarchy *local and documented*; a pattern `switch` over it is **exhaustive** — the compiler rejects a missing case, so adding a variant surfaces every switch that must learn it. Operations like `eval` live entirely in client code: zero edits to the type declarations. That is the sandbox run: a new operation written against three untouched records ([[What is the difference between pattern matching and a switch statement]]).

## Choosing by the axis of change

If variants are stable and operations multiply — compilers, AST walkers, exporters — the sealed-plus-switch shape (or Visitor) wins ([[What is double dispatch and how do you implement it in Java]]). If operations are stable and variants multiply — plugin-style domain entities — open interfaces and subtype polymorphism win ([[What mechanisms implement polymorphism in Java]]). If *both* axes churn, the honest answers are modular visitors or object algebras — heavier machinery that exists precisely because the plain combinations cannot satisfy both demands.

```d2
direction: right
oop: "subtyping + override\nadd VARIANT: easy\nadd OPERATION: edit every class" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
fp: "closed sum + switch\nadd OPERATION: client-side\nadd VARIANT: edit every switch" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
mid: "sealed + exhaustive switch\nclient-side operations\ncompiler-checked coverage" {
  width: 270
  height: 80
  style.fill: "#e8f5e9"
}
oop -> mid: "seal the hierarchy"
fp -> mid: "move ops out of classes"
```

**Fig. 1.** Each style owns one extension axis; sealing plus exhaustive switching trades openness for checked coverage.

```java
sealed interface Expr permits Num, Neg, Add {}
record Num(int v) implements Expr {}
record Neg(Expr e) implements Expr {}
record Add(Expr l, Expr r) implements Expr {}

public class Demo {
    static int eval(Expr e) {
        return switch (e) {                    // exhaustive: compiler knows all subtypes
            case Num n              -> n.v();
            case Neg x              -> -eval(x.e());
            case Add(Expr l, Expr r) -> eval(l) + eval(r);
        };
    }
    public static void main(String[] args) {
        Expr e = new Add(new Num(2), new Neg(new Num(3)));
        System.out.println("eval = " + eval(e));
        System.out.println("permitted subtypes = " + Expr.class.getPermittedSubclasses().length);
    }
}
```

**Listing 1.** A new operation (`eval`) written entirely in client code against untouched type declarations.

```text
eval = -1
permitted subtypes = 3
```

**Listing 2.** Verbatim run (JDK 21.0.12.1, sandbox `oop_13`): the client-side operation evaluates 2 + (−3) = −1; the hierarchy reports its three permitted variants.

> [!warning] "Visitor solves the expression problem" is false
> Visitor only **flips the axis**: adding operations becomes easy, but each new element type breaks *every existing* visitor — the asymmetry is preserved, not removed ([[What is double dispatch and how do you implement it in Java]]). The same trap in reverse: believing sealed hierarchies are "closed to extension" — they are closed to *unchecked* extension; extending them is a compile-time-guided, deliberate edit of one line.

> [!tip] Interview answer
> The expression problem: add both new data variants and new operations without editing shipped code, keeping static safety. Classical subtyping favors new variants; exhaustive switches over sealed hierarchies favor new operations written client-side with compiler-checked coverage. I choose by the axis of change — growing operations means sealed switch or Visitor, growing variants means open interfaces.
