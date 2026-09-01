<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS

# How do you enable Java assertions for a package or class?

> [!abstract] Short answer
> **Put a filter on `-ea`:** `-ea:com.example.MyClass` for one class, `-ea:com.example...` for a package **and its subpackages**. Repeat `-ea:` for several classes. Punch a hole with `-da:` on a class or a more specific `package...`.

## Filters on `-ea` / `-da`

Bare `-ea` enables every non-system class ([[How do you enable Java assertions at runtime]]). To narrow it, append `:` and a name. The same shapes work on `-da` ([[How do you disable Java assertions at runtime]]):

| Filter | What it enables (or disables) |
| --- | --- |
| `classname` | that class only |
| `packagename...` | that package **and nested packages** |
| `...` | the unnamed package |

The three dots are part of the option, not a placeholder. `-ea:pack1` (no dots) is the **class** `pack1`, not package `pack1`.

Switches are processed left to right before any class loads ([[How are Java assertion flags combined on the command line]]). A class-level `-da:` overrides a package `-ea:...`. When two package filters overlap, the **most specific** package wins (for example `-ea:pack1... -da:pack1.pack2...` leaves `pack1.pack2` and below off). Nested classes follow the top-level class’s setting.

```d2
direction: down
ea: "-ea:filter" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
cls: "Name with no dots\none class" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
pkg: "name...\npackage + subpackages" {
  width: 280
  height: 70
  style.fill: "#fff8e1"
}
hole: "then -da:Class or -da:sub..." {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
ea -> cls
ea -> pkg
pkg -> hole
```

**Fig. 1.** Class filter vs `package...`. Use `-da` on a class or a nested `package...` to cut an exception out of a wider enable.

```text
java -ea:pack1.B Main
java -ea:pack1.B -ea:pack1.pack2.C Main
java -ea:pack1... Main
java -ea:pack1... -da:pack1.B Main
java -ea:pack1... -da:pack1.pack2... Main
```

**Listing 1.** One class; two classes; package and subpackages; package except one class; package except a nested subtree. The `...` forms are the package filters.

> [!warning] Dumps that write `-ea:pack1` for a package are wrong
> Without `...`, `pack1` is a class name. “Every class in package `pack1`” is `-ea:pack1...`, and that **includes** subpackages. There is no launcher filter for “this package only, not children”; exclude a subtree with a later `-da:pack1.pack2...`.

> [!warning] Bare `-ea` is still not system classes
> A class or `package...` filter on `-ea` **does** apply to system classes if the name matches. Bare `-ea` does not. System-wide on/off remains `-esa` / `-dsa` ([[What is the difference between -ea and -esa]]).

> [!tip] Interview answer
> **Enable one class with `-ea:fully.qualified.Name` and a package with `-ea:pkg...` — the dots mean that package and subpackages.** Repeat `-ea:` for more classes, and use `-da:` on a class or a nested `package...` to punch a hole. Forgetting `...` names a class, not a package.
