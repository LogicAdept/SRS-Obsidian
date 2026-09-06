<!--
reps: 0
priority: 0
-->
#Java/Servlet #Java/Security #SRS

# What servlet authentication mechanisms exist?

> [!abstract] Short answer
> Jakarta Servlet **6.1 §13.6** names four **container** mechanisms a web client can use: **HTTP Basic**, **HTTP Digest**, **form-based**, and **HTTPS client certificate**. You pick one in **`login-config` / `<auth-method>`** (`BASIC`, `DIGEST`, `FORM`, `CLIENT-CERT`). **Digest is SHOULD**; the others are the specified set. **`HttpServletRequest.login` / `authenticate` / `logout`** (3.0+) are **programmatic** ways to drive or clear that login. Extra HTTP-layer plugins: **Jakarta Authentication** (container profile). Auth vs access: [[What is the difference between authentication and authorization]]. Protecting URLs: [[How do you restrict servlet endpoints to users with a valid session]]. 3.0 `login`: [[What features were added in the Servlet 3 specification]].

## Four `auth-method`s plus programmatic login

A **`security-constraint` with an `auth-constraint`** means the user **must authenticate**. **No auth-constraint** → the container **must not** demand a login.

| Mechanism | `auth-method` | How | Spec notes |
| --- | --- | --- | --- |
| **HTTP Basic** | `BASIC` | RFC 7617: browser prompts; **username:password** in **`Authorization`**, **base64** (not encryption). **Realm** string. | **Not secure** on plain HTTP. Use **HTTPS** / network protection. |
| **HTTP Digest** | `DIGEST` | Hash of password + nonce; **password not on the wire**. Container still needs a **password equivalent** to recompute the digest. | Containers **SHOULD** support it. |
| **Form** | `FORM` | App login page. Fields **`j_username` / `j_password`**. Action **`j_security_check`**. Error page on failure (**200**). Success → **redirect** to the stored URL (prefer **303**). | **Required**. Do **not** pair with **URL rewriting** for the session. Password field **`autocomplete="off"`**. |
| **Client cert** | `CLIENT-CERT` | **TLS** client **Public Key Certificate**. | Strong; often SSO in the browser. |

**Programmatic:** **`login(user, password)`** for a **custom** screen; **`authenticate(response)`** to run the **configured** mechanism; **`logout()`**. After a successful login: **`getUserPrincipal()` / `getRemoteUser()` / `isUserInRole`**. Session **timeout/invalidate** after form login **logs the user out** (SSO may span apps in the same container). **`login()`** can replace the look of **`FORM`**.

**§13.6.5:** containers **should** expose APIs for **more** HTTP-layer mechanisms; portable path is the **Jakarta Authentication** servlet-container profile.

```d2
direction: down
trig: "constrained request\n(auth-constraint)" {
  width: 240
  height: 48
}
mech: "BASIC / DIGEST / FORM / CLIENT-CERT" {
  width: 300
  height: 40
  style.fill: "#e8f5e9"
}
ok: "principal + roles\nthen authorization" {
  width: 220
  height: 48
  style.fill: "#e3f2fd"
}
trig -> mech -> ok
```

**Fig. 1.** **Authentication** establishes **who**. **`security-constraint` roles** decide **whether**.

```xml
<!-- Conceptual — Jakarta Servlet 6.1 web.xml -->
<login-config>
  <auth-method>FORM</auth-method>
  <form-login-config>
    <form-login-page>/login.jsp</form-login-page>
    <form-error-page>/login-error.jsp</form-error-page>
  </form-login-config>
</login-config>
```

**Listing 1.** **`FORM`**. The page must POST **`j_security_check`** with **`j_username`** and **`j_password`**.

> [!warning] Basic and form are cleartext without TLS
> **Basic** is **base64**. **Form** posts passwords as fields. Spec: run the **login page and submit** over **CONFIDENTIAL** when the triggering request was secure. **Digest** still needs **stored password equivalents** in the container.

> [!warning] Form login vs URL rewriting
> Form login **should only** be used when the session is tracked by **cookies or SSL**. **`j_security_check`** is **fixed**; a custom action URL will **not** complete container form auth. Failure returns **200** on the **error page**, not necessarily **401**.

> [!tip] Interview answer
> Servlet containers authenticate with BASIC, DIGEST, FORM, or CLIENT-CERT, selected in login-config. BASIC and FORM need TLS in production; DIGEST hashes the password but is only SHOULD; CLIENT-CERT uses a TLS client certificate. Since Servlet 3 I can also call login, authenticate, or logout on the request. That is identity; security-constraint is still authorization.
