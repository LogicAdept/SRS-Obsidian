<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection/Members #SRS

# What is the difference between getField and getDeclaredField?

> [!abstract] Short answer
> **`getField(name)` returns a public field, including one inherited from a superclass or superinterface. `getDeclaredField(name)` returns a field declared on that class or interface, any access, and does not walk the hierarchy.** Both take the field’s **simple** name and throw `NoSuchFieldException` if there is no match. Neither finds an array’s `length`. Since 1.1.

## Public-and-inherited vs declared-here

`getField` reflects “the specified **public** member field.” Search, for class or interface `C`:

1. A **public** field `C` itself declares with that name.
2. Else each **direct superinterface**, in declaration order, with the same algorithm.
3. Else the **superclass**, recursively. No superclass → `NoSuchFieldException`.

So a public field on a parent or an interface is visible on the subclass’s `Class`. A private, package-private, or protected field is not, even if `C` declared it.

`getDeclaredField` reflects “the specified **declared** field” of this `Class`. Public, protected, package-private, and private all count; **inherited fields do not**. A private field on the superclass is found only by calling `getDeclaredField` on **that** superclass.

```d2
direction: down
c: "Class<?> c" {
  width: 160
  height: 40
}
gf: "getField(name)\npublic, walk supers / interfaces" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
gdf: "getDeclaredField(name)\ndeclared here, any access" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
c -> gf
c -> gdf
```

**Fig. 1.** Same `Field` type afterward. Lookup rules differ; using a non-public `Field` still needs `setAccessible(true)` ([[What does setAccessible do in the Reflection API]], [[How do you access static fields using reflection]]).

`getFields()` / `getDeclaredFields()` are the array forms with the same split: all accessible **public** fields of the class plus supers and superinterfaces, versus **all declared** fields on this type (any access, not inherited). Order is unspecified. Array types, primitives, and `void` yield an empty array from both; `getField` / `getDeclaredField` still do **not** reflect `length` ([[How can you determine if a Class represents an array]]).

```java
class Super {
    public int pub = 1;
    private int hid = 2;
}

class Sub extends Super {
    private int hid = 3;
}

class Lookup {
    static Field publicInherited() throws Exception {
        return Sub.class.getField("pub");           // Super.pub
    }

    static Field privateHere() throws Exception {
        return Sub.class.getDeclaredField("hid");   // Sub.hid, not Super.hid
    }
}
```

**Listing 1.** `Sub.class.getField("hid")` is `NoSuchFieldException` (not public). `Sub.class.getDeclaredField("pub")` is also `NoSuchFieldException` (`pub` is declared on `Super`). After `getDeclaredField`, `setAccessible(true)` then `get` / `set`. The methods analogue is `getMethod` / `getDeclaredMethod` ([[What is the difference between getMethod and getDeclaredMethod]]).

`name == null` → `NullPointerException`. A security manager may require `RuntimePermission("accessDeclaredMembers")` for the declared APIs when the caller’s loader is not this class’s loader.

> [!warning] `getField` does not see private
> Interview miss: “I called `getField` on the class that declares it.” Visibility is still **public**. Private and package-private are `getDeclaredField` on the declaring `Class`.

> [!warning] Declared is not “inherited private”
> `getDeclaredField` does not walk superclasses. A hidden field on the parent stays on the parent. `getDeclaredFields()` on a subclass will not list it.

> [!tip] Interview answer
> **`getField` is public members only, including inherited. `getDeclaredField` is whatever this class declared, including private, and it does not inherit.** Private access is `getDeclaredField` plus `setAccessible(true)`, then `get`/`set`. **Neither API finds array `length`.**
