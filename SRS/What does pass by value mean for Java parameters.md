<!--
reps: 0
priority: 0
-->
#Java/Language/Parameters #DataAndState/ValueSemantics #SRS

# What does pass by value mean for Java parameters?

> [!abstract] Short answer
> It means the callee receives a **new variable holding a copy of the argument's value**, not an alias of the caller's variable and not a clone of a heap object. That value is either primitive bits or a **reference** (a pointer). Copying the pointer still shares the object; copying is not deep copy.

## The value that gets copied

On every invocation Java creates fresh parameter variables and initializes them with the argument values. Pass-by-value is that copy-in step. There is no later copy-out: when the body finishes, the parameters disappear and the caller's variables are unchanged except for mutations you made **through** a copied pointer.

Two kinds of values exist, so two kinds of copies:

- **Primitive.** The bits move. `n = n + 1` inside the method does not change the caller's `int`.
- **Reference.** The pointer moves. The callee's parameter and the caller's variable can refer to the **same** instance or array. Field writes are visible. `param = other` is not.

```d2
direction: right
arg: "argument value\nbits or pointer" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
copy: "parameter =\ncopy of that value" {
  width: 230
  height: 80
  style.fill: "#fff3e0"
}
not: "not an alias of the\ncaller's name, not a clone" {
  width: 260
  height: 80
  style.fill: "#ffebee"
}
arg -> copy
copy -> not: "does not mean"
```

**Fig. 1.** Pass-by-value names the copy. It does not name object cloning.

```java
public final class PassByValueMeans {
    static void bump(int n) {
        n++;
    }

    static void rename(StringBuilder sb) {
        sb = new StringBuilder("copy");
    }

    static void append(StringBuilder sb) {
        sb.append('!');
    }

    public static void main(String[] args) {
        int n = 1;
        bump(n);                              // n is still 1

        StringBuilder b = new StringBuilder("hi");
        rename(b);                            // b is still "hi"
        append(b);                            // b is "hi!"
    }
}
```

**Listing 1.** Independent primitive copy; independent pointer copy; shared object when you follow the pointer ([[How are parameters passed in Java]], [[Does Java pass arguments by reference or by value]]).

That is the whole meaning in Java. Constructors and lambdas use the same create-and-copy rule. There is no second mode in which a parameter **is** the caller's variable ([[Does Java pass arguments by reference or by value]]). Returning a value is the same kind of copy on the way out ([[How do Java methods accept parameters and return values]]).

> [!warning] “By value” does not mean “the object is copied”
> Interview answers that split “primitives by value, objects by reference” are using the term wrong. Both are by value. If objects were copied by value in the deep-copy sense, `list.add(x)` inside a method could not change the caller's list. It does — because the **reference** was the value that was copied.

> [!tip] Interview answer
> Pass-by-value means the method gets a copy of the argument in a new variable. For an `int` that copy is the number; for an object it is the reference, so the object is shared but the caller's variable is not. It never means Java cloned the object, and it never means objects are passed by reference.
