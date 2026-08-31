<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #Java/Spring/Security/PasswordEncoder #SRS

# What is DaoAuthenticationProvider?

> [!abstract] Short answer
> **`DaoAuthenticationProvider`** is the **username/password `AuthenticationProvider`**. It **`supports` only `UsernamePasswordAuthenticationToken`**. It **`loadUserByUsername`s**, runs **account-status** checks, then **`PasswordEncoder.matches`**. Default encoder is **`PasswordEncoderFactories.createDelegatingPasswordEncoder()`**. On success it returns a **new authenticated** token with **`FACTOR_PASSWORD`**. Form login and HTTP Basic use it when a **`UserDetailsService`** is present. A missing user is **`UsernameNotFoundException`**, hidden as **`BadCredentialsException`** by default (**`hideUserNotFoundExceptions == true`**). Returning **`null`** from the service is **`InternalAuthenticationServiceException`**, not “user not found.”

## Retrieve, check flags, then the hash

Extends **`AbstractUserDetailsAuthenticationProvider`**. Construct with **`new DaoAuthenticationProvider(userDetailsService)`** — the no-arg setter path is gone. **`ProviderManager`** calls it for form/Basic tokens ([[What is AuthenticationManager and AuthenticationProvider in Spring Security]], [[What is UserDetails and UserDetailsService in Spring Security]], [[What is an authenticated versus unauthenticated UsernamePasswordAuthenticationToken]]).

Parent **`authenticate`** ([[What account status flags does UserDetails expose]], [[How do you create a custom UserDetailsService in Spring Security]]):

1. **`retrieveUser`** → **`UserDetailsService.loadUserByUsername`**. **`UsernameNotFoundException`**: dummy **`matches`** against a cached **`userNotFoundPassword`** hash (**SEC-2056** timing), then rethrow. With default **hide**, that becomes **`BadCredentialsException`** ([[What is UsernameNotFoundException]]).
2. **Pre-checks** (before password): locked / disabled / account expired.
3. **`additionalAuthenticationChecks`**: null credentials or **`!passwordEncoder.matches(presented, user.getPassword())`** → **`BadCredentialsException`**. If pre-check already failed, **`alwaysPerformAdditionalChecksOnUser`** (default **true**, **since 5.7.23**) still runs **`matches`** for constant time, then rethrows the **status** exception.
4. **Post-check**: credentials expired.
5. **`createSuccessAuthentication`**: optional **`CompromisedPasswordChecker`** (**since 6.3**) → **`CompromisedPasswordException`**; optional **`UserDetailsPasswordService`** rehash; then **`FACTOR_PASSWORD`**.

In-memory / JDBC **`UserDetailsService`** beans plug into this provider ([[How do you configure JDBC authentication in Spring Security]]). **LDAP bind** and **JWT** are **other** providers. JWT uses a **different `Authentication` type**, so it does **not** race DAO. **LDAP and DAO both `support` username/password** — the **first `AuthenticationException` aborts `ProviderManager`**; a DAO miss **never falls through** to LDAP. A leftover **`AuthenticationProvider` `@Bean`** can **replace** auto-wired DAO entirely ([[How do you configure a custom AuthenticationProvider in Spring Security]]).

```java
@Bean
DaoAuthenticationProvider daoAuthenticationProvider(UserDetailsService users, PasswordEncoder encoder) {
	DaoAuthenticationProvider dao = new DaoAuthenticationProvider(users);
	dao.setPasswordEncoder(encoder);
	return dao;
}
```

**Listing 1.** Explicit wiring. Prefer **`http.authenticationProvider(dao)`** or a **single** provider bean — **two** `@Bean` providers are **ignored** when the builder already has one.

```java
if (!this.passwordEncoder.get().matches(presentedPassword, userDetails.getPassword())) {
	throw new BadCredentialsException("Bad credentials");
}
```

**Listing 2.** Core of **`additionalAuthenticationChecks`**. Stored value must already be encoded (`{bcrypt}…`).

```d2
direction: down
uds: "UserDetailsService.loadUserByUsername" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
pre: "preAuthenticationChecks\nlock / disabled / expired" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
pe: "PasswordEncoder.matches" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
post: "credentials expired +\nFACTOR_PASSWORD token" {
  width: 260
  height: 70
  style.fill: "#fce4ec"
}

uds -> pre -> pe -> post
```

**Fig. 1.** Flags can fail **before** the encoder. **`matches`** is the password gate.

> [!warning] `hideUserNotFoundExceptions` is the default
> Callers see **`BadCredentialsException`** for both unknown user and wrong password. Set **`false`** only if you accept **user enumeration**. **`loadUserByUsername` must not return `null`**. Timing protection still **`matches`** a dummy hash on not-found — skipping the encoder on that path is how you leak existence.

> [!warning] Two username/password providers
> If **DAO is first** and the user lives only in **LDAP**, you get **401**, not a second try. JWT resource-server tokens never hit this class. Publishing a **custom `AuthenticationProvider` bean** while also exposing **`UserDetailsService`** is how the DAO you expected **never runs**.

> [!tip] Interview answer
> DaoAuthenticationProvider is the default username/password provider: it loads UserDetails, checks lock/disabled/expiry, then PasswordEncoder.matches. It only supports UsernamePasswordAuthenticationToken, so form login and HTTP Basic use it. UsernameNotFoundException is hidden as BadCredentialsException by default, and I never return null from UserDetailsService. A second provider only runs if this one returns null, not if it throws.
