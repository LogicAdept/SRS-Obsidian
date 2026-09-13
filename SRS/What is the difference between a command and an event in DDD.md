<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What is the difference between a command and an event in DDD?

> [!abstract] Short answer
> A command is an imperative request that something happen - PlaceOrder, CancelShipment - addressed to one known handler, which may reject it. An event is a past-tense fact that something did happen - OrderPlaced - published to anyone interested, which nobody can refuse or undo. Commands carry intent and can fail; events carry history and cannot. The pipeline "command in, state changed, events out" runs through that asymmetry.

## The two vocabularies

The mechanical tells: naming (imperative versus past tense), addressing (one handler versus many subscribers), cardinality (exactly one processor versus zero or many), and failure semantics (a command can be invalid, declined, or time out - an event has already happened and the only response is reaction). A rejected command changed nothing; a received event requires every consumer to decide what it means for their own model. That is why the verb tense in message names is not cosmetics: it encodes who owns the outcome. The immutability consequences are covered separately - events are frozen history, commands are frozen requests ([[Should commands and events be immutable]]).

```java
record PlaceOrder(long orderId, long customerId) {}    // command: imperative, to one handler
record OrderPlaced(long orderId, long customerId, long totalCents) {}   // event: past tense

order.place(42);                            // handler executes the command
System.out.println(order.pullEvents());     // [OrderPlaced[orderId=77, customerId=42, ...]]
```

**Listing 1.** Verified on JDK 21.0.12.1: the command `PlaceOrder` is executed by exactly one handler and, on success, the aggregate records `OrderPlaced` - intent goes in, fact comes out, and the names encode which is which.

```d2
direction: right
caller: "Caller\napp service / UI" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
cmd: "Command\nPlaceOrder\nimperative, one handler" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
agg: "Aggregate\nvalidates, mutates,\nrecords" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
evt: "Event\nOrderPlaced\npast tense, published" {
  width: 260
  height: 90
  style.fill: "#ffebee"
}
subs: "Subscribers\nzero or many\nreact in own tx" {
  width: 240
  height: 90
  style.fill: "#f3e5f5"
}
caller -> cmd
cmd -> agg: "executes or rejects"
agg -> evt: "records"
evt -> subs
```

**Fig. 1.** Commands flow toward one validator-executor and may die at its gate; events flow outward from a committed change and demand reaction, not permission.

## Where each one belongs

Commands are the application layer's input vocabulary: a use case receives one, loads aggregates, executes, commits. Events are the output vocabulary of committed change and the input of every consumer downstream - projections, policies, other aggregates, other contexts. Across bounded contexts the asymmetry becomes an integration decision: publishing an event preserves each context's autonomy (consumers translate and react), while sending a command across a boundary is a deliberate synchronous coupling that assumes the receiver's availability and right of refusal ([[Can you send a command or publish an event across bounded contexts]] works through that choice). In CQRS the pair is the grammar: commands mutate the write model, events fan out to rebuild every read model ([[What is a domain event in DDD]] covers the recording side).

> [!warning] Events addressed like commands
> The hybrid lie: "publish the OrderPlaced event to the Inventory service so it decrements stock". Publish-and-expect specific behavior is a command with worse error handling - if Inventory is the required performer, call it a command and own the rejection path; if Inventory is free to react whenever, stop expecting a particular side effect. The same confusion in reverse - subscribers "rejecting" events - produces dead letters that nobody owes anyone. Name the message for what it is and the failure modes sort themselves out.

> [!tip] Interview answer
> A command is an imperative, addressed request - one handler, may be rejected, expresses intent. An event is a past-tense fact - published, immutable, any number of subscribers, already happened. Commands are the write side's input; events are the output of committed change and everyone else's input. The tense in the name tells you who owns the outcome.

