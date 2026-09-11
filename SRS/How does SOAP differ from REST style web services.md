<!--
reps: 0
priority: 0
-->
#API/REST #API/SOAP #SRS

# How does SOAP differ from REST style web services

> [!abstract] Short answer
> SOAP is a protocol — a fixed XML envelope, a formal WSDL contract, and a WS-* standards library. REST is an architectural style over HTTP's native features — resources, uniform methods, representations, and status codes, with contracts described in OpenAPI when needed. SOAP standardizes machinery REST leaves to web infrastructure; REST bets on the web's own scalability model.

## The dimensions that actually differ

Message and transport: SOAP mandates its envelope — XML only, with header blocks, roles, and a structured Fault — over any transport; REST messages are negotiable representations (JSON today) whose semantics come from HTTP itself ([[What is SOAP]] for the envelope; [[What is content negotiation in REST APIs]] for representations). Contract: WSDL is a schema-complete, tool-consumable interface definition that generates exact stubs; OpenAPI plays that role for REST but describes, rather than prescribes, and REST tolerates informal contracts. Errors: SOAP has Fault; REST has status classes plus a body convention ([[How do you design error responses in a REST API]]). Infrastructure: REST inherits HTTP's caching, statelessness, and intermediaries — a whole scalability story SOAP largely forgoes (its messages are POST-shaped and cache-hostile). Enterprise features: WS-Security signs and encrypts at the message level (end-to-end across intermediaries — beyond TLS), WS-ReliableMessaging standardizes delivery guarantees; REST achieves equivalents with OAuth2, TLS, idempotency keys, and outbox/inbox patterns, composed per system ([[What is idempotency in HTTP and in messaging]]).

```d2
cmp: SOAP vs REST
cmp.msg: {
  s1: fixed XML Envelope
  r1: any representation (JSON)
}
cmp.contract: {
  s2: WSDL (formal, generative)
  r2: OpenAPI (descriptive)
}
cmp.errors: {
  s3: Fault element
  r3: status codes + body convention
}
cmp.infra: {
  s4: WS-* stack
  r4: HTTP caching, proxies, TLS
}
cmp.style: {
  s5: protocol
  r5: architectural style
}
```

**Fig. 1.** The comparison axes: message shape, contract, errors, infrastructure, and the category difference — protocol versus style.

## Choosing in 2026

Greenfield public APIs are REST (or GraphQL/gRPC per shape of workload); the deciding cases for SOAP are integration obligations — banks, payment processors, government and telecom gateways, ERP middleware — where the counterparty mandates WSDL or message-level security is contractually required. The honest comparison summary: SOAP optimizes for formal cross-org contracts and standardized enterprise machinery; REST optimizes for web-scale simplicity, cacheability, and client diversity ([[What is the relationship between HTTP and REST]]). Interview traps: "SOAP can only use HTTP" (false — transport-neutral), "REST replaced SOAP everywhere" (false — integration estates persist for decades), and "SOAP is always XML-based and verbose, REST always JSON" (REST has no format mandate — XML REST APIs existed).

```text
the same read, two stacks

SOAP: POST /OrderService  Content-Type: application/soap+xml
      <soap:Envelope><soap:Body><o:GetOrder><id>7</id></o:GetOrder></soap:Body></soap:Envelope>
      -> 200 envelope | soap:Fault (Code, Reason)

REST: GET /orders/7  Accept: application/json
      -> 200 {"id":7,...} | 404 + problem+json
```

**Listing 1.** One read: SOAP tunnels the verb through a POSTed envelope with Fault errors; REST uses the uniform method and status codes (conceptual).

> [!warning] The comparison is category-crossed by default
> Asking "SOAP versus REST" mixes a protocol with a style — the fair pairings are SOAP versus HTTP-native resource APIs in practice, and protocol versus style in theory. Say which sense you are comparing; otherwise the answer degenerates into tooling preferences.

> [!tip] Interview answer
> SOAP is a protocol: fixed XML envelopes, WSDL contracts, WS-* standards for message-level security and reliability. REST is a style over HTTP: resources and uniform methods, negotiable representations, status codes, and web infrastructure doing the work SOAP standardizes. Today SOAP survives as an integration obligation where formal contracts or message-level security are mandated; for greenfield APIs I default to REST and compose its equivalents from OAuth2, TLS, and idempotency.
