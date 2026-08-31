<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# How do you create a custom UserDetailsService in Spring Security?

> [!abstract] Short answer
> Implement **`UserDetailsService.loadUserByUsername(String)`**: load a fully populated **`UserDetails`** or throw **`UsernameNotFoundException`** — **never `null`**. Return Spring’s **`User`** (or your type) with **password**, **authorities** (never `null`), and account flags. Expose it as a **`@Bean`**. **`DaoAuthenticationProvider`** calls it on username/password login and matches the stored hash with a **`PasswordEncoder`**.

## One method, then a bean

Javadoc: *Core interface which loads user-specific data* — the strategy **`DaoAuthenticationProvider`** uses. Lookup may be case-sensitive or not; the returned username may differ in case from the request ([[What is UserDetails and UserDetailsService in Spring Security]], [[What is DaoAuthenticationProvider]], [[What is UsernameNotFoundException]]).

```java
public class JpaUserDetailsService implements UserDetailsService {

	private final UserRepository users;

	public JpaUserDetailsService(UserRepository users) {
		this.users = users;
	}

	@Override
	public UserDetails loadUserByUsername(String username) {
		return users.findByUsername(username)
			.map(this::toUser)
			.orElseThrow(() -> UsernameNotFoundException.fromUsername(username));
	}

	private UserDetails toUser(AppUser u) {
		return User.builder()
			.username(u.username())
			.password(u.passwordHash())
			.disabled(!u.enabled())
			.accountLocked(u.locked())
			.roles(u.roles().toArray(String[]::new))
			.build();
	}
}
```

**Listing 1.** Conceptual JPA adapter. **`fromUsername`** is since **7.0**. **`User.builder()`** / the 7-arg **`User`** constructor are the stock implementation. Implement **`UserDetails`** yourself for extra principal fields (email, tenant). **`getAuthorities()`** and **`getUsername()`** must not be **`null`**. Flag methods default to **`true`** if you do not override them.

```java
@Bean
UserDetailsService userDetailsService(UserRepository users) {
	return new JpaUserDetailsService(users);
}
```

**Listing 2.** Official registration pattern (`CustomUserDetailsService` in the servlet reference). Used **only if** **`AuthenticationManagerBuilder` is empty** and **no `AuthenticationProvider` bean** exists. An extra **`DaoAuthenticationProvider`** bean **wins** and this loader never runs ([[How do you choose among InMemoryUserDetailsManager JdbcUserDetailsManager and a custom UserDetailsService]]).

```d2
direction: down
login: "formLogin / httpBasic" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
dao: "DaoAuthenticationProvider\nPasswordEncoder.matches" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
uds: "UserDetailsService\nloadUserByUsername" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
flags: "pre-auth UserDetailsChecker\nlocked / disabled / expired" {
  width: 280
  height: 70
  style.fill: "#f3e5f5"
}

login -> dao -> uds
dao -> flags
```

**Fig. 1.** The service **loads**; the provider **checks password and flags**. JDBC’s default schema does not load lock/expiry — that is why apps write a custom service ([[What account status flags does UserDetails expose]]).

Store **already encoded** passwords (`{bcrypt}…`). **`DaoAuthenticationProvider.setPasswordEncoder`** defaults to **`PasswordEncoderFactories.createDelegatingPasswordEncoder()`**. Encode at registration; do not store raw passwords.

**`User` is not immutable** (`CredentialsContainer.eraseCredentials`). Return a **new** instance each call if you would otherwise reuse a cached `User` whose password was cleared.

> [!warning] `null` is not “user not found”
> The contract is a complete **`UserDetails`** or **`UsernameNotFoundException`** (also if the user has **no** `GrantedAuthority`). Returning **`null`** is invalid. By default **`hideUserNotFoundExceptions`** is **`true`**, so a missing user becomes **`BadCredentialsException`** at the provider — same as a wrong password.

> [!warning] Correct password, still fail
> **`isEnabled` / `isAccountNonLocked` / `isAccountNonExpired` / `isCredentialsNonExpired`** are checked (**`LockedException`**, **`DisabledException`**, …). Defaults are **all `true`** — if you implement **`UserDetails`** and forget the flags, locked users still log in. A leftover **`AuthenticationProvider`** bean **ignores** your `UserDetailsService` bean.

> [!tip] Interview answer
> I implement UserDetailsService.loadUserByUsername, look the user up, and either return User.builder() with hash, roles, and flags, or throw UsernameNotFoundException — never null. I expose it as a bean so DaoAuthenticationProvider uses it, with a PasswordEncoder matching the stored hashes. Account flags on UserDetails are why a right password can still be rejected, and a custom AuthenticationProvider bean will skip this service entirely.
