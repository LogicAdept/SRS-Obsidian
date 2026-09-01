<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS

# How do you enable Java assertions at runtime?

> [!abstract] Short answer
> **Pass `-ea` (`-enableassertions`) to the `java` launcher.** Assertions are off by default, so `java Test` does not run `assert` statements and `java -ea Test` does. Bare `-ea` enables them in all **non-system** classes. `-esa` is the separate switch for system classes.

## Runtime flag, not a compiler switch

`javac` still compiles `assert`. Enablement is decided when the program starts ([[Why are Java assertions disabled by default]]). A disabled `assert` is a no-op: the condition is not evaluated. Enabled and false, it throws `AssertionError` ([[What happens when a Java assert statement fails]]).

`-ea` / `-enableassertions` takes an optional filter ([[How do you enable Java assertions for a package or class]]):

- no argument — all packages and classes **except system classes**
- `packagename...` — that package and subpackages
- `...` — the unnamed package
- `classname` — that one class

`-esa` / `-enablesystemassertions` enables assertions in **all system classes**. Mix `-ea` with `-da` to punch holes; switches are processed left to right before any class loads ([[How do you disable Java assertions at runtime]], [[How are Java assertion flags combined on the command line]], [[What is the difference between -ea and -esa]]).

```d2
direction: down
cmd: "java [-ea] Main" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
off: "no flag (default)\nassert is a no-op" {
  width: 260
  height: 70
  style.fill: "#eceff1"
}
on: "-ea\nuser classes enabled" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
sys: "-esa\nsystem classes too" {
  width: 260
  height: 70
  style.fill: "#fff8e1"
}
cmd -> off
cmd -> on
on -> sys
```

**Fig. 1.** Enablement is a launcher choice. Default off; `-ea` covers user classes; `-esa` is extra for system classes.

```text
java Test
java -ea Test
java -enableassertions Test
java -ea:com.example... -esa Test
```

**Listing 1.** The first command leaves assertions off. The next two are the same flag. The last enables a package (and subpackages) plus system classes.

> [!warning] This is not a `javac` option
> There is no compile-time switch that “turns asserts on.” `javac` always accepts the `assert` statement (for 1.4+ source). If you forget `-ea`, the bytecode is still there; it simply does nothing at run time.

> [!warning] Bare `-ea` skips `java.*`
> No-argument `-ea` does not apply to system classes. Need `-esa` as well if you intend to enable those. After a class is initialized, its assertion status is fixed for that run.

> [!tip] Interview answer
> **Enable assertions at runtime with `-ea` or `-enableassertions` on the `java` command; they are off unless you do.** Bare `-ea` covers your classes, not system classes (`-esa`). It is not a `javac` flag — the compiler still emits `assert`.
