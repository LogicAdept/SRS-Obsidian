<!--
reps: 0
priority: 0
-->
#Java/Collections #Java/Generics #SRS

# What are heterogeneous collections and generic variance in Java

> [!abstract] Short answer
> A type-safe heterogeneous container holds values of many different types in one structure and still returns each value without casts: the classic recipe keys a `Map<Class<?>, Object>` by type tokens and returns `T` via `Class<T>.cast`. Generic variance is the wildcard mechanism (`? extends`, `? super`) that lets one collection parameterization stand for a family of them at API boundaries.

A plain `Map<String, Object>` loses the type of each value; every read needs a cast and a prayer. The heterogeneous container pattern recovers the type by making the key carry it: a `Class<T>` object is a **type token**, so the key's type determines the value's type for `put` and `get` alike.

## The type-safe heterogeneous container

The pattern stores everything as `Object` but exposes a generic face: `put` takes `(Class<T>, T)` so the value must match the key, and `get` takes `Class<T>` and hands back `T` — the `cast` call does a runtime check that [[How does type erasure work for Java generics]] makes necessary, because the map itself is erased to `Map<Object, Object>`.

```d2
direction: right
put: "put(Class<T>, T)\nkey carries the type" {
  width: 280
  height: 100
  style.fill: "#e3f2fd"
}
map: "Map<Class<?>, Object>\n(erased inside)" {
  width: 280
  height: 100
  style.fill: "#fff3e0"
}
get: "get(Class<T>)" {
  width: 230
  height: 90
  style.fill: "#e3f2fd"
}
cast: "type.cast(value)\n-> T, no caller cast" {
  width: 290
  height: 100
  style.fill: "#e8f5e9"
}
put -> map: values keyed by token
map -> get
get -> cast
```

**Fig. 1.** The type token rides in as the key; the checked cast on the way out restores the exact type.

```java
import java.util.HashMap;
import java.util.Map;

public class HeterogeneousDemo {

    static class Favorites {
        private final Map<Class<?>, Object> values = new HashMap<>();

        public <T> void put(Class<T> type, T value) {
            values.put(type, type.cast(value)); // Class<T> is a type token: cast is checked
        }

        public <T> T get(Class<T> type) {
            return type.cast(values.get(type)); // unchecked raw Map becomes type-safe here
        }
    }

    public static void main(String[] args) {
        Favorites f = new Favorites();
        f.put(String.class, "java");
        f.put(Integer.class, 21);
        f.put(Class.class, Favorites.class); // Class<?> keys are heterogeneous too

        String s = f.get(String.class);   // no cast at call site
        Integer i = f.get(Integer.class);
        Class<?> c = f.get(Class.class);
        System.out.println(s + " " + i + " " + c.getSimpleName()); // java 21 Favorites

        // f.put(String.class, 42); // compile-time error: value must be a String
        // f.put(List<Integer>.class, null); // compile-time error: List<Integer> is not reifiable
    }
}
```

**Listing 1.** One map, many unrelated value types, and typed reads — the compiler enforces key-value agreement at every call.

## Where variance enters the picture

The container itself is invariant; flexibility comes from wildcards at the API surface. Bounded tokens widen what a key may express: `Class<? super T>` accepts tokens for `T` and its ancestors, so `getAnnotatedReceiverType`-style APIs and frameworks can look up by supertype. The same `? super T` / `? extends T` shapes drive collection APIs — a method filling a collection takes `Collection<? super T>`, one reading takes `Collection<? extends T>` — which is exactly the use-site variance drilled in [[How would you explain wildcard bounded and unbounded types in Java generics]] and [[How would you explain the PECS rule for generic method signatures]]. Dependency injection by type is the same idea industrialized: Spring resolves a bean by its type token, see [[How do you inject all beans of a given type as a collection or map]].

> [!warning] Type tokens only work for reifiable types
> `String.class` exists; `List<Integer>.class` does not — the class object belongs to the erasure, so there is exactly one `List.class` token and it cannot distinguish parameterizations. A `Map<Class<?>, Object>` therefore cannot key on `List<Integer>` versus `List<String>` without extra machinery (super type tokens trade on anonymous subclasses, still unchecked inside). And a raw `Map<Class<?>, Object>` without the checked `cast` in the accessor is just an untyped bag with deferred [[When can a ClassCastException be thrown in Java]] risk.

> [!tip] Interview answer
> A heterogeneous container is one structure holding many types type-safely: key it by `Class<T>` tokens, put `(Class<T>, T)`, and get returns `T` through a checked `cast` — no caller casts, wrong pairings fail to compile. Variance is the other half: wildcards make one parameterization stand for a family, `extends` for producers, `super` for consumers. The pattern's limit: tokens are reifiable types only, so `List<Integer>.class` does not exist and generic keys need workarounds.

