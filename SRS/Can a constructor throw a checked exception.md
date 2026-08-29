<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #Java/OOP/Constructors #SRS

# Can a constructor throw a checked exception?

> [!abstract] Short answer
> **Yes.** A constructor may throw a checked exception. The body is under the same catch-or-specify rule as a method: a checked type that can leave the constructor must be named in that constructor's `throws` clause (or a supertype of it). `new C(...)` then carries those types, so the enclosing method or constructor must catch them or declare them.

## Catch-or-specify applies to constructors

A constructor's `throws` clause has the same shape and compile-time meaning as a method's. For every checked exception class `E` that the constructor body can throw, `E` or a supertype of `E` must appear in `throws`, or the class does not compile. Unchecked types (`RuntimeException`, `Error`, and their subclasses) do not need to be declared.

A class instance creation expression `new C(...)` can throw `E` when `E` is among the exception types of the chosen constructor. The caller of `new` is therefore checked the same way as a caller of a method with that `throws` clause.

```d2
direction: down
body: "constructor body\ncan throw checked E" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
throws: "constructor throws E\n(or a supertype of E)" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
newExpr: "new C(...)\ncan throw E" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
caller: "caller catch E\nor declare throws E" {
  width: 280
  height: 70
  style.fill: "#f3e5f5"
}
body -> throws
throws -> newExpr
newExpr -> caller
```

**Fig. 1.** Checked exceptions flow from the constructor body through `throws` onto `new`, then to the caller.

```java
import java.io.IOException;

class Config {
    Config(String path) throws IOException {
        if (path.isBlank()) {
            throw new IOException("empty path");
        }
    }
}

class App {
    static Config open(String path) throws IOException {
        return new Config(path);
    }

    static Config openOrNull(String path) {
        try {
            return new Config(path);
        } catch (IOException e) {
            return null;
        }
    }
}
```

**Listing 1.** `Config`'s constructor declares `throws IOException`. `open` declares the same type; `openOrNull` catches it. Omitting both is a compile-time error. See [[What happens if you neither catch nor declare a checked exception]] and [[How would you explain the throws clause for checked exceptions]].

If the constructor body invokes a method that can throw `IOException`, that is the same rule: catch it in the constructor, or add `throws IOException` on the constructor.

## Subclass constructors cannot hide `super(...)` checked types

A constructor invocation (`super(...)` or `this(...)`) can throw every exception class named by the invoked constructor. Those types are treated as thrown by the subclass constructor body.

The constructor invocation is a distinct part of the constructor body, not a statement you can nest inside `try`. You cannot wrap `super(...)` in `catch`. The only compile-time option is to declare the checked types (or a supertype) on the subclass constructor.

```java
import java.io.IOException;

class Config {
    Config(String path) throws IOException {
        if (path.isBlank()) {
            throw new IOException("empty path");
        }
    }
}

class SpecialConfig extends Config {
    SpecialConfig(String path) throws IOException {
        super(path);
    }
}
```

**Listing 2.** `SpecialConfig` must declare `throws IOException` because `super(path)` can throw it. A `try` around `super(...)` does not parse.

> [!warning] Default constructor has no `throws`
> If a class declares no constructor, the implicit default constructor has **no** `throws` clause and is equivalent to `C() { super(); }`. That is a compile-time error unless the superclass supplies an accessible no-argument constructor that itself has **no** `throws` clause — even `throws RuntimeException` on the superclass no-arg constructor is enough to reject the default constructor. Write an explicit constructor. For a checked type from `super()`, that explicit constructor must declare it.

```java
import java.io.IOException;

class Parent {
    Parent() throws IOException {}
}

class Child extends Parent {
    Child() throws IOException {
        super();
    }
}
```

**Listing 3.** `Child` must be declared this way. Deleting `Child()` so that a default constructor is synthesized does not compile, because `Parent()` has a `throws` clause.

`throws` is the constructor's contract with callers of `new`, not a list of what this particular body actually executes. It is legal to declare a checked type that the body never throws; callers of `new` must still catch or declare that type. The reverse is not legal: a checked type the body can throw must be covered.

Instance variable initializers and instance initializers of a named class may throw a checked exception only if the class has at least one explicitly declared constructor and **every** constructor names that type (or a supertype) in `throws`. A static initializer cannot throw a checked exception at all — see [[Can a static initializer throw a checked exception]].

> [!warning] `new` in a static initializer
> `static { new Config("x"); }` is a compile-time error if `Config()` throws a checked type. There is no `throws` on a static initializer, and catching is the only remaining option.

> [!tip] Interview answer
> **Yes — constructors follow the same catch-or-specify rule as methods: a checked exception that can leave the constructor must appear in that constructor's `throws`, and callers of `new` must catch or declare it. A subclass constructor that calls `super(...)` cannot wrap that call in `try`, so it must declare the checked exceptions of the superclass constructor. The implicit default constructor has no `throws` and will not compile if the superclass no-arg constructor declares any throws clause.**
