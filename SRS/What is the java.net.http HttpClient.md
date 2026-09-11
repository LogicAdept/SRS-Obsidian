<!--
reps: 0
priority: 0
-->
#Java/Versions/11 #SRS

# What is the java.net.http HttpClient

> [!abstract] Short answer
> **`java.net.http.HttpClient` (standard in Java 11, JEP 321) is the JDK's modern HTTP client: builder-configured, immutable, supporting HTTP/2 with automatic 1.1 fallback, synchronous `send` and asynchronous `sendAsync` returning `CompletableFuture`, `BodyHandlers` for strings/bytes/files/streams, and a WebSocket API.** It replaced the "use `HttpURLConnection` and apologize" era; Spring's `WebClient` and `RestClient` ride higher-level stacks, but the JDK client needs no dependency at all ([[What is WebClient]]).

## Shape of the API

Build an `HttpClient` once (immutable, reusable, typically one per application): `HttpClient.newBuilder().version(HTTP_2).connectTimeout(...).build()`. Build an `HttpRequest` per call (URI, headers, method, body publishers). Execute: `client.send(req, BodyHandlers.ofString())` blocks; `client.sendAsync(req, ...)` returns a `CompletableFuture<HttpResponse<T>>` for composition. Response `BodyHandlers` cover `ofString`, `ofByteArray`, `ofFile`, `ofInputStream` (streaming — the memory-safe default for large payloads); request `BodyPublishers` cover strings, bytes, files, and input streams. Push promises and the WebSocket subprotocol are part of the standard API.

HTTP/2 is negotiated over TLS via ALPN or via HTTP/1.1 `Upgrade`; the client falls back transparently. HTTP/3 support (JEP 517) landed as a later evolution in 26 ([[What was new in Java after 21]]).

```d2
direction: down
b1: "HttpClient.newBuilder()\nversion, timeouts, executor" {
  width: 320
  height: 65
  style.fill: "#e3f2fd"
}
b2: "HttpRequest.newBuilder(uri)\nmethod, headers, body" {
  width: 320
  height: 65
  style.fill: "#e3f2fd"
}
s1: "send(req, BodyHandlers.ofString())\nblocking HttpResponse<T>" {
  width: 360
  height: 65
  style.fill: "#e8f5e9"
}
s2: "sendAsync(req, ...)\nCompletableFuture<HttpResponse<T>>" {
  width: 380
  height: 65
  style.fill: "#e8f5e9"
}
b1 -> b2
b2 -> s1
b2 -> s2
```

**Fig. 1.** One immutable client, many immutable requests, two execution modes — the streaming body handler is what keeps large downloads off the heap.

```java
import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class V16_HttpClient {
    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        server.createContext("/greet", ex -> {
            byte[] body = "hello from jdk server".getBytes();
            ex.getResponseHeaders().add("Content-Type", "text/plain");
            ex.sendResponseHeaders(200, body.length);
            try (var out = ex.getResponseBody()) { out.write(body); }
        });
        server.start();
        try {
            HttpClient client = HttpClient.newBuilder().version(HttpClient.Version.HTTP_1_1).build();
            HttpRequest req = HttpRequest.newBuilder(URI.create("http://127.0.0.1:" + server.getAddress().getPort() + "/greet")).build();
            HttpResponse<String> res = client.send(req, HttpResponse.BodyHandlers.ofString());
            System.out.println("status: " + res.statusCode());
            System.out.println("body: " + res.body());
        } finally {
            server.stop(0);
        }
    }
}
```

**Listing 1.** Verified on JDK 21 (V16_HttpClient in empirics): `status: 200`, `body: hello from jdk server` — a real loopback round trip through the standard client against a throwaway JDK server (out/V16_HttpClient.txt).

> [!warning] Defaults that bite: no redirects, no timeout, no credentials
> The client follows **no redirects by default** (`Redirect.NEVER`) and sets **no overall request timeout** — a hung endpoint hangs your `send` until the OS gives up; set `connectTimeout` on the builder and `.timeout(...)` per request. Authentication is explicit (an `Authenticator` on the builder), and cookies need a `CookieHandler`. Do not call it "the new RestTemplate" — it is deliberately low-level: connection pooling and HTTP/2 multiplexing are internal, but retry, load-balancing, and serialization are your job ([[What was new in Java 11]]).

> [!tip] Interview answer
> **java.net.http.HttpClient is the Java 11 standard client: immutable builder-based client, HTTP/2 with 1.1 fallback, sync send and CompletableFuture-based sendAsync, streaming BodyHandlers, WebSockets.** Watch the defaults — no redirect following, no per-request timeout unless you set one. Dependency-free HTTP for services and tools.
