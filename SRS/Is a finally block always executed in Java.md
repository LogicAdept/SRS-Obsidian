<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS

# Is a `finally` block always executed in Java?

> [!abstract] Short answer
> **No.** A `finally` block is executed when control leaves the associated `try`/`catch` normally or abruptly, but there are cases where the JVM cannot execute it at all.

## Typical cases

```java
try {
    riskyOperation();
} catch (Exception e) {
    handle(e);
} finally {
    cleanup();
}
```

`finally` normally runs when:

* the `try` block completes normally;
* an exception is thrown and handled by a matching `catch`;
* an exception is thrown and propagates out of the method;
* the method returns from `try` or `catch`;
* control leaves via `break` or `continue`.

> [!warning] Important exception
> `finally` is **not guaranteed** if the JVM terminates before reaching it. The classic example is `System.exit(...)`.

```java
try {
    System.out.println("try");
    System.exit(0);
} finally {
    System.out.println("finally"); // Not executed
}
```

Other abnormal JVM termination scenarios, such as a process being forcibly killed or the JVM crashing, can also prevent `finally` from executing.

## `return` does not skip `finally`

A common misconception is that `return` prevents `finally` from running.

```java
static int getValue() {
    try {
        return 1;
    } finally {
        System.out.println("cleanup");
    }
}
```

The `finally` block executes **before the method actually returns**.

The same applies to `return` from a `catch` block.

> [!warning] `finally` can override `return`
> Avoid returning from `finally`. A `return` there can suppress an exception or replace an earlier return value.

```java
static int getValue() {
    try {
        return 1;
    } finally {
        return 2; // Bad practice: returns 2
    }
}
```

Here the method returns `2`, not `1`.

## `finally` and resource management

For resources such as files, sockets, and database connections, prefer [[Java/IO]] `try-with-resources` over manually closing them in `finally`.

```java
try (var input = new FileInputStream("data.txt")) {
    process(input);
}
```

This is generally safer because Java handles resource closing even when an exception is thrown.

> [!tip] Interview answer
> **`finally` is executed in almost all normal control-flow paths, including exceptions and `return`, but it is not an absolute guarantee. It may not execute if the JVM terminates before control reaches it, for example through `System.exit()`, a JVM crash, or external process termination.**

> [!example] Mental model
> Think of `finally` as **“run this when leaving the `try`/`catch` construct”**, not **“the JVM guarantees this code will always run.”**

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Всегда ли исполняется блок `finally`?**

Код в блоке `finally` будет выполнен всегда, независимо от того, выброшено исключение или нет.
