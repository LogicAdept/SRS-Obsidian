<!--
reps: 0
priority: 0
-->
#Java/OOP/Initialization #Java/Exceptions/Checked #SRS

# How would you explain what happens if in block initialization occurs exceptional situation?

> [!abstract] Short answer
> **Checked** exceptions: a `static { }` (or static field initializer) **must not** be able to throw them. An instance `{ }` of a **named** class may throw them only if **every explicitly declared constructor** lists that type (or a supertype) in `throws`—and you **must** declare constructors; a default constructor has no `throws`. **Unchecked** exceptions compile. At run time a failing **static** initializer **aborts class initialization** (`ExceptionInInitializerError` unless it was already an `Error`); a failing **instance** initializer **aborts that `new`**. After a failed class init: [[What happens if you use a class after ExceptionInInitializerError]]. Blocks: [[How would you explain static and instance initializer blocks in Java]].

## Compile time, then run time

**Static `{ }` / static field initializer.** If it can throw a **checked** exception, that is a compile-time error—even with `throw new IOException()` written “explicitly.” Catch it inside the block, or throw only **unchecked** types. The dump’s “any explicit throw in a static block fails to compile” is **false** for `RuntimeException` and `Error`.

**Instance `{ }` / instance field initializer (named class).** A checked exception is a compile-time error unless the class has **at least one explicit constructor** and **each** of them declares it. If you rely on the synthesized default constructor, you cannot throw checked exceptions from `{ }` ([[How would you explain the default constructor synthesized by the Java compiler]]). Anonymous classes get a generated constructor whose `throws` matches the initializers.

**`return` / complete normally.** An initializer must be able to complete normally. A block whose every path `throw`s is a compile-time error; use a non-constant condition if you need a throw for tests.

**Run time — static.** Superclass static init has already run. Remaining static initializers of this class stop. If the thrown object is not an `Error`, it is wrapped in `ExceptionInInitializerError`. The class is **erroneous**; later use throws `NoClassDefFoundError` ([[How would you explain static initialization order in Java]]; [[How would you explain static initializer blocks in Java]]).

**Run time — instance.** After `super(...)` returns, instance initializers run in textual order. The first throw **stops** later initializers and the constructor body. The class instance creation completes abruptly with **that same exception** (not wrapped). The caller never receives the reference ([[How would you explain instance initializer blocks versus constructors]]; [[What is constructor]]).

```d2
direction: down
st: "static { } throws" {
  width: 200
  height: 36
  style.fill: "#ffebee"
}
ei: "ExceptionInInitializerError\nclass erroneous" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
inst: "instance { } throws" {
  width: 200
  height: 36
  style.fill: "#e3f2fd"
}
newf: "new completes abruptly\nsame exception" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
st -> ei
inst -> newf
```

**Fig. 1.** Static failure poisons the class. Instance failure fails that construction.

```java
import java.io.IOException;

class Cache {
    static boolean boom = true;

    static {
        if (boom) {
            throw new IllegalStateException("static");
        }
    }
}

class Doc {
    boolean boom = true;

    {
        if (boom) {
            throw new IOException("instance");
        }
    }

    Doc() throws IOException {}
}

class Use {
    static void go() throws IOException {
        Doc d = new Doc();
    }
}
```

**Listing 1.** First use of `Cache` fails class initialization with `ExceptionInInitializerError` whose cause is `IllegalStateException`. `new Doc()` can throw `IOException` because the only constructor declares it. Uncommenting `throw new IOException()` inside `Cache`’s `static` block would not compile.

> [!warning] Checked vs unchecked — the dump mixed them
> Static initializers cannot throw **checked** exceptions. They **can** throw `RuntimeException`. Instance `{ }` may throw checked exceptions only via **every explicit** constructor’s `throws`. A no-arg `throws` on one constructor is not enough if another constructor omits it.

> [!warning] Failed static init is sticky
> Catching `ExceptionInInitializerError` on the first use does not repair the class. The next `Cache.x` or `new Cache()` is `NoClassDefFoundError`. Do not retry initialization.

> [!warning] Unconditional `throw` is also a compile-time error
> Initializers must be able to complete normally. `static { throw new RuntimeException(); }` fails for that reason, not because unchecked throws are banned. Guard the throw with a non-constant condition.

> [!tip] Interview answer
> A static initializer may not throw a checked exception; an unchecked one aborts class initialization, usually as `ExceptionInInitializerError`, and the class stays broken. An instance initializer that throws aborts `new` with that exception; checked throws are legal only if every explicit constructor lists them. The default constructor has no `throws`, so it cannot coexist with a checked throw from `{ }`.
