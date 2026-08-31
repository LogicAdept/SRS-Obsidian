<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS

# What is filterObject in method security SpEL?

> [!abstract] Short answer
> **`filterObject` is the current element while `@PreFilter` / `@PostFilter` walk a collection.** The expression is evaluated per item; **`false` drops that item** (it does not throw). It is **not** `returnObject` — that is the **whole** return value on `@PostAuthorize`.

## One name, two moments

`MethodSecurityExpressionOperations` holds `filterObject` (and `returnObject`). The filter interceptors set it for each element:

| Annotation | What is filtered | When |
|---|---|---|
| `@PreFilter` | A method **argument** | Before the target runs |
| `@PostFilter` | The **return** collection | After the target returns |

Official example: `filterObject.owner == authentication.name`. `filterObject` is each `Account` in `accounts`.

Supported shapes (Security **7.1**): arrays, collections, maps, and **open** streams. For a **`Map`**, use **`filterObject.value`** (and `filterObject.key` if you need the key) — the element is the map entry. `@PreFilter` needs a **non-null** target; with **more than one** collection argument, set **`filterTarget`** to the parameter name (omit it when there is only one).

False does **not** mean `AccessDeniedException`. Matching items stay; the rest are removed in memory. That is why `@PostFilter` on a huge query is a performance trap — [[Why is PostFilter a performance trap]].

```java
@PreFilter("filterObject.owner == authentication.name")
public Collection<Account> updateAccounts(Account... accounts) { /* ... */ }

@PreFilter("filterObject.value.owner == authentication.name")
public Collection<Account> updateAccounts(Map<String, Account> accounts) { /* ... */ }

@PostFilter("filterObject.owner == authentication.name")
public Collection<Account> readAccounts(String... ids) { /* ... */ }

@PostAuthorize("returnObject.owner == authentication.name")
public Account readAccount(String id) { /* ... */ }
```

**Listing 1.** Conceptual Security **7.1** — last method uses `returnObject` on a **single** `Account`, not `filterObject`.

```d2
direction: down
col: "Collection / array / map / stream" {
  width: 260
  height: 45
  style.fill: "#e3f2fd"
}
el: "filterObject\n(one element at a time)" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
keep: "true → keep   false → drop" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}

col -> el -> keep
```

**Fig. 1.** Filter SpEL is per-element. `@PostAuthorize` decides once on `returnObject`. See [[What is the difference between returnObject and filterObject]], [[What is PreFilter and PostFilter in Spring Security]], [[What is authentication in method-security SpEL]].

> [!warning] `filterObject` is not `returnObject`
> `@PostAuthorize("filterObject.owner == …")` has no current element — that name is empty or wrong. `@PostFilter("returnObject.owner == …")` tests the **list**, not each member. Maps need **`filterObject.value`**. A **null** `@PreFilter` argument fails at runtime; pick `filterTarget` when two collections are on the method.

> [!tip] Interview answer
> `filterObject` is the item `@PreFilter` and `@PostFilter` test in a loop. False removes it; it is not an access-denied throw. `returnObject` is the entire `@PostAuthorize` return value. For maps, filter the entry’s `value`.
