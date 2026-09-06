<!--
reps: 0
priority: 0
-->
#Java/JSP #Java/Servlet #SRS

# Why do you need JSP?

> [!abstract] Short answer
> You need **JSP** when the response is **mostly template** (HTML/XML) with **holes for dynamic data**. Jakarta Pages **4.0**: **textual specification** of a response; **template data** is first-class; **translation** produces a **servlet**. A servlet **`println`s** the same markup as Java strings — easy to break, hard for a **page author** who is not a Java programmer. JSP **does not replace** servlets: it **is** a servlet after translation. What JSP is: [[What is Java Server Pages JSP]]. Servlet base: [[What is a servlet]]. Keep logic out of the page: [[Why should JSP scriptlets be avoided in modern applications]].

## What JSP buys you

Spec **benefits**: **write once / run anywhere**; **author vs developer** roles; **beans and tag libraries**; **static vs dynamic** split; EL / actions; Jakarta EE **front end**.

| Need | Servlet-only | JSP |
| --- | --- | --- |
| Markup | Nested **`out.write` / `println`** | File looks like the **page** |
| Who edits it | Java programmer | **Page author** (HTML/XML; **need not know Java** if they stick to actions/EL) |
| Runtime | You write the servlet | Container **translates** to an **implementation class**, then **same lifecycle** as a servlet |
| When it compiles | Your build | **Precompile**, **deploy**, or **first request** (**§1.1.9**). First hit can **lag**. |

**On-demand translation** is why dumps say **“hot replace the page.”** You still **compile** — just **the container** does it, **per page**, not the whole WAR. The spec **does not** promise **no restart** or that **include** changes are watched.

```d2
direction: down
j: "foo.jsp template + EL" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
t: "JSP translator" {
  width: 160
  height: 36
}
s: "servlet implementation class" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
j -> t
t -> s
```

**Fig. 1.** JSP is **authoring**. The engine still **runs a servlet**.

```java
// Conceptual — servlet view vs JSP
out.println("<h1>" + title + "</h1>");
```

```jsp
<%-- Conceptual --%>
<h1>${title}</h1>
```

**Listing 1.** Same HTML. JSP keeps the **template** in the file; EL fills the hole.

> [!warning] JSP is not “skip the servlet container”
> After translation you have **`HttpJspPage`**, **`_jspService`**, the same **request/response**. **Business rules in scriptlets** fight the **role split** the spec wants. Disable scripting in **`jsp-property-group`** when the page is **view-only**.

> [!warning] “Hot deploy without compile” is oversold
> Replacing **`foo.jsp`** may **retranslate** that page. It is **not** a substitute for **precompile** in production, and **not** guaranteed **without** container policy. **Serious logic** still belongs in **beans / servlets / MVC**, not in the JSP.

> [!tip] Interview answer
> I use JSP so the page can stay HTML with EL and tags instead of a servlet full of printlns. The container turns that file into a servlet, so I still need the servlet engine. I keep the JSP as the view and put business work in Java types the page only reads.
