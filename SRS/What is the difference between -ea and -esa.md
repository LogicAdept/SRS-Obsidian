<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS

# What is the difference between `-ea` and `-esa`?

> [!abstract] Short answer
> **Bare `-ea` enables assertions in non-system classes; `-esa` enables them in system classes.** System classes are those with no explicit class loader (the platform). `-ea` can take a class or `package...` filter; `-esa` cannot — it is all system classes, or you use `-dsa` to turn that domain off.

## Two knobs

| Flag | Long form | What it enables |
| --- | --- | --- |
| `-ea` | `-enableassertions` | No argument: every class **except** system classes. Optional `:classname` or `:packagename...` (and `:...` for the unnamed package). |
| `-esa` | `-enablesystemassertions` | All system classes. No filter. |

Matching disables: `-da` / `-disableassertions` (same filter rules as `-ea`, and the same “bare form skips system classes” exception) and `-dsa` / `-disablesystemassertions` ([[How do you enable Java assertions at runtime]], [[How do you disable Java assertions at runtime]]).

Default is both domains off ([[Why are Java assertions disabled by default]]). `java -ea Main` therefore does **not** run `assert` inside platform classes. `java -esa Main` does not enable your application classes.

A filter on `-ea` **does** apply to system classes if the name matches (`-ea:java.lang.String`). Bare `-ea` is the form that deliberately skips them. You can mix the four flags; they are processed left to right before any class loads ([[How are Java assertion flags combined on the command line]], [[How do you enable Java assertions for a package or class]]).

```d2
direction: down
launch: "java [flags] Main" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
ea: "-ea\nuser / app classes" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
esa: "-esa\nsystem classes" {
  width: 260
  height: 70
  style.fill: "#fff8e1"
}
launch -> ea
launch -> esa
```

**Fig. 1.** `-ea` and `-esa` are separate enable switches. Bare `-ea` never means “including the platform.”

```text
java -ea Main
java -esa Main
java -ea -esa Main
java -ea:com.example... -esa Main
```

**Listing 1.** First: application classes only. Second: system classes only. Third: both domains. Fourth: one package (and subpackages) plus all system classes.

> [!warning] `-ea` is not “enable everything”
> Interview dumps treat `-ea` as user classes and `-esa` as JDK classes. That is true for the **no-argument** forms. `-ea:java.util...` can still enable a platform package. `-esa` has no `:` filter to narrow system classes; pair it with `-dsa` or with a later `-da:some.Class` if you need a hole.

> [!warning] `-esa` without `-ea` leaves your code off
> Enabling system assertions does not turn on `assert` in `Main`. If you wanted both, pass both flags (order among domains still matters when `-da`/`-dsa` appear too).

> [!tip] Interview answer
> **`-ea` enables assertions in your classes; `-esa` enables them in system classes that have no explicit class loader.** Bare `-ea` does not turn on the JDK. `-ea` can take a class or `package...` filter; `-esa` is all-or-nothing for the system domain.
