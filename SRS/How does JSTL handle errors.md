<!--
reps: 0
priority: 0
-->
#Java/JSP/JSTL #SRS

# How does JSTL handle errors?

> [!abstract] Short answer
> **Most JSTL actions do not catch body exceptions; they propagate.** Wrap recoverable work in `<c:catch>`. The optional `var` stores the `Throwable` in **page** scope (removed if nothing was thrown). Without `var`, the throwable is swallowed. This complements JSP `errorPage`, it does not replace it.

## `c:catch` vs letting it reach the error page

By default, Jakarta Tags actions **do not** catch exceptions from their body, from the action itself, from EL, or from XPath. Those failures propagate. When the spec requires an action to throw, the type is `JspException` (or a subclass). If a tag catches a nested failure and rethrows, the original is the **root cause**.

`<c:catch>` catches any `java.lang.Throwable` from nested actions (and other JSP content in its body). It is the page-author analogue of a local `try`/`catch`: secondary work can fail without invoking the JSP error-page mechanism; **central** actions should stay **outside** `c:catch` so they still go to `errorPage` / `web.xml` ([[How do you handle errors on JSP pages]], [[How would you explain JSTL the JSP Standard Tag Library]], [[How is the JSTL tag library organized]]).

`var` is always **page** scope. After a throw, it holds the exception object. If the body completes normally, that name is **removed** if it existed. Omit `var` and the exception is caught and **not** saved — the error page is not invoked, and you have nothing to inspect.

Failed `c:import` (bad URL, include `IOException`, non-2xx) is specified to throw `JspException`. Wrap that import in `c:catch` if the include is optional ([[What is the difference between JSTL import jsp include and the include directive]]).

```d2
direction: down
fail: "tag or body throws" {
  width: 280
  height: 50
}
catch: "c:catch (optional var)" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
page: "JSP errorPage / web.xml" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
fail -> catch
fail -> page
```

**Fig. 1.** `c:catch` is local recovery. Unwrapped throwables still use the JSP error page.

```jsp
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<c:catch var="ex">
  <c:import url="optional-fragment.jsp"/>
</c:catch>
<c:if test="${ex != null}">
  ${ex.message}
</c:if>
```

**Listing 1.** Optional import: failure stays on the page. Drop `var` and the same failure is silent. A critical import should not sit inside `c:catch`.

> [!warning] No `var` means swallow
> The throwable never reaches `errorPage`, and you cannot read a message. That is easy to confuse with “nothing went wrong.”

> [!warning] Do not wrap the whole page
> The spec’s intent is granular handling: wrap secondary actions only. Putting every tag in `c:catch` hides failures that should hit the error page.

> [!tip] Interview answer
> **JSTL does not automatically catch errors; they propagate like any JSP throwable.** Use `<c:catch var="ex">` for work you can recover from; `ex` is page-scoped and cleared if nothing was thrown. Leave important actions unwrapped so JSP `errorPage` still runs.
