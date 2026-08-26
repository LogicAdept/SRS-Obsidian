<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS

# How do you set a Spring cache key with SpEL?

> [!abstract] Short answer
> Set **`key`** on `@Cacheable` / `@CachePut` / `@CacheEvict` to a **SpEL** expression over arguments and `#root`. Examples: **`#isbn`**, **`#isbn.rawNumber`**, **`T(someType).hash(#isbn)`**. Use this when only **some** parameters identify the entry. Do **not** also set **`keyGenerator`** — that combination throws.

## Pick arguments with `key`

Spring *Custom Key Generation Declaration*: default `SimpleKeyGenerator` uses **every** parameter, including flags that should not be part of the identity. `key` lets you select arguments, nested properties, or a static method — recommended as signatures grow. Default algorithm: [[How does Spring generate a cache key by default]].

```java
@Cacheable(cacheNames = "books", key = "#isbn")
public Book findBook(ISBN isbn, boolean checkWarehouse, boolean includeUsed) { /* ... */ }

@Cacheable(cacheNames = "books", key = "#isbn.rawNumber")
public Book findBook(ISBN isbn, boolean checkWarehouse, boolean includeUsed) { /* ... */ }

@Cacheable(cacheNames = "books", key = "T(someType).hash(#isbn)")
public Book findBook(ISBN isbn, boolean checkWarehouse, boolean includeUsed) { /* ... */ }

@Cacheable(cacheNames = "books", keyGenerator = "myKeyGenerator")
public Book findBook(ISBN isbn, boolean checkWarehouse, boolean includeUsed) { /* ... */ }
```

**Listing 1.** Official examples. Shared algorithm → `KeyGenerator` **bean name** in `keyGenerator`.

SpEL context (Framework table): `#root.methodName`, `#root.method`, `#root.target`, `#root.targetClass`, `#root.args[0]`, `#root.caches[0].name`. Named args (`#isbn`) need `-parameters` or the compiler’s names; otherwise **`#a0` / `#p0`**. Concatenation like `#author.name + '_' + #genre` is valid SpEL if those properties exist.

```d2
direction: right
args: "isbn, flags…" {
  width: 160
  height: 50
  style.fill: "#e3f2fd"
}
spel: "key = \"#isbn\"" {
  width: 180
  height: 50
  style.fill: "#fff3e0"
}
cache: "Cache.get/put(that key)" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}

args -> spel -> cache
```

**Fig. 1.** Flags still affect the method; they are omitted from the cache identity.

`#result` is **not** available for `@Cacheable` **`key`** (lookup happens before invoke). It **is** listed for **`@CachePut` key** and for **`unless`**. Do not copy `#result` into a Cacheable key.

> [!warning] `key` and `keyGenerator` together fail
> Mutually exclusive; specifying both **results in an exception**.

> [!warning] Same SpEL, different flags, one cache entry
> `key = "#isbn"` with `includeUsed` changing the loaded book **overwrites** or **returns the wrong** variant. Include every field that changes the result, or use different cache names.

> [!warning] Argument names need debug/parameter metadata
> Without names, `#isbn` fails; use `#p0` / `#a0` or compile with `-parameters`.

> [!tip] Interview answer
> **Set `key` to a SpEL expression over the arguments you care about**, for example `#isbn` when extra booleans must not be in the key. That is the usual alternative to `SimpleKeyGenerator`. For a shared algorithm, name a `KeyGenerator` bean — never set both `key` and `keyGenerator`.
