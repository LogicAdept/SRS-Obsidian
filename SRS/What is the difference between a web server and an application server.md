<!--
reps: 0
priority: 0
-->
#Networking/Web #Java/JavaEE #SRS

# What is the difference between a web server and an application server

> [!abstract] Short answer
> **The terms describe different dimensions: a web server is defined by *what protocol it speaks* — HTTP delivery of content — while an application server is defined by *what it executes* — application code with runtime services.** One product can be both (Tomcat), one role can exist without the other (a static Apache httpd is a web server but not an application server), and an executing system without HTTP (a database with heavy stored procedures) can be an application server without being a web server.

## Two questions, not two product boxes

Ask two separate questions of any server: "Does it accept and answer HTTP?" — that makes it a web server. "Does it run programs that process requests and produce results?" — with component lifecycle and runtime services, that makes it an application server. The answers combine independently.

```d2
direction: right
q1: "Serves over HTTP?\n(web server role)" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
q2: "Executes application code?\n(application server role)" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
t: "Tomcat\nboth: HTTP + servlet runtime" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
a: "Apache httpd, static files\nweb server only" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}
db: "DB heavy on stored procedures\napplication execution, no HTTP" {
  width: 330
  height: 100
  style.fill: "#fff3e0"
}
q1 -> t
q2 -> t
q1 -> a
q2 -> db
```

**Fig. 1.** The two roles intersect: Tomcat checks both boxes; static Apache checks one; a logic-heavy database checks the other.

Worked examples (the classic set): **Tomcat** executes applications (servlets) *and* answers HTTP — both roles. **Apache httpd with no language modules** serves files and images over HTTP — a web server only. **Enable PHP/CGI in httpd** and it starts executing programs — it gains the application-server role for that workload. **A relational database** running complex stored procedures that even send SMS answers application logic but not over HTTP — application execution without the web-server role. The full Java EE lineage of application servers adds the platform services layer — pooled DataSources, JTA transactions, JMS — described in [[What is an application server]].

> [!warning] The question is a trap about categories, not vocabulary
> The failing answer treats them as tiers of the same axis ("app server = bigger web server") and then defends it. The boundary is: *protocol/delivery role* versus *execution/runtime role*. Three follow-up traps. First, "Tomcat is not an application server" — true only for the full-EE definition of the role; Tomcat genuinely executes web applications, so the correct nuance is "servlet container: the web-component subset of application serving". Second, reverse proxies confuse people: Nginx in front of Tomcat is doing the web-server role (and often the *only* HTTP-facing role), while Tomcat behind it does the executing — the deployment shape shows the two roles split across processes. Third, the modern twist: Spring Boot's embedded Tomcat blurs the line again — the "application" and the "server" ship as one artifact; comparing "app server versus web server" as infrastructure choices is 2009 vocabulary. For the services a full application server contributes beyond HTTP: [[What is an application server]]; for how HTTP itself reports delivery-versus-rights outcomes: [[What is the difference between HTTP 401 and 403]].

> [!tip] Interview answer
> **They are different dimensions, not two tiers. Web server = a server that delivers over HTTP — static files, proxies. Application server = a server that executes your application with runtime services. Tomcat is both — an HTTP servlet container; static Apache httpd is only a web server; a database with heavy stored procedures executes application logic without HTTP at all. Modern Spring Boot embeds the executing side, so the two roles often live in one process now.**

