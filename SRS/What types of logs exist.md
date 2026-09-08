<!--
reps: 0
priority: 0
-->
#Java/Logging #SRS

# What types of logs exist?

> [!abstract] Short answer
> By **content and audience**, operational logging is conventionally split into three types: **system logs** — what the platform did (service start/stop, inter-module calls, connection pools, GC and JVM events); **security (audit) logs** — who did what to what, with which result (login, password check, permission denied, record access); and **application (business) logs** — what the business domain did (order accepted, payment processed, invoice exported). The classic interview example walks one user action across all three: a user logs in and their password is verified — a **security** event; they start a module — an **application** event; that module calls another module for data — a **system** event. The distinction matters because the types have **different consumers, retention and access rules**: system logs feed SRE dashboards, security logs feed auditors and often must be tamper-resistant and long-lived, business logs feed product analytics — and mixing them into one stream pollutes all three. Mechanically the types are not separate frameworks: they are **logger subtrees and appenders** (see [[What are the components of the log4j logging system]]), separated by naming, destination and level policy.

## System logs: the platform's diary

System logs record the machine's view of the application: startup and shutdown with versions and configuration, infrastructure calls between modules, pool and connection lifecycle, scheduling, and — at the JVM boundary — the runtime's own events (GC pauses, class loading, unified JVM logging via `-Xlog`). Their primary consumers are engineers and SRE tooling: they answer "is the platform healthy", "why was module X restarted", "which downstream service timed out first". Levels lean INFO/DEBUG for routine operation with WARN for degradations (retry storms, pool exhaustion). Volume is high and churn is constant, so system logs pair with rotation policies and short retention. A useful interview detail: framework and server internals — Tomcat, Spring, Hibernate — write *their* system logs into named loggers (`org.apache.*`, `org.hibernate.*`), so the same name hierarchy that organizes your application also separates platform noise from business signal: raise the root to WARN, leave `com.myapp` at INFO, and the platform quiets down without hiding your code. See [[What are log4j logging levels in order of increasing severity]] for the gate semantics.

## Security logs: who did what, and can you prove it

Security (audit) logs record identity, action, target and result: successful and failed logins, password/permission checks, role grants, access to sensitive records, configuration changes. Their consumers are not developers but auditors and security teams, and their lifecycle is different by law and contract — long retention, restricted read access, sometimes append-only or externally shipped storage so an attacker (or an insider) cannot silently edit them. The engineering consequences are concrete: a login attempt is *not* an INFO line among others — it belongs to a dedicated logger subtree (`audit` or `security`), routed to its **own appender** (separate file or shipping pipeline), with structured fields (actor, action, target, source ip, outcome) rather than free text, and with careful scrubbing — passwords, tokens and card numbers must never reach any log, security logs included. This is also the type where "log everything" is the wrong instinct: an audit trail of *meaningful* security-relevant decisions beats a firehose nobody can query. The type taxonomy earns its keep here — no one would ever mix this stream with the TRACE firehose from [[What is a log4j Logger]].

## Application logs: the business domain's narration

Application (business) logs narrate what the domain did: order accepted, payment declined with reason, invoice generated, shipment dispatched. Their consumers are product and support teams; their questions are "what happened to customer X's order" and "when did this feature misbehave" — which is why these lines carry **business identifiers** (order id, customer id, tenant) and why thread-context correlation (a request id stamped into `%X{requestId}`) is applied to exactly this stream most visibly. The taxonomy's practical payoff is routing: business events can go to their own appender with their own structure (JSON for product analytics), while system internals stay in the operations stream — and when the types are tangled, support asks engineering to grep code-level stack traces to find out whether an order shipped. The three types in one sentence each — *platform events, accountable actions, business actions* — is the shape the interviewer wants; the senior part is the *consequences*: different appenders, different retention, different access control, all achieved with logger subtrees plus configuration rather than separate frameworks. Wiring details: [[What configuration approaches exist for log4j]] and [[What is a log4j Appender]].

```java
public class LoginService {
    // Type separation lives in logger names -> config routes them apart.
    private static final Logger audit =
            LogManager.getLogger("audit.security");      // SECURITY type
    private static final Logger business =
            LogManager.getLogger("com.myapp.orders");    // APPLICATION type
    private static final Logger system =
            LogManager.getLogger("com.myapp.system");    // SYSTEM type

    public Session login(String user, String password) {
        system.debug("login attempt, module=auth, node=n3");   // platform diary
        boolean ok = credentials.check(user, password);
        audit.info("LOGIN user={} outcome={} ip={}",
                   user, ok ? "granted" : "denied", request.ip());
        // Security log: structured actor/action/outcome. NEVER the
        // password itself - scrubbing is part of the contract.
        if (ok) business.info("session opened, user={}", user);
        return ok ? Session.start(user) : null;
    }
}

// log4j2.xml routes the types to different destinations:
// <Logger name="audit.security" level="INFO" additivity="false">
//     <AppenderRef ref="auditFile"/>      <!-- separate, access-restricted -->
// </Logger>
// <Root level="INFO"><AppenderRef ref="console"/></Root>
```

**Listing 1.** One user action, three log types: logger subtrees per type, an audit line with structured actor/outcome fields, and configuration routing audit output to its own appender.

```d2
direction: right
user: "user action\nlogin -> open module" {style.fill: "#e3f2fd"}
sec: "SECURITY / audit\nwho, what, outcome\nrestricted access,\nlong retention" {style.fill: "#ffebee"}
app: "APPLICATION / business\norder accepted, payment done\nproduct & support" {style.fill: "#e8f5e9"}
sys: "SYSTEM / platform\nstart/stop, calls, pools\nSRE dashboards" {style.fill: "#fff8e1"}
user -> sec: "password verified"
user -> app: "module started"
app -> sys: "module calls module"
```

**Fig. 1.** One user journey crosses all three log types; each has its own consumers, retention and access rules — hence its own logger subtree and appender.

## Vocabulary the interview actually tests

Three distinctions are graded. **Type vs level**: system/security/application is *content taxonomy*; INFO/WARN/ERROR is *severity* — an audit denial may be INFO-severity yet belong to the security stream. **Type vs framework**: the types are not Log4j features or separate libraries — they are naming and routing conventions implemented with logger subtrees and appenders; JVM-internal events (`-Xlog`) are system logs of a different producer but the same taxonomy. **Audit vs debug**: the security stream exists for accountability and must survive independently of the developer-facing stream; folding it into the application log means an incident review depends on whatever happens to still be in the rotated app log. A senior bonus: the example journey — password check = security, module start = application, inter-module call = system — is the expected illustration; producing it unprompted signals the taxonomy is understood, not memorized.

> [!warning] "It's all just logs" — the three types have different legal and operational contracts
> The careless version of this answer treats the taxonomy as trivia and then mixes streams in practice — which is exactly the production failure being tested for. Concrete traps: **secrets in logs** (a password or token printed during a failed login converts your app log into a liability — scrub at the call site, never log what you would not show the user); **wrong retention** (security logs deleted with the 7-day app-log rotation is an audit finding, not a tuning detail); and **PII drift** (business logs that accumulate user emails into unrestricted storage). The operational smell that engineers will be judged on: if an auditor and an SRE read the *same file*, the types are not actually separated — separation is measured in appenders, access control and retention, not in naming conventions.

> [!tip] Interview answer
> **Three content types. System logs — the platform's diary: startup, inter-module calls, pools, JVM events; consumers are engineers and SRE tooling. Security or audit logs — who did what with which outcome: logins, permission checks, record access; they have their own retention and access rules because auditors consume them, and they must never contain secrets. Application or business logs — what the domain did: order accepted, payment processed — with business identifiers for support and product. One login action crosses all three: password check is security, module start is application, the inter-module call is system. Mechanically they're not separate frameworks — they're logger subtrees routed by configuration to separate appenders with separate retention.**
