<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS

# How do you integrate Spring Security with Thymeleaf?

> [!abstract] Short answer
> Add **`thymeleaf-extras-springsecurity6`** (Security 5: **`…springsecurity5`**) and the **`sec`** dialect. **`sec:authorize`**, **`#authentication`**, and **`#authorization`** hide or show markup from **`SecurityContext`**. They do **not** replace **`authorizeHttpRequests`** or method security. Unsafe **`th:action`** POSTs get a CSRF hidden field through **`RequestDataValueProcessor`**.

## Dialect for the view, filters for the request

`SpringSecurityDialect` (package `org.thymeleaf.extras.springsecurity6.dialect`, prefix **`sec`**) is the Thymeleaf equivalent of the Spring Security JSP tag library. Boot registers the dialect bean when **`SpringSecurityDialect`** and **`CsrfToken`** are on the classpath — add the extras artifact plus the Thymeleaf and Security starters; you do not declare the dialect by hand.

```html
<html xmlns:th xmlns:sec>
  <div sec:authorize="isAuthenticated()">
    Hello, <span sec:authentication="name">user</span>
  </div>
  <div sec:authorize="hasRole('ADMIN')">Admin tools</div>
  <a sec:authorize-url="/admin" th:href="@{/admin}">Admin</a>
</html>
```

**Listing 1.** Conceptual markup. **`sec:authorize` / `sec:authorize-expr`** evaluate a Spring Security expression (same family as **`hasRole`**, **`isAuthenticated()`**). **`sec:authorize-url`** asks whether the current **`Authentication`** may call that path (optional `POST /admin`). **`#authentication`** is the **`Authentication`**; **`#authorization.expression('…')`** is the **`th:if`** form of the same check.

Those attributes only decide whether **tag children are rendered**. A user who forges a GET still hits **`AuthorizationFilter`** / **`@PreAuthorize`**. Hide a button ≠ protect the controller ([[Why does method security still matter if URL rules exist]], [[How do you configure authorizeHttpRequests in Spring Security 6]]).

CSRF is a separate integration: **`CsrfRequestDataValueProcessor`** plus Thymeleaf’s **`RequestDataValueProcessor`** support. A **`th:action`** form with an unsafe method (POST) gets the token automatically — Spring Security’s custom login template relies on that. AJAX still needs the token in a header from **`_csrf`** ([[How do you handle CSRF tokens in AJAX requests in Spring Security]], [[What is hasRole in PreAuthorize versus Secured]]).

```html
<form th:action="@{/login}" method="post">
  <input type="text" name="username"/>
  <input type="password" name="password"/>
  <input type="submit" value="Log in"/>
</form>
```

**Listing 2.** Custom **`/login`** POST. No extra hidden field in the template; Thymeleaf writes **`_csrf`**. Fields must stay **`username`** / **`password`**.

```d2
direction: down
req: "HTTP request" {
  width: 140
  height: 40
  style.fill: "#e3f2fd"
}
chain: "FilterChain +\nmethod security" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
view: "SpringSecurityDialect\nsec:authorize" {
  width: 220
  height: 50
  style.fill: "#c8e6c9"
}

req -> chain
chain -> view
```

**Fig. 1.** The dialect reads **`SecurityContext`** while rendering. Authorization of the **next** request is still the filter chain.

Match the extras artifact to Spring Security: **`thymeleaf-extras-springsecurity6`** for Security 6 / Boot 3+, **`…springsecurity5`** for Security 5. The dialect class package name follows that digit. The XML namespace URI is optional (IDE only); a wrong URI does not stop processing.

> [!warning] `sec:authorize` is not an access rule
> Omitting a menu item does not 403 the URL. Keep **`authorizeHttpRequests`** and method security. View-layer expressions are convenience, not defense in depth.

> [!warning] Artifact digit and `hasRole` prefix
> **`springsecurity5` on Boot 3 / Security 6** means the dialect bean never appears (`ThymeleafSecurityDialectConfiguration` looks for the **6** class). Extras samples use **`hasRole('ROLE_ADMIN')`**; Spring’s **`hasRole('ADMIN')`** already prepends **`ROLE_`**. Doubling the prefix hides the block for a real admin.

> [!tip] Interview answer
> Integration is thymeleaf-extras-springsecurity6 plus the sec dialect: sec:authorize and #authentication read SecurityContext to show or hide markup. Boot auto-registers the dialect when that jar and CsrfToken are present. th:action POSTs pick up CSRF via RequestDataValueProcessor. The dialect never replaces filter or method authorization — hide the button and still lock the endpoint.
