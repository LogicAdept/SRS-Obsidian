<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/ServiceDiscovery #SRS

# What is the third-party registration pattern in microservices

> [!abstract] Short answer
> Third-party registration is the registration style where a deployment platform component — the registrar — registers a service instance with the registry on the instance's behalf: the instance itself never talks to the registry. The registrar observes instances (as it deploys, restarts or kills them) and keeps the registry in sync with reality. It is the contrast case to self registration and the natural mode on platforms that already own instance lifecycle.

## The mechanics: the platform knows first, anyway

The orchestrator or deployment platform is the first to know when an instance starts, crashes or is replaced — so it is the best source of registration truth. The registrar watches the platform's state (deployments, processes, VMs), and for every running instance performs the registry interaction: register on start with location and metadata, re-assert or heartbeat while it runs, deregister on termination. The instance stays ignorant: no registry credentials, no SDK, no heartbeat code. Benefits: uniform behavior for every runtime — a legacy app, a script, a polyglot service are all registered identically (this is the polyglot argument that also drives server-side discovery, [[How would you explain server side service discovery]]); no failure mode where a buggy app forgets to deregister and pollutes the registry; and platform metadata (zone, deployment version) lands in the registry for free. Costs: the registrar is critical glue — if it lags, the registry drifts from reality in both directions; and it is one more component per platform to operate ([[How would you explain the service registry pattern]] defines the registry both styles feed; Registrator on Docker and Kubernetes-style platform integration are Richardson's examples).

```d2
direction: down
plat: "Deployment platform
deploy / restart / kill" {style.fill: "#eceff1"}
reg1: "Registrar
watches platform state" {style.fill: "#e3f2fd"}
reg2: "Registry" {shape: cylinder; style.fill: "#fff3e0"}
app: "Service instance
ignorant of registry" {style.fill: "#e8f5e9"}
plat -> reg1: events
reg1 -> reg2: register / heartbeat / deregister
plat -> app: runs
```

**Fig. 1.** The registrar is the platform's shadow writer: instances come and go; the registry mirrors the platform, not the app's cooperation.

## Self registration versus third party — choosing per constraint

Self registration ([[How would you explain self registration with a service registry]]) puts the logic in the instance: simplest platforms, but every language needs the library and a crashed instance can leave a stale entry unless leases expire it. Third-party registration moves the logic to the lifecycle owner: uniform across runtimes and immune to app-level registration bugs, but binding the registry's accuracy to the registrar's health. The choice usually follows the platform: on orchestrators the platform effectively forces third-party style (it owns the truth anyway); on plain VMs, self registration with lease expiry is the pragmatic default. Either way, the registry side must treat registration as advisory and keep lease-based expiry as the backstop — a registrar that fails silently must not leave dead entries routing traffic ([[What is the health check API pattern]] supplies the deeper liveness signal that registries and balancers act on).

> [!warning] A stale registration is a traffic-routing bug, whoever registers
> Third-party registration shrinks the staleness window but does not eliminate it: a partitioned registrar stops updating, an instance can be dying between platform health and registry state. The registry still needs TTLs and the consumers still need the dead-instance path (timeouts, retry on another candidate). Registration style decides who writes entries; it never removes the reader's duty to distrust them.

> [!tip] Interview answer
> In third-party registration the deployment platform's registrar updates the registry on the instance's behalf — register on start, heartbeat while alive, deregister on termination — so instances never carry registry code. It's uniform across runtimes and immune to app-level registration bugs, at the cost of a critical registrar component. I get this style for free on orchestrators; on plain VMs I'd lean self registration with lease expiry and keep TTLs as the backstop either way.
