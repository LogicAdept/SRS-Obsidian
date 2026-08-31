<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/Authentication #SRS

# What is `X509AuthenticationFilter`?

> [!abstract] Short answer
> The **mutual-TLS pre-authentication** filter (`http.x509()`). It extends **`AbstractPreAuthenticatedProcessingFilter`**, reads the client certificate the **servlet container** already put on the request (`jakarta.servlet.request.X509Certificate`), maps it to a username with an **`X509PrincipalExtractor`**, and builds a **`PreAuthenticatedAuthenticationToken`**. It does **not** run the TLS handshake, does **not** validate the cert, and is **not** [[What is PasswordEncoder in Spring Security]]. Sibling of [[What is UsernamePasswordAuthenticationFilter]] and [[What is BasicAuthenticationFilter]], not of a login page.

## Container cert, then `AuthenticationManager`

The filter never talks to the socket. Jakarta Servlet exposes a presented client certificate as `X509Certificate[]` on that request attribute (first element is the client cert). `X509AuthenticationFilter.extractClientCertificate` returns `certs[0]`, or **null** if the attribute is missing or empty. Principal comes from `principalExtractor.extractPrincipal(cert)` — default **`SubjectX500PrincipalExtractor`** takes **CN**; `setExtractPrincipalNameFromEmail(true)` takes `emailAddress` instead. Credentials are the **`X509Certificate` itself**.

```d2
direction: down
tls: "container TLS handshake\nclientAuth true / want" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
attr: "request attribute\njakarta.servlet.request.X509Certificate" {
  width: 320
  height: 50
}
x509: "X509AuthenticationFilter" {
  width: 280
  height: 40
  style.fill: "#e3f2fd"
}
token: "PreAuthenticatedAuthenticationToken\nprincipal + cert" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
am: "AuthenticationManager\nPreAuthenticatedAuthenticationProvider" {
  width: 320
  height: 50
  style.fill: "#e8f5e9"
}

tls -> attr
attr -> x509
x509 -> token: "cert present"
x509 -> am: "null principal: skip"
token -> am
```

**Fig. 1.** Pre-auth: the container authenticated the cert; Spring Security only **extracts** it and loads `UserDetails`. XML alias **`X509_FILTER`** / `<x509 />`. Java: `http.x509(...)`. Architecture TRACE: after Logout / OAuth2 authorization-request filters, **before** form login and Basic — see [[What is FilterOrderRegistration]] (`X509AuthenticationFilter` then `AbstractPreAuthenticatedProcessingFilter`). End-to-end request path: [[How does Spring Security authenticate an HTTP request end to end]].

`AbstractPreAuthenticatedProcessingFilter.doAuthenticate`: if principal is **null**, it returns and **`chain.doFilter` still runs**. If a principal exists, it calls `AuthenticationManager` with that token. **`X509Configurer`** (since **3.2**) also registers a **`PreAuthenticatedAuthenticationProvider`** (loads the user by extracted name via `UserDetailsService`; it does **not** check a password) and an **`Http403ForbiddenEntryPoint`**. Success **continues** the chain — no form-login redirect. Default **`continueFilterChainOnUnsuccessfulAuthentication`** is **true**, so a failed lookup can still fall through to form login, Basic, or [[What is AnonymousAuthenticationFilter]]. If the `SecurityContext` already has an `Authentication`, the filter does nothing unless `checkForPrincipalChanges` is set.

```java
http.x509(Customizer.withDefaults());

SubjectX500PrincipalExtractor extractor = new SubjectX500PrincipalExtractor();
extractor.setExtractPrincipalNameFromEmail(true);
http.x509((x509) -> x509.x509PrincipalExtractor(extractor));
```

**Listing 1.** First line is enough when CN is the username and a `UserDetailsService` bean exists. Second overrides CN → email. `subjectPrincipalRegex` / `SubjectDnX509PrincipalExtractor` is the **deprecated** regex path. Passing `x509AuthenticationFilter(custom)` skips populating the configurer’s extractor, details source, and repository onto that instance. See [[What is HttpSecurity in Spring Security]] and [[How do you require HTTPS with Spring Security]] (HTTPS redirect is a **different** filter; it does not request a client cert).

`http.x509()` sets the filter’s `SecurityContextRepository` to **`RequestAttributeSecurityContextRepository`** (request-scoped). Constructing the filter yourself keeps the superclass default **`HttpSessionSecurityContextRepository`**. Spring Security **7** `HttpSecurity` DSL also grants **`FACTOR_X509`** for multi-factor authorization.

> [!warning] The filter cannot invent a certificate
> Mutual TLS must be turned **on in the container** (`clientAuth="true"` require, or `"want"` optional on Tomcat’s SSL connector). `http.x509()` does not call `needClientAuth`. If Tomcat never negotiated a client cert, the attribute is absent, principal is null, and this filter **skips** — it does not 401 by itself. With `clientAuth="want"`, clients that omit a cert still get HTTPS; they stay unauthenticated unless another mechanism (form, Basic) runs. Pair `authorizeHttpRequests` with that fact. The filter also does **not** replace [[What is UsernamePasswordAuthenticationFilter]] as an `addFilterBefore` landmark in a UI chain.

> [!tip] Interview answer
> X509AuthenticationFilter is Spring Security’s client-certificate filter: it reads jakarta.servlet.request.X509Certificate, extracts a username (CN by default), and authenticates a PreAuthenticatedAuthenticationToken. http.x509 adds it. The servlet container must request the cert; the filter does not handshake TLS and does not use PasswordEncoder. No cert means the filter skips and the chain continues.
