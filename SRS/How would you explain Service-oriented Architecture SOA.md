<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/SOA #SRS

# How would you explain Service-oriented Architecture SOA

> [!abstract] Short answer
> SOA is an architectural style that organizes software as discrete, remotely callable services - reusable units of business functionality that communicate over a network through standardized, self-describing interfaces, historically WSDL and SOAP plus an enterprise service bus. Its goals are reuse and interoperability across an enterprise; microservices later re-cut the same idea with finer granularity and decentralized infrastructure.

## The mechanics

A service is a discrete unit of functionality that can be accessed remotely and updated independently, presenting a black-box interface that hides its implementation. Services publish machine-readable descriptions of their operations and message formats - in the classical stack, WSDL contracts over SOAP - so consumers bind to the description, not to the implementation. IBM's definition stresses the practical goal: software components become reusable and interoperable through service interfaces, so applications can be assembled from building blocks instead of being rewritten.

The widely cited principles of service-orientation include:

* **Standardized service contract** - services advertise a communications agreement.
* **Loose coupling** - services minimize mutual assumptions; reference autonomy and location transparency.
* **Service abstraction** - logic beyond the contract stays a black box.
* **Service autonomy** - a service controls its own runtime and logic.
* **Statelessness** - state is externalized so requests stay composable.
* **Discoverability and reusability** - services can be found and composed into new applications.

```d2
direction: right
c1: "Consumer app A" {
  width: 210
  height: 70
  style.fill: "#e3f2fd"
}
c2: "Consumer app B" {
  width: 210
  height: 70
  style.fill: "#e3f2fd"
}
esb: "Enterprise Service Bus\nrouting, transformation,\nprotocol mediation" {
  width: 280
  height: 100
  style.fill: "#fff3e0"
}
s1: "Customer service" {
  width: 210
  height: 70
  style.fill: "#e8f5e9"
}
s2: "Billing service" {
  width: 210
  height: 70
  style.fill: "#e8f5e9"
}
c1 -> esb
c2 -> esb
esb -> s1
esb -> s2
```

**Fig. 1.** The classical SOA deployment puts a bus between consumers and services; the bus carries the routing and translation weight that individual services then do not have to.

## SOA versus microservices

Both are service-oriented styles; the difference is in granularity and infrastructure. SOA aimed at enterprise-wide integration and reuse, with an ESB centralizing routing, transformation, and protocol mediation, and services often sharing data stores through the bus. The microservices style in [[What is microservices]] flips the control: smart endpoints and dumb pipes, decentralized data, and deployment per service. The practical bridge between the two worlds is that both need traffic management at the network edge - [[What is the API gateway pattern in microservices]] is the modern, thinner answer to what an ESB did, and [[How would you explain the service mesh pattern]] moves resiliency into sidecars instead.

> [!warning] SOA is not SOAP and an ESB is not SOA
> SOA is an architectural style; SOAP is one protocol that implementations often used, and you can build SOA over REST-style interfaces too. IBM itself notes the ESB became so identified with SOA that the terms are used as synonyms, which is exactly the confusion to avoid in an interview.

> [!tip] Interview answer
> SOA is the architectural style of discrete, independently accessible services communicating through standardized, self-describing contracts, historically SOAP/WSDL with an enterprise service bus mediating between them. Its enterprise goals are reuse and interoperability, backed by principles like standardized contracts, loose coupling, abstraction, and statelessness. I would place it on the line that runs from distributed computing to today's microservices, and I would compare it with [[What is SOAP]] as the protocol it rode on and [[How does SOAP differ from REST style web services]] for how the interface style moved on.
