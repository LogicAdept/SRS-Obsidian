<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS

# Why use wrapper types for JavaBean properties?

> [!abstract] Short answer
> JavaBeans **do not require** wrappers — an `int` getter/setter is a legal property. Use `Integer` / `Boolean` / … when **`null` must mean unset or unknown**. A primitive field defaults to `0` / `false`, which can be a **real** value (`age == 0`). The wrapper’s extra state is absence; callers who unbox that `null` get `NullPointerException`.

## Properties can be `int`; wrappers add a third state

A bean property is a pair of accessors the introspector recognizes (`getAge` / `setAge`, or `isRunning` for `boolean`). The official examples use **primitive** `int` (`getMouthWidth` / `setMouthWidth`). That is a perfectly valid read/write property.

Choose a wrapper when `0` or `false` is not a good stand-in for “not provided”:

| Type | Unset field | Can you tell “unknown”? |
| --- | --- | --- |
| `int age` | `0` | no — 0 may be a real age |
| `Integer age` | `null` | yes |
| `boolean active` | `false` | no — false is a real answer |
| `Boolean active` | `null` | yes |

That is the same primitive-vs-wrapper default rule as any field ([[What default values do wrapper-typed fields receive in Java]], [[Why cannot a Java primitive variable be null]]), applied to bean-shaped accessors ([[Why are wrapper classes needed in Java]]).

```d2
direction: down
prim: "int age → 0\nlooks like a value" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
wrap: "Integer age → null\nunknown" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Wrappers on properties are for absence, not because beans forbid `int`.

```java
public class Customer {
    private Integer age;                 // null = unknown
    public Integer getAge() { return age; }
    public void setAge(Integer age) { this.age = age; }
}

Customer c = new Customer();
Integer maybe = c.getAge();              // null
// int years = c.getAge();               // NPE — unboxing
```

**Listing 1.** Conceptual: optional age as `Integer`; unboxing is the caller’s hazard ([[What is the difference between int and Integer in Java]]).

Use a primitive when the property is always present and `0`/`false` is a legitimate default (the `mouthWidth = 90` style). Mixing both in one bean is normal: required counts as `int`, optional quantities as `Integer`.

> [!warning] `null` on a getter is a feature and a footgun
> Forms, SQL NULLs, and “user skipped the field” need `Integer`. UI code that writes `int age = customer.getAge()` will throw. Document the property as nullable, or keep a primitive and use a separate `boolean ageSet` if you must avoid wrappers.

> [!tip] Interview answer
> **Beans happily use `int` properties. You pick wrappers when you need `null` for “not set,” because a primitive `0` cannot mean unknown.** That is why `age` is often `Integer`. Callers must not unbox without a null check.
