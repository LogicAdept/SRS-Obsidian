<!--
reps: 0
priority: 0
-->
#Java/Logging #Java/Library/Log4j #SRS

# What are log4j logging levels in order of increasing severity?

> [!abstract] Short answer
> From most specific to most severe, the standard Log4j 2 levels are **TRACE → DEBUG → INFO → WARN → ERROR → FATAL**, bracketed by two extremes: **ALL** (every event passes) and **OFF** (nothing passes). The `org.apache.logging.log4j.Level` javadoc names them and their intent: OFF — "no events will be logged"; FATAL — "a fatal event that will prevent the application from continuing"; ERROR — "an error in the application, possibly recoverable"; WARN — "an event that might possible lead to an error"; INFO — "an event for informational purposes"; DEBUG — "a general debugging event"; TRACE — "a fine-grained debug message, typically capturing the flow through the application". A logger's effective level is the gate: events at the configured level **and more severe** pass, everything less severe is dropped before message formatting even runs. Log4j 1.x used the same severity ladder (its javadoc: "ALL has the lowest possible rank and is intended to turn on all logging") and Log4j 2 additionally supports **custom levels** via `Level.forName`. Semantic neighbors: [[What is a log4j Logger]] (who holds the gate), [[What are the components of the log4j logging system]].

## The ladder and its semantics

Severity order is what makes one configuration line operational: set `com.myapp.db` to WARN and you keep errors and warnings while discarding hundreds of DEBUG lines; set `root` to INFO for a normal fleet and raise a single package to DEBUG for a live investigation. The javadoc's table is worth internalizing as *semantics*, not just names — FATAL is reserved for events that stop the application (the next line after it is a crash), ERROR means a failed operation the application survives (a rejected request, a failed payment call), WARN means something suspicious that has not yet broken anything (retry about to happen, pool near exhaustion, deprecated API use), INFO is business-level narration (service started, order accepted), DEBUG is developer-facing detail (parameters, intermediate states), TRACE is "follow the execution flow" instrumentation. Choosing the level is a *contract with the person who will read the log at 3 a.m.* — the interviewer wants to hear that FATAL is rare and meaningful, not a synonym for ERROR.

## Increasing severity, and why the direction matters

The phrase "in order of increasing severity" defines both the list and the filtering rule. As severity increases, **volume decreases and importance increases** — TRACE floods, FATAL is a page-the-once-a-quarter event. The filtering rule reads in the same direction: with the effective level at INFO, an INFO event and every *more* severe event (WARN, ERROR, FATAL) pass, while DEBUG and TRACE — *less* severe — are rejected. The Log4j 2 configuration documentation phrases it from the other side: events "less severe than" the configured level are excluded from the output. Level resolution then inherits down the logger name hierarchy — the nearest configured ancestor wins, with `root` as the tree-wide default — so severity policy is itself hierarchical: strict at the root, surgical per package. Log4j 2 also allows **custom levels** between or beyond the standard ones (`Level.forName("PERF", 350)`), which is useful for domain-specific tiers like "performance trace"; the standard seven remain the interview vocabulary. For the framework-level picture see [[What is a log4j Appender]] (what a passing event reaches next) and [[What types of logs exist]] (what content deserves which tier).

## Levels are not the whole severity story

Three nuances separate a rehearsed list from understanding. First, **the level check is per logger, at call time** — the same `logger.info()` call site can pass in one environment and drop in another, which is precisely why parameterized logging matters (a rejected event costs no formatting). Second, **levels interact with appenders, not only loggers**: an event that passes the logger's gate may still be filtered per destination by an appender's own filter — shipping JSON ERROR-only while the console shows INFO — so "level" is not one knob but a chain of gates. Third, **OFF and ALL are operational tools, not severity values**: OFF on a package is how you silence a hopelessly chatty third-party logger; ALL (rarely used in production, except when a vendor asks for a full-trace capture) opens everything. The extreme levels bracket the ladder; they do not slot between TRACE and DEBUG.

```java
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class PaymentService {
    private static final Logger log = LogManager.getLogger(PaymentService.class);

    public Receipt pay(Order o) {
        log.trace("pay() entered, order={}", o.id());        // flow instrumentation
        log.debug("retrying gateway call, attempt {}", n);   // developer detail
        log.info("payment accepted, order={}, amount={}", o.id(), o.total());
        log.warn("gateway latency {} ms exceeds budget", ms); // suspicious, not broken
        try {
            return gateway.charge(o);
        } catch (GatewayDownException e) {
            // operation failed, application survives
            log.error("charge failed for order {}", o.id(), e);
            throw new PaymentUnavailable(e);
        }
        // log.fatal(...) - only where the application cannot continue,
        // e.g. startup: "config store unreachable, terminating".
    }
}

// log4j2.xml gates the ladder per subtree:
// <Root level="INFO"/>                          TRACE/DEBUG dropped
// <Logger name="com.myapp.payment" level="DEBUG"/>  DEBUG+ for payments only
// <Logger name="com.myapp.chattyvendor" level="OFF"/>  silence entirely
```

**Listing 1.** The seven standard tiers as usage contracts, and the three configuration verbs — raise a subtree, keep the root strict, OFF a nuisance.

```d2
direction: right
trace: "TRACE\nflow detail" {style.fill: "#e3f2fd"}
debug: "DEBUG\ndeveloper detail" {style.fill: "#e3f2fd"}
info: "INFO\nbusiness narration" {style.fill: "#e8f5e9"}
warn: "WARN\nmight become an error" {style.fill: "#fff8e1"}
error: "ERROR\noperation failed,\napp survives" {style.fill: "#ffebee"}
fatal: "FATAL\napp cannot continue" {style.fill: "#b71c1c"}
trace -> debug -> info -> warn -> error -> fatal: "increasing severity,\ndecreasing volume"
gate: "logger effective level\n(INFO here)" {style.fill: "#fff3e0"}
gate -> info: "passes: info and above"
gate -> debug: "dropped: below" {style.stroke: "#c62828", style.stroke-dash: 4}
```

**Fig. 1.** The severity ladder: the gate admits events at or above the configured level; volume shrinks as severity grows, with ALL and OFF bracketing both ends.

## Vocabulary the interview actually tests

The graded distinctions: **severity vs verbosity** — increasing severity means decreasing volume, and OFF/ALL are the extremes of *filtering*, not extra tiers on the ladder. **Level of the logger vs level of the event** — the event's level is set at the call site; the logger's effective level is configuration; the comparison between them is the gate. **WARN vs ERROR** — WARN is "hasn't broken yet" (retries, budget breaches), ERROR is "an operation failed but the app lives"; FATAL means the process is about to stop. A senior bonus: mention that Log4j 2 supports custom levels via `Level.forName`, and that JUL's names differ (`SEVERE`/`WARNING`/`FINE`…) but the concept is identical — the ladder is a convention shared by every logging framework.

> [!warning] "OFF is the least severe level" — the direction is backwards
> A surprisingly common recital, including in circulated question dumps, is `OFF < TRACE < DEBUG < ... < ALL`. It inverts reality: **OFF silences everything** (the javadoc: "No events will be logged"), and the Log4j 1 javadoc says **ALL "has the lowest possible rank"** — OFF sits at the top of the filtering ladder, ALL at the bottom. Reciting the inverted order to an interviewer who knows Log4j reads as "never actually enabled logging". Two adjacent slips: treating FATAL as a loud ERROR (it means the application cannot continue — if you still expect the process to serve requests afterwards, it was ERROR), and setting `root` to DEBUG in production because "we can always lower it later" — you will drown in volume long before you raise it back.

> [!tip] Interview answer
> **In increasing severity: TRACE, DEBUG, INFO, WARN, ERROR, FATAL — bracketed by ALL, which passes everything, and OFF, which logs nothing; that bracketing is why OFF is not 'the least severe'. The effective level on the logger is the gate: events at or above it pass, less severe ones are dropped before formatting, and levels inherit down the logger-name hierarchy from root. Semantics: TRACE follows flow, DEBUG is developer detail, INFO is business narration, WARN might become an error, ERROR failed an operation the app survives, FATAL means the app cannot continue. Log4j 2 adds custom levels via Level.forName; Log4j 1 used the same ladder with ALL lowest — and it's end of life since 2015.**
