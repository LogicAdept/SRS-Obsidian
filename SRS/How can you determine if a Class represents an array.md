<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #Java/Arrays #SRS

# How can you determine if a Class represents an array?

> [!abstract] Short answer
> **Call `Class.isArray()`.** It is `true` exactly when that `Class` object is an **array class** (`String[].class`, `int[].class`, `obj.getClass()` for an array instance). It is `false` for the component type itself (`String.class`, `int.class`). `getComponentType()` (same as `componentType()` since 12) returns the next level, or `null` if `isArray()` is false.

## `isArray`, then peel `getComponentType`

Every array has a `Class` object, **shared by all arrays with the same component type**. Length is not part of the type: `new int[3].getClass() == new int[6].getClass()`. An array type is not a class in the language, but that `Class` still behaves as if the direct superclass is `Object` and the interfaces are `Cloneable` and `Serializable` (JLS 10.8). `isArray()` is the predicate for that case ([[What is the Class class in Java reflection]], [[Is a Java array a primitive or an object]]).

```d2
direction: down
c: "Class<?> t" {
  width: 160
  height: 45
}
q: "t.isArray()?" {
  width: 160
  height: 50
}
yes: "array class" {
  width: 180
  height: 45
  style.fill: "#e8f5e9"
}
no: "not an array Class" {
  width: 200
  height: 45
  style.fill: "#ffebee"
}
comp: "getComponentType()\none level, or null" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
c -> q
q -> yes: "true"
q -> no: "false"
yes -> comp
```

**Fig. 1.** Predicate first. `getComponentType` is the next rank, not a substitute for `isArray`.

```java
class Probe {
    static boolean arrayClass(Class<?> type) {
        return type.isArray();
    }

    static Class<?> component(Class<?> type) {
        return type.getComponentType();
    }
}
```

**Listing 1.** `isArray` is the check. `getComponentType` is `null` when the `Class` is not an array.

```java
class Facts {
    static void show() {
        String[].class.isArray();              // true
        String.class.isArray();                // false
        int[].class.isArray();                 // true
        int.class.isArray();                   // false
        int.class.isPrimitive();               // true
        int[].class.isPrimitive();             // false — array of primitives is still an array class

        int[][] grid = new int[2][3];
        grid.getClass().isArray();             // true
        grid.getClass().getComponentType();    // int[].class, not int.class

        new int[3].getClass() == new int[6].getClass(); // true
        String[].class.getName();              // "[Ljava.lang.String;"
        String[].class.getSimpleName();        // "String[]"
    }
}
```

**Listing 2.** Component type is one `[]` off. Nested arrays: walk `getComponentType` while `isArray()` is true to reach the **element** type. `getName()` is the JVM encoding (`[` + table: `I`, `J`, `Z`, `L`binary`;`, …), not source syntax.

`Class.arrayType()` (since 12) builds the array `Class` whose component is `this` (fails for `void` or rank > 255). Creating an instance of an array class is `Array.newInstance`, not `Constructor` / `Class.newInstance` ([[How can you create an instance of a class using reflection]], [[How can you access constructors using reflection]]). `java.lang.reflect.Array` is also how you `get` / `set` / `getLength` when the component type is only a `Class` at run time.

Obtain an array `Class` with `String[].class`, `array.getClass()`, or `Class.forName` using the `getName` encoding (`"[Ljava.lang.String;"`) ([[How can you get the Class object in Java]], [[What does Class.forName do and what are its overloads]]).

> [!warning] `String[].class` is not `String.class`
> Identity and `isAssignableFrom` treat them as different types. `isArray()` / `getComponentType()` are the API; do not scrape `getName()` for a leading `'['` unless you are matching binary names.

> [!warning] `int[]` is not a primitive `Class`
> `isPrimitive()` is true only for the eight primitives and `void`. `int[].class.isArray()` is true; `int[].class.isPrimitive()` is false. The **component** may be primitive ([[Is array is primitive in java]]).

> [!tip] Interview answer
> **`clazz.isArray()` — that is the check.** `true` for `String[].class` and `int[].class`, `false` for `String.class` and `int.class`. **`getComponentType()` peels one level** (`int[][]` → `int[]`, not `int`), and all arrays with the same component type share one `Class` regardless of length.
