<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is X.509 authentication in Spring Security?

> [!abstract] Short answer
> Spring Security’s **X.509** support is **mutual TLS client-certificate** login, not “the browser checked the **server** cert.” The **container** (Tomcat/Netty) **requests and validates** the client certificate during the TLS handshake. **`X509AuthenticationFilter`** then reads that cert from the servlet request, **`SubjectX500PrincipalExtractor`** (**since 7.0**) takes the **CN** (or **emailAddress**), and **`PreAuthenticatedAuthenticationProvider`** loads **`UserDetails`** for that name. **`http.x509()`** (**`X509Configurer` since 3.2**) also adds **`FACTOR_X509`**. There is **no password** and **no `DaoAuthenticationProvider`**.

## Container validates the cert; Spring maps it to a user

Official X.509 chapter: ordinary HTTPS is the **server** proving itself to the browser. **Mutual authentication** is the **server asking the client** for a certificate. Get **clientAuth** working in the connector **before** wiring Spring. `clientAuth="true"` **requires** a cert; **`want`** allows the handshake without one — those clients still **cannot** pass X.509-only rules unless you add another mechanism such as form login.

**`X509Configurer`**: validation already happened at connect time. Spring **looks up `Authentication`**. Filter: **`X509AuthenticationFilter`** (`AbstractPreAuthenticatedProcessingFilter`). Provider: **`PreAuthenticatedAuthenticationProvider`**. If you omit **`authenticationUserDetailsService`**, the shared **`UserDetailsService`** is wrapped (**`UserDetailsByNameServiceWrapper`**). Entry point: **`Http403ForbiddenEntryPoint`** (typically **403**, not a login page) ([[What is UserDetails and UserDetailsService in Spring Security]], [[What is AuthenticationEntryPoint]]).

Default extractor **`SubjectX500PrincipalExtractor`**: **CN** from **`X509Certificate.getSubjectX500Principal()`** (RFC 2253). **`setExtractPrincipalNameFromEmail(true)`** uses the **emailAddress** OID instead. **`subjectPrincipalRegex`** is **deprecated** — use **`x509PrincipalExtractor`**. The extracted name **must exist** as a user (not locked/disabled/expired). **`http.x509()`** grants **`FACTOR_X509`** ([[How do you implement two-factor authentication in Spring Security]], [[What authentication mechanisms does Spring Security support]]).

This is **pre-authentication**: credentials on the token are the **certificate**, not a password. **`DaoAuthenticationProvider` is the wrong provider** ([[What is DaoAuthenticationProvider]], [[How do you configure HTTP Basic authentication in Spring Security]]).

```java
http
	.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
	.x509(Customizer.withDefaults());
```

**Listing 1.** Official servlet DSL. Needs a **`UserDetailsService`** whose usernames match **CN** (default).

```java
SubjectX500PrincipalExtractor extractor = new SubjectX500PrincipalExtractor();
extractor.setExtractPrincipalNameFromEmail(true);
http.x509((x509) -> x509.x509PrincipalExtractor(extractor));
```

**Listing 2.** Username from **emailAddress** instead of **CN**.

```d2
direction: down
tls: "TLS handshake\ncontainer validates client cert" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
filter: "X509AuthenticationFilter\nextract CN / email" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
uds: "UserDetailsService\nPreAuthenticatedAuthenticationProvider" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}

tls -> filter -> uds
```

**Fig. 1.** Spring never **issues** the cert. It **maps** a container-authenticated cert to **`UserDetails`**.

> [!warning] HTTPS server cert is not this feature
> A dump that only describes the **padlock / CA list** is **ordinary TLS**. **`http.x509()`** does nothing useful unless the connector **asks for a client certificate** (`clientAuth`). Spring **does not** re-verify the CA chain.

> [!warning] CN must match a user
> Default lookup is **`loadUserByUsername(CN)`**. A valid cert for an unknown CN is still **authentication failure** (**403** with the stock entry point). **`clientAuth="want"`** plus **`authenticated()`** still **denies** browsers that sent no cert. Pair with **`formLogin`** if you need a fallback.

> [!tip] Interview answer
> Spring Security X.509 is mutual TLS: the servlet container authenticates the client certificate, then X509AuthenticationFilter extracts CN (or email) and PreAuthenticatedAuthenticationProvider loads UserDetails. http.x509() adds FACTOR_X509. It is not the browser trusting the server certificate, and it does not use DaoAuthenticationProvider or a password.
