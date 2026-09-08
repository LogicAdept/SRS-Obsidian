<!--
reps: 0
priority: 0
-->
#Java/Logging #Java/Library/Log4j #SRS

# What is a log4j Logger?

> [!abstract] Short answer
> A **Logger** is the named object your application code calls to produce log events — in Log4j 1.x the class `org.apache.log4j.Logger`, in Log4j 2 a handle obtained from `LogManager.getLogger(name)` that implements `org.apache.logging.log4j.Logger`. It does three things: it carries a **name** (dot-separated, mirroring package/class structure — `com.myapp.db.Pool`), it carries an **effective level** that makes the first filtering decision — an event below the level never gets built — and it forwards surviving events to the logging pipeline (appenders via its configuration). Loggers form a **hierarchy by name**: `com.myapp` is the parent of `com.myapp.db`, levels and appender sets inherit down the tree, and the `root` logger sits at the top. In Log4j 2 the logger is deliberately thin: the level and the appender set live in the **`LoggerConfig`** the name selects, so the same call site's behavior can be changed by configuration alone. Gateway to the rest of the system: [[What is a log4j Appender]], [[What are the components of the log4j logging system]].

## The name is the design

A logger is retrieved, not constructed: `LogManager.getLogger("com.myapp.db")` or `getLogger(MyClass.class)` (which derives the class name as the logger name). The dot-separated name is not cosmetic — it *is* the configuration model. The framework walks up the name components until it finds a configured node; everything under `com.myapp` inherits that node's level and appenders unless a deeper node overrides them. This is why the convention "one logger per class, named after the fully-qualified class name" is nearly universal: it gives operations a tree they can reason about ("raise `com.myapp.db` to DEBUG without touching anything else") and it gives the code a stable handle. In Log4j 2 the lookup is also cheap — loggers are cached in the `LoggerContext`, so repeated `getLogger` calls with the same name return the same instance.

## The level check is the first gate

Calling `logger.info(...)` is not "write a line". The logger compares the call's level against its **effective level** and drops the event early if it is less severe — the point is that the rejected call costs (almost) nothing, which is why enabling a lower level is a runtime configuration decision, not a code change. The manual's own example frames it: configuration sets "log4j2.level" and events "less severe than" it are filtered out of the output. Effective level resolution walks the hierarchy: if `com.myapp.db` has no explicit level, it inherits from `com.myapp`, which inherits from `root`. Beyond the boolean pass, the logger builds the **`LogEvent`** — timestamp, thread name, level, logger name, message and parameters, thread context — and hands it to its configuration's appender list. Parameterized messages (`log.info("user {} logged in", name)`) defer formatting until after the level check, which is the habit that makes high-frequency debug calls affordable.

## Log4j 1 vs Log4j 2: the Logger split

In Log4j 1.x the `Logger` object *was* the configuration carrier: it held its `Level` and its `Appender` list directly, and "logging behavior" and "logging handle" were one object. Log4j 2 split them: the `Logger` you hold is a handle, and the **`LoggerConfig`** — the manual's words — "encapsulates configuration for a Logger, as `AppenderControl` and `AppenderRef` for `Appender`s". Several loggers can share one `LoggerConfig`; one logger's behavior can change when configuration reassigns its `LoggerConfig`. Two practical consequences follow. First, reconfiguration is cheap and complete: swap the configuration and existing logger handles start behaving differently. Second, a JVM can host several `LoggerContext`s (the composition anchor that creates loggers — for example, two web apps in one container), each with its own tree; two loggers with the same *name* in different contexts are different objects. Related cards: [[What are log4j logging levels in order of increasing severity]] for the gate semantics, [[What is a Layout in log4j]] for the formatting stage the event reaches after the logger.

```java
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class Pool {
    // Conventional: name = fully qualified class name ("com.myapp.db.Pool")
    private static final Logger log = LogManager.getLogger(Pool.class);

    public void acquire() {
        // Level check first: if Pool's effective level is INFO,
        // the DEBUG call below is rejected BEFORE formatting the message.
        log.debug("acquiring connection, free={}", freeCount);

        // Parameterized logging: {} placeholders are substituted only
        // if the event passes the level check.
        log.info("connection acquired in {} ms", took);
    }
}

// Configuration speaks the same language as the names:
// <Logger name="com.myapp.db" level="DEBUG"/>   <- subtree override
// <Root level="INFO"/>                          <- tree default
// com.myapp.db.Pool inherits DEBUG + the appenders of com.myapp.db.
```

**Listing 1.** A logger is a named handle; its effective level and appenders are resolved from the name hierarchy in configuration.

```d2
direction: top-down
root: "Root\nlevel=INFO" {style.fill: "#ffebee"}
myapp: "com.myapp\n(inherits INFO)" {style.fill: "#fff3e0"}
db: "com.myapp.db\nlevel=DEBUG\n+ file appender" {style.fill: "#e8f5e9"}
pool: "com.myapp.db.Pool\n(inherits DEBUG)" {style.fill: "#e8f5e9"}
svc: "com.myapp.OrderService\n(inherits INFO)" {style.fill: "#fff3e0"}
root -> myapp -> db
db -> pool
myapp -> svc
```

**Fig. 1.** The logger name hierarchy: each node resolves its effective level and appenders from the nearest configured ancestor — configuring `com.myapp.db` reconfigures `Pool` without touching `OrderService`.

## Vocabulary the interview actually tests

Three distinctions decide whether you sound senior. **Get vs new**: loggers are looked up from the framework (`LogManager.getLogger`), never `new`-ed — the framework owns caching and context. **Logger vs LoggerConfig**: Log4j 2 separates the handle from the configuration node; saying "the logger holds the appenders" is the Log4j 1 mental model. **Name hierarchy vs call hierarchy**: the tree is about *names*, not code inheritance — `getLogger(Pool.class)` in a subclass still names the subclass, and two classes in the same package share a parent node. A bonus point: the **root logger** is the top of every tree and the place "default everything to WARN" lives.

> [!warning] "The logger writes the log line" — it does not
> The logger only *decides and forwards*; the appender writes and the layout formats. Three real traps follow from blurring this. First, expensive message building: `log.debug("got " + heavy.toJson())` pays for `toJson()` even when DEBUG is off — use parameterized `log.debug("got {}", heavy)` or a guarded check. Second, in Log4j 2 a logger's behavior can change underneath the same handle after reconfiguration, because the handle is not the configuration. Third, logger names are arbitrary strings — `getLogger("POOL")` compiles fine but escapes the package tree, silently orphaning the logger from the configuration you meant to apply.

> [!tip] Interview answer
> **A logger is the named API object the code calls — Log4j 2 gives it to you from LogManager.getLogger, named after the class by convention. It gate-keeps: its effective level, resolved by walking up the dot-separated name hierarchy, decides whether an event exists at all, and parameterized messages skip formatting on rejection. Surviving events become LogEvents and flow to the appender pipeline. The 1.x logger carried its level and appenders itself; Log4j 2 splits that into a thin logger handle plus a LoggerConfig that holds the configuration — which is why config-only changes redirect an entire subtree, and the root logger is the tree's default.**
