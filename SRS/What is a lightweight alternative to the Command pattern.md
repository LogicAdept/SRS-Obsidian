<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Behavioral #SRS

# What is a lightweight alternative to the Command pattern

> [!abstract] Short answer
> In modern languages the whole command hierarchy often collapses into a **lambda or a functional interface**: the operation itself becomes the object. In Java, `Runnable`, `Callable`, and `java.util.function` types carry the request; a captured closure plays the role of the pre-configured command fields.

## When the lambda is enough

Command's everyday benefits — parameterizing an invoker, passing the request as an argument, queueing and deferring — need only "an object that runs later". Java had that since Java 1.1 as anonymous classes and since Java 8 as lambdas: an executor consumes `Runnable`, a scheduler consumes `Callable`, and the lambda body closes over exactly the state the command's constructor fields would have held. A queue of `Runnable` is a command queue; `executor.submit(() -> exporter.sync(now))` is a pre-configured command handed to an invoker. The same reasoning is why Strategy often shrinks to a `Comparator` — and it is the catalog's own criticism that some patterns exist to compensate for languages without function types, discussed in [[What are downsides of design patterns]].

```java
Deque<Runnable> history = new ArrayDeque<>();
history.push(() -> editor.deleteSelection());
history.push(() -> mailer.send(report));

history.pop().run();                             // deferred execution
```

**Listing 1.** Queueing and deferred execution without a single command class: each lambda captures its receiver and arguments, like constructor-configured command fields.

## When the full pattern still wins

The class-based command earns its keep when the operation needs structure a lambda cannot carry: undo with state backups across many fields, commands that must be serialized to a file or wire — lambdas are not `Serializable` by default and a captured closure is a poor wire format — commands with a dozen configuration fields, or a family of related operations that want the discipline of named types. Rule of thumb: if all you need is "run this later", pass the lambda; if you need history, remote transport, or rich per-command configuration, write the classes.

> [!warning] Two closure traps
> A lambda can only capture effectively final locals — you cannot mutate the captured variable inside the command, which surprises people building stateful closures. And side effects still fire at creation time for arguments: `submit(export(now()))` calls `now()` immediately; only `() -> export(now())` defers it — the reactive twin of this trap is noted in [[What roles do Observable and Observer play in reactive programming]].

> [!tip] Interview answer
> The lightweight alternative is a lambda over a functional interface: Runnable, Callable, or Supplier replaces the command interface, the closure replaces the constructor-configured fields, and an executor or queue replaces the invoker. Keep the full Command pattern when you need undo with backups, serializable or remote commands, or heavyweight per-command configuration.
