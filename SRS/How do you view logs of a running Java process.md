<!--
reps: 0
priority: 0
-->
#Java/Logging #SRS

# How do you view logs of a running Java process?

> [!abstract] Short answer
> It depends on **which logs** — and naming that split is the point of the question. **Application logs** (log4j/Log4j 2, SLF4J, JUL) live where the logging framework's **appenders** wrote them: a file you `tail -f /var/log/app.log`, stdout captured by the service manager — `journalctl -u myapp -f` on systemd — or a container's stdout — `docker logs -f <container>` (then `kubectl logs -f <pod>` in Kubernetes); if the appender shipped events to a socket or database, the local machine has *nothing* to tail and you follow them in the log server. **JVM's own logs** (GC, class loading, safepoints — the *unified logging* framework) are configured with `-Xlog` and can be inspected **at runtime** without restarting: `jcmd <pid> VM.log` — per its man page it "lists current log configuration, enables/disables/configures a log output, or rotates all logs". There is no command that "dumps the application log from the process" — application log events exist only where appenders put them. Background: [[What is a log4j Appender]], [[What are the components of the log4j logging system]].

## Application logs: follow the appender

The first diagnostic step is identifying the appender configuration, because it defines the *only* reliable places to look. A file appender names the path (and the rotation scheme — the live file plus compressed rolls; see [[What is a log4j Appender]] for policies); `tail -f` with `-F` (capital — follows across rotation) is the basic tool, `less +F` adds paging, and `grep`/`jq` filter by request id. Console appenders write to stdout, and in service deployments stdout is captured, not lost: under systemd it lands in the journal — `journalctl -u myapp -f`; under Docker it is collected by the container engine — `docker logs -f` (with `--since` and `--tail` for windowing); under Kubernetes, `kubectl logs -f pod [-c container]`, which reads what the runtime captured on the node. Remote appenders (Socket, JMS, JDBC, syslog) move the story off-box entirely — you follow the event in the aggregator (Graylog, Elastic, Loki), and the local diagnostic becomes "is the shipping pipeline up?". The habit worth stating in an interview: *logs are configured, not found* — check the logging configuration first instead of hunting the filesystem for mystery files.

## JVM logs: -Xlog at launch, jcmd VM.log at runtime

The JVM itself emits structured diagnostics — GC activity, class loading, safepoints, module issues — through the **unified logging framework**, configured at launch with `-Xlog`: tag selections, level, output and decorations (e.g. `-Xlog:gc*`, `-Xlog:gc:file=gc.log:time,uptime:filecount=5,filesize=20m`). The runtime twist the question probes: you can change where these go **without restarting** the process — `jcmd <pid> VM.log list` shows the current configuration, and `VM.log output="..." what=... tags=...` enables or redirects outputs; the man page's own summary is that it "lists current log configuration, enables/disables/configures a log output, or rotates all logs". This is the tool when a long-running JVM suddenly needs GC visibility — start writing `gc.log` now, no restart, no agent. For *reading* the files once written, the same tail/journalctl/docker habits apply. Diagnosing the JVM's internals beyond logs (threads, heap) is a different toolkit — see [[What is a heap dump and a thread dump]] — while app-log level changes at runtime are a framework feature (Log4j 2 hot reload, Actuator's `/loggers` endpoint: [[How do you change log levels at runtime with Actuator]]); `VM.log` speaks *unified JVM logging*, not application frameworks.

## The decision procedure, compressed

When asked live, walk the decision tree: (1) *Whose logs?* Application framework → (2) *Which appender?* File → tail the file (`tail -F`), rotation-aware; Console/stdout → service-manager or container capture (`journalctl -f`, `docker logs -f`, `kubectl logs -f`); Socket/DB/syslog → the log server, not the local box. JVM diagnostics → (3) `-Xlog` for configuration and `jcmd <pid> VM.log list` for the current state; enable a new output if you need more. Then the safety checks that separate seniors: verify **rotation** will not break your tail (use `-F` not `-f` on files), verify you are on the **right instance** of a scaled service before grepping (the id you want may be in the shipped stream, not this pod), and for anything past quick triage, pull logs into the aggregator where request-id correlation works across services. If the answer must be one sentence: application logs go where their appenders write them — file, journal, container stdout, or a log server — while the JVM's own logs are `-Xlog` streams you can reconfigure live with `jcmd VM.log`.

```bash
# 1) File appender: follow across rotation (-F, not -f)
tail -F /var/log/myapp/app.log | grep --line-buffered "requestId=abc123"

# 2) Console appender under systemd / Docker / Kubernetes
journalctl -u myapp -f --since "10 minutes ago"
docker logs -f --tail 200 myapp
kubectl logs -f myapp-pod-7d4f --all-containers

# 3) JVM unified logging: inspect and reconfigure at runtime
jcmd 12345 VM.log list                          # current outputs/tags/levels
jcmd 12345 VM.log output="file=gc.log" what="gc+heap=info"  # start GC log now

# 4) Launch-time configuration of the JVM's own logs:
java -Xlog:gc*:file=gc.log:time,uptime:filecount=5,filesize=20m -jar app.jar
```

**Listing 1.** The four practical routes: tail the appender's file, read the captured stdout, inspect JVM logging with `jcmd VM.log`, and configure `-Xlog` at launch.

```d2
direction: right
proc: "running Java process" {style.fill: "#e3f2fd"}
app: "application logs\n(log4j / SLF4J / JUL)" {style.fill: "#e8f5e9"}
jvm: "JVM logs\nunified logging (-Xlog)" {style.fill: "#fff8e1"}
file: "file appender" {style.fill: "#eceff1"}
console: "console appender\nstdout" {style.fill: "#eceff1"}
remote: "socket / db / syslog\nappender" {style.fill: "#eceff1"}
tail: "tail -F app.log" {style.fill: "#e8f5e9"}
cap: "journalctl -f / docker logs -f /\nkubectl logs -f" {style.fill: "#e8f5e9"}
agg: "log server\n(Graylog / Elastic / Loki)" {style.fill: "#e8f5e9"}
jcmd: "jcmd <pid> VM.log\nlist / enable / rotate" {style.fill: "#f3e5f5"}
xl: "-Xlog:gc*:file=gc.log" {style.fill: "#f3e5f5"}
proc -> app -> file -> tail
app -> console -> cap
app -> remote -> agg
proc -> jvm
jvm -> jcmd
jvm -> xl
```

**Fig. 1.** Where to look is decided by configuration: appender destinations for application logs, `-Xlog` outputs for JVM logs — with `jcmd VM.log` adjusting the latter live.

## Vocabulary the interview actually tests

Two distinctions are graded. **Application logs vs JVM logs** — the former belong to logging frameworks and their appenders; the latter are the unified-logging streams (`-Xlog`) of the JVM itself, and `jcmd VM.log` manages *those*, not the application's. **Captured vs remote stdout** — console appenders make `journalctl`/`docker logs`/`kubectl logs` the reader; socket/database appenders make the local box a dead end and the log server the reader. A senior bonus: knowing `tail -F` follows rotation while `tail -f` does not, and that `jcmd VM.log` can *start* a GC log on a misbehaving long-running process without restart — the move that actually saves a production evening. Conversely, the answer's anti-pattern is the classic draft one-liner ("tail -f, journalctl, docker logs") with no mention of appenders or `-Xlog` — it reads as someone who has only ever read logs, never configured them.

> [!warning] "jcmd dumps the application's log" — no such command exists
> The trap inside this question is conflating the two log worlds. `jcmd` has **no** command to read an application's log events: once a `logger.info` call has been filtered and routed, the event exists only where the appender wrote it — the process's memory holds no replayable log buffer by default (JUL's `MemoryHandler` aside, it is a bounded ring, not a retrieval tool). Symmetrically, `-Xlog:gc` will not capture `logger.error` business events — unified logging speaks JVM tags (`gc`, `class`, `metaspace`...), not framework categories. Also mind rotation: `tail -f` dies on rollover, `tail -F` follows; and `docker logs -f` on a chatty container with a large history can take minutes before it reaches "live" — scope with `--since`/`--tail` first.

> [!tip] Interview answer
> **Split the question first. Application logs live where the framework's appenders write them: file — tail -F with rotation awareness; console stdout — captured by journalctl -f under systemd, docker logs -f or kubectl logs -f in containers; socket or database appenders — the log server, not the local box. The JVM's own logs are the unified logging framework: configure -Xlog at launch — say -Xlog:gc*:file=gc.log with size and count caps — and at runtime inspect or reconfigure with jcmd VM.log, which lists, enables or rotates outputs without a restart. And be explicit: there's no command that dumps application logs from the process memory — if the appender didn't write it somewhere, it doesn't exist.**
