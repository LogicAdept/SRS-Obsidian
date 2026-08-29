<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #Career/Interview #SRS

# Why are wide `throws` clauses on methods often discouraged?

> [!abstract] Short answer
> **Because `throws` is a checked contract: callers must `catch` or redeclare every checked type you list.** `throws Exception` (or `Throwable`) forces that tax on every client, hides which failures actually happen, and makes `catch (Exception)` — which also catches `RuntimeException` — the easy, lossy response.

## A wide clause is a wide obligation

A method that can throw a checked exception must `catch` it or list it (or a supertype) in `throws`. Clients of that method inherit the same catch-or-specify duty ([[How would you explain the throws clause for checked exceptions]], [[Must every caller catch exceptions declared in a throws clause]]).

`throws Exception` means “any checked exception is allowed.” Callers cannot tell I/O from a domain failure without reading the body. The usual workaround is `catch (Exception e)`, which also catches `RuntimeException` ([[Does catch Exception also catch RuntimeException]], [[Does catching Exception satisfy a checked exception obligation]]).

On types meant to be overridden, a wide parent clause is sticky: an override may **narrow** the checked set, but callers who use the **superclass** type still see the wide contract. An override may not **widen** it ([[How do checked exceptions work with method overriding]], [[What happens if an override declares a broader checked exception than the parent]]).

Listing only the checked types the method can actually throw keeps the contract small. Unchecked types in `throws` are optional documentation; they do not create this compiler tax. A few platform callbacks (`AutoCloseable.close`, `Callable.call`) still declare `Exception` because the implementation is unknown — that is the exception, not the default for application APIs ([[What is your view on checked exceptions in Java]], [[How would you explain criticisms of checked exceptions in Java]]).

```d2
direction: down
api: "method throws Exception" {
  width: 300
  height: 50
}
caller: "every caller" {
  width: 280
  height: 50
}
tax: "catch Exception or throws Exception" {
  width: 320
  height: 50
  style.fill: "#fff8e1"
}
api -> caller
caller -> tax
```

**Fig. 1.** A wide `throws` is copied up the stack or swallowed with a wide `catch`.

```java
interface Store {
    void save() throws java.io.IOException;
}

class Demo {
    static void tooWide() throws Exception {
        throw new java.io.IOException("disk");
    }
}
```

**Listing 1.** `throws IOException` names the failure. `throws Exception` on `tooWide` makes every caller handle `Exception`.

> [!warning] `catch (Exception)` is the usual follow-on bug
> Once the clause is `Exception`, handlers often catch the same type and hide `NullPointerException` with the I/O path.

> [!warning] You cannot “narrow” the contract through a wide supertype
> Callers of `Parent` still compile against the parent `throws`, even if the override lists nothing.

> [!tip] Interview answer
> **`throws Exception` is discouraged because it is a checked contract with no useful detail.** Every caller must handle or redeclare `Exception`, which usually becomes a catch-all. Prefer the specific checked types the method can actually throw.
