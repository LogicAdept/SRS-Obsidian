<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection/Class #Java/OOP #SRS

# How do you inspect a class superclass and interfaces with reflection?

> [!abstract] Short answer
> **`getSuperclass()` is the direct superclass `Class`; `getInterfaces()` is the directly implemented (or, on an interface, directly extended) interfaces, in source order.** Neither walks the rest of the graph. For an is-a test without walking, use `Super.class.isAssignableFrom(Sub.class)` — the receiver is the type you want to assign **to**.

## Direct links, then walk or `isAssignableFrom`

```d2
direction: down
c: "Class<?> t" {
  width: 160
  height: 45
}
sc: "getSuperclass()\none class or null" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
it: "getInterfaces()\ndirect only, source order" {
  width: 280
  height: 60
  style.fill: "#fff3e0"
}
isa: "Super.isAssignableFrom(t)" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
c -> sc
c -> it
c -> isa: "full is-a, no walk"
```

**Fig. 1.** One hop vs assignability. Recurse `getSuperclass` / `getInterfaces` only when you need the explicit graph ([[What is the Class class in Java reflection]], [[How can you get the Class object in Java]]).

`getSuperclass()` returns the **direct** superclass. It is **`null`** for `Object`, an **interface**, a **primitive**, or `void`. For an **array** class it is `Object.class` ([[How can you determine if a Class represents an array]]).

`getInterfaces()` returns **directly** implemented interfaces for a class (`implements` order), or **directly** extended interfaces for an interface (`extends` order). Empty array if there are none, and for primitive/`void`. For an array type the result is `Cloneable` then `Serializable`, matching JLS 10.8.

```java
interface FloorWax {}
interface DessertTopping {}

class Shimmer implements FloorWax, DessertTopping {}

class Inspect {
    static Class<?> superOf(Class<?> type) {
        return type.getSuperclass();
    }

    static Class<?>[] directInterfaces(Class<?> type) {
        return type.getInterfaces();
    }
}
```

**Listing 1.** `Shimmer.class.getSuperclass()` is `Object.class`. `getInterfaces()[0]` is `FloorWax`, `[1]` is `DessertTopping` — declaration order, not a flatten of `FloorWax`’s own superinterfaces.

Parameterized super types: `getGenericSuperclass()` / `getGenericInterfaces()` return `Type` (often `ParameterizedType`) with the actual type arguments from source. `getSuperclass()` / `getInterfaces()` erase to raw `Class`.

`isAssignableFrom(Class)` asks whether the argument type can be converted to **this** type by identity or widening reference conversion (primitives: only the exact same `Class`). So `CharSequence.class.isAssignableFrom(String.class)` is true; swap the receiver and it is false. `isInstance(obj)` is the same idea for a live object.

Sealed types add `isSealed()` / `getPermittedSubclasses()` for **permitted** direct subtypes — that is not `getInterfaces()` ([[How would you explain Sealed classes]]).

> [!warning] `getInterfaces()` is one `implements` / `extends` clause
> Superinterfaces of those interfaces, and interfaces implemented only by a **superclass**, are absent until you recurse. One `getSuperclass()` call is equally shallow: `ArrayList.class.getSuperclass()` is `AbstractList`, not `Object`.

> [!warning] `isAssignableFrom` is backwards from English “does this class implement”
> The object you call it **on** is the destination type: `MyInterface.class.isAssignableFrom(MyClass.class)`. Calling it on the implementation asks whether the interface is a subtype of the class, which is usually false.

> [!tip] Interview answer
> **`getSuperclass()` for the immediate parent class — `null` on `Object` and on interfaces — and `getInterfaces()` for the direct `implements` / `extends` list.** Those are not a full hierarchy; walk them or use `Super.class.isAssignableFrom(sub)`. **Arrays report superclass `Object` and interfaces `Cloneable`, `Serializable`.**
