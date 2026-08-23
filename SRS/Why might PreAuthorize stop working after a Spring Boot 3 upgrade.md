<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS

# Why might PreAuthorize stop working after a Spring Boot 3 upgrade?

> [!abstract] Short answer
> Boot 3 ships **Spring Security 6**, which replaces **`@EnableGlobalMethodSecurity`** with **`@EnableMethodSecurity`** and changes defaults. **`@PreAuthorize` becomes a no-op** when method security is not activated, when **`prePostEnabled` stays off**, or when the config class is no longer picked up as a **`@Configuration`** bean.

## Common silent failures after upgrade

### 1. Method security never enabled

**`spring-boot-starter-security`** secures HTTP but **does not turn on method-level authorization by default**. You still need **`@EnableMethodSecurity`** on a configuration class (or **`<sec:method-security/>`** in XML).

Without it, **`@PreAuthorize` annotations compile but are never enforced**.

### 2. Leftover `@EnableGlobalMethodSecurity` without `prePostEnabled = true`

**`@EnableGlobalMethodSecurity`** is **deprecated**. Its **`prePostEnabled` defaults to `false`**, so **`@PreAuthorize` / `@PostAuthorize` do nothing** unless you explicitly set **`prePostEnabled = true`**.

**`@EnableMethodSecurity`** supersedes it and enables pre/post annotations **by default** (`prePostEnabled = true`).

| Annotation | `@PreAuthorize` active by default? |
|---|---|
| `@EnableGlobalMethodSecurity` | **No** — need `prePostEnabled = true` |
| `@EnableMethodSecurity` | **Yes** |

Migration equivalence from the reference:

```java
// Old — pre/post ON only with explicit flag
@EnableGlobalMethodSecurity(prePostEnabled = true)

// New — equivalent default
@EnableMethodSecurity
```

**Listing 1.** Boot 3 migrations should switch annotations, not only bump the dependency.

### 3. Missing `@Configuration` on the security config class

In Spring Security 6, **`@Configuration` is no longer meta-present on `@EnableMethodSecurity`** (and related enable annotations). A class that only had **`@EnableGlobalMethodSecurity`** may **stop being processed** as configuration unless you add **`@Configuration`** explicitly.

### 4. Still on deprecated global method security

If you temporarily keep **`@EnableGlobalMethodSecurity`**, the migration guide notes you may need the **`spring-security-access`** module on the classpath. The supported path is **`@EnableMethodSecurity`**, which wires the **`AuthorizationManager`**-based method interceptors.

```d2
direction: right
boot3: "Spring Boot 3\nSecurity 6" {
  width: 180
  height: 60
  style.fill: "#e3f2fd"
}
enable: "@EnableMethodSecurity\n(prePost default true)" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
pre: "@PreAuthorize\nenforced" {
  width: 180
  height: 60
  style.fill: "#c8e6c9"
}

boot3 -> enable -> pre
```

**Fig. 1.** Boot 3 upgrade path: activate the new method-security switch, then annotations take effect.

> [!warning] Compiles ≠ enforced
> **`@PreAuthorize` on a service method gives no compile-time guarantee** that interceptors exist. After upgrade, verify **`@EnableMethodSecurity`**, confirm **`prePostEnabled`** is not disabled, and check that method-security advisor beans are registered. See [[What is EnableMethodSecurity]] and [[Why does method security still matter if URL rules exist]].

> [!tip] Interview answer
> After Boot 3, @PreAuthorize often stops working because method security was never enabled, because @EnableGlobalMethodSecurity defaults prePostEnabled to false, or because the config class lost @Configuration. Replace with @EnableMethodSecurity, which enables pre/post annotations by default.
