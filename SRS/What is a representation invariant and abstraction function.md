<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Methodologies/Principles #SRS

# What is a representation invariant and abstraction function?

> [!abstract] Short answer
> Liskov and Guttag's vocabulary for ADT implementations. The **rep invariant (RI)** is a predicate the private fields must satisfy in every legal object state — for `Fraction`: `den > 0` and `gcd(|num|, den) = 1`. The **abstraction function (AF)** maps the rep to the abstract value the client sees — `3/2` and `6/4` are different reps denoting the same rational. Disciplined code documents both and runs a private **checkRep** on every rep-touching path ([[What is encapsulation]]).

## The rep invariant: what fields may hold

The RI narrows what the raw fields are allowed to mean. A fraction's fields could legally hold `6/4`, but the class *chooses* the normalized form so that `equals`, `hashCode`, and arithmetic stay simple and safe ([[What is the Object equals contract]]). Every constructor and every mutator must **establish or preserve** the RI; a method may *assume* it on entry — that is the implementor's shield that keeps bodies short, and it only works if access control actually fences the rep from outside writes ([[How would you explain encapsulation in object oriented design]]).

## The abstraction function: what the fields mean

The AF is the mapping from concrete state to abstract value: fields `(3, 2)` denote the rational 3/2. It is **many-to-one** — `(6, 4)` would denote the same value had the RI allowed it. Clients reason only in the abstract space; the AF is precisely the part that must not leak, which is why "return the internal list" breaks the abstraction, not just encapsulation ([[What is an anemic domain model and is it useful]] keeps invariants *in* the object for the same reason).

## checkRep: making the invariant executable

The practice from *Program Development in Java*: a private `checkRep()` asserting the RI, called on entry to and exit from every rep-affecting method during development. Java `assert` is disabled by default, so in production it costs nothing — but while developing, a violation surfaces at the mutation site instead of three operations later ([[When is the assert detail expression evaluated]]). The sandbox run shows the constructor normalizing `6/4` to `3/2` and rejecting `den = 0` outright ([[How would you explain programming by contract and preconditions]]).

```d2
direction: down
rep: "rep space\n(3,2)  (6,4)  (9,6)" {
  width: 240
  height: 64
  style.fill: "#fff3e0"
}
af: "AF: many-to-one\nRI filters legal reps" {
  width: 260
  height: 60
  style.fill: "#fff8e1"
}
abs: "abstract space\nthe rational 3/2" {
  width: 240
  height: 56
  style.fill: "#e8f5e9"
}
rep -> af
af -> abs
```

**Fig. 1.** Many concrete reps may denote one abstract value; the RI decides which reps are legal at all.

```java
class Fraction {
    private int num;
    private int den;                     // rep invariant: den > 0 && gcd(|num|, den) == 1

    Fraction(int num, int den) {
        if (den == 0) throw new IllegalArgumentException("den = 0");
        if (den < 0) { num = -num; den = -den; }
        int g = gcd(Math.abs(num), den);
        this.num = num / g;
        this.den = den / g;
        checkRep();
    }
    private static int gcd(int a, int b) { return b == 0 ? a : gcd(b, a % b); }
    private void checkRep() {
        if (den <= 0 || gcd(Math.abs(num), den) != 1)
            throw new IllegalStateException("rep invariant broken: " + num + "/" + den);
    }
    @Override public String toString() { return num + "/" + den; }
}
```

**Listing 1.** Normalization establishes the RI; `checkRep` verifies it on every rep-touching path.

```text
normalized: 3/2
den=0 -> rejected: den = 0
```

**Listing 2.** Verbatim run (JDK 21.0.12.1, sandbox `oop_15`): `6/4` enters, the RI-compliant `3/2` is stored and printed; `den = 0` is rejected at construction.

> [!warning] "The invariant is the constructor's job, done once" is false
> Every path that touches the rep must restore the RI — mutators, factories, deserialization, builders. A single `setDenominator` that skips normalization invalidates `equals` and every arithmetic method downstream. That is why disciplined code runs `checkRep` on entry *and* exit, and why invariants belong inside the object rather than in whatever service happens to touch the data ([[What does behavioral subtyping require beyond matching signatures]]).

> [!tip] Interview answer
> The rep invariant states what the private fields must always satisfy; the abstraction function says which abstract value a concrete state denotes — many states may denote the same one. Together they are the implementor's contract: methods inside may assume the RI and must re-establish it before returning. I write a private checkRep early in development so violations are caught at the mutation site, not three operations later.
