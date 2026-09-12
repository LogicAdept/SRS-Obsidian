<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #Patterns/Architecture/Microservices/ServiceCollaboration #SRS

# What is a saga, and how would you explain one with a real-world example?

> [!abstract] Short answer
> A saga is a sequence of local transactions that together implement a business process spanning several services, where each step commits its own database and the process coordinates what happens next - and undoes previous steps with compensating transactions when one fails. There is no distributed lock or two-phase commit; consistency is achieved step by step, eventually: a sequence of local transactions across multiple services, coordinated so the overall process stays consistent.

## The two coordination styles

Choreography: no coordinator - each service performs its local transaction and publishes an event, and the next service reacts to that event. Simple for a few steps, harder to see the whole flow as step count grows. Orchestration: a dedicated coordinator (the saga orchestrator) tells each participant which operation to run and interprets the results. Explicit and easy to monitor, but the coordinator is an extra component to make reliable. The vocabulary worth repeating in interviews: compensable transactions (can be undone), pivot transactions (the point of no return - once a pivot succeeds, compensable transactions are no longer relevant), and retryable transactions (idempotent steps after the pivot that must eventually succeed). Each step commits its own aggregate; the per-transaction discipline is the aggregate rule from [[Why should one transaction update only one aggregate]].

```d2
direction: right
order: "Order: PENDING" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
inv: "Inventory: RESERVE" {
  width: 220
  height: 60
  style.fill: "#fff3e0"
}
pay: "Payment: CHARGE" {
  width: 220
  height: 60
  style.fill: "#fff3e0"
}
comp: "compensating\ntransactions" {
  width: 230
  height: 70
  style.fill: "#fde8e8"
}
done: "Order: CONFIRMED" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}
order -> inv -> pay
pay -> done: "success"
pay -> comp: "declined"
comp -> order: "release stock, cancel order"
```

**Fig. 1.** The pivot is the payment charge: before it, every step can be undone; after it, the remaining steps are retryable until the process completes.

## A concrete example

Trip booking from the Microsoft saga guidance: the customer books a car, a hotel, and a flight in one request. Three local transactions, three services. The flight charge is the pivot - once the airline ticket is issued, cancelling is not possible, only rebooking. If the car or hotel booking fails before the pivot, the saga runs compensations: cancel the flight booking and release whatever was reserved. If the payment database times out after the pivot, the charge step is retried - which is why retryable steps must be idempotent, or the customer gets charged twice ([[What is idempotency in HTTP and in messaging]]). Each step's local state change and the event announcing it must be committed together, which is what the transactional outbox is for ([[How would you explain the transactional outbox pattern]]). The reason the saga exists at all - what pushed two-phase commit out of the architecture - is [[Why is two-phase commit a poor fit for microservices]].

> [!tip] Interview answer
> A saga chains local transactions across services: each step commits its own data and triggers the next step via events or orchestration; a failure runs compensating transactions for everything that can still be undone. On the trip-booking example: car, hotel, flight are reserved, the flight charge is the pivot, and a hotel failure before it triggers cancellations instead of a two-phase commit. I name choreography vs orchestration and mention idempotent retries to show I have run one.
