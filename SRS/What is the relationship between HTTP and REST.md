<!--
reps: 0
priority: 0
-->
#API/REST #SRS

# What is the relationship between HTTP and REST

> [!abstract] Short answer
> HTTP is the application protocol; REST is the architectural style that the web's protocol family happens to embody. REST does not require HTTP and HTTP does not guarantee REST — but HTTP's verbs, status codes, headers, and caching model map one-to-one onto REST's uniform-interface and cacheability constraints, which is why "REST API" in practice means "HTTP API built in this style".

## Why HTTP is REST's natural carrier

The dissertation analyzed the existing web architecture, so HTTP was already REST-shaped: URIs identify resources (uniform interface: identification); methods like GET, PUT, DELETE manipulate representations (uniform interface: manipulation); status codes and headers make messages self-descriptive; ETag and Cache-Control implement cacheability; intermediaries (proxies, CDNs) exploit all of it. HTTP adds what a style cannot: a concrete grammar. That division of labor is why you design REST and speak HTTP — the style tells you which properties you want, the protocol gives you the mechanism ([[What is REST]]). It also explains the failure mode: using only HTTP's transport features (a single POST verb, session affinity, status 200 for everything) keeps the protocol but drops the style.

```d2
rest: REST constraint
http: HTTP mechanism
rest.u: uniform interface {
  u1: identification of resources
  u2: manipulation via representations
  u3: self-descriptive messages
}
http.u1: URI
http.u2: GET PUT DELETE...
http.u3: status codes + headers
rest.u.u1 -> http.u1: realized by
rest.u.u2 -> http.u2: realized by
rest.u.u3 -> http.u3: realized by
rest.c: cacheable -> http.c: Cache-Control / ETag (realized by)
```

**Fig. 1.** Each REST constraint has a concrete HTTP mechanism that realizes it; the style is the intent, the protocol is the mechanism.

## The two classic mixups

First: "REST and HTTP are the same thing" — false in both directions. You can build REST on other protocols (the dissertation's target was general hypermedia), and you can build non-REST RPC over HTTP ([[How does SOAP differ from REST style web services]] — SOAP deliberately ignores HTTP's resource model; [[How do you represent non-CRUD actions in a REST API]] shows where HTTP's verb set strains). Second: "any HTTP API is RESTful" — the constraints are exactly the part HTTP does not force; a server-side-session API on HTTP violates statelessness no matter how many verbs it uses. State which side you are claiming when you design or describe an API.

```text
constraint                HTTP mechanism
----------------------    --------------------------------------
identify resources        URI  /orders/7
manipulate via repr.      GET / PUT / DELETE / PATCH
self-descriptive msgs     status codes + Content-Type + ETag
cacheable                 Cache-Control: max-age=60
layered                   proxies/CDNs read the same message
```

**Listing 1.** Constraint-to-mechanism mapping: the style states the property, the protocol supplies the feature (conceptual).

> [!warning] HTTP compatibility is not REST conformance
> Every framework can emit JSON over HTTP; none can emit architecture. Adding Spring Boot does not make an API RESTful — removing server-side sessions, adopting uniform verbs and real status codes, and exposing resources is what does.

> [!tip] Interview answer
> REST is the architectural style, HTTP is the protocol that best embodies it: URIs give resource identification, the method set gives uniform manipulation, headers and status codes make messages self-describing, and ETag plus Cache-Control give cacheability. REST does not need HTTP and HTTP does not enforce REST — an API can ride HTTP while violating every constraint. The style is the design intent; the protocol is the carrier.
