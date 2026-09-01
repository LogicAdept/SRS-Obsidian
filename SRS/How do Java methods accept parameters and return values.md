<!--
reps: 0
priority: 0
-->
#Java/Language/Parameters #SRS

# How do Java methods accept parameters and return values?

> [!abstract] Short answer
> They **copy argument values in** to new parameter variables, run the body, then **copy a result out** if the method has a return type. `void` produces no value. A `return expr;` makes `expr`'s value become the value of the call. A returned reference is a pointer, just like an incoming one — not a clone of the object.

## In: parameters

The declaration lists **parameters**. The call supplies **arguments**. Each invocation creates new parameter variables and initializes them with the argument values (after conversion to the parameter types). A primitive argument copies bits. A class, interface, or array argument copies a **reference** ([[How are parameters passed in Java]], [[Does Java pass arguments by reference or by value]]).

The callee can mutate a shared mutable object through that copied pointer. Assigning a new object to the parameter does not retarget the caller.

## Out: the result

The method's **result** is either a return type or `void`.

- **`void`:** the invocation produces no value, so it can only appear where a value is not needed. A bare `return;` is optional and only exits early. `return expr;` does not compile.
- **A return type `T`:** the body must not "drop off the end." Every normal path uses `return expr;` where `expr` is assignable to `T`. A method that always throws may omit `return` entirely. `return;` with no value does not compile. Constructors have no result; they cannot `return expr`.

The value of `expr` becomes the value of the invocation. That outbound value follows the same split as inbound arguments: a primitive result copies bits; a reference result copies a pointer. Returning `this` or a parameter therefore shares the object with the caller.

A subclass may override with a **narrower reference** return type ([[Can you declare a narrower return type when overriding a method]]). Primitive return types must stay identical.

```d2
direction: right
in: "Copy arguments\ninto fresh parameters" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
body: "Run the body" {
  width: 160
  height: 80
  style.fill: "#fff3e0"
}
out: "void: no value\nelse: return expr" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
in -> body -> out
```

**Fig. 1.** Copy-in, run, then either no result or a copy of the returned value.

```java
public final class AcceptAndReturn {
    static int scale(int n, int factor) {
        return n * factor;
    }

    static StringBuilder appendBang(StringBuilder sb) {
        sb.append('!');
        return sb;
    }

    static void bump(int[] cells) {
        cells[0]++;
    }

    public static void main(String[] args) {
        int x = scale(3, 4);                 // 12; 3 is unchanged

        StringBuilder b = new StringBuilder("ok");
        StringBuilder same = appendBang(b);  // b == same, contents "ok!"

        int[] a = { 1 };
        bump(a);                             // a[0] is 2
        // int z = bump(a);                  // does not compile: void
    }
}
```

**Listing 1.** Primitive copy-in/copy-out (`scale`), shared builder returned (`appendBang`), and a `void` writer (`bump`).

If `return` sits inside `try`, every enclosing `finally` still runs before control reaches the caller. A `return` or `throw` in that `finally` **replaces** the original result.

```java
static int displaced() {
    try {
        return 1;
    } finally {
        return 2;
    }
}
```

**Listing 2.** `displaced()` returns `2`. The `return 1` never becomes the invocation's value.

> [!warning] `finally` can discard the value you thought you returned
> `return` always completes abruptly. A `finally` that itself `return`s or throws wins. The same surprise happens when you return a live mutable object: the caller holds a pointer, not a snapshot, so later `append` on that object is visible ([[Why is java.lang.String immutable and final]]).

> [!tip] Interview answer
> Parameters are copy-in: new variables holding the argument values, bits for primitives and a pointer for objects. The result is either `void` or a `return` expression whose value becomes the call's value — again a copy, not a cloned object. A non-void method cannot fall off the end of the body; `finally` can still replace that returned value.
