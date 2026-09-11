<!--
reps: 0
priority: 0
-->
#API/REST #Networking/Web #SRS

# Which HTTP status codes matter most in REST API design

> [!abstract] Short answer
> The workhorse set: 200/201/202/204 for success, 304 for conditional reuse, 400 versus 422 for malformed versus semantically invalid input, 401 versus 403 for unauthenticated versus unauthorized, 404/405/409/410/412/415/429 for the standard failure modes, and 5xx for server-side faults. The discipline is to let the status code carry the outcome class and reserve the body for details.

## The success family

200 OK returns a representation of the result. 201 Created follows a successful POST that created a resource, and MUST be paired with a Location header pointing at the new resource — clients should never parse the body to discover its URI. 202 Accepted says the work was queued but is not done; it belongs to async patterns and pairs with a status resource or callback ([[How do you handle long-running operations in a REST API]]). 204 No Content closes a successful mutation with no body — DELETE and PUT normally land here. 304 Not Acceptable is not an error: conditional GET answers it when If-None-Match matches, letting the client reuse its cached copy ([[How do you make REST API responses cacheable]]).

## The failure families clients must program against

400 Bad Request: syntactically malformed input (broken JSON, wrong types). 422 Unprocessable Content (generalized into the HTTP core by RFC 9110 from WebDAV): well-formed but semantically rejected — insufficient funds, a negative age. 401 Unauthorized: "you are nobody (or your credentials are bad)"; 403 Forbidden: "I know who you are and this is not allowed" — the response must not reveal whether the resource exists to outsiders. 404 Unknown resource; 405 Method Not Allowed must carry an Allow header listing what would work; 409 Conflict for state clashes (duplicate create, stale version without If-Match); 412 Precondition Failed when an explicit If-Match/If-Unmodified-Since check fails; 415 Unsupported Media Type for payloads in formats you do not accept; 429 Too Many Requests for throttling, normally with Retry-After ([[How do you design rate limiting for a REST API]]). 5xx means the server side is at fault — retryable, not the client's bug; never fake a 200 with an error body inside ([[Why does GraphQL often return HTTP 200 when a field errors]] for the counter-example).

```text
POST   /api/orders        -> 201 Location=/api/orders/42 {"id":42}
POST   /api/orders        -> 400 {"error":"body required"}
GET    /api/orders        -> 405 Allow=POST
DELETE /api/orders/7      -> 204
PUT    /api/orders/7      -> 204
POST   /api/orders/7/pay  -> 422 {"type":"...insufficient-funds","status":422}
PUT    /api/orders/7 (stale If-Match) -> 412 {"error":"precondition failed"}
GET    /api/orders        (5th in window) -> 429 Retry-After=30
```

**Listing 1.** Verified on JDK 21 (com.sun.net.httpserver): the status families in one routing table — 201+Location, 400 vs 422, 405+Allow, 412, 429+Retry-After (out/A01_EndpointBasics.txt, A06, A08).

```d2
outcome: request outcome
ok: 2xx {
  r200: 200 read/update done
  r201: 201 created + Location
  r202: 202 accepted, async
  r204: 204 done, no body
}
redir: 304 reuse cache copy
cerr: 4xx client's fault {
  c400: 400 malformed
  c422: 422 invalid content
  c401: 401 who are you
  c403: 403 not allowed
  c404: 404 no resource
  c409: 409 state conflict
  c429: 429 slow down
}
serr: 5xx server's fault
outcome -> ok
outcome -> redir
outcome -> cerr
outcome -> serr
```

**Fig. 1.** The status classes an API design actually uses, grouped by whose fault the outcome is.

> [!warning] 401 is the most commonly misused code
> "Unauthorized" sounds like authorization and gets thrown for permission failures; it means authentication failed (or is required — with WWW-Authenticate). Permission failure is 403. Conflating them misleads every client-side error handler that distinguishes "re-login" from "do not retry".

> [!tip] Interview answer
> I carry the outcome class in the status and details in the body: 200, 201 with Location, 202 for accepted async work, 204 for body-less success, 304 for conditional GET. On the failure side: 400 for malformed input versus 422 for well-formed but semantically invalid, 401 for missing auth versus 403 for denied permission, 404, 405 with Allow, 409 for conflicts, 412 for failed preconditions, 415 for wrong media types, 429 with Retry-After, and 5xx only for server faults. No 200-with-error-body.
