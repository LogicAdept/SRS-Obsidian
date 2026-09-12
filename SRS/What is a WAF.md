<!--
reps: 0
priority: 0
-->
#Security/NetworkSecurity #SRS

# What is a WAF

> [!abstract] Short answer
> A Web Application Firewall (WAF) filters and monitors **HTTP(S) traffic to a web application** at layer 7 - inspecting requests and responses against rules rather than routing packets like a network firewall. It is deployed inline (reverse proxy, cloud service, host module), works from a negative security model (signatures/blocklists) or a positive one (allow-lists), and its strongest practical role is **virtual patching** - shielding a known vulnerability at the HTTP layer until the code is fixed.

## Where it sits and what it inspects

```d2
direction: right
c: "Client" { width: 130; height: 60; style.fill: "#e3f2fd"
w: "WAF\nL7 rules, rate limits, bot filters" { width: 300; height: 90; style.fill: "#fff3e0"
a: "Web application" { width: 200; height: 70; style.fill: "#e8f5e9"
d: "Database" { width: 150; height: 60; style.fill: "#e8f5e9"
c -> w -> a -> d
```

**Fig. 1.** The WAF sees what the application sees - URLs, parameters, headers, bodies - which is exactly why it can block an SQLi payload pattern a packet firewall cannot even parse.

- **Negative model**: signatures of known attacks (OWASP Core Rule Set), IP reputation, rate limits - broad coverage, tunable, bypassable with enough encoding creativity.
- **Positive model**: explicitly allow the requests each endpoint should accept - strong, but it prices like building a schema for the whole app.
- **Deployment**: cloud WAF at the edge, reverse proxy in front of the app, or a module in the web server (ModSecurity lineage).

## Virtual patching - the reason teams keep it

OWASP's virtual patching cheat sheet defines the practice precisely: enforce a policy at a layer **before** the vulnerable code so exploitation is prevented while the proper fix ships. A CVE in a framework endpoint becomes a WAF rule that drops the exploit pattern today - and a tracked ticket that removes the rule when the patched release deploys. PCI DSS leans on the same idea for public web applications: an automated technical solution (a WAF class of control) is one accepted way to meet the web-application-attack requirement ([[What is PCI DSS]]).

> [!warning] "We have a WAF, so we are protected against the OWASP Top 10"
> A signature WAF stops the *loud* versions of a few classes - generic SQLi strings, known exploit paths - and routinely misses business-logic abuse, authenticated flows, and lightly encoded payloads. A WAF that nobody tunes per application blocks legitimate traffic and gets relaxed into irrelevance. It is one layer of [[What is defense in depth]] in front of code that still has to be fixed ([[What is the OWASP Top 10]] is the risk list; the WAF is not the checklist).

> [!tip] Interview answer
> A WAF is an L7 filter in front of the web app - signature or allow-list rules over HTTP semantics, unlike packet firewalls. I value it mainly for virtual patching: drop the exploit pattern at the edge while the real fix is in the pipeline. It is tuning-heavy, bypassable, and never a substitute for fixing the code - it buys time, not safety.
