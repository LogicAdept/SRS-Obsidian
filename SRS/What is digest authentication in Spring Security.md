<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #Java/Spring/Security/PasswordEncoder #SRS

# What is digest authentication in Spring Security?

> [!abstract] Short answer
> HTTP **Digest** (RFC **2617**, with RFC **2069** clients) is a **challenge/response** header scheme. The server sends **401** plus **`WWW-Authenticate: Digest`**. The client retries with **`Authorization: Digest`** (`username`, `realm`, `nonce`, `uri`, `response`, and for **`qop=auth`**: `nc`, `cnonce`). **`DigestAuthenticationFilter`** recomputes the **MD5** response from the stored password (or precomputed **HA1**) and compares it. There is **no** `http.digest()` DSL. Official guidance: **do not use Digest in modern applications** — it needs **plaintext or MD5** storage (**`NoOpPasswordEncoder`**), not bcrypt/Argon2. Prefer **TLS** plus **HTTP Basic** or **Bearer** ([[How do you configure HTTP Basic authentication in Spring Security]], [[What authentication mechanisms does Spring Security support]]).

## Challenge, nonce, then an MD5 in the filter

Unlike Basic, the password is **not** Base64 on the wire. The client proves knowledge of **username + realm + password** plus the request **method** and **URI**. Spring implements **`qop="auth"`** only (**not** `auth-int`). Algorithm is **MD5** (`DigestAuthUtils.md5Hex`). **RFC 7616** SHA-256 Digest is **not** this filter.

**`DigestAuthenticationEntryPoint`** ([[What is AuthenticationEntryPoint]]) writes the challenge. Nonce is **stateless**: `base64(expirationTime + ":" + md5Hex(expirationTime + ":" + key))`. Default validity **300 seconds**. Expired nonce → **`NonceExpiredException`** → **`stale=true`** so a capable client retries without a new password prompt. **`realmName`** and **`key`** are required.

**`DigestAuthenticationFilter`** (since **1.0**; still in **7.1.1**) runs if **`Authorization`** starts with **`Digest `**. It loads **`UserDetails`** ([[What is UserDetails and UserDetailsService in Spring Security]]), computes the server digest, and on match puts a **`UsernamePasswordAuthenticationToken`** on **`SecurityContextHolder`**. Default **`SecurityContextRepository`** is **request-attribute only** (not the session). Filter order sits **just before** Bearer and **`BasicAuthenticationFilter`** ([[What is BasicAuthenticationFilter]]).

The digest check is **not** **`PasswordEncoder.matches`** / **`DaoAuthenticationProvider`**. That provider only matters if you leave **`createAuthenticatedToken`** at default **false** (unauthenticated token so a later provider could still run account-status checks) ([[What is DaoAuthenticationProvider]], [[What account status flags does UserDetails expose]], [[What is an authenticated versus unauthenticated UsernamePasswordAuthenticationToken]]). **`true`**: trusted token + authorities; **flags skipped**; **`UserDetailsService`** called once.

```java
DigestAuthenticationEntryPoint digestEntryPoint() {
	DigestAuthenticationEntryPoint entry = new DigestAuthenticationEntryPoint();
	entry.setRealmName("My App Realm");
	entry.setKey("3028472b-da34-4501-bfd8-a355c42bdf92");
	return entry;
}

DigestAuthenticationFilter digestAuthenticationFilter(UserDetailsService users) {
	DigestAuthenticationFilter filter = new DigestAuthenticationFilter();
	filter.setUserDetailsService(users);
	filter.setAuthenticationEntryPoint(digestEntryPoint());
	return filter;
}

@Bean
SecurityFilterChain filterChain(HttpSecurity http, UserDetailsService users) throws Exception {
	http
		.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
		.exceptionHandling((exceptions) -> exceptions.authenticationEntryPoint(digestEntryPoint()))
		.addFilter(digestAuthenticationFilter(users));
	return http.build();
}
```

**Listing 1.** Official **7.x** shape: **`addFilter`** + the Digest entry point on **`exceptionHandling(Customizer)`**. XML: **`<custom-filter … position="DIGEST_AUTH_FILTER"/>`**. You still need **insecure plaintext** storage (**`NoOpPasswordEncoder`**) ([[What is NoOpPasswordEncoder]]).

```http
WWW-Authenticate: Digest realm="My App Realm", qop="auth", nonce="…"
Authorization: Digest username="…", realm="My App Realm", nonce="…", uri="…", response="…", qop=auth, nc=…, cnonce="…"
```

**Listing 2.** Challenge then client **`response`**. **HA1** is **MD5(`username:realm:password`)**. Set **`passwordAlreadyEncoded`** if the DAO already stores HA1 instead of the raw password.

```d2
direction: down
chal: "DigestAuthenticationEntryPoint\n401 + WWW-Authenticate Digest" {
  width: 320
  height: 70
  style.fill: "#fff3e0"
}
hdr: "Authorization: Digest …" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
md5: "DigestAuthenticationFilter\nMD5 vs stored password / HA1" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
ctx: "SecurityContextHolder" {
  width: 220
  height: 50
  style.fill: "#fce4ec"
}

chal -> hdr -> md5 -> ctx
```

**Fig. 1.** The filter **is** the authenticator. **`DaoAuthenticationProvider`** does not compute this MD5.

> [!warning] Official: do not use Digest in modern apps
> You must store **plaintext**, reversible ciphertext, or **MD5 HA1**. Adaptive hashes (**bcrypt**, **PBKDF2**, **SCrypt**) **cannot** participate. **`NoOpPasswordEncoder`** is **deprecated as insecure**. Digest is **not** “Basic plus TLS.” Use **HTTPS** anyway; nonce replay is only bounded by **`nonceValiditySeconds`**. **RFC 7616** SHA-256 Digest is a different standard — this class is still **RFC 2617 MD5**.

> [!warning] Default token is unauthenticated
> **`createAuthenticatedToken`** defaults to **false**: the context holds **`UsernamePasswordAuthenticationToken.unauthenticated`**. Javadoc intends a later **`AuthenticationProvider`** to check **enabled / lock / expiry**. The default **`authorizeHttpRequests`** chain does **not** call **`authenticate`** for you. Set **`true`** when Digest is the only check, and accept skipped flags — or cache **`UserDetailsService`** instead.

> [!tip] Interview answer
> Digest is RFC 2617 challenge/response: the browser hashes username, realm, password, method, and URI with a server nonce so the password is not Base64 on the wire. Spring’s DigestAuthenticationFilter still uses MD5 and needs the password or HA1 in a recoverable form, which is why the reference says not to use it on new work. There is no http.digest(); you add the filter and DigestAuthenticationEntryPoint yourself. For APIs, prefer TLS with Basic or a Bearer token.
