<!--
reps: 0
priority: 0
-->
#Java/Language/Parameters #DataAndState/ValueSemantics #SRS

# How are parameters passed in Java?

> [!abstract] Short answer
> **By copying values into new parameter variables.** The call first evaluates the argument expressions, then assigns each resulting value into a **fresh** parameter for that invocation. A primitive argument copies the bits. A class, interface, or array argument copies the **reference** (a pointer to the object). The caller's variables are not aliases of those parameters.

## Call sequence

**Parameter** means a variable in the method or constructor declaration. **Argument** means the value supplied at the call site. They must match in type and order.

On each invocation:

1. Argument expressions run left to right, producing argument values.
2. A new activation frame is created. Each formal parameter becomes a **new** variable, initialized with the corresponding argument value (after invocation conversion to the parameter type). An instance call also receives the target object as `this`.
3. The body runs, using those parameter names.
4. When the body completes, the parameter variables cease to exist. Nothing writes the copies back into the caller.

Constructor parameters and lambda parameters follow the same create-and-initialize rule.

```d2
direction: right
eval: "1. Evaluate arguments\nleft to right" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
copy: "2. Copy values into\nfresh parameters" {
  width: 230
  height: 80
  style.fill: "#fff3e0"
}
body: "3. Run the body\nthen drop the copies" {
  width: 230
  height: 80
  style.fill: "#e8f5e9"
}
eval -> copy -> body
```

**Fig. 1.** Passing is copy-in. There is no copy-out and no alias of the caller's variable.

```java
public final class HowArgsArePassed {
    static int twice(int n) {
        n = n * 2;
        return n;
    }

    static void fill(int[] cells, int value) {
        cells[0] = value;
        cells = new int[] { -1 };
    }

    public static void main(String[] args) {
        int x = 4;
        int y = twice(x);     // x is still 4; y is 8

        int[] a = { 0 };
        fill(a, 7);           // a[0] is 7; a is still the same array
    }
}
```

**Listing 1.** `twice` rewrites only its copy of `4`. `fill` writes through the copied array pointer, then rebinds its own `cells` — the caller still holds `{ 7 }` ([[Does Java pass arguments by reference or by value]], [[What does pass by value mean for Java parameters]]).

A reference value is a pointer to a class instance or an array (or `null`). Copying it gives the callee a second pointer to the **same** object, which is why `cells[0] = value` is visible. Replacing the pointer (`cells = new int[] { -1 }`) is not.

That is the whole passing mode. Java has no pass-by-reference form that would let the callee retarget the caller's variable. `final` on a parameter only forbids assigning that copy again; it does not freeze a mutable object. Immutable types such as `String` only hide mutation because there is nothing to mutate ([[Why is java.lang.String immutable and final]]).

> [!warning] Visible mutation is not a second passing mode
> If a method does `list.add(x)` or `arr[i] = v` and the caller sees it, the **object** was shared. The **parameter** was still a copied pointer. A later `list = new ArrayList<>()` or `arr = new int[0]` inside the method leaves the caller's variable unchanged. Same rule for `Integer` vs `int`: only the copied value differs ([[What is the difference between int and Integer in Java]]).

> [!tip] Interview answer
> Arguments are passed by value: the method gets brand-new parameter variables holding copies of the argument values. For objects that copy is the reference, so the callee shares the object and can change its state, but assigning a new object to the parameter does not change the caller. Evaluate arguments, copy them in, run the body, throw the copies away.
