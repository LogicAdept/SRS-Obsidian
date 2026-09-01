<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS

# How do you disable Java assertions at runtime?

> [!abstract] Short answer
> **Pass `-da` (`-disableassertions`) to the `java` launcher.** Bare `-da` turns assertions off in all non-system classes. `-dsa` (`-disablesystemassertions`) turns them off in system classes. Assertions are already off by default, so `-da` is mainly how you turn them **back** off after a broader `-ea`.

## Command-line switches, not `javac`

These flags are runtime options of the `java` command, not of the compiler ([[How do you enable Java assertions at runtime]]). A disabled `assert` is a no-op: the condition is not evaluated and nothing is thrown.

`-da` / `-disableassertions` takes the same optional filter as `-ea`:

- no argument — disable in all packages and classes **except system classes**
- `packagename...` — that package and subpackages
- `...` — the unnamed package
- `classname` — that one class

`-dsa` / `-disablesystemassertions` disables assertions in **all system classes** (no filter). Filters on `-da` (a package or class name) also apply to system classes; the bare form does not.

Because the default is already off, a lone `java -da Main` does not change much ([[Why are Java assertions disabled by default]]). The useful pattern is enable broadly, then disable a slice: `java -ea:com.wombat.fruitbat... -da:com.wombat.fruitbat.Brickbat MyClass` ([[How do you enable Java assertions for a package or class]], [[How are Java assertion flags combined on the command line]]). Several switches are processed **left to right** before any class loads.

```d2
direction: down
start: "java ... Main" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
da: "-da\nnon-system default off" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
dsa: "-dsa\nsystem classes off" {
  width: 260
  height: 70
  style.fill: "#fff8e1"
}
hole: "-ea:pkg... then -da:SomeClass\npunch a hole" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
start -> da
start -> dsa
start -> hole
```

**Fig. 1.** Disable is a launcher flag: default off, `-da` for user classes, `-dsa` for system classes, or a class/package hole after `-ea`.

```text
java -da Main
java -dsa Main
java -ea:com.wombat.fruitbat... -da:com.wombat.fruitbat.Brickbat MyClass
```

**Listing 1.** Bare `-da` skips system classes. `-dsa` is the system-class switch. The third line is the usual “enable package, disable one class” combination.

> [!warning] Bare `-da` does not mean “including `java.*`”
> No-argument `-da` and `-ea` never apply to system classes. If you enabled them with `-esa`, you need `-dsa` (or a later `-dsa` after `-esa`) to turn that domain off again. Order matters ([[What is the difference between -ea and -esa]]).

> [!warning] Too late once the class is initialized
> The launcher applies these switches before loading classes. After a class is initialized, its assertion status is fixed; you cannot flip it with another flag on that same run.

> [!tip] Interview answer
> **Disable at runtime with `-da` / `-disableassertions` on the `java` command; `-dsa` is the system-class counterpart.** The default is already off, so you mostly use `-da` with a class or `package...` filter to undo part of a broader `-ea`. Flags are applied left to right before any class loads.
