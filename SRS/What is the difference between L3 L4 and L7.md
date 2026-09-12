<!--
reps: 0
priority: 0
-->
#Networking #SRS
# What is the difference between L3 L4 and L7

> [!abstract] Short answer
> L3, L4 and L7 name OSI stack layers where a device or load balancer makes its decision: L3 routes by IP addresses, L4 forwards or balances by transport endpoints (IP + port, TCP/UDP connection state), and L7 inspects the application protocol itself — HTTP methods, headers, host, path, cookies, or gRPC metadata — before choosing a target.

## Layer by layer

| Layer | Decision input | Typical device / balancer | What it cannot see |
|---|---|---|---|
| L3 Network | source/destination IP, protocol number | router, L3 switch | ports, payload |
| L4 Transport | IP + source/destination port, TCP flags, connection state | TCP/UDP load balancer (AWS NLB, HAProxy TCP mode, LVS) | URLs, headers, body |
| L7 Application | HTTP host, path, method, headers, cookies, gRPC routes | reverse proxy (NGINX, HAProxy HTTP mode, Envoy, AWS ALB) | nothing above the chosen protocol |

```d2
direction: down
l3: "L3: route by IP\npacket -> next hop" {
  width: 300; height: 80; style.fill: "#e3f2fd"
}
l4: "L4: pick backend by\nIP + port / conn state" {
  width: 300; height: 80; style.fill: "#fff3e0"
}
l7: "L7: inspect HTTP host, path,\nheaders -> route, rewrite, cache" {
  width: 340; height: 90; style.fill: "#e8f5e9"
}
l3 -> l4
l4 -> l7
```

**Fig. 1.** Each layer adds decision input the layer below cannot use; an L4 balancer forwards what it never parses, while an L7 proxy terminates and re-originates the conversation.

## Practical consequences

An L3/L4 balancer is a fast packet forwarder: it can run in DSR (direct server return) mode, keep connections alive for weeks, and costs little per connection because it never buffers application data. An L7 proxy must terminate the connection (and often TLS), parse the request, and open a new upstream connection — that is why L7 adds latency per request but enables path-based routing, header rewrites, rate limiting per API key, caching, and compression. [[How do you optimize a high traffic web service]] usually starts with pushing as much traffic as possible to L4 and reserving L7 for what genuinely needs content-aware routing.

> [!warning] Terminology trap
> These numbers come from the OSI reference model, but real stacks mix them: Linux netfilter can match at both L3 and L4, and an HTTP proxy still runs on top of TCP, so the "L7 balancer" is also a full L4 endpoint. Saying "L7 is faster because it understands more" inverts the tradeoff — more inspection means more work per byte.

Related: [[At which OSI layer does a router primarily operate]] and [[At which OSI layer does a switch primarily operate]] show the same layer reasoning for individual devices, while [[What is NAT and how does it work]] is the classic L4 rewrite mechanism.

> [!tip] Interview answer
> L3 decides on IP addresses, L4 on IP plus port and transport state, L7 on the application message itself — URL, headers, method. Lower layers are faster and protocol-agnostic; L7 buys content-aware routing, rewriting and caching at the cost of terminating the connection. Name a concrete example: NLB versus ALB, or HAProxy TCP mode versus HTTP mode.
