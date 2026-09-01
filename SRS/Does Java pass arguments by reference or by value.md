<!--
reps: 0
priority: 0
-->
#Java/Language/Parameters #DataAndState/ValueSemantics #DataAndState/ReferenceSemantics #SRS

# Does Java pass arguments by reference or by value?

> [!abstract] Short answer
> **By value.** The call does not pass the caller's variable. It creates a **new parameter variable** and copies the argument **value** into it. For a primitive that copy is the bits. For a class, interface, or array it is a **reference** (a pointer), not a clone of the object. The callee can mutate a shared mutable object through that copied pointer. It cannot make the caller's variable point somewhere else.

## What actually gets copied

`foo(x)` evaluates `x`, then copies that result. Each invocation creates fresh parameter variables, initializes them with those values, and runs the body. When the body finishes, the parameters go away. Nothing is written back into `x`. `final` on the caller's variable does not change that copy-in.

There are two kinds of values you can pass: primitive values and reference values. A reference is a pointer to a class instance or an array (or `null`). Copying a reference gives the callee a second pointer to the **same** object. That is still pass-by-value: the value being copied happens to be a pointer.

```d2
direction: right
caller: "caller: box\nstill points here" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
param: "parameter: boxCopy\ncopy of the pointer" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
obj: "heap object\nshared if mutable" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
caller -> obj
param -> obj
```

**Fig. 1.** Two variables, one object. Rebinding `boxCopy` does not rebind `box`.

```java
public final class PassByValue {
    static void bump(int n) {
        n = n + 1;
    }

    static void replace(StringBuilder sb) {
        sb = new StringBuilder("other");
    }

    static void append(StringBuilder sb) {
        sb.append('!');
    }

    static void swap(StringBuilder a, StringBuilder b) {
        StringBuilder tmp = a;
        a = b;
        b = tmp;
    }

    public static void main(String[] args) {
        int n = 1;
        bump(n);                          // n is still 1

        StringBuilder left = new StringBuilder("A");
        StringBuilder right = new StringBuilder("B");
        replace(left);                    // left is still "A"
        append(left);                     // left is "A!"
        swap(left, right);                // left still "A!", right still "B"
    }
}
```

**Listing 1.** `bump` / `replace` / `swap` rewrite only the copies. `append` mutates the one shared builder ([[What does pass by value mean for Java parameters]], [[How are parameters passed in Java]]).

The same reassignment check with `Object` and `int`: a method that does `o = null` and `i = 1000` leaves the caller's `o` and `i == 10` unchanged. A true pass-by-reference language would let `replace` and `swap` retarget the caller's variables. Java has no such mode: no `ref` / `out` parameters, and constructors and lambda parameters follow the same copy-in rule ([[How do Java methods accept parameters and return values]]).

A method that appears to swap two locals mutated a **holder** (array slot, `AtomicReference`, a one-field box) whose reference you copied, or the caller assigned returned values (`x = next(x)`).

## Why mutation looks like “by reference”

`append` changes fields of the object both pointers already share, so the caller sees `"A!"`. Arrays are objects too: `a[0] = 9` is visible; `a = new int[] { 9 }` is not. `list.add(x)` is visible for the same reason: only the pointer was copied, not the list.

`final` on a parameter only forbids assigning that parameter again. It does not freeze the object. A `final StringBuilder` can still `append`.

Immutable types hide the distinction. `String` and the wrappers have no mutating methods, so the only thing a method can do with its copy is rebind it — which the caller never sees. That is [[Why is java.lang.String immutable and final]] and [[Are Java wrapper types immutable]], not a second passing mode. Primitive `int` versus `Integer` is the same copy rule; only the value being copied differs ([[What is the difference between int and Integer in Java]]).

> [!warning] “Objects are passed by reference” is the wrong slogan
> Interviewers use a swap, a `String` reassignment, `o = null`, or `foo = new Foo()` after a mutation to catch this. If the callee cannot redirect the **caller's** variable, it was never pass-by-reference. “The parameter is a copy of the object” is also wrong: the object is not cloned, so field writes still show up.

> [!tip] Interview answer
> Java is pass-by-value only: the method gets a new variable holding a copy of the argument, not an alias of the caller's name. For objects that copy is the reference, so you can change the object's state and the caller will see it, but assigning a new object to the parameter — or swapping two parameters — does not change the caller's variables. The line “primitives by value, objects by reference” is the usual wrong split.
