<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #Java/Collections/Map #Java/Language/Primitives #SRS

# Can a primitive value be used directly as a `Map` key in Java?

> [!abstract] Short answer
> **Yes at the call site, but not as the map's key type.** Java generic type arguments must be reference types, so you cannot declare `Map<int, String>`. With `Map<Integer, String>`, however, an `int` can be passed directly to `put` or `get` because Java automatically boxes it to `Integer`.

## What happens when an `int` is used as a key?

`Map<K,V>` declares its key as the reference type `K`, and `put` accepts a parameter of that type. An `int` therefore cannot be the declared type argument, but it can be converted to `Integer` at a method invocation through boxing conversion.

```java
Map<Integer, String> map = new HashMap<>();

int key = 42;

map.put(key, "answer");
String value = map.get(key);
```

**Listing 1.** The source code uses an `int`, but `put` and `get` receive an `Integer` after boxing.

Conceptually, the calls behave like:

```java
map.put(Integer.valueOf(key), "answer");
String value = map.get(Integer.valueOf(key));
```

**Listing 2.** Conceptual form showing the primitive-to-wrapper conversion.

The same rule applies to the other primitives: `long` → `Long`, `boolean` → `Boolean`, `char` → `Character`, and so on. Java defines these as boxing conversions.

## Why `Map<int, String>` is illegal

Generic type arguments are restricted to reference types or wildcards. A primitive such as `int` therefore cannot appear between the angle brackets.

```java
Map<int, String> wrong = new HashMap<>();       // does not compile
Map<Integer, String> correct = new HashMap<>(); // valid
```

**Listing 3.** `Integer`, not `int`, is the key type of a generic `Map`.

Once the value is boxed, normal key semantics of the concrete map apply. For a `HashMap`, the stored key is an `Integer` object, so lookup uses the map's normal hashing and equality rules rather than primitive-key storage.

> [!warning] Interview trap
> Saying **“Java collections can use primitive types as generic parameters”** is false. They cannot. What makes `map.put(42, value)` compile is **autoboxing**, so the map actually stores an `Integer`, not a primitive `int`. This also means boxing has object-allocation/caching and performance considerations.

> [!tip] Interview answer
> **You cannot declare a primitive map key type such as `Map<int, V>` because Java generics require reference-type arguments. But you can pass an `int` directly to `Map<Integer, V>` methods because Java autoboxes the `int` to `Integer`. So the source code can look primitive, while the actual key is a wrapper object.**