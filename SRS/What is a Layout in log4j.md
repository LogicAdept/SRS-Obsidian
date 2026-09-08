<!--
reps: 0
priority: 0
-->
#Java/Logging #Java/Library/Log4j #SRS

# What is a Layout in log4j?

> [!abstract] Short answer
> A **Layout** is the component that **formats** a log event before an appender writes it — the third member of the classic Logger / Appender / Layout triad. Log4j 2's manual states the pairing in one sentence: an appender "delivers a `LogEvent` to a target (file, socket, database, etc.) and typically uses a `Layout` to encode log events". Layouts decide whether output is human-readable text or machine-parseable structure: Log4j 2 ships **PatternLayout** (printf-style conversion patterns — the manual's answer for output "suitable for tests and local development"), **JSON Template Layout**, **GelfLayout** ("encodes log events in the GELF specification version 1.1"), CSV and other layouts; Log4j 1.x offered the classic **`SimpleLayout`** (level + message), **`PatternLayout`** with the famous pattern `"%r [%t] %-5p %c - %m%n"` producing lines like `176 [main] INFO org.foo.Bar - Located nearest gas station`, plus **`HTMLLayout`**, **`XMLLayout`** and **`TTCCLayout`** (time, thread, category, context). Because **each appender owns its layout**, the same event is text in the console and JSON in the shipping pipeline. Upstream components: [[What is a log4j Logger]], [[What is a log4j Appender]].

## The job: encoding, not decoration

A layout sits between the event object and the destination's byte stream. The appender has already accepted the `LogEvent` (timestamp, level, logger name, thread, message, thread context); the layout serializes that structure — text via conversion patterns, or structured via JSON/XML/GELF — and hands the bytes back for delivery. This is why layout choice is a *consumer* decision, not an aesthetic one. Humans tailing a console want aligned columns and relative times; a log aggregator (Elastic, Loki, Sentry, a SIEM) wants self-describing structured records so fields like `logger`, `level`, `thread`, `orderId` arrive as fields, not as substrings to be regexed out. The cost of choosing wrong is concrete: a grep-only pipeline over free-text patterns breaks every time someone changes the pattern, while JSON records survive field additions. That is also why Log4j 2's manual positions PatternLayout as the local-development choice and pushes structured layouts for machine consumption.

## PatternLayout: the conversion pattern vocabulary

PatternLayout is the layout you will be asked about. Its conversion patterns are a small vocabulary worth reading fluently: `%d{ISO8601}` or `%d` — timestamp; `%p` (with width `%-5p`) — level, left-aligned to five; `%c{1}` — logger name, last component only; `%t` — thread name; `%m` — message, `%n` — newline; `%X{key}` — a value from the **thread context** (MDC), the standard way to stamp a request id onto every line of a request; `%throwable` — the exception stack trace. The Log4j 1.2 manual's own example is the canonical reading exercise: the pattern `"%r [%t] %-5p %c - %m%n"` yields `176 [main] INFO org.foo.Bar - Located nearest gas station` — 176 ms since startup, the main thread, a left-aligned INFO, the logger's short name, the message. Reading a *given* pattern aloud and predicting its line is a common interview check; so is knowing `%X{requestId}` is how request correlation reaches text logs. Structured layouts remove the parsing problem entirely: JSON Template Layout and GELF (GELF 1.1, the standard for Graylog pipelines) emit events as records with typed fields.

## Layouts across versions, and where they break

The 1.x classics still anchor the vocabulary: `SimpleLayout` prints "level - message"; `HTMLLayout` formats events as table rows for a browser page; `XMLLayout` produced event records for chainsaw-style tools; `TTCCLayout` named the time/thread/category/context fields explicitly; `EnhancedPatternLayout` extended `%c`-style conversions. Log4j 2 kept the roles, replaced the implementations, and added the structured family (PatternLayout, JSON Template Layout, GelfLayout, CSV, Syslog-oriented layouts). Two practical failure notes give the answer depth. First, **stack traces**: a pattern forgetting `%throwable` (or an exception argument not passed as the last parameter) loses the stack — the single most common "why is my log useless" bug. Second, **format drift**: anything downstream that parses text patterns (regex-based ingestion) breaks silently when a developer "just adds a field" to the pattern — the argument for structured layouts in shipped pipelines, text for consoles. Wiring refresher: [[What is a log4j Appender]]; level context: [[What are log4j logging levels in order of increasing severity]].

```java
// log4j2.xml: same event, two layouts, two consumers
<Configuration>
  <Appenders>
    <Console name="console" target="SYSTEM_OUT">
      <!-- human: 2026-09-08 21:14:03,512 [http-nio-8080-exec-3] INFO  OrderService - order 42 accepted -->
      <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c{1} - %X{requestId} %m%n"/>
    </Console>
    <RollingFile name="ship" fileName="logs/app.log" filePattern="logs/app-%d{yyyyMMdd}-%i.log.gz">
      <!-- machine: one JSON object per line, fields preserved -->
      <JsonLayout compact="true" eventEol="true"/>
    </RollingFile>
  </Appenders>
  <Loggers>
    <Root level="INFO">
      <AppenderRef ref="console"/>
      <AppenderRef ref="ship"/>
    </Root>
  </Loggers>
</Configuration>

// In code, the context value the pattern's %X{requestId} prints:
import org.apache.logging.log4j.ThreadContext;
ThreadContext.put("requestId", requestId);   // stamped once per request
try {
    next.handle(req);
} finally {
    ThreadContext.clearAll();                 // thread pools reuse threads
}
```

**Listing 1.** One event, two encodings: a pattern for humans and JSON for machines; `%X{requestId}` carries correlation into the text format via the thread context.

```d2
direction: right
evt: "LogEvent\nlevel, logger, thread,\nmessage, context" {style.fill: "#e3f2fd"}
app: "Appender" {style.fill: "#fff3e0"}
pattern: "PatternLayout\n%d %-5p %c{1} %m%n" {style.fill: "#f3e5f5"}
json: "JsonLayout /\nJSON Template / GELF" {style.fill: "#f3e5f5"}
human: "console\ngrep / tail -f" {style.fill: "#e8f5e9"}
machine: "log aggregator\nfields, dashboards" {style.fill: "#e8f5e9"}
evt -> app
app -> pattern -> human
app -> json -> machine
```

**Fig. 1.** The layout is the encoding step: each appender picks its own — text patterns for human consumers, structured records for aggregators.

## Vocabulary the interview actually tests

Graded pairs: **Layout vs appender** — the layout encodes, the appender delivers; "the layout writes to the file" is a category error. **PatternLayout vs structured layouts** — free text for humans, JSON/GELF/CSV for machines, and each appender owns its own layout so both coexist. **Reading patterns** — `%d`, `%p`, `%c`, `%t`, `%m`, `%n`, and `%X{key}` for the thread context (the request-correlation answer). Version vocabulary: 1.x `SimpleLayout`/`TTCCLayout`/`HTMLLayout`/`XMLLayout` and the `%r [%t] %-5p %c - %m%n` classic; 2.x PatternLayout, JSON Template Layout, GelfLayout. A senior bonus: `%throwable` (or passing the exception as the last argument) is what keeps stack traces in the output — patterns without it silently discard the most diagnostic part of the event.

> [!warning] "The layout is just formatting — change it freely" — downstream disagrees
> Two traps live here. First, text patterns are an API to every regex that consumes your logs: reformatting `%-5p` or adding a field breaks ingestion rules that nobody remembers owning — this is the standing argument for structured layouts in shipping pipelines and text only on consoles. Second, losing stacks: a PatternLayout that omits `%throwable`, or a call like `log.error("failed: " + e)` that embeds the exception into the message instead of passing it as the argument, produces one line where a stack trace should be — the bug is discovered the first time someone needs the stack. Historical footnote worth knowing: 1.x's `EnhancedPatternLayout` and `TTCCLayout` are museum pieces; quoting them as current Log4j 2 components dates the whole answer.

> [!tip] Interview answer
> **A layout is the component that encodes a log event for its appender's destination — the third part of the logger/appender/layout triad, and each appender owns its own. PatternLayout is the classic: printf-style conversions — %d timestamp, %-5p level, %c logger, %t thread, %m message, %n newline, and %X{key} for thread-context values like a request id. The log4j 1.2 manual's example %r [%t] %-5p %c - %m%n prints '176 [main] INFO org.foo.Bar - Located nearest gas station'. For machines, Log4j 2 offers JSON Template Layout and GelfLayout — self-describing records for aggregators instead of regexes. And pass the exception as the last argument so %throwable keeps the stack trace.**
