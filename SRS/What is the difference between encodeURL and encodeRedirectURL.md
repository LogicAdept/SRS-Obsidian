<!--
reps: 0
priority: 0
-->
#Java/Servlet/Sessions #Networking/Web/UrlEncoding #SRS

# What is the difference between encodeURL and encodeRedirectURL?

> [!abstract] Short answer
> Both are **`HttpServletResponse`** methods that may append **`;jsessionid=…`** when the container must **rewrite URLs** because **cookies are not usable**. **`encodeURL`** is for **every URL you emit in the page** (links, form `action`, images). **`encodeRedirectURL`** is **only** for the string you pass to **`sendRedirect`**. They are **separate** because **whether to encode can differ** for a **normal link** vs a **redirect `Location`**. Neither is **`URLEncoder`** (percent-encoding). Rewriting: [[What is URL rewriting for session tracking]]. Sessions: [[How would you explain HTTP sessions in servlet based applications]]. Response API: [[How would you explain the ServletResponse interface]].

## Two encode methods, two call sites

Jakarta Servlet **6.1** `HttpServletResponse`:

| Method | Use with | JavaDoc rule |
| --- | --- | --- |
| **`encodeURL(String)`** | `<a href>`, form action, any **emitted** URL | Run **all URLs the servlet emits** through this, or **cookie-less** clients **drop the session**. |
| **`encodeRedirectURL(String)`** | **`sendRedirect(…)` only** | Run **all redirect targets** through this for the same reason. |

**Same when encoding is skipped:** browser **already has cookies**, or **session tracking is off** → both return the string **unchanged**.

**Why two methods:** the JavaDoc states that **the rules for deciding** to attach the session id **can differ** from those for a **normal link**, so **`encodeRedirectURL` is not `encodeURL`**. Typical difference: a **redirect** may be an **absolute URL on another host**; stuffing **`jsessionid`** there would leak the id and would not come back to **this** container. A **same-app relative href** is the **`encodeURL`** case.

**Spec §7.1.3:** session id in the path as **`jsessionid`** (`…/page;jsessionid=1234`). **URL rewriting** is the **lowest common denominator** when the client **will not accept cookies**. Prefer **cookies** (required) or **SSL session** when they work. Relative URLs to either encode method are **relative to the current `HttpServletRequest`**. Invalid URL → **`IllegalArgumentException`**. **`encodeUrl` / `encodeRedirectUrl`** (lowercase `url`) are the **2.1-deprecated** spellings.

```d2
direction: down
page: "HTML / JSON you write" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
redir: "sendRedirect Location" {
  width: 220
  height: 40
  style.fill: "#fff8e1"
}
enc: "encodeURL" {
  width: 140
  height: 36
  style.fill: "#e8f5e9"
}
encR: "encodeRedirectURL" {
  width: 180
  height: 36
  style.fill: "#e8f5e9"
}
page -> enc
redir -> encR
```

**Fig. 1.** **Call site** chooses the method. Both may no-op if a **cookie** already tracks the session.

```java
// Conceptual — Jakarta Servlet 6.1
String cart = resp.encodeURL(req.getContextPath() + "/cart");
out.println("<a href=\"" + cart + "\">cart</a>");

resp.sendRedirect(resp.encodeRedirectURL(req.getContextPath() + "/next"));
```

**Listing 1.** **`encodeURL`** for markup. **`encodeRedirectURL`** wrapping **`sendRedirect`**. Do not swap them.

> [!warning] This is not `URLEncoder.encode`
> **`java.net.URLEncoder`** percent-encodes **form** data. **`encodeURL`** may insert **`;jsessionid=`**. Putting a session id on a **foreign** redirect host leaks it in **logs, bookmarks, and `Referer`**. Spec: do **not** rely on rewriting when **cookies or SSL sessions** already work.

> [!warning] `sendRedirect(encodeURL(url))` is the wrong helper
> **`encodeRedirectURL`** exists because **redirect rules can differ**. **`encodeURL`** on a **`Location`** may attach **`jsessionid`** when the redirect helper would **not**, or the reverse. If cookies work, **both look like no-ops** in tests — cookie-off is the case that shows the bug.

> [!tip] Interview answer
> encodeURL is for every link I put in the response; encodeRedirectURL is for the URL I pass to sendRedirect. Both add jsessionid only when URL rewriting is needed, usually because the client has no session cookie. They are different methods because the container may apply different rules for a page link versus a redirect Location. I never confuse them with URLEncoder.
