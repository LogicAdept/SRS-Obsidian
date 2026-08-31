<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is SimpleGrantedAuthority?

> [!abstract] Short answer
> **`SimpleGrantedAuthority`** is the stock **`GrantedAuthority`**: one **non-empty `String`**, returned by **`getAuthority()`**. The constructor takes that string **including any prefix** — Javadoc example **`ROLE_ADMIN`**. It does **not** add **`ROLE_`**. **`hasRole("ADMIN")`** looks for **`ROLE_ADMIN`** on this string; **`hasAuthority("REPORT_READ")`** looks for **`REPORT_READ`**. Authorization architecture: every built-in **`AuthenticationProvider`** populates **`Authentication`** with this type. Other implementations (**`FactorGrantedAuthority`**, **`JaasGrantedAuthority`**) exist; **`equals` is only vs another `SimpleGrantedAuthority`**.

## A string on Authentication, nothing else

**`final`** class. Field is named **`role`** internally — that is still just the authority text, not a separate role type ([[What is GrantedAuthority in Spring Security]], [[What is hasRole versus hasAuthority in Spring Security]]). **`Assert.hasText`**: empty/null constructor argument **throws**. **`toString()`** is the same string. **`hashCode` / `equals`** use that string.

**`User.roles("ADMIN")`** builds **`new SimpleGrantedAuthority("ROLE_ADMIN")`** and **rejects** `"ROLE_ADMIN"` as input. **`User.authorities("ADMIN")` / `AuthorityUtils.createAuthorityList`** store **`ADMIN`** with **no** prefix. JDBC **`authorities.authority`** is loaded as this class. **`DaoAuthenticationProvider`** copies **`UserDetails.getAuthorities()`** onto the success token ([[What is UserDetails and UserDetailsService in Spring Security]], [[What is DaoAuthenticationProvider]]).

**`hasRole("ADMIN")`** on HTTP **throws** if you pass **`ROLE_ADMIN`**. **`hasAuthority("ROLE_ADMIN")`** matches this object’s string **exactly**. **`FactorGrantedAuthority.PASSWORD_AUTHORITY`** is **not** this class — MFA factors are a different `GrantedAuthority` ([[How do you implement two-factor authentication in Spring Security]]).

```java
new SimpleGrantedAuthority("ROLE_ADMIN");
User.builder().roles("ADMIN").build(); // same stored string
User.builder().authorities("ADMIN").build(); // stores ADMIN — hasRole("ADMIN") misses
```

**Listing 1.** Prefix is **your** job (or **`roles()`**). **`hasRole`** will look for **`ROLE_` + argument**.

```java
http.authorizeHttpRequests((authorize) -> authorize
	.requestMatchers("/admin/**").hasRole("ADMIN")
	.requestMatchers("/reports/**").hasAuthority("REPORT_READ"));
```

**Listing 2.** **`hasRole`** ↔ **`ROLE_ADMIN`**. **`hasAuthority`** ↔ **`REPORT_READ`** as stored.

```d2
direction: down
sga: "SimpleGrantedAuthority\ngetAuthority() string" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
auth: "Authentication.getAuthorities()" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
rule: "hasRole / hasAuthority" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}

sga -> auth -> rule
```

**Fig. 1.** Authorization compares **strings**. This class is the usual holder.

> [!warning] It never prefixes `ROLE_`
> **`new SimpleGrantedAuthority("ADMIN")` + `hasRole("ADMIN")`** looks for **`ROLE_ADMIN`** and **denies**. **`hasRole("ROLE_ADMIN")` on `authorizeHttpRequests` throws.** Put the **full** string in the constructor, or use **`User.roles(...)`**.

> [!warning] `equals` is type-narrow
> Two authorities with the same **`getAuthority()`** are **not** `equals` if one is **`SimpleGrantedAuthority`** and the other is **`FactorGrantedAuthority`** / **`JaasGrantedAuthority`**. **`AuthorityAuthorizationManager`** compares **strings**, not **`equals`**. Do not put a **null** `getAuthority()` here — this class **always** has a text value (complex authorities are a **different** type).

> [!tip] Interview answer
> SimpleGrantedAuthority is Spring Security’s usual GrantedAuthority: a string such as ROLE_ADMIN or a custom permission name. It does not add ROLE_; User.roles("ADMIN") does. hasRole("ADMIN") therefore matches ROLE_ADMIN, and hasAuthority matches whatever I stored exactly. Mixing authorities("ADMIN") with hasRole("ADMIN") is the classic miss.
