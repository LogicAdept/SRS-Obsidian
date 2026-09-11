<!--
reps: 0
priority: 0
-->
#API/REST #SRS

# What is HATEOAS

> [!abstract] Short answer
> HATEOAS (Hypermedia as the Engine of Application State) is the uniform-interface constraint that makes responses drive the interaction: a client starts at one entry URI and thereafter discovers what it can do next from links inside representations, instead of hard-coding endpoint knowledge. It is the reason a browser user needs no web-spec to click through a site.

## How the engine works

The client holds no map of the API beyond the entry point and a vocabulary of link relations. A representation of /orders/7 carries links: self, and while the order is cancellable, a cancel link with its method; once cancelled, the link disappears — the server's state change just removed an action from the client's menu without any client redeploy. That is the "engine of application state": transitions are published as hypermedia. The client follows rel names (self, next, cancel, or namespaced curies), never concatenates URLs, and never embeds knowledge like "after POST /orders, poll /jobs/N" — that workflow lives server-side ([[What is a resource in a RESTful context]] for representation-level thinking; [[What is HAL in REST APIs]] for the concrete media type encoding).

```text
step1 self: {"id":7,"status":"NEW","links":[{"rel":"self","href":"/orders/7","method":"GET"},{"rel":"cancel","href":"/orders/7/cancellation","method":"POST"}]}
step2 follow rel=cancel -> POST /orders/7/cancellation
step3 self after: {"id":7,"status":"CANCELLED","links":[{"rel":"self","href":"/orders/7","method":"GET"}]}
step4 rel=cancel now absent -> null
```

**Listing 1.** Verified on JDK 21 (com.sun.net.httpserver): the client follows the cancel rel from the representation; after cancellation the link disappears — the server withdrew the affordance (out/A12_Hateoas.txt).

```d2
entry: / (entry point)
o: /orders/7 {
  links: self, cancel
}
c: /orders/7/cancellation {
  shape: document
}
entry -> o: follow self/next
o -> c: rel=cancel (only while NEW)
o: after cancel: links = self only
```

**Fig. 1.** State transitions are advertised as links; the same representation in another state offers different actions.

## What it buys, and the honest cost

The property Fielding insists on: clients survive server changes — moved endpoints, added steps, new workflows — because no client logic names URLs or encodes the state machine. Workflow changes deploy server-side only. The cost is equally real: clients and frameworks must understand link structures (generic hypermedia clients instead of generated SDKs that bake in paths), payloads grow, and designing a stable link-relation vocabulary is work. This is why mainstream "REST" APIs stop at level 2 of the Richardson Maturity Model and ship SDKs with baked-in routes — a defensible engineering trade, but then the claim "we have HATEOAS" is false ([[What does RESTful mean compared with REST]] for the maturity vocabulary; [[What is REST]] for the constraint's home). HTML over HTTP is the existence proof that hypermedia scales to the whole web.

> [!warning] Link text is not HATEOAS
> Scattering URLs in JSON bodies that clients still parse and hard-code buys nothing — the engine-of-state property requires clients to select next actions by rel semantics, not by path templating. A links array the SDK ignores is decoration.

> [!tip] Interview answer
> HATEOAS makes hypermedia the engine of application state: responses carry links that say what the client can do next, so the client only knows the entry URI and a vocabulary of relations. Cancel an order and the cancel link disappears — the server withdrew the affordance without a client release. It buys real decoupling of workflows, at the cost of generic clients and payload weight, which is why most production APIs consciously stop at Richardson level 2.
