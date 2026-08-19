<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/AppSec #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Browser AJAX POSTs are state-changing, so CSRF is on by default. Dumps put the token and header name in meta tags and attach them on every ajaxSend:

```html
<meta name="_csrf" content="${_csrf.token}"/>
<meta name="_csrf_header" content="${_csrf.headerName}"/>
```

```javascript
var token = $("meta[name='_csrf']").attr("content");
var header = $("meta[name='_csrf_header']").attr("content");
$(document).ajaxSend(function(e, xhr, options) {
    xhr.setRequestHeader(header, token);
});
```

CookieCsrfTokenRepository.withHttpOnlyFalse() is the SPA variant so JavaScript can read the cookie.
> [!warning] Unverified traps from the dump
> - HttpOnly cookies cannot be read by JS; withHttpOnlyFalse is required for a cookie-based SPA token.
> - GET must stay side-effect free; CSRF tokens protect POST/PUT/PATCH/DELETE.
