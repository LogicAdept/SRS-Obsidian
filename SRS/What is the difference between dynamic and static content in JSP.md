<!--
reps: 0
priority: 0
-->
#Java/JSP #SRS

# What is the difference between dynamic and static content in JSP?

> [!abstract] Short answer
> **Static content is template data: text the translator does not interpret and later writes to `out`.** **Dynamic content is what the container evaluates per request** — EL, standard/custom actions, and scripting — and **inserts into that template**. Jakarta Pages **4.0** calls this **separation of static template from dynamic inserts** (beans and tag libraries). Includes use the same words for a **different** split: [[What is the difference between JSTL import jsp include and the include directive]]. What a page is: [[What is Java Server Pages JSP]].

## Template data vs elements

A JSP page is **elements** plus **template data**. An **element** has a type the container knows (directive, action, scripting). **Template data is everything else** — HTML, XML fragments, CSS, client script, even `<!-- … -->`. At translation, template becomes code that **`out.print`s** those characters (whitespace kept). That is **static** in the spec’s sense: the **markup is fixed in the page**; it is not “computed,” even though it still **runs on every request**. Why the template exists: [[Why do you need JSP]]. `out`: [[What is the difference between JspWriter and servlet PrintWriter]].

**Dynamic elements** (spec §6.2.3) are **EL expressions**, **scripting**, **standard actions**, and **custom actions**. They run in **`_jspService`** (except directives, which are **translation-only** and are **not** listed as dynamic elements). EL may sit **inside** template text; those `${…}` pieces are still **dynamic** and become **`String`s** when the response is rendered: [[What do you know about the JSP Expression Language]]. Actions (`jsp:include`, `c:out`, your tags) compute or dispatch using **this request**.

**Authoring split.** Page authors compose **static markup + holes**; developers supply beans and tag libraries that fill the holes. That is the benefit the spec names **separation of dynamic and static content**.

**Same words, different mechanism (includes).** `<%@ include file %>` treats the resource as a **static object**: its **source text** is parsed into this translation unit. `<jsp:include page>` treats it as a **dynamic object**: the **request is sent** there and its **output** is included. Table JSP.1-10. Do not mix that table with “HTML vs EL.”

```d2
direction: down
src: "JSP source" {
  width: 220
  height: 36
  style.fill: "#fff8e1"
}
stat: "template data\nHTML / XML / text\n→ out.print (fixed chars)" {
  width: 280
  height: 56
  style.fill: "#e8f5e9"
}
dyn: "dynamic elements\nEL · actions · scripting\n→ computed this request" {
  width: 280
  height: 56
  style.fill: "#e3f2fd"
}
src -> stat
src -> dyn
```

**Fig. 1.** Static = **uninterpreted template**. Dynamic = **evaluated inserts**. Both become the response stream.

```jsp
<%-- Conceptual — static template with dynamic inserts --%>
<!DOCTYPE html>
<html>
  <h1>Catalog</h1>
  <p>Welcome, <c:out value="${requestScope.user.name}"/></p>
</html>
```

**Listing 1.** `<!DOCTYPE>`, `<html>`, `<h1>Catalog</h1>` are **static**. `${…}` and `<c:out>` are **dynamic**. Comments: [[How do you comment code in JSP]].

```jsp
<%-- Conceptual — two different “static/dynamic” meanings --%>
<%@ include file="/WEB-INF/fragments/header.jspf" %>
<jsp:include page="/WEB-INF/fragments/nav.jsp"/>
```

**Listing 2.** Directive: **static object** (text merged at translation). Action: **dynamic object** (execute now). Not the same as Listing 1.

> [!warning] HTML comments do not freeze JSP; EL in template is not static
> `<!-- … -->` is **template text**, so **actions, scriptlets, and EL inside it still run**. Only `<%-- --%>` is ignored. `${user}` in the middle of HTML is **dynamic**, even with no tag around it. `tagdependent` bodies skip EL. A `.html` fragment pulled in with **`jsp:include`** is **not parsed as JSP**; the same file pulled with **`<%@ include %>`** is.

> [!tip] Interview answer
> In JSP, static content is template data the translator does not understand and later writes to out, typically HTML. Dynamic content is EL, actions, and scripting that the container evaluates for this request and inserts into that template. I keep markup in the page and data in beans or tags. I do not confuse that with the include directive versus jsp:include, which is static source versus a request-time dispatch.
