<!--
reps: 0
priority: 0
-->
#API/REST #SRS

# What is content negotiation in REST APIs

> [!abstract] Short answer
> Content negotiation is how one resource URI serves multiple representations: the client states preferences in Accept headers, the server picks a representation and answers with Content-Type. Server-driven negotiation uses Accept, Accept-Language, and friends; when the server cannot satisfy the request it answers 406 Not Acceptable, and a payload format it cannot consume is 415 Unsupported Media Type.

## How the negotiation proceeds

The client lists media types with optional quality factors — Accept: text/csv;q=0.9, application/json — and may use wildcards. The server selects the best supported type, marks the response with Content-Type, and should include Vary: Accept so caches know the representation varies with that header. If nothing acceptable matches, 406 with an Accept header (or body) stating the supported set is the honest answer; wildcard ranges match by preference order, and a missing Accept header means the client accepts anything. The same mechanism guards inputs: request bodies carry Content-Type, and a body the server cannot parse into any supported input format gets 415. Self-descriptive messages are the REST constraint underneath: the representation states what it is, so caches and intermediaries can route and store correctly ([[What is the relationship between HTTP and REST]], [[What is a resource in a RESTful context]]).

```text
client: 200 CT=application/json {"id":7,"name":"Mouse"}          <- Accept: application/json
client: 200 CT=text/csv id,name|7,Mouse|                         <- Accept: text/csv;q=0.9
client: 406 CT=application/json {"error":"Not Acceptable",...}   <- Accept: application/xml
client: 200 CT=application/json {"id":7,...}                     <- Accept: */* (default)
```

**Listing 1.** Verified on JDK 21 (com.sun.net.httpserver): one /items/7 URI serving JSON and CSV, 406 with the supported list for application/xml, wildcard falling back to the default (out/A04_ContentNegotiation.txt).

```d2
c: client
s: server /items/7
c -> s: GET + Accept: text/csv;q=0.9, application/json
s -> s: pick best match
s -> c: 200 Content-Type: text/csv
+ Vary: Accept
alt: no match {
  shape: text
}
s -> alt: application/xml?
alt -> c: 406 + supported list
```

**Fig. 1.** Server-driven negotiation: the Accept header expresses preferences; the server answers with the chosen representation, or 406 when nothing matches.

## Practice and pitfalls

Versioning via media type (application/vnd.myapi.v2+json) is negotiation doing double duty as a version signal — it keeps URIs stable but costs debuggability ([[How should you version a public API]] compares the options). Pragmatic fallbacks exist: a format query parameter is common despite not being negotiation proper, and vendor types (GitHub's application/vnd.github+json) show the production pattern. The pitfalls interviewers probe: caches MUST key on Vary or JSON clients will get CSV; 406 is for representation mismatch, not for unknown resources (that stays 404) and not for unsupported input (415); and over-negotiating — five formats nobody uses — multiplies testing surface. Keep two or three formats, all self-describing, and remember the caching contract they create ([[How do you make REST API responses cacheable]]'s Vary discussion).

> [!warning] Forgetting Vary: Accept silently poisons caches
> A shared cache that ignores representation variance will hand the CSV export to the JSON web client the moment both hit the same URI. Every negotiated header belongs in Vary, or the resource must not be cached at all.

> [!tip] Interview answer
> One URI, many representations: the client sends Accept with optional q-values, the server picks, answers with Content-Type and Vary: Accept so caches key correctly. Unsatisfiable preferences give 406 with the supported list; unparseable input gives 415. I use it for JSON/CSV and vendor-versioned media types, and keep the negotiated surface small — every extra format multiplies tests and cache keys.
