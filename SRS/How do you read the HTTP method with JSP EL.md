<!--
reps: 0
priority: 0
-->
#Java/JSP/EL #Java/Servlet #Networking/Web/Protocols/HTTP #SRS

# How do you read the HTTP method with JSP EL?

> [!abstract] Short answer
> **`${pageContext.request.method}`.** EL’s implicits do **not** include `request`. `pageContext` is the `PageContext`; `.request` is `getRequest()`; `.method` is `HttpServletRequest.getMethod()` (for example `GET`, `POST`, `PUT`). `${request.method}` is **not** the scripting variable `request`. Scopes: [[What are the implicit EL scope objects in JSP and how do they differ from servlet scoped objects]]. EL off: [[How do you disable Expression Language in JSP]].

## `pageContext`, then the servlet request

Jakarta Pages **4.0** §2.4 lists EL names that are **always** available. The servlet request is reached as **`${pageContext.request}`**. The spec’s own example is **`${pageContext.request.requestURI}`** (from `HttpServletRequest`). **`method`** is the same JavaBeans path: `BeanELResolver` maps `.method` to **`getMethod()`**.

`getMethod()` returns the HTTP method **with which this request was made**. It is **not** an HTTP header; `${header…}` will not give you GET vs POST.

Scriptlets still have the §1.8.3 implicit **`request`**: `<%= request.getMethod() %>`. EL does **not**. A bare `${request}` is `findAttribute("request")` (page → request → session → application), then `.method` on whatever object that was — or **`null`**.

On an **error page**, the container **must** dispatch the error as **HTTP GET**. The **original** method is the request attribute `RequestDispatcher.ERROR_METHOD` (`jakarta.servlet.error.method`). JSP **4.0** `ErrorData.getMethod()` exposes that; EL: **`${pageContext.errorData.method}`** (only meaningful with `isErrorPage="true"`). Status via the same object: [[How do you handle errors on JSP pages]]. What EL is: [[What do you know about the JSP Expression Language]].

```d2
direction: down
el: "${pageContext.request.method}" {
  width: 300
  height: 40
  style.fill: "#fff8e1"
}
pc: "PageContext.getRequest()" {
  width: 280
  height: 36
  style.fill: "#e8f5e9"
}
m: "HttpServletRequest.getMethod()" {
  width: 300
  height: 36
  style.fill: "#e3f2fd"
}
el -> pc -> m
```

**Fig. 1.** One property chain: implicit `pageContext` → servlet request → HTTP method name.

```jsp
<%-- Conceptual — Jakarta Pages 4.0 --%>
<p>${pageContext.request.method}</p>
<%-- ${request.method} is not the scripting implicit request --%>
```

**Listing 1.** Normal page: the client method as a `String`.

```jsp
<%-- Conceptual — error page, JSP 4.0 ErrorData --%>
<%@ page isErrorPage="true" %>
<p>dispatched ${pageContext.request.method}</p>
<p>original ${pageContext.errorData.method}</p>
```

**Listing 2.** After an error dispatch, `.request.method` is **GET**. Use **`errorData.method`** for the method that failed.

> [!warning] `${request.method}` is not `request.getMethod()`
> EL has no `request` implicit. That name is a **scoped attribute** lookup. If EL is ignored (`isELIgnored`), the characters `${pageContext.request.method}` print as template text. `${header.method}` is a **header** named `method`, not the request line.

> [!warning] Error pages lie about the method on `request`
> Servlet **6.1** error dispatches are **GET**. A failed **POST** still shows **GET** on `${pageContext.request.method}`. Read **`${pageContext.errorData.method}`** on `isErrorPage="true"` (JSP **4.0**).

> [!tip] Interview answer
> I use `${pageContext.request.method}` because EL exposes PageContext, not the scriptlet request object. That calls HttpServletRequest.getMethod. I do not write ${request.method}. On an error page I use pageContext.errorData.method, because the container re-dispatches errors as GET.
