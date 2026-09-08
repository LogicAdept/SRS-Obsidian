<!--
reps: 0
priority: 0
-->
#Java/JVM #Java/Language #SRS

# Why should you use Java?

> [!abstract] Short answer
> Use it when you want a **portable binary**, a **specified** language (types, exceptions, threads, GC), and a **large Standard Edition API** on one VM. Source compiles to **machine-independent bytecode**; a JVM runs that `class` file on another host. Memory is **reclaimed**, not `free`’d. `try`/`catch`/`throw` are in the language; so are **threads and monitors**. Libraries then add collections, I/O filters, **JDBC**, and **HTTP**. What Java *is*: [[What is Java]]. Language vs VM: [[How would you explain distinctive traits of the Java programming language]], [[How would you explain distinctive traits of the Java platform]].

## Language guarantees, then the SE catalog

**Portability.** Compile time yields a `class` file, not a Windows or Linux `exe`. The same bytes run wherever a compatible JVM exists ([[What is the JVM]], [[Why is Java described as platform independent]]).

**Robustness.** Automatic storage management avoids `free`/`delete` use-after-free. Array access is **bounds-checked**. Exceptions are objects (`Throwable`); the compiler tracks **checked** exceptions so handlers exist ([[How would you explain distinctive traits of the Java programming language]]). Strong static typing catches many mistakes before run time ([[How would you explain static typing in Java]]).

**Concurrency in the language.** `Thread`, `synchronized`, and a **memory model** are specified, not a bolt-on C library. Pools and virtual threads are libraries on top of that ([[How would you explain Virtual Threads]]).

**Standard libraries (Java SE, not “the language”).** `java.util` is the **collections framework** (`List`, `Set`, `Map`, `Deque`, plus legacy `Stack` / `Vector`). Arrays are a language construct; lists are not. `FilterInputStream` / `FilterOutputStream` wrap another stream and transform or extra-function it (`BufferedInputStream`, `DataInputStream`, …). `java.net` covers sockets; `java.net.http.HttpClient` (**since 11**) sends HTTP/1.1 or HTTP/2 and reads responses. Older `HttpURLConnection` is still there. **JDBC** (`java.sql` / `javax.sql`) is the SE API for SQL against pluggable drivers ([[What is JDBC]]). **RMI** (`java.rmi`, since 1.1) invokes a `Remote` object on another JVM; it is a real SE API, not the usual 2026 reason to pick Java.

**Later language surface.** Generics are **Java 5** (`@since 1.5`) ([[In which Java version were generics introduced]]). Lambdas and method references are **Java 8**; they capture enclosing locals that are final or effectively final — that is Java’s “closure.” Streams and `java.util.function` are **libraries** from the same release ([[What major language features arrived in Java 8]], [[How would you explain lambda expressions in Java]]).

Third-party libraries exist in volume; that is an ecosystem fact, not a count in the spec.

```d2
direction: down
lang: "language + VM\nbytecode, GC, exceptions, threads" {
  width: 320
  height: 55
  style.fill: "#e3f2fd"
}
se: "Java SE API\ncollections, I/O, JDBC, HTTP" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
eco: "libraries on top of SE\nnot the language" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
lang -> se
se -> eco
```

**Fig. 1.** Interview “why Java” is three layers. Do not quote Jakarta or a random HTTP client as if they were the language.

```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.List;

class Demo {
    static int n() throws Exception {
        List<String> names = List.of("a", "b");
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest req = HttpRequest.newBuilder(URI.create("https://example.com/")).GET().build();
        client.send(req, HttpResponse.BodyHandlers.discarding());
        return names.size();
    }
}
```

**Listing 1.** SE catalog on one VM: collections plus `HttpClient` (Java 11). JDBC and filters are the same idea — standard APIs, vendor drivers or stream wrappers underneath.

> [!warning] SQLJ, JDO, and JPA are not “why the Java language”
> **JDBC** is Java SE. **SQLJ** is embedded SQL in source, not a Java SE language feature. **JDO** is a separate persistence JSR. **JPA** is **Jakarta Persistence**, commonly used *with* Java, not a reason the *language* exists. Do not list them as core “use Java because.”

> [!warning] Threads were not “ported to Python from Java”
> Java specified monitors and a memory model. Other languages have threads independently. RMI is also not “simple networking”: it is remote *Java* objects. Prefer sockets / HTTP for a general networking answer. `java.util.Stack` is a legacy vector-backed class; say `Deque` unless the interviewer asked for the old name.

> [!tip] Interview answer
> **I use Java for portable bytecode, GC, specified exceptions and threads, and a huge SE API — collections, I/O, JDBC, HTTP — plus the library ecosystem on that VM.** Generics landed in 5, lambdas in 8. I do not sell SQLJ/JDO/JPA or “Python copied our threads” as the language pitch.
