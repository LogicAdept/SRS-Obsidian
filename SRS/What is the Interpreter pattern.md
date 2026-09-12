<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Behavioral #SRS

# What is the Interpreter pattern

> [!abstract] Short answer
> Interpreter is a behavioral pattern: for a simple language, it defines a representation of its grammar as an Expression class hierarchy and an interpret operation that evaluates sentences of that language - instances of the problem become sentences the interpreter runs.

## How the pattern works

When a class of problems recurs - boolean search expressions, arithmetic formulas, rule conditions - the problem instances can be modeled as sentences of a small language. Interpreter represents the grammar as one class per rule: a terminal expression for the atomic tokens and a non-terminal expression per grammar rule, each implementing an interpret method that takes a context and returns a result. Non-terminals hold child expressions, so a parsed sentence forms a tree, and calling interpret on the root evaluates the whole sentence by recursion.

```java
import java.util.Map;

interface Expression {
    int interpret(Map<String, Integer> context);
}

record Number(int value) implements Expression {
    @Override
    public int interpret(Map<String, Integer> context) {
        return value;
    }
}

record Variable(String name) implements Expression {
    @Override
    public int interpret(Map<String, Integer> context) {
        return context.get(name);
    }
}

record Plus(Expression left, Expression right) implements Expression {
    @Override
    public int interpret(Map<String, Integer> context) {
        return left.interpret(context) + right.interpret(context);
    }
}
```

**Listing 1.** Each grammar rule becomes a class; `new Plus(new Number(2), new Variable("x")).interpret(Map.of("x", 40))` evaluates to 42 through the recursion.

```d2
direction: down
root: "Plus (non-terminal)\ninterpret = left + right" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
num: "Number (terminal)\n2" {
  width: 190
  height: 70
  style.fill: "#e8f5e9"
}
var: "Variable (terminal)\nx -> 40 from context" {
  width: 250
  height: 80
  style.fill: "#e8f5e9"
}
root -> num
root -> var
```

**Fig. 1.** A parsed sentence is a tree of expression objects; interpret flows from the root and the context supplies the terminal values.

## Where it fits and where it stops

The expression tree is a composite, so Interpreter and [[What is the Composite pattern]] share the recursive structure - the composite stores the tree, the interpreter gives it behavior. Adding new operations over the same tree rather than new grammar rules is the job of the [[How would you explain the Visitor design pattern]]. Interpreter appears in parsers for rule engines, query filters, and DSL fragments, often wrapped behind a facade or built with parser tooling instead of hand-written classes. Among [[What are examples of behavioral design patterns]] it is the rarest in mainstream business code, which is exactly why interviewers ask it occasionally.

> [!warning] Grammars grow, classes multiply
> One class per grammar rule means a rich language explodes the hierarchy, and any grammar change touches every expression class that references the rule - hand-maintaining a complex grammar this way is a losing battle, which is why real parsers switch to parser generators or data-driven tables. The pattern earns its place only for small, stable languages with a handful of rules; presenting it as the general way to build compilers is a red flag.

> [!tip] Interview answer
> Interpreter turns a simple language into an object structure: one class per grammar rule - terminals and non-terminals - each with an interpret method that recurses over child expressions against a context. A parsed sentence is a tree, so evaluating it is calling interpret on the root. It suits small, stable DSLs like boolean filters or formula evaluation; for large grammars the class count kills it, and you use parser tooling instead.
