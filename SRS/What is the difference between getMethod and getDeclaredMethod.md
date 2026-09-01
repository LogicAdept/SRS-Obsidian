<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection/Members #SRS

# What is the difference between getMethod and getDeclaredMethod?

> [!abstract] Short answer
> **`getMethod(name, parameterTypes)` returns a public method, including one inherited from a superclass or superinterface. `getDeclaredMethod` returns a method declared on that class or interface, any access, and does not walk the hierarchy.** Both match **simple name** plus an exact `Class[]` of formal parameter types (`null` means no-arg). Neither finds constructors or `<clinit>`. Since 1.1.

## Public-and-inherited vs declared-here

Same split as fields ([[What is the difference between getField and getDeclaredField]]). `getMethod` reflects “the specified **public** member method.” It unions matching public methods from this type, then the superclass (if not `Object`), then instance methods of direct superinterfaces, and keeps the **most specific** match (class declaration beats interface; a more specific return type wins, which is how a covariant override beats its bridge). `NoSuchMethodException` if nothing matches, if `parameterTypes` contains `null`, or if the name is `<init>` or `<clinit>`.

`getDeclaredMethod` reflects “the specified **declared** method” of this `Class`. Public, protected, package-private, and private all count; **inherited methods do not**. Several declared methods with the same parameters but different return types: the more specific return type is chosen, otherwise one is arbitrary. An array type’s `Class` does **not** find `clone()` here.

```d2
direction: down
c: "Class<?> c" {
  width: 160
  height: 40
}
gm: "getMethod(name, types)\npublic, walk supers / interfaces" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
gdm: "getDeclaredMethod(name, types)\ndeclared here, any access" {
  width: 320
  height: 70
  style.fill: "#fff3e0"
}
c -> gm
c -> gdm
```

**Fig. 1.** Lookup is not `invoke`. After you have a `Method`, `invoke` still enforces access unless `setAccessible(true)` succeeded ([[How can you invoke a method using reflection]], [[What does setAccessible do in the Reflection API]]).

`getMethods()` / `getDeclaredMethods()` are the array forms: all **public** methods including inherited, versus **all declared** methods (any access, plus compiler bridges/synthetics, still no `<clinit>`). A **class** always has public methods from `Object`; an **interface**’s `getMethods` / `getMethod` do **not** include implicit `Object` methods. An array type’s `getMethod` finds public `Object` methods except `clone()`.

Overloads are distinguished only by that `Class[]`, not by javac’s conversion rules. `int.class` is not `Integer.class` ([[How do you invoke overloaded methods using reflection]]). Constructors are `getConstructor` / `getDeclaredConstructor`, not these APIs ([[How can you access constructors using reflection]]).

```java
class Super {
    public void ping() {}
    private void hid() {}
}

class Sub extends Super {
    private void hid() {}
}

class Lookup {
    static Method publicInherited() throws Exception {
        return Sub.class.getMethod("ping");              // Super.ping
    }

    static Method privateHere() throws Exception {
        return Sub.class.getDeclaredMethod("hid");       // Sub.hid
    }
}
```

**Listing 1.** `Sub.class.getMethod("hid")` is `NoSuchMethodException` (not public). `Sub.class.getDeclaredMethod("ping")` is also `NoSuchMethodException` (`ping` is declared on `Super`). Private use: `getDeclaredMethod` + `setAccessible(true)` + `invoke`. Static: `invoke(null, args)`.

`name == null` → `NullPointerException`. Declared lookup may need `RuntimePermission("accessDeclaredMembers")` under a security manager when the caller’s loader is not this class’s loader.

> [!warning] `getMethod` does not see private
> Declaring the method on `C` is not enough. Visibility must still be **public**. Private and package-private are `getDeclaredMethod` on the declaring `Class`.

> [!warning] Name alone is not an overload
> `getMethod("print", String.class)` will not pick `print(Object)`. A wrong token is `NoSuchMethodException`, not a conversion. `getDeclaredMethod` does not inherit a public parent method.

> [!tip] Interview answer
> **`getMethod` is public methods only, including inherited. `getDeclaredMethod` is whatever this class declared, including private, and it does not inherit.** You pass the exact parameter `Class` tokens; then `invoke`. **Private is `getDeclaredMethod` plus `setAccessible(true)`. Constructors are a different API — these methods never return `<init>`.**
