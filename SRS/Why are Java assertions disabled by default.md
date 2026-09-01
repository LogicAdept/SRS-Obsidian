<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #Java/Performance #SRS

# Why are Java assertions disabled by default?

> [!abstract] Short answer
> **So deployed code does not pay for internal checks.** `assert` is meant for development and test; at run time the default is off, which makes a disabled `assert` a no-op. You leave the statements in the source and pass `-ea` when you want them. They are not a substitute for production validation.

## Off until the launcher says otherwise

The `java` launcher starts with assertions disabled in every class ([[How do you enable Java assertions at runtime]]). Enablement is a **runtime** choice (`-ea`, `-esa`, filters). `javac` still compiles `assert`; nothing is stripped unless you use a separate idiom (`if (ASSERTS) assert ...` with a `static final boolean`).

The point of the default is performance in deployment: when assertions are disabled, they are equivalent to empty statements in semantics and cost. That is the opposite of leftover `System.out.println` debug lines, which still run and still write unless you delete or gate them.

Because they may be off, you must not use them for work the program needs, or for a public contract (`main` arguments, public preconditions). Those checks have to throw `IllegalArgumentException` / `NullPointerException` even without `-ea` ([[When is it appropriate to use Java assertions]], [[Why should you not use assert to validate public method arguments]], [[Why must Java assert expressions be free of side effects]]).

```d2
direction: down
run: "java Main" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
off: "default: asserts off\nno-op, no extra cost" {
  width: 280
  height: 70
  style.fill: "#eceff1"
}
on: "java -ea Main\nchecks run" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
run -> off
run -> on
```

**Fig. 1.** Default off is a deployment/performance choice. `-ea` is how you turn the checks on for development and test.

```text
java Main
java -ea Main
```

**Listing 1.** First command: `assert` does not run. Second: it does. The bytecode still contains the statement either way.

> [!warning] Disabled does not mean “safe to use for input checks”
> Production traffic usually has no `-ea`. A public-argument `assert` silently disappears. That is why the default-off design and “don’t validate public args with assert” are the same story.

> [!warning] They are not deleted at compile time
> Forgetting `-ea` does not fail the build. The statements remain in the class file as no-ops. If you need them on in the field, you must start the JVM with `-ea` (or `-esa`); the default will not do it for you.

> [!tip] Interview answer
> **Assertions default to off so a release does not pay for internal invariant checks.** You keep `assert` in the source and enable it with `-ea` while developing and testing. Because they may be off, they are the wrong tool for public validation or any logic the program still needs in production.
