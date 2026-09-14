<!--
reps: 0
priority: 0
-->
#Java/Language/Expressions #SRS

# What is a unary expression in Java?

> [!abstract] Short answer
> A **unary expression** is one unary operator applied to one operand: prefix `++` and `--`, unary `+` and `-`, `!`, `~`, or the cast — and the grammar routes switch expressions through this level too. Postfix `x++` and `x--` are *not* unary expressions: they are postfix expressions, one level lower. Unary operators group right-to-left, so `-~x` means `-(~x)`.

## The grammar above the postfix level

```d2
direction: down
u: "UnaryExpression" {
  width: 260
  height: 60
  style.fill: "#e3f2fd"
}
pre: "PreIncrement / PreDecrement\n++ x   -- x" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
plus: "Unary plus and minus\n+ x   - x\n(operand: any UnaryExpression)" {
  width: 320
  height: 90
  style.fill: "#fff3e0"
}
np: "UnaryExpressionNotPlusMinus\nno leading + or -\npostfix | ~ | ! | cast | switch" {
  width: 340
  height: 100
  style.fill: "#ffebee"
}
not: "~ x   ! x\n(operand: UnaryExpression)" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
cast: "CastExpression\n(Type) operand" {
  width: 250
  height: 60
  style.fill: "#fff3e0"
}
post: "PostfixExpression\nprimary | name | x++ | x--" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}
u -> pre
u -> plus
u -> np
np -> not
np -> cast
np -> post
```

**Fig. 1.** `~` and `!` recurse back into full unary expressions, while the operand slot under a cast — `UnaryExpressionNotPlusMinus` — never starts with `+` or `-`; postfix expressions are its base.

## Why the NotPlusMinus split exists

`+` and `-` are the only unary operators that are also binary operators, so the grammar splits the cast into cases. A cast to a **primitive type** takes any unary expression — a primitive keyword inside the parentheses can only start a cast, so `(double) + q` compiles as casting `+q`. A cast to a **reference type** takes a `UnaryExpressionNotPlusMinus`, so with a variable `p`, `(p) - q` is a subtraction of two values, never a cast of `-q`. The same operand slot accepts an entire postfix chain, which is why the method call lands inside the cast in [[Why does (Integer) t.intValue() not compile when t is declared as Object]].

## Small types and boxed operands

Operands of unary `+`, `-`, and `~` sit in a numeric arithmetic context: a boxed operand is unboxed first ([[When does autoboxing occur in Java]]), and `byte`, `short`, and `char` widen to `int`, so negating a `byte` yields an `int` ([[What are the storage sizes of Java primitive types]]).

```java
byte b = 2;
int promoted = -b;          // -2, of type int — byte widened
// short sh = -b;           // does not compile: int is not assignable to short
int x = 5;
int neg = -x;               // -5
int compl = ~x;             // -6 (same as -(x + 1))
int floor = -Integer.MIN_VALUE;   // wraps to Integer.MIN_VALUE, no exception
Integer boxed = null;
// int boom = +boxed;       // NullPointerException — unboxing in a numeric context
```

**Listing 1.** Unary minus widens small integer types to `int`, and negating `Integer.MIN_VALUE` overflows back to itself instead of throwing.

> [!warning] The postfix trap
> Quizzes like the claim "`x++` is a unary operator." It takes one operand, but in the grammar it is a **postfix** expression, not a unary expression — and the reverse surprise is that the **cast** *is* a unary operator. If a question asks what a unary expression includes, `x++` stays off the list while `(int) x` is on it.

> [!tip] Interview answer
> **A unary expression is one unary operator on one operand:** prefix `++`/`--`, `+`, `-`, `!`, `~`, or a cast, grouped right-to-left. Postfix `x++`/`x--` are postfix expressions instead, and reference-type casts take an operand that cannot start with `+` or `-` — the disambiguation that makes `(p) - q` a subtraction when `p` is a variable. Under unary `+`, `-`, and `~`, small types widen to `int`.

The base of this tower — primaries and suffix chains — is in [[What is a primary expression in Java]], and the wrap-around of the minimum value in [[What is the value range of the Java int type]].
