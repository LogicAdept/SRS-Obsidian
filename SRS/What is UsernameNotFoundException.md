<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is UsernameNotFoundException?

> [!abstract] Short answer
> **`UsernameNotFoundException`** is the **`AuthenticationException`** **`UserDetailsService.loadUserByUsername`** must throw when it cannot return a user — javadoc: missing username **or a user with no `GrantedAuthority`**. **Never return `null`.** **`fromUsername(username)`** (**since 7.0**) sets **`getName()`** and the message **`user not found`**. **`DaoAuthenticationProvider`** default **`hideUserNotFoundExceptions == true`** turns it into **`BadCredentialsException`** so callers cannot tell **unknown user** from **wrong password**. A **`null`** return is **`InternalAuthenticationServiceException`**, not this type.

## The not-found contract, then hide

Thrown if a **`UserDetailsService`** cannot locate the user (class javadoc). Two-arg / message constructors leave **`getName()` null**. Prefer **`fromUsername` / `fromUsername(username, cause)`** so the invalid name is on the exception. Stock **`InMemoryUserDetailsManager`** / **`JdbcDaoImpl`** throw it when the map or SQL miss ([[What is UserDetails and UserDetailsService in Spring Security]], [[How do you create a custom UserDetailsService in Spring Security]]).

**`AbstractUserDetailsAuthenticationProvider.retrieveUser`** (**`DaoAuthenticationProvider`**):

1. Call **`loadUserByUsername`**.
2. On **`UsernameNotFoundException`**: dummy **`PasswordEncoder.matches`** against a cached **`userNotFoundPassword`** hash (**SEC-2056**, timing).
3. If **`hideUserNotFoundExceptions`** (default **true**): throw **`BadCredentialsException`**. If **false**: rethrow **`UsernameNotFoundException`**.

**`null` from the service** is wrapped as **`InternalAuthenticationServiceException`**. That type **aborts** **`ProviderManager`** (**SEC-546**). Hidden not-found is **`BadCredentialsException`**, which **does not** abort the list — a later provider can still succeed ([[What is DaoAuthenticationProvider]], [[What is ProviderManager in Spring Security]]).

Form **`POST /login`** still lands on **`AuthenticationFailureHandler`** (**`/login?error`**) for both unknown user and bad password when hide is on ([[What is AuthenticationFailureHandler]]).

```java
return users.findByUsername(username)
	.map(this::toUser)
	.orElseThrow(() -> UsernameNotFoundException.fromUsername(username));
```

**Listing 1.** Correct miss. Do **not** `return null`.

```java
dao.setHideUserNotFoundExceptions(true); // default
```

**Listing 2.** Keep **true** in production so login errors do not enumerate accounts.

```d2
direction: down
uds: "loadUserByUsername" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
unfe: "UsernameNotFoundException" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
hide: "hideUserNotFoundExceptions?" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
bad: "BadCredentialsException" {
  width: 240
  height: 50
  style.fill: "#ffcdd2"
}

uds -> unfe -> hide
hide -> bad: "true (default)"
hide -> unfe: "false: rethrow"
```

**Fig. 1.** The service throws **this**. The provider **usually** reports **bad credentials**.

> [!warning] `null` is not not-found
> Dump “NPE inside the provider” is the wrong failure. **`null`** → **`InternalAuthenticationServiceException`** (fatal to **`ProviderManager`**). Empty authorities is **this** exception per **`UserDetailsService`** javadoc. Catching only **`UsernameNotFoundException`** around **`authenticate()`** misses the default **hide** path.

> [!warning] Do not turn hide off to “help users”
> **`hideUserNotFoundExceptions = false`** lets the UI say “unknown user,” which **enumerates** accounts. Status flags (**disabled / locked**) are **different** exceptions and still run **after** a successful load ([[What account status flags does UserDetails expose]]).

> [!tip] Interview answer
> UsernameNotFoundException is what loadUserByUsername throws when the user is missing or has no authorities — never return null. In 7.0 I use fromUsername. DaoAuthenticationProvider hides it as BadCredentialsException by default so unknown user and wrong password look the same. A null return is InternalAuthenticationServiceException, which is a different, fatal path.
