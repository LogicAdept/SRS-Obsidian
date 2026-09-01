<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS

# How are Java assertion flags combined on the command line?

> [!abstract] Short answer
> **Left to right, before any class is loaded.** You can mix `-ea`/`-da` with `-esa`/`-dsa`. Bare `-ea`/`-da` set the default for non-system classes; `-esa`/`-dsa` flip system classes. A later switch overrides an earlier one for the same target, and a class-level `-da:` can disable one type inside an earlier package `-ea:...`. With no flags, assertions stay off.

## One pass, two domains

The launcher options are `-enableassertions`/`-ea`, `-disableassertions`/`-da`, `-enablesystemassertions`/`-esa`, and `-disablesystemassertions`/`-dsa` ([[How do you enable Java assertions at runtime]], [[How do you disable Java assertions at runtime]], [[What is the difference between -ea and -esa]]). If several appear, they are processed **in order**, before loading any classes.

`-ea` / `-da` take an optional filter:

- no argument — all packages and classes **except system classes**
- `packagename...` — that package and its subpackages (`...` is required)
- `...` — the unnamed package
- `classname` — that one class

Bare `-ea` does **not** turn on system classes. `-esa` / `-dsa` do that as a separate on/off for system classes. Filters on `-ea`/`-da` (a package or class name) **do** apply to system classes as well as to ordinary loaders.

At initialization, a class-specific setting beats the most specific package setting, which beats the loader default ([[How do you enable Java assertions for a package or class]]). That is why `-ea:com.wombat.fruitbat... -da:com.wombat.fruitbat.Brickbat` enables the package and then punches a hole for one class. Once a class is initialized, its assertion status does not change.

```d2
direction: down
line: "java [flags...] Main" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
user: "-ea / -da\nnon-system default\n(+ filters)" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
sys: "-esa / -dsa\nsystem classes" {
  width: 260
  height: 70
  style.fill: "#fff8e1"
}
line -> user
line -> sys
```

**Fig. 1.** One left-to-right pass; user-class defaults and system classes are separate knobs unless a filter names a class or package.

```text
java -ea:com.wombat.fruitbat... -da:com.wombat.fruitbat.Brickbat MyClass
java -ea -esa -dsa -ea -dsa -esa Test
```

**Listing 1.** First command: package on, `Brickbat` off. Second: user classes stay on from `-ea`; system classes end **on** because the last system flag is `-esa`. The repeated `-ea` and `-dsa` are not no-ops in general — they overwrite the previous value of that knob.

> [!warning] `-ea:com.foo` is not the package
> A package filter must end in `...`. `-ea:com.foo` enables the **class** `com.foo`. `-ea:com.foo...` enables package `com.foo` and subpackages. Dumps that write `-ea:pack1` then `-da:pack1.B` are using the class form for `pack1`, not a package enable.

> [!warning] Bare `-ea` never means “everything, including `java.*`”
> `-ea` then `-esa` then `-dsa` leaves user classes on and system classes **off**. Order across the two domains matters. Default with **no** flags remains off ([[Why are Java assertions disabled by default]]).

> [!tip] Interview answer
> **The flags are applied left to right before any class loads.** Mix `-ea`/`-da` for your classes with `-esa`/`-dsa` for system classes; bare `-ea` does not enable system classes. Later flags override earlier ones for the same target, so you can enable a package with `...` and disable one class inside it.
