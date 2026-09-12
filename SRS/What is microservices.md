<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices #SRS

# What is microservices

> [!abstract] Short answer
> The microservice architectural style builds an application as a suite of small, independently deployable services, each running in its own process, owning its data, and communicating over lightweight mechanisms such as HTTP APIs or lightweight messaging. It trades the monolith's single deployable for per-team autonomy and per-service scaling, at the cost of running a distributed system.

## The defining traits

Fowler and Lewis characterize the style by nine common traits, and any interview answer should hit the load-bearing ones:

* **Componentization via services** - components are out-of-process services linked by calls, not in-process libraries, so they can be deployed and replaced independently.
* **Organized around business capabilities** - service boundaries follow business functions, not technical layers; Conway's law made explicit.
* **Smart endpoints and dumb pipes** - logic lives in the services; the transport stays simple (HTTP or lightweight messaging), the opposite of a heavyweight bus transforming traffic in the middle.
* **Decentralized data management** - each service owns its storage; see [[How would you explain the database per service pattern]].
* **Decentralized governance** - teams choose their own tools instead of one mandated standard.
* **Design for failure** - the network will fail, so consumers handle unavailability, degradation, and retries.
* **Infrastructure automation** - CI/CD pipelines and automated provisioning make many deployables survivable.
* **Products not projects** - teams own services long-term.
* **Evolutionary design** - services are replaceable building blocks, decomposed progressively.

```d2
direction: right
mono: "Monolith\none process, one database\nscale = replicate everything" {
  width: 300
  height: 100
  style.fill: "#ffebee"
}
split: "Decompose by capability" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
web: "Orders service\n+ own DB" {
  width: 200
  height: 90
  style.fill: "#e8f5e9"
}
acc: "Accounts service\n+ own DB" {
  width: 200
  height: 90
  style.fill: "#e8f5e9"
}
rep: "Reporting service\n+ own DB" {
  width: 210
  height: 90
  style.fill: "#e8f5e9"
}
mono -> split
split -> web
split -> acc
split -> rep
```

**Fig. 1.** Decomposition turns one oversized deployable into independently deployable and independently scalable services, each with its own datastore - and turns every internal call into a network call.

```java
// Conceptual: a service owns its slice and speaks HTTP, nothing more
@RestController
class OrderController {
    private final OrderService orders;

    @PostMapping("/orders")
    ResponseEntity<OrderView> place(@RequestBody PlaceOrder cmd) {
        OrderView view = orders.place(cmd);   // orders DB only this service owns
        return ResponseEntity.accepted().body(view);
    }
}
```

**Listing 1.** A single service endpoint: the intelligence sits in the endpoint, the pipe stays plain HTTP.

## Where the style pays and what it costs

The wins: independent deployment per service, scaling only what needs scaling, team autonomy, and technology freedom per service - the upsides are the subject of [[What advantages do microservices have over a monolith]]. The costs are the standard distributed-systems bill: network latency and partial failure, eventual consistency across databases, operational complexity, and heavier testing. Decomposition is a project of its own - [[How do you decompose a monolith into microservices]] and the incremental [[What is the strangler fig pattern and when do you use it]] are the safe paths, while cross-service interactions still need deliberate choices from [[Which interaction styles do you know in microservices]] and edge concerns from [[What is the API gateway pattern in microservices]]. The style descends from SOA - [[How would you explain Service-oriented Architecture SOA]] - with finer services and decentralized infrastructure.

> [!warning] "Start every new project with microservices" is the classic overreach
> Fowler's own advice is monolith-first: a new system's service boundaries are unknown, and premature decomposition pays distributed-systems costs before earning any autonomy benefit. "Microservices are just SOA" is equally sloppy - the ESB-centric, enterprise-reuse version of SOA is a different animal.

> [!tip] Interview answer
> Microservices are independently deployable services organized around business capabilities, each owning its data and talking over lightweight pipes - smart endpoints, dumb pipes. I expect decentralized data management, design for failure, and heavy automation; I get per-service scaling and team autonomy but inherit a distributed system with eventual consistency and real operational load. I do not default greenfield projects to it: I justify it per team and per scaling need, decompose incrementally, and compare against SOA honestly when asked.
