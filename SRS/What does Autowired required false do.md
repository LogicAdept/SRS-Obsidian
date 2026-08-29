<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Autowiring #Java/Annotations #SRS

# What does `@Autowired(required = false)` do?

> [!abstract] Short answer
> `@Autowired` **defaults to `required = true`**: no matching bean → startup fails. `required = false` marks that **injection point** optional. A **field** keeps its default (`null` unless you set one); a **setter / config method is not invoked** if any argument cannot be satisfied. On a **constructor**, `required = false` means “this constructor is an autowire **candidate**,” not “each parameter may be missing.” Use `Optional`, `@Nullable`, or a Kotlin `?` type for a single optional **argument**.

## Fields and methods vs constructors

`@Autowired` (since **2.5**) is Spring’s injection annotation; unlike JSR-330 `@Inject`, it adds required-vs-optional semantics ([[What is the difference between Autowired Resource and Inject]]).

**Fields and config methods** (including setters): the default is a **required** dependency. `@Autowired(required = false)` lets the container **skip** a point it cannot satisfy:

- Field: not populated; Java default remains (typically `null`). You can assign a default in the field initializer and optionally override it by injection.
- Method: **not called at all** if that dependency — or **any** argument of a multi-arg method — is missing. `required` applies to **all** arguments of that method.

**Arrays / collections / maps:** with required semantics, at least one matching element is expected (empty is a failure) — except a **single-constructor** class, where those multi-element points may resolve to **empty** instances so you can declare every collaborator on one constructor ([[How do you inject all beans of a given type as a collection or map]]).

**Constructors** are a different algorithm. Only **one** constructor may use `@Autowired` with `required = true`. If several constructors are annotated, **each** must be `required = false`; Spring picks the one with the **most** dependencies it can actually satisfy; if none work, a primary/default constructor. A class with **only one** constructor is always used, **even without** `@Autowired` ([[Why is Autowired often omitted on a single constructor in modern Spring]]).

For one **parameter** that may be absent, keep `@Autowired` (possibly required) and declare `Optional<MovieFinder>`, `@Nullable MovieFinder` (any `@Nullable` in any package), or a Kotlin nullable type. Those override the base `required` semantics on that parameter.

```java
public class SimpleMovieLister {

    private MovieFinder movieFinder = MovieFinder.none();

    @Autowired(required = false)
    public void setMovieFinder(MovieFinder movieFinder) {
        this.movieFinder = movieFinder;
    }
}
```

**Listing 1.** Conceptual. If there is no `MovieFinder` bean, `setMovieFinder` is never called and the field initializer stays.

```java
public class MovieLister {

    public MovieLister(MovieFinder finder, Catalog catalog) { /* always used if this is the only ctor */ }

    @Autowired(required = false)
    public MovieLister(MovieFinder finder) { /* candidate among several ctors */ }

    @Autowired
    public void setOptionalDao(Optional<CustomerPreferenceDao> dao) { /* per-parameter optional */ }
}
```

**Listing 2.** Conceptual. Constructor `required = false` competes with other constructors. `Optional` (or `@Nullable`) is the per-argument switch.

```d2
direction: down
ann: "@Autowired(required = false)" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
field: "Field / setter\nskip if no bean" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
ctor: "Constructor\ncandidate selection" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
param: "Optional / @Nullable / T?\none argument" {
  width: 240
  height: 70
  style.fill: "#fce4ec"
}

ann -> field
ann -> ctor
param -> ctor
```

**Fig. 1.** Same flag, two meanings: skip a property, or include a constructor in the resolution set. Optional arguments are a third, parameter-level mechanism.

`@Inject` has no `required` attribute; use `Optional` / `@Nullable` there. `@Resource` is a different model (name, then type) — not Spring’s `required` flag.

You cannot use `@Autowired` on your own `BeanPostProcessor` / `BeanFactoryPostProcessor` types; those processors perform the injection.

> [!warning] Constructor `required = false` is not “inject null”
> Several `@Autowired(required = false)` constructors mean “try these; pick the greediest match.” A missing bean can make Spring **choose another constructor**, not leave a parameter `null`. For a null-able **dependency**, use `Optional`, `@Nullable`, or Kotlin `?`.

> [!warning] Skipped setter vs `null` field
> A skipped **method** never runs, so it cannot NPE inside the setter — but the field stays at whatever you initialized. A skipped **field** is `null` unless you wrote an initializer. Required collection injection fails on **zero** beans; do not assume `required = false` on a `List` unless you actually set it.

> [!tip] Interview answer
> Autowired is required by default, so a missing bean fails startup. required false on a field or setter makes that point optional: the setter is skipped and the field keeps its default. On constructors the flag marks which constructors are candidates when several exist; a single constructor does not need Autowired at all. For one optional parameter use Optional or Nullable, not constructor-level required false.
