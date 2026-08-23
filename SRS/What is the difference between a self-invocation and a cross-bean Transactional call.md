<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/SelfInvocation #SRS

# What is the difference between a self-invocation and a cross-bean `Transactional` call?

> [!abstract] Short answer
> A **cross-bean** call enters through the Spring **proxy**, so **`TransactionInterceptor`** reads the callee’s `@Transactional` attributes (propagation, rollback rules, and so on). A **self-invocation** (`this.inner()`) calls the **target object directly**, bypassing the proxy — the inner annotation is **ignored**, even when the outer method is already transactional.

## Two call paths

Spring’s `@Transactional` documentation and AOP proxy docs agree: in default **proxy** mode, only **external** calls through the proxy are advised. Once execution is inside the target instance, `this` references invoke plain Java methods on the target.

```d2
direction: right
cross: "Other bean\ncalls service.inner()" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
proxy: "Proxy →\nTransactionInterceptor" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
self: "outer() calls\nthis.inner()" {
  width: 220
  height: 80
  style.fill: "#ffebee"
}
bypass: "Target.inner()\ninterceptor skipped" {
  width: 240
  height: 80
  style.fill: "#ffebee"
}

cross -> proxy
self -> bypass
```

**Fig. 1.** Cross-bean calls are proxied; same-class `this` calls are not.

```java
@Service
public class UserService {

    public void registerUser(User user) {
        saveUser(user); // self-invocation — saveUser's @Transactional ignored
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void saveUser(User user) {
        userRepository.save(user);
    }
}

@RestController
class UserController {

    @Autowired UserService users;

    @PostMapping("/users")
    void create(@RequestBody User user) {
        users.saveUser(user); // cross-bean → proxy → real REQUIRES_NEW boundary
    }
}
```

**Listing 1.** Conceptual: `registerUser()` does **not** get an independent `REQUIRES_NEW` transaction; the controller call **does**.

## “Still in a transaction” is not the same as “inner `@Transactional` ran”

If `registerUser()` itself were `@Transactional(REQUIRED)` and entered through the proxy, a self-call to `saveUser()` still executes **inside the outer physical transaction** — but **not** because `REQUIRED` on `saveUser` joined. The inner interceptor **never ran**, so `REQUIRES_NEW`, custom rollback rules, or `readOnly` on `saveUser` do not apply.

That distinction matters for [[How does REQUIRES_NEW transaction propagation work]], [[Why can a self-invoked REQUIRES_NEW method still roll back the outer transaction]], and [[What happens when a non-transactional method calls a Transactional method in the same class]].

Both **JDK interface proxies** and **CGLIB class-based proxies** behave the same way: self-calls on `this` bypass advice. Subclassing the target does not intercept internal calls — see [[Why does a self-invocation skip Spring AOP advice]].

Fixes when the inner annotation must run: separate bean, injected self-proxy, AspectJ transaction mode, or programmatic demarcation — [[How do you make an inner Transactional method honor its annotation]].

> [!warning] Tests through the proxy hide production self-calls
> Integration tests that invoke only the **public entry** through Spring may show transactions working while a private `this.helper()` loop in production never opens the inner boundary.

> [!warning] Do not read propagation from self-called inner methods
> Explaining inner `REQUIRES_NEW` or `MANDATORY` on a `this`-called method describes annotations that **never executed**. Only cross-bean (or AspectJ-woven) paths count.

> [!tip] Interview answer
> **Cross-bean: proxy → interceptor → inner `@Transactional` applies. Self-invocation: `this.inner()` skips the proxy, so inner attributes are ignored.** If the outer method was already transactional, the inner code may still run in that outer TX — but because the interceptor never ran, not because propagation joined. JDK and CGLIB proxies both behave this way.
