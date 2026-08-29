<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #SRS

# What happens if you use a class after `ExceptionInInitializerError`?

> [!abstract] Short answer
> **The next use throws `NoClassDefFoundError`.** After static initialization fails, the class is marked **erroneous**. The JVM does **not** retry the static block. The first failure is typically `ExceptionInInitializerError` wrapping the initializer’s exception; later `new`, static-method, or static-field use throws `NoClassDefFoundError` instead of a second `ExceptionInInitializerError`.

## Failed initialization is sticky

`new A()`, a static method call, or a non-constant static field read can trigger class initialization. If a static initializer or class-variable initializer completes abruptly with an exception `E` that is **not** an `Error`, that `E` is wrapped in `ExceptionInInitializerError` and the class is labeled erroneous ([[Can a static initializer throw a checked exception]], [[Which exception is thrown when static class initialization fails]]).

If `E` **is** already an `Error`, that `Error` is thrown as-is, and the class is still erroneous.

On any later attempt to initialize that same class, initialization is impossible: the procedure throws **`NoClassDefFoundError`** immediately. Static initializers are not run again.

That `NoClassDefFoundError` is **not** the “`.class` missing from the classpath” story. The class was present; initialization failed. `ClassNotFoundException` is the checked load-by-name type ([[What is the difference between ClassNotFoundException and NoClassDefFoundError]]).

`ExceptionInInitializerError` and `NoClassDefFoundError` are both `Error`s (unchecked). `catch (Exception e)` does not catch them ([[Are Error subclasses checked or unchecked]], [[Does catch Exception also catch Error]], [[Why should you not catch java.lang.Error]]).

```d2
direction: down
first: "first new A()\nstatic { 1/0 }" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
eiie: "ExceptionInInitializerError\ncause: ArithmeticException" {
  width: 320
  height: 70
  style.fill: "#ffebee"
}
next: "later new A()" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
ncd: "NoClassDefFoundError\n(no retry)" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
first -> eiie -> next -> ncd
```

**Fig. 1.** One failed initialization; every later use is `NoClassDefFoundError`.

```java
class A {
    static {
        int n = 1 / 0;
    }
}

class Demo {
    static void twice() {
        try {
            new A();
        } catch (ExceptionInInitializerError e) {
            System.out.println(e.getCause());
        }
        new A();
    }
}
```

**Listing 1.** `1 / 0` is `int` division, so `ArithmeticException` (not an infinity) ([[Does floating-point division by zero throw ArithmeticException]]). The first `new A()` is `ExceptionInInitializerError` with that cause. After the `catch`, the second `new A()` throws `NoClassDefFoundError`. `getCause()` on that second error is not a second `ArithmeticException` from a rerun static block.

> [!warning] The second failure is not another `ExceptionInInitializerError`
> Catching the first `Error` and “trying again” does not recover the class. Prevent the initializer from throwing; do not catch and retry construction.

> [!warning] Same type name, different `NoClassDefFoundError` story
> Interview dumps also use `NoClassDefFoundError` for a missing compiled class. Here the class **did** load; it **failed to initialize**. The detail message may mention initialization, but the type is still `NoClassDefFoundError`.

> [!tip] Interview answer
> **After `ExceptionInInitializerError`, the class is broken for the rest of the run.** The next `new` or static use throws `NoClassDefFoundError`; static initialization is not retried. Catching the first error and constructing again does not help.
