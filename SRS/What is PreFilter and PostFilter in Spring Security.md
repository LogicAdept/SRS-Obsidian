<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS

# What is PreFilter and PostFilter in Spring Security?

> [!abstract] Short answer
> **`@PreFilter` and `@PostFilter` are SpEL annotations that drop collection elements, not grant/deny the call.** `@PreFilter` removes arguments the caller may not submit. `@PostFilter` removes return elements the caller may not see. `false` **drops that item**; it does not throw. They ride `@EnableMethodSecurity` pre/post (on by default). `@Secured` cannot filter.

## Filter the collection, still invoke

`@EnableMethodSecurity` publishes `AuthorizationManagerBeforeMethodInterceptor.preFilter()` and `AuthorizationManagerAfterMethodInterceptor.postFilter()`. Advisor order: `@PreFilter` **100**, `@PreAuthorize` **200**, then the after-advice family. Deprecated `@EnableGlobalMethodSecurity` needs `prePostEnabled = true`.

Each element is tested as **`filterObject`**. Official 7.1 shapes: arrays, collections, maps, and **open** streams. For a **`Map`**, use **`filterObject.value`**. With more than one collection argument, `@PreFilter` needs **`filterTarget`**. A **null** `@PreFilter` target fails.

| Annotation | When | What is walked |
|---|---|---|
| `@PreFilter` | Before the target | A method **argument** |
| `@PostFilter` | After the target returns | The **return** value |

That is not `@PreAuthorize` / `@PostAuthorize`. Those allow or deny the **invocation** / **whole** `returnObject`. `@PostFilter` still **runs the method** (including the query); it then trims the list in memory. Official note: in-memory filtering can be expensive — filter in the data layer when the set is large. `@Secured` is a list of authority strings; it has no `filterObject`.

```java
@PreFilter("filterObject.owner == authentication.name")
public Collection<Account> updateAccounts(Account... accounts) {
    return updated;
}

@PreFilter("filterObject.value.owner == authentication.name")
public Collection<Account> updateAccounts(Map<String, Account> accounts) {
    return updated;
}
```

**Listing 1.** Conceptual Security **7.1** — unowned arguments never reach the method body.

```java
@PostFilter("filterObject.owner == authentication.name")
public Collection<Account> readAccounts(String... ids) {
    return accounts;
}
```

**Listing 2.** Conceptual — the finder **loads everything**; forbidden rows are dropped afterward. See [[Why is PostFilter a performance trap]].

```d2
direction: down
pre: "@PreFilter\nargument collection" {
  width: 220
  height: 50
  style.fill: "#c8e6c9"
}
call: "target method" {
  width: 160
  height: 45
  style.fill: "#e3f2fd"
}
post: "@PostFilter\nreturn collection" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}

pre -> call
call -> post
```

**Fig. 1.** Drop elements; do not skip the join point. See [[What is filterObject in method security SpEL]], [[What is the difference between returnObject and filterObject]], [[What is PostAuthorize in Spring Security]], [[What is PreAuthorize]].

> [!warning] `false` is a drop, not `AccessDeniedException`
> An empty filtered collection is still a successful call. `@PostAuthorize("returnObject.owner == …")` on a **single** object denies; `@PostFilter` on a list silently shrinks it. Do not use `@PostFilter` as a substitute for query-level tenant/owner predicates on large results.

> [!tip] Interview answer
> `@PreFilter` and `@PostFilter` are method-security SpEL that filter collections with `filterObject`. PreFilter trims arguments before the method; PostFilter trims the return after it ran. They do not deny the call the way `@PreAuthorize` does, and `@Secured` cannot do this. PostFilter is an in-memory pass after the full load — prefer filtering in the query when the list is large.
