<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What account status flags does UserDetails expose?

> [!abstract] Short answer
> Four **boolean** methods besides username, password, and authorities: **`isEnabled`**, **`isAccountNonLocked`**, **`isAccountNonExpired`**, **`isCredentialsNonExpired`**. Interface **defaults are all `true`** (usable). **`DaoAuthenticationProvider`** enforces them through **`UserDetailsChecker`s**: lock / disabled / account-expired **before** the password; **credentials-expired after** a matching password. A **correct** password still fails with **`DisabledException`**, **`LockedException`**, **`AccountExpiredException`**, or **`CredentialsExpiredException`** — not **`BadCredentialsException`**.

## Four flags, two check points

**`UserDetails`** stores data; it is not the security interceptor ([[What is UserDetails and UserDetailsService in Spring Security]]). The four status methods are **default** on the interface (**all `true`**). Implement the interface and forget them, and locked users **still authenticate**. **`User.builder()`** inverts the names: **`disabled(true)`** / **`accountLocked(true)`** / **`accountExpired(true)`** / **`credentialsExpired(true)`** (builder defaults **`false`** = healthy).

**`AbstractUserDetailsAuthenticationProvider`** (parent of **`DaoAuthenticationProvider`**) ([[What is DaoAuthenticationProvider]], [[How do you create a custom UserDetailsService in Spring Security]]):

| When | Flag | `false` means | Exception |
| --- | --- | --- | --- |
| **Pre**-password | **`isAccountNonLocked`** | locked | **`LockedException`** |
| **Pre**-password | **`isEnabled`** | disabled | **`DisabledException`** |
| **Pre**-password | **`isAccountNonExpired`** | account expired | **`AccountExpiredException`** |
| **Post**-password | **`isCredentialsNonExpired`** | password expired | **`CredentialsExpiredException`** |

All four extend **`AccountStatusException`**. **`DisabledException`** / **`CredentialsExpiredException`** javadoc: they **do not claim** the password was valid. The provider still runs **`additionalAuthenticationChecks`** when pre-checks fail if **`alwaysPerformAdditionalChecksOnUser`** is **`true`** (default, **since 5.7.23**) so timing does not leak “disabled vs bad password”; the **thrown** type remains the **status** exception.

**`AccountStatusUserDetailsChecker`** (used outside this provider, e.g. some pre-auth / OTT checkers) tests **all four** in that same order in **one** `check`. JDBC’s default **`users.enabled`** maps to **`isEnabled`**; lock and expiry are **not** in the default schema unless you remap queries ([[How do you configure JDBC authentication in Spring Security]]). Missing user is **`UsernameNotFoundException`**, hidden as **`BadCredentialsException`** by default — a **different** path from these flags ([[What is UsernameNotFoundException]]).

```java
UserDetails user = User.builder()
	.username("alice")
	.password("{bcrypt}$2a$10$GRLdNijSQMUvl/au9ofL.eDwmoohzzS7.rmNSJZ.0FxO/BTk76klW")
	.roles("USER")
	.disabled(true)
	.accountLocked(false)
	.accountExpired(false)
	.credentialsExpired(false)
	.build();
```

**Listing 1.** Builder flags are **positive** (`disabled`); **`UserDetails`** getters are **`Non*`** except **`isEnabled`**. This user fails with **`DisabledException`** even if the password matches.

```d2
direction: down
load: "UserDetailsService.loadUserByUsername" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
pre: "preAuthenticationChecks\nlocked / disabled / account expired" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
pwd: "PasswordEncoder.matches" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
post: "postAuthenticationChecks\ncredentials expired" {
  width: 280
  height: 70
  style.fill: "#fce4ec"
}

load -> pre -> pwd -> post
```

**Fig. 1.** Account flags can reject **before** the hash. Expired **credentials** reject **after** a good password (typical “must change password” flow).

> [!warning] `true` means “OK”
> **`isAccountNonLocked() == false`** is locked. Returning **`true`** from all four is the interface default — a custom **`UserDetails`** that never overrides them **disables** lockout. Do not map **`disabled`** to **`BadCredentialsException`** in a failure handler if you need a distinct “account disabled” page (**`ExceptionMappingAuthenticationFailureHandler`** keys on exception **class names**).

> [!warning] JDBC `enabled` is only one flag
> Stock **`JdbcDaoImpl`** does not load lock or expiry. Apps that only set **`users.enabled`** never hit **`LockedException`**. Pre-checks on a **cached** `UserDetails` can be stale; the provider reloads and re-checks when a cached pre-check fails.

> [!tip] Interview answer
> UserDetails exposes isEnabled, isAccountNonLocked, isAccountNonExpired, and isCredentialsNonExpired, all defaulting to true. DaoAuthenticationProvider’s pre-checker throws LockedException, DisabledException, or AccountExpiredException before PasswordEncoder, and CredentialsExpiredException after a matching password. A right password can still fail, and a custom UserDetails that skips the defaults will never lock or disable anyone.
