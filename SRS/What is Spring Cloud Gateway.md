<!--
reps: 0
priority: 0
-->
#Java/Spring/Cloud/Gateway #SRS

# What is Spring Cloud Gateway?

> [!abstract] Short answer
> **Spring Cloud Gateway** is Spring Cloud’s **API gateway**: a Boot app that **routes** HTTP (and WebSocket) to backends and applies **cross-cutting** filters — security, metrics, resiliency. A **route** is an **id**, a destination **URI**, **predicates** (match the request), and **filters** (mutate before/after the proxy hop). The original **Server** is **WebFlux + Reactor + Netty**, not a servlet WAR. There is also a **Server MVC** flavor and a **Proxy Exchange** helper for annotated controllers. It is **not** Netflix Zuul and **not** only a load balancer.

## Route, predicate, filter

Clients hit the gateway. **Gateway Handler Mapping** tests predicates; a match goes to the **Gateway Web Handler**, which runs a **filter chain**: all **pre** logic, then the **proxy** call, then **post** logic ([[How do you achieve server-side load balancing with Spring Cloud]], [[What is Spring Cloud]]).

Predicates AND together (Path, Host, Method, Header, …). Built-in filters include **RewritePath** / **StripPrefix**, **RequestRateLimiter**, **CircuitBreaker** (Spring Cloud CircuitBreaker / Resilience4J), **TokenRelay**, header and body rewrites. Destination may be a literal `https://…` or **`lb://serviceId`** when LoadBalancer is on the classpath. Discovery can **generate** `lb://` routes (`spring.cloud.gateway.discovery.locator.enabled=true`).

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: catalog
          uri: lb://catalog-service
          predicates:
            - Path=/catalog/**
          filters:
            - StripPrefix=1
            - name: CircuitBreaker
              args:
                name: catalogCb
                fallbackUri: forward:/catalog-fallback
```

**Listing 1.** Conceptual. Predicate match, prefix strip, load-balanced URI, circuit-breaker fallback.

```d2
direction: down
client: "Client" {
  width: 120
  height: 40
  style.fill: "#fff3e0"
}
map: "Handler Mapping\npredicates" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
pre: "pre filters" {
  width: 140
  height: 40
  style.fill: "#fce4ec"
}
proxy: "proxy hop" {
  width: 140
  height: 40
  style.fill: "#e8f5e9"
}
post: "post filters" {
  width: 140
  height: 40
  style.fill: "#fce4ec"
}
down: "backend" {
  width: 140
  height: 40
  style.fill: "#e8f5e9"
}
client -> map
map -> pre
pre -> proxy
proxy -> down
down -> post
post -> client
```

**Fig. 1.** Match a route, then pre → proxy → post ([[How would you explain Circuit Breaker]]).

Classic starter `spring-cloud-starter-gateway` is **WebFlux**. Docs for that stack: **Netty** runtime; it **does not** run in a traditional servlet container or as a **WAR**. Newer docs also document **Gateway Server MVC** and **Proxy Exchange** (`ProxyExchange` method parameter). Prefer the starter that matches the stack you actually run.

> [!warning] WebFlux Gateway is not a servlet app
> The WebFlux server **requires Netty**. Blocking servlet libraries and “drop it in Tomcat as a WAR” do not apply. Filters return `Mono`; blocking I/O on the event loop stalls **other** requests, not only yours.

> [!warning] Path on the route URI is ignored
> The destination **path** on `uri:` is discarded. Put path changes in **predicates/filters** (`StripPrefix`, `SetPath`, `RewritePath`). Missing port on `http`/`https` URIs defaults to **80** / **443**.

> [!tip] Interview answer
> Gateway is a Boot API gateway: routes are id + URI + predicates + filters, with a pre/proxy/post chain. Use it for edge routing, `lb://` discovery, rate limits, and circuit breaking. The well-known stack is WebFlux/Netty, not Zuul 1 on a servlet container.
