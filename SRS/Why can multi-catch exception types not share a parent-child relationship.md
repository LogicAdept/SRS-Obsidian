<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS

# Why can multi-catch exception types not share a parent-child relationship?

> [!abstract] Short answer
> **Because the parent alternative already catches the child, so the child type in `catch (Child | Parent e)` is redundant.** The compiler rejects a union where one alternative is a subtype of another. Write `catch (Parent e)` instead. This is a **union** error, not the separate-clause unreachable-catch error.

## The parent already covers the child

A multi-`catch` names a **union** of alternatives: `catch (A | B e)`. Every alternative must be `Throwable` or a subclass. It is a compile-time error if the union contains two types where one is a **subtype** of the other.

Think of the union as “this handler runs for A **or** B.” If `FileNotFoundException` extends `IOException`, then `IOException` already includes `FileNotFoundException`. Listing both does not add a new case; it duplicates the parent ([[Does throws IOException cover FileNotFoundException]], [[What are common examples of checked exceptions in Java]]).

Siblings are fine: `ClassNotFoundException | IllegalAccessException` (both under `ReflectiveOperationException`, neither a subclass of the other).

The parameter’s declared type is the **least upper bound** of the alternatives. The parameter is **implicitly `final`**; you cannot reassign `e` in the handler ([[How many catch blocks execute for one thrown exception]]).

**Separate** `catch` clauses are a different rule: `catch (IOException e)` then `catch (FileNotFoundException e)` is an **unreachable catch** because the first clause already takes the child. Multi-catch forbids the same redundancy **inside one** `|` list ([[What is an unreachable catch block error]]).

Use multi-catch only when the **same** body is correct for every alternative. If the handling differs, use separate clauses (child first).

```d2
direction: down
union: "catch (FileNotFoundException | IOException e)" {
  width: 380
  height: 50
  style.fill: "#ffebee"
}
reject: "compile error: child already covered by parent" {
  width: 380
  height: 50
  style.fill: "#ffebee"
}
parent: "catch (IOException e)" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
ok: "covers FileNotFoundException too" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
union -> reject
parent -> ok
```

**Fig. 1.** Parent in the union already includes the child; drop the child alternative.

```java
class Demo {
    static void siblings(boolean byName) {
        try {
            if (byName) {
                throw new ClassNotFoundException();
            } else {
                throw new IllegalAccessException();
            }
        } catch (ClassNotFoundException | IllegalAccessException e) {
            // same handler; e is implicitly final
        }
    }
}
```

**Listing 1.** Sibling alternatives compile. `catch (FileNotFoundException | IOException e)` does **not** compile. `catch (IOException e)` is the handler that already includes `FileNotFoundException`. `catch (Exception e)` also catches `RuntimeException`; that is assignment, not a `|` union ([[Does catch Exception also catch RuntimeException]]).

> [!warning] Unreachable catch vs illegal union
> `catch (IOException e) { } catch (FileNotFoundException e) { }` is unreachable **second clause**. `catch (FileNotFoundException | IOException e)` is an illegal **union**. Same hierarchy, two different diagnostics.

> [!warning] Implicitly `final`
> You cannot assign to the multi-catch parameter. Uni-catch is not implicitly `final` unless you write `final` or never assign.

> [!tip] Interview answer
> **Multi-catch forbids parent and child in the same `|` list because the parent already catches the child.** That alternative would be redundant. Use `catch (Parent e)`, or list only unrelated types that share the same handler. Separate clauses with parent first are the unreachable-catch error, not this union error.
