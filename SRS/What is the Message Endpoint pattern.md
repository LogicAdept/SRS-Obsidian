<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Endpoints #SRS

# What is the Message Endpoint pattern?

> [!abstract] Short answer
> A **Message Endpoint** is the client code through which an application touches the messaging system: it converts between the application's native calls/data and messages on channels, so the rest of the application stays ignorant of channels, formats, and client APIs.

## The application's only port to the middleware

Endpoints are custom code on both axes — specific to this application and to this messaging system's client API. Inbound, an endpoint receives a message, extracts the contents, and hands them to the application in a meaningful form; outbound, it takes a command or piece of data, builds a message, and sends it on a particular channel. Everything else in the application deals only with domain types and method calls. This is the base contract from which the endpoint family specializes: [[What is the Messaging Gateway pattern]] (domain-facing facade), [[What is the Service Activator pattern]] (invoking services), the consumer styles [[What is the Polling Consumer pattern]] and [[What is the Event-Driven Consumer pattern]], plus the adapter for non-messaging apps in the [[What is the Channel Adapter pattern]].

```d2
direction: right
app: "Application\ndomain code only" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}
ep: "Message Endpoint\napp types <-> messages" {
  width: 230
  height: 70
  style.fill: "#fff3e0"
}
ms: "Messaging system\nchannels, client API" {
  width: 210
  height: 70
  style.fill: "#e3f2fd"
}
app -> ep -> ms```

**Fig. 1.** All messaging knowledge concentrates in one component per application.

## What the boundary absorbs

```text
Concern                     Lives in endpoint?   Lives in app?
--------------------------  -------------------  --------------
Channel names, destinations  yes                  no
Client API objects           yes                  no
Header manipulation          yes                  no
Domain logic                 no                   yes
```

**Listing 1.** The checklist for endpoint thinness: if domain decisions appear in endpoint code, the boundary has leaked.

> [!warning] Endpoints rot into hidden applications
> Retry loops, business validation, and database lookups that creep into endpoint code make the messaging layer stateful and untestable — and couple it to the domain it was supposed to insulate. Keep endpoints translating; give business logic its own home.

> [!tip] Interview answer
> A Message Endpoint is the piece of client code connecting an application to the messaging system: it turns domain calls and data into messages on channels and back, so the application never sees the client API or channel details. It is custom on both sides — app and middleware — and the whole endpoint family (gateways, activators, consumer styles) are specializations of it.
