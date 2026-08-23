<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS

# What is the difference between returnObject and filterObject?

> [!abstract] Short answer
> In method-security SpEL, **`returnObject`** is the **entire return value** available to **`@PostAuthorize`**. **`filterObject`** is the **current element** (or map entry) being tested while **`@PreFilter`** or **`@PostFilter`** walks a collection, array, map, or stream.

## `returnObject` — authorize the whole result

**`@PostAuthorize`** runs **after** the method returns. Spring binds the method’s return value as **`returnObject`** in the SpEL expression. The expression must evaluate to true or the call is denied (typically with `AccessDeniedException`).

```java
@PostAuthorize("returnObject.owner == authentication.name")
Account findById(long id) {
    return accountRepository.findById(id);
}
```

**Listing 1.** Official pattern: the whole `Account` is `returnObject`; access is allowed only if the owner matches the authenticated name.

Use **`@PostAuthorize`** when the authorization decision depends on the loaded object (for example defending against insecure direct object references). Prefer checking **before** a write when possible — a denied `@PostAuthorize` after a DB mutation can leave work already done.

## `filterObject` — keep or drop each element

**`@PreFilter`** filters a **method argument** before the method body runs. **`@PostFilter`** filters the **return value** after the method returns. In both cases SpEL sees each candidate as **`filterObject`**.

```java
@PreFilter("filterObject.owner == authentication.name")
void saveAll(List<Account> accounts) { /* ... */ }

@PostFilter("filterObject.owner == authentication.name")
List<Account> findAll() {
    return accountRepository.findAll();
}
```

**Listing 2.** Each list element is `filterObject`; elements that fail the expression are removed from the collection Spring passes onward or returns.

Supported shapes include arrays, collections, maps, and open streams. For **maps**, expressions often use **`filterObject.value`** (and related map-entry accessors) because the iteration item is the map entry, not only the value object.

```d2
direction: right
postAuth: "@PostAuthorize\nreturnObject = whole result" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
filters: "@PreFilter / @PostFilter\nfilterObject = each element" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}

postAuth -> filters: "different\nSpEL bindings"
```

**Fig. 1.** Same method-security stack, different SpEL variables by annotation.

| Variable | Annotations | Meaning |
|---|---|---|
| **`returnObject`** | `@PostAuthorize` | The method’s full return value |
| **`filterObject`** | `@PreFilter`, `@PostFilter` | Current element (or map entry) under test |

> [!warning] Do not mix the variables
> **`@PostAuthorize("filterObject.owner == …")`** is wrong — **`filterObject` is not defined** for post-authorize. Likewise, **`returnObject` is not the per-element variable** inside `@PreFilter` / `@PostFilter`. A typo often compiles as SpEL and fails at runtime or silently evaluates incorrectly. See [[What is EnableMethodSecurity]] and [[Why is PostFilter a performance trap]].

> [!tip] Interview answer
> returnObject is the entire return value in @PostAuthorize. filterObject is each element while @PreFilter or @PostFilter walks a collection. Mixing them — like filterObject in @PostAuthorize — is a common SpEL mistake.
