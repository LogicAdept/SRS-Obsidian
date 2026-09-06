<!--
reps: 0
priority: 0
-->
#Java/JSP/JSTL #SRS

# How is the JSTL tag library organized?

> [!abstract] Short answer
> **As five separate tag libraries, not one TLD.** Jakarta Tags **3.0** (JSTL) is “the” standard library in name only: **core**, **XML**, **fmt** (i18n/formatting), **SQL**, and **functions**, each with its own URI and namespace. Import the ones you use with `<%@ taglib %>`. Spec prefixes are **`c`**, **`x`**, **`fmt`**, **`sql`**, **`fn`** — authors may pick others. Extension mechanism: [[How can you extend JSP functionality]]. What JSTL is: [[How would you explain JSTL the JSP Standard Tag Library]]. Not `jsp:` actions: [[Why are built in JSP tags not configured in web.xml]].

## One product, five namespaces

The spec groups actions by **functional area** so each area has a **URI**. You cannot pull in “all of JSTL” with a single `taglib`.

| Area | URI | Usual prefix | Role |
| --- | --- | --- | --- |
| Core | `jakarta.tags.core` | `c` | `out` / `set` / `remove` / `catch`; `if` / `choose`; `forEach` / `forTokens`; URL `import` / `url` / `redirect` |
| XML | `jakarta.tags.xml` | `x` | Parse, XPath flow, transform |
| I18n / format | `jakarta.tags.fmt` | `fmt` | Locales, bundles, numbers, dates, time zone, request encoding |
| SQL | `jakarta.tags.sql` | `sql` | Query / update / transaction / `setDataSource` |
| Functions | `jakarta.tags.functions` | `fn` | **EL functions** (`${fn:length(…)}`), not custom **actions** |

**Core** is several chapters (general-purpose, conditionals, iterators, URLs) under **one** URI. **fmt** is i18n plus formatting under **one** URI. **fn** is the EL extension set (length, substring, trim, `escapeXml`, …). Errors in core: [[How does JSTL handle errors]].

Jakarta Tags **3.0** renamed the URIs to `jakarta.tags.*` (Java EE JSTL used Sun-hosted `jsp/jstl` paths). Declare the URI the TLD actually advertises. Container: Tags **3.0** requires Pages **3.0** / EL **4.0** as a baseline; a Pages **4.0** app still imports these libraries the same way. `web.xml` `taglib` maps are optional URI→TLD shortcuts: [[How is JSP configured in the web deployment descriptor]].

```d2
direction: down
jstl: "Jakarta Tags (JSTL)" {
  width: 240
  height: 36
  style.fill: "#fff8e1"
}
c: "jakarta.tags.core\nc"
fmt: "jakarta.tags.fmt\nfmt"
x: "jakarta.tags.xml\nx"
sql: "jakarta.tags.sql\nsql"
fn: "jakarta.tags.functions\nfn (EL)"
jstl -> c
jstl -> fmt
jstl -> x
jstl -> sql
jstl -> fn
```

**Fig. 1.** Singular “JSTL”, five `taglib` URIs.

```jsp
<%-- Conceptual — Jakarta Tags 3.0 --%>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<%@ taglib prefix="fmt" uri="jakarta.tags.fmt" %>
<%@ taglib prefix="fn" uri="jakarta.tags.functions" %>
<p><c:out value="${fn:toUpperCase(name)}"/></p>
<p><fmt:formatNumber value="${price}" type="currency"/></p>
```

**Listing 1.** Three libraries, three directives. `fn:toUpperCase` is an **EL function**; `c:out` and `fmt:formatNumber` are **actions**.

> [!warning] `c:` is not the whole of JSTL
> `<fmt:formatDate>` under a core prefix is a **translation error** (unknown action for that TLD). `fn` has **no** tags: `<fn:length>` does not exist; write `${fn:length(items)}`. Prefixes are **not** reserved — only the **URI** selects the library.

> [!warning] SQL and XML are optional libraries, not “core”
> They ship as JSTL, but each needs its **own** `taglib`. A page that only declared core cannot use `<sql:query>` or `<x:parse>`. Validators (`PermittedTaglibsTLV`) can **forbid** libraries you did not list.

> [!tip] Interview answer
> JSTL is five tag libraries: core, fmt, xml, sql, and functions, each with its own jakarta.tags URI. I import only what the page needs, usually with prefixes c, fmt, x, sql, and fn. Functions are EL, not tags, and core does not include formatting or SQL.
