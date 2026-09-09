<!--
reps: 0
priority: 0
-->
#Java/JavaEE #SRS

# What is an application server

> [!abstract] Short answer
> **An application server is a runtime platform that hosts and manages your application: it owns the process, HTTP endpoints, component lifecycle, and (in full Java EE/Jakarta EE form) services like transactions, pooled DataSources, naming (JNDI), and security integration.** In the Java world it spans from a servlet container (Tomcat — HTTP + servlets only) to a full Jakarta EE server (WildFly, Payara) providing the whole platform.

## What "hosting an application" concretely means

An application server sits between the OS and your code. You hand it a deployment artifact (WAR, EAR); it loads your classes, wires your components into its lifecycle, routes HTTP to them, and offers platform services so your code does not hand-roll them: connection pools behind a `DataSource`, JTA transactions, managed schedulers, JMS endpoints, security realms.

```d2
direction: right
os: "OS process\nJVM + server distribution" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
svc: "Platform services\npooled DataSource, JTA, JMS,\nsecurity realms, JNDI" {
  width: 320
  height: 110
  style.fill: "#fff3e0"
}
http: "HTTP endpoint / listener\nroutes to your components" {
  width: 310
  height: 100
  style.fill: "#fff3e0"
}
app: "Your application\nservlets, EJBs, WAR/EAR" {
  width: 250
  height: 90
  style.fill: "#e8f5e9"
}
os -> svc
os -> http
http -> app
svc -> app
```

**Fig. 1.** The server process supplies the plumbing — HTTP routing and platform services — around the deployed application.

The spectrum matters more than the label. A **servlet container** (Tomcat, Jetty) handles HTTP + the servlet/JSP layer only — Tomcat's own documentation calls it a "servlet container"; it is what Spring Boot embeds today. A **full Jakarta EE application server** (WildFly, Payara, WebSphere/Liberty) additionally implements the whole platform spec set: EJB, JTA, JMS, JPA providers, CDI containers, connector architecture. The historical heavyweight model — deploy to a shared app server, look up resources in JNDI — inverted over the last decade into the embedded model: Spring Boot packages the server inside your jar; microservices run one server per app instead of many apps per server.

> [!warning] "Application server" is a role, not a product certificate — and the market moved
> Interview traps. First, treating the category as binary: whether something "is an application server" depends on which services it actually provides — Tomcat executes web components but ships no JTA/JMS/JPA platform; calling it "not an app server" or "a full EE server" are both wrong (the web-server-versus-application-server boundary is unpacked in [[What is the difference between a web server and an application server]]). Second, answering with the 2010 vocabulary: "you deploy your WAR into a shared app server" describes a shrinking deployment style — modern Spring Boot flips the model (the app carries an embedded servlet container, `java -jar` runs it), and the embedded-versus-standalone trade-off (shared platform services vs self-contained deployments) is the current interview question. Third, the health angle: an application server is also an *operational* component — thread pools, monitoring, graceful restarts, hot redeploy; skipping that dimension makes the answer sound purely academic. The security side of the runtime (authn/authz integration) is covered by [[What is authorization and authentication how they differ]] and [[How do you configure HTTP Basic authentication in Spring Security]].

> [!tip] Interview answer
> **An application server is the platform your application runs inside: it owns the JVM process and HTTP listeners and offers services — pooled DataSources, transactions, messaging, security — so apps don't build them. The Java spectrum runs from servlet containers like Tomcat or Jetty through full Jakarta EE servers like WildFly. Modern practice inverts deployment: Spring Boot embeds the container in your jar instead of deploying into a shared one.**

