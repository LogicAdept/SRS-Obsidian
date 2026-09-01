<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection/Members #SRS

# How do you access static fields using reflection?

> [!abstract] Short answer
> **Look up the `Field`, then `get(null)` / `set(null, value)`.** For a static field the `obj` argument is **ignored** and **may be null**. `getField` finds a **public** field (including inherited). `getDeclaredField` finds a field **declared** on that class, any access — then `setAccessible(true)` if it is not accessible. A static **final** still cannot be written with `Field.set` ([[Can you change the value of a final field using reflection]]).

## `null` receiver, class is initialized

The lookup is the same API as instance fields ([[What is the difference between getField and getDeclaredField]]). The difference is the receiver: instance `get`/`set` require a live object (`null` → `NullPointerException`; wrong type → `IllegalArgumentException`). Static `get`/`set` skip that check — `obj` is not used.

```d2
direction: down
cls: "Class<?> c" {
  width: 160
  height: 45
}
pub: "getField(name)" {
  width: 200
  height: 45
  style.fill: "#e3f2fd"
}
dec: "getDeclaredField(name)" {
  width: 240
  height: 45
  style.fill: "#fff3e0"
}
f: "Field (static)" {
  width: 180
  height: 45
}
rw: "get(null) / set(null, value)" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
cls -> pub: "public, inherited OK"
cls -> dec: "declared here"
pub -> f
dec -> f
f -> rw
```

**Fig. 1.** Same `Field` object; static access does not need an instance. First `get`/`set` **initializes** the declaring class if needed (`ExceptionInInitializerError` if `<clinit>` fails).

```java
class Holder {
    public static String label = "open";
    private static int secret = 7;
}

class Access {
    static String label() throws Exception {
        Field f = Holder.class.getField("label");
        return (String) f.get(null);
    }

    static void setLabel(String value) throws Exception {
        Holder.class.getField("label").set(null, value);
    }

    static int secret() throws Exception {
        Field f = Holder.class.getDeclaredField("secret");
        f.setAccessible(true);
        return f.getInt(null);
    }
}
```

**Listing 1.** Public static via `getField` + `get`/`set(null, …)`. Private static via `getDeclaredField` + `setAccessible` + `getInt(null)` ([[What does setAccessible do in the Reflection API]]). Primitive getters wrap the same `obj` rule.

Passing a random instance is legal for a static field (it is ignored) but it does not “select” an instance — there isn’t one. The idiom is `null`, the same pattern as `Method.invoke(null, …)` for a static method ([[How can you invoke a method using reflection]]).

`getDeclaredField` does **not** see a static field declared only on a **superclass** or superinterface; use `getField` for a public inherited field, or call `getDeclaredField` on the class that actually declares it. `getFields()` / `getDeclaredFields()` are the array forms with the same public-vs-declared split.

> [!warning] `static final` is read, not written
> `Field.get(null)` can read a static final (including a constant variable’s runtime slot). `Field.set` still throws `IllegalAccessException` for static finals even after `setAccessible(true)`: write access requires a **non-static** field ([[Can you change the value of a final field using reflection]]).

> [!warning] `null` is NPE only for instance fields
> `instanceField.get(null)` is `NullPointerException`. `staticField.get(null)` is the documented static read. Mixing them up is the usual interview miss — decide with `Modifier.isStatic(field.getModifiers())` if the `Field` came from a mixed list.

> [!tip] Interview answer
> **`getField` or `getDeclaredField`, then `get(null)` and `set(null, value)` — the instance argument is ignored for static fields.** Private statics need `getDeclaredField` plus `setAccessible(true)`. **You can read a static final; you cannot `Field.set` it.**
