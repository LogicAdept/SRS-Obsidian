<!--
reps: 0
priority: 0
-->
#Java/Language/Expressions #SRS

# What is a primary expression in Java?

> [!abstract] Short answer
> A **primary expression** is the simplest kind of expression that all others are built from: a literal, a class literal, `this`, a parenthesized expression, an object or array creation, a field access, an array access, a method invocation, or a method reference. Every bigger expression bottoms out in a primary, and nothing — not even a cast — can parse between a primary and the suffixes attached to it.

## The base of the expression grammar

```d2
direction: up
prim: "Primary\nliterals, class literals, this, (expr),\nnew, field access, array access,\nmethod invocation, method reference" {
  width: 380
  height: 140
  style.fill: "#e8f5e9"
}
post: "PostfixExpression\nPrimary | plain name | primary++ | primary--" {
  width: 360
  height: 80
  style.fill: "#fff3e0"
}
np: "UnaryExpressionNotPlusMinus\npostfix | ~ | ! | cast | switch" {
  width: 340
  height: 80
  style.fill: "#fff3e0"
}
un: "UnaryExpression\n++ -- + - on top of NotPlusMinus" {
  width: 340
  height: 70
  style.fill: "#fff3e0"
}
bin: "Binary operators\n* / % then + - then shifts, comparisons" {
  width: 360
  height: 70
  style.fill: "#e3f2fd"
}
prim -> post
post -> np
np -> un
un -> bin
```

**Fig. 1.** Each grammar level wraps the one below it, so the whole tower stands on primaries; a cast applies at the unary level, above the entire postfix chain.

## What counts as a primary

```java
String s = "abc";                  // literal — a primary
Class<?> c = String.class;         // class literal — a primary
int n = (1 + 2) * 3;               // (1 + 2) is a parenthesized primary
Object o = new Object();           // instance creation — a primary
int[] a = new int[3];              // array creation — a primary
int first = a[0];                  // array access — a primary
String up = s.concat("x")          // one primary: prefix s
             .toUpperCase();       // with .concat(...) and .toUpperCase() as suffixes
```

**Listing 1.** Every line bottoms out in a primary; suffix calls and index reads stay glued to their prefix.

## Names join one level up

A bare variable name such as `t` is not, strictly, a primary: the grammar keeps names separate so that a parser with one-token lookahead can tell `(z[3])` (a parenthesized array access) from `(z[])` (the start of a cast). Names and primaries become interchangeable at the postfix level — which is why a variable, a field read, and a method call all behave the same as cast operands and increment targets.

> [!warning] A cast cannot cut into a primary
> The popular reading of `(Integer) t.intValue()` — "cast `t`, then call `intValue`" — is impossible: the whole `t.intValue()` is one primary (prefix plus suffix), it becomes the cast operand as a unit, and `Object` has no `intValue()` to call. To invoke on the cast result you need a parenthesized primary: `((Integer) t).intValue()` — the parentheses themselves form a primary that the `.intValue()` suffix attaches to. The full trace is in [[Why does (Integer) t.intValue() not compile when t is declared as Object]].

Literals being primaries is also where constant expressions start — a [[What is a compile-time constant in Java]] is assembled from literals and constant variables before the compiler folds it.

> [!tip] Interview answer
> **A primary expression is the atomic unit of the Java grammar:** literals, `this`, parenthesized expressions, `new`, field accesses, array accesses, and method invocations. Unary and binary operators are layered on top, and a suffix chain like `t.intValue()` is a single primary — which is why `(Integer) t.intValue()` casts the whole call rather than just `t`, and why `((Integer) t).intValue()` needs parentheses.

The next level of the same tower — postfix and unary operators — is in [[What is a unary expression in Java]].
