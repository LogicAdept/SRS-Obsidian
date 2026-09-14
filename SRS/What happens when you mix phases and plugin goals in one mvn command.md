<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #SRS

# What happens when you mix phases and plugin goals in one mvn command

> [!abstract] Short answer
> **Maven processes the arguments left to right: a phase argument expands to the full prefix of its lifecycle up to that phase, a `plugin:goal` argument runs just that goal at its position in the line.** So `mvn clean dependency:copy-dependencies package` cleans, then copies dependencies, then builds the default lifecycle up to `package`.

One command line can chain as many phases and goals as needed, in any order, and the order is exactly the execution order. `clean` is a phase of the clean lifecycle, so its prefix (`pre-clean`, `clean`) runs. `dependency:copy-dependencies` is a direct goal invocation — it executes at that spot, nothing else from the default lifecycle runs around it. `package` then walks the default lifecycle from `validate` through `package` ([[What are the phases of the three Maven lifecycles]] lists what that includes).

## The line, annotated

```text
mvn clean dependency:copy-dependencies package
    |     |                            |
    |     |                            +-- default lifecycle: validate .. package
    |     +-- direct goal: copies dependency jars to target/dependency
    +-- clean lifecycle: pre-clean, clean
```

**Listing 1.** Each argument is resolved independently; the `|` marks the three execution segments in order.

Two interactions matter. First, a directly invoked goal is not exempt from its own bindings: if that goal is also bound to a lifecycle phase which a later argument reaches, it runs again — the documentation's rule is that a bound goal "will be called in all those phases". Second, a phase argument does not mean "just that phase": it means the whole ordered prefix, which is why `mvn clean install` recompiles even when nothing changed ([[How would you explain mvn clean install]] walks that full command). Direct goal invocation is the precision tool — `mvn surefire:test` runs tests without recompiling, accepting that prerequisites like resources or compilation may be stale ([[How would you explain the Maven build lifecycle]] covers the trade-off).

> [!warning] Argument order is responsibility order
> `mvn package clean` is not the same as `mvn clean package`: the first builds the jar and then deletes it. A direct goal placed after a phase that fails will never run, and a cleaning phase placed anywhere near packaging deserves a second look. The left-to-right rule has no exceptions and no reordering.

> [!tip] Interview answer
> **Arguments run left to right. A phase name pulls its whole lifecycle prefix with it; a plugin:goal token runs exactly that goal in place — so `mvn clean dependency:copy-dependencies package` means clean lifecycle, then the copy goal, then default validate-through-package. A bound goal can still fire again when a later phase reaches it, and phase-with-no-bound-goals does nothing.**
