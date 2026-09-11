<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Behavioral #SRS

# How would you explain the chain of responsibility design pattern

> [!abstract] Short answer
> Chain of Responsibility passes a request along a line of **handlers**: each handler decides either to process the request or to pass it to the next one, and can stop the chain. The sender never needs to know which handler will actually do the work.

## The mechanism

Every handler implements one interface and holds a reference to the next link. Two styles coexist, and naming both is what separates a real answer from a definition recital. In the process-and-forward style — middleware, servlet filters, web framework interceptors — each handler runs its own logic and then forwards, so the request accumulates processing along the way. In the handle-or-forward style — the more canonical one — the handler either processes the request or passes it on untouched, and exactly one handler wins; GUI event bubbling is the catalog's example, where a click travels from the button up through panels to the window until some element handles it. Chains are assembled at runtime by linking handlers, and a chain can even be extracted from an object tree branch, since each node already knows its container.

```java
abstract class Handler {
    protected final Handler next;
    Handler(Handler next) { this.next = next; }
    abstract void handle(Request req);
}

class AuthHandler extends Handler {
    AuthHandler(Handler next) { super(next); }
    void handle(Request req) {
        if (!req.authenticated()) return;        // stop the chain
        next.handle(req);                        // pass it on
    }
}
```

**Listing 1.** The shape: a next reference in the base class, a decision in each concrete handler — process, forward, or stop.

## What makes it useful and what it costs

The pattern fits when the kinds of requests and their order are known only roughly: authentication, then sanitization, then rate limiting, then caching can be reordered or extended without touching client code — the Open/Closed benefit. It also fits when several handlers must run in a prescribed order. The cost the catalog names honestly: **some requests may end up unhandled** — a chain with no terminal handler silently drops them — and the dynamic composition means behavior depends on how the client wired the links, which is invisible at the call site. The behavioral set this pattern belongs to is surveyed in [[What are examples of behavioral design patterns]].

```d2
direction: right
h1: "AuthHandler" { width: 170; height: 80; style.fill: "#e3f2fd" }
h2: "RateLimitHandler" { width: 200; height: 80; style.fill: "#fff3e0" }
h3: "CacheHandler" { width: 180; height: 80; style.fill: "#fff3e0" }
biz: "Business logic" { width: 170; height: 80; style.fill: "#e8f5e9" }
req: "Request" { width: 130; height: 70; style.fill: "#f3e5f5" }
req -> h1 -> h2 -> h3 -> biz: passes along
h2 -> req: may stop
```

**Fig. 1.** The request travels handler by handler; any link may terminate the journey, and an unhandled request falls off the end.

> [!warning] The silent-drop trap
> Nothing in the pattern guarantees a request is processed: if no handler stops the chain and no terminal handler exists, the request just disappears — real filter chains answer this with a final default handler. A related trap is describing Spring Security as "a Command pattern chain"; the framework docs call it a chain of servlet filters — see [[What design patterns does the Spring Framework use]] for where each GoF name actually appears there.

> [!tip] Interview answer
> Chain of Responsibility lines up handlers behind one interface, each holding a next reference. Each handler processes or forwards — middleware-style chains process and pass, canonical ones pass until a single capable handler takes the request. You get runtime-composable, reorderable processing with no sender coupling, but you must plan for requests that fall off the end unhandled.
