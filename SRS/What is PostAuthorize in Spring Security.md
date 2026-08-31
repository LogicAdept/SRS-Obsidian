<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS

# What is PostAuthorize in Spring Security?

> [!abstract] Short answer
> **`@PostAuthorize` is a SpEL check that runs after the method returns.** `returnObject` is that result. Official 7.1: `@PostAuthorize("returnObject.owner == authentication.name")` — the value is returned only if the expression passes; otherwise `AccessDeniedException`. The method **already ran**. Use `@PreAuthorize` when the call must not happen.

## After the join point, then decide

`@EnableMethodSecurity` publishes `AuthorizationManagerAfterMethodInterceptor.postAuthorize()` (`PostAuthorizeAuthorizationManager`). Pre/post is **on by default**; deprecated `@EnableGlobalMethodSecurity` needs `prePostEnabled = true`. JavaDoc (since **3.0**): the expression is evaluated **after** the protected method is invoked.

`returnObject` is the whole return value (`MethodSecurityExpressionOperations`). It is **not** `filterObject` (per-element `@PostFilter`). Meta-annotations, class, and interface placement work the same as `@PreAuthorize`. It is the documented fit for **Insecure Direct Object Reference**: load by id, then refuse if the caller does not own the row.

Denial is after the target returns. Reads that did I/O already paid the cost; **writes already happened**. Official note: do **not** put `@PostAuthorize` on methods that perform database writes (typical: `@Transactional` on the same method). Read first with `@PostAuthorize`, then write if that read was allowed. If you must stack them, put `@EnableTransactionManagement` **before** `@EnableMethodSecurity` so the transaction can still roll back on deny.

```java
@Component
public class BankService {

    @PostAuthorize("returnObject.owner == authentication.name")
    public Account readAccount(String id) {
        return this.accounts.findById(id);
    }
}
```

**Listing 1.** Conceptual Security **7.1** — IDOR check on the loaded `Account`. The finder **runs** even for the wrong user; the caller gets `AccessDeniedException` instead of the object.

```java
@Transactional
@PostAuthorize("returnObject.owner == authentication.name")
public Account updateBalance(String id, Money amount) {
    Account account = this.accounts.findById(id);
    account.credit(amount);
    return account;
}
```

**Listing 2.** Conceptual — **avoid**. The credit runs before the owner check. Prefer `@PreAuthorize` / a prior authorized read, then a separate write.

```d2
direction: down
pre: "@PreAuthorize\nbefore invoke" {
  width: 200
  height: 50
  style.fill: "#c8e6c9"
}
call: "target method" {
  width: 160
  height: 45
  style.fill: "#e3f2fd"
}
post: "@PostAuthorize\nreturnObject" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}

pre -> call: "may skip"
call -> post: "already ran"
```

**Fig. 1.** Before vs after. See [[What is PreAuthorize]], [[What is the difference between returnObject and filterObject]], [[What is authentication in method-security SpEL]], [[What exception does a failed method-security check throw]], [[What is EnableMethodSecurity]].

> [!warning] Side effects already happened
> `@PostAuthorize` cannot un-call the method. Use `@PreAuthorize` (parameters, roles) when the work must not run. `@PostFilter` **drops elements** on a collection; `@PostAuthorize` **denies** the whole return. `returnObject` on a collection is the list, not each item.

> [!tip] Interview answer
> `@PostAuthorize` is SpEL after the method returns, with `returnObject` as the result. It is the usual IDOR check — load the entity, then confirm the owner. The method still executes, so do not use it to guard writes; use `@PreAuthorize` when the call must not happen.
