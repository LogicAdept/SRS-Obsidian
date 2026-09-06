<!--
reps: 0
priority: 0
-->
#Java/Servlet/Container #Java/JavaEE #SRS

# Why use Java EE application servers when servlet containers exist?

> [!abstract] Short answer
> Use a **Jakarta EE application server** when the app needs **platform services the Servlet spec does not require**: **JNDI environment**, **container transactions**, **persistence**, **CDI**, and on the **full Platform** **JMS**, **Mail**, **Connectors**, **Batch**, **XA**. A **servlet container** is the **web/HTTP engine** only. Servlet **6.1 §1.1**: it **can be standalone** or **built into** an application server. The server **does not replace** the servlet container — it **contains** it and adds **other containers** (EJB, application client) plus **injected** tx, security, and **resource pooling** (Platform **§2.4**). Engine duties: [[What typical responsibilities does a servlet container have]]. Identity: [[What is a servlet container]]. What a servlet is: [[What is a servlet]].

## When the servlet engine is enough — and when it is not

**Servlet container:** decode HTTP, map URLs, run **filters / `service`**, sessions. **§15.2.2** EE naming (`resource-ref`, `ejb-ref`, …) is **required** only if the engine is part of a **Jakarta EE product**; standalone engines are **encouraged**, not obliged.

**Web Profile** (Web Profile **§1.1**): most web apps also need **transactions, security, persistence**. Those APIs are **rarely** on a **plain** servlet container. Web Profile adds Pages, Faces, **EJB Lite**, **JTA**, **JPA**, CDI, Validation, Security, REST, … **Jakarta Messaging is not required** (**§1.2**).

**Platform product:** Web Profile **plus** Messaging (default factory), Mail, Connectors, Batch, full EJB, **two-phase commit** across JDBC/JMS. Platform **§2.2**: Servlet + JTA together is a **programming model** neither spec defines **alone**.

| You are building | Typical product |
| --- | --- |
| WAR, HTTP, filters, maybe JSP | Servlet container |
| WAR + JPA + JTA + CDI, no JMS | **Web Profile** server |
| EAR, MDB, JMS, mail, EIS adapters, XA | **Platform** application server |

```d2
direction: down
need: "need JTA / JPA / JMS / JNDI?" {
  width: 280
  height: 40
}
sc: "servlet container" {
  width: 200
  height: 36
  style.fill: "#e3f2fd"
}
ee: "Jakarta EE product" {
  width: 200
  height: 36
  style.fill: "#e8f5e9"
}
need -> sc: "no"
need -> ee: "yes"
```

**Fig. 1.** Choose the **contract**, not the brand. An EE server still **hosts** servlets.

```java
// Conceptual — portable only on a Jakarta EE web/platform product
@Resource(lookup = "java:comp/env/jdbc/app")
DataSource ds;

@Resource
UserTransaction utx;
```

**Listing 1.** **`@Resource` / `UserTransaction`** are why you pick an **application server**. A **plain** servlet engine **may warn** and skip the EE environment (**Servlet §15.2.2 / §10.11**).

> [!warning] Tomcat-style pools are not the Platform
> A servlet engine **may** ship a **vendor DataSource**. That is **not** portable **JTA/XA**, **not** **JMS**, and **not** a **Jakarta EE** TCK product. **Web Profile ≠ full Platform**: **JMS out of the box** is **Platform**.

> [!warning] Clustering consoles are vendor, not Java EE
> **AdminServer**, **SAML/XACML**, **live queue migration**, and **datacenter session copy** are **products**. The Servlet spec **does not** call standalone clustering “primitive.” Distributed containers **need not** propagate session events.

> [!tip] Interview answer
> A servlet container is the HTTP runtime. I use a Jakarta EE application server when I need the platform to inject transactions, naming, persistence, and on the full platform messaging and connectors. The application server includes a servlet container; I am paying for the extra containers and the combined programming model.
