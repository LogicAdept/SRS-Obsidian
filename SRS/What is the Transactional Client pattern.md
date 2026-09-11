<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/TransactionalClient #SRS

# What is the Transactional Client pattern?

> [!abstract] Short answer
> A **Transactional Client** makes its **session with the messaging system transactional**, so the client — sender or receiver — decides the transaction boundaries: a message is not really on the channel until the sender commits, and not really removed until the receiver commits.

## Who draws the boundary

A messaging system is transactional internally; the pattern is about giving the external client control of that boundary. Sender side: with the session uncommitted, the message is invisible to consumers — atomic with whatever else the sender's transaction did. Receiver side: the message is not actually removed from the channel until the receiver commits; a rollback puts it back (redelivery). The two sides are independent — a transactional sender can talk to a non-transactional receiver and vice versa, and a channel can mix both kinds of senders and receivers. In JMS this is `createSession(true, SESSION_TRANSACTED)` plus `commit()`/`rollback()`; Spring's `@Transactional` with a `ChainedKafkaTransactionManager`-style setup or JMS `SessionTransacted` listeners expresses the same control. The transactional receiver is the first defense that turns broker redelivery from a data-loss risk into a correctness mechanism — completed by [[What is the Idempotent Receiver pattern]] for duplicate handling; Kafka-specific transaction semantics are in [[What are Kafka commitSync and commitAsync for]] and [[How do you achieve exactly-once processing in Kafka]].

```d2
direction: down
send: "Sender\nbusiness work + send" {
  width: 240
  height: 65
  style.fill: "#e3f2fd"
}
tx1: "commit()" {
  width: 120
  height: 45
  style.fill: "#fff3e0"
}
ch: "Channel\nmessage now visible" {
  width: 240
  height: 60
  style.fill: "#fff3e0"
}
rx: "Receiver\nprocess + commit" {
  width: 220
  height: 65
  style.fill: "#e8f5e9"
}
rb: "rollback()\nmessage returns" {
  width: 190
  height: 55
  style.fill: "#ffebee"
}
send -> tx1 -> ch -> rx
rx -> rb: "on failure"
rb -> rx: "redelivery" {
  style.stroke-dash: 4
}```

**Fig. 1.** Both ends draw their own boundary; rollback at either end leaves no visible trace on the channel.

## JMS transacted session

```java
Session session = connection.createSession(true, Session.SESSION_TRANSACTED);
producer.send(queue, orderMessage);      // invisible until commit
session.commit();                        // boundary: now it is on the channel
// receiver: listener processes, container commits; on exception -> rollback
```

**Listing 1.** The commit call is the whole pattern: everything before it can be undone as one unit.

> [!warning] Client transactions are not distributed transactions
> The messaging transaction covers the channel leg only — the database update and the send are still two systems unless you coordinate them (JTA/XA, Kafka transactions, or an outbox design). And rollback-driven redelivery without idempotent handlers converts a failed message into a duplicate-processing machine: redelivery is guaranteed, at-least-once is the contract.

> [!tip] Interview answer
> A Transactional Client controls the transaction boundaries of its messaging session: senders' messages become visible only on commit, receivers remove them only on commit, and rollback triggers redelivery. The sender's and receiver's transactions are independent. It pairs with idempotent receivers because the delivery contract becomes at-least-once, and it does not by itself make the database and the broker atomic.
