<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Messaging/GuaranteedDelivery #SRS

# What is the Guaranteed Delivery pattern?

> [!abstract] Short answer
> **Guaranteed Delivery** makes the messaging system **persist messages to disk** so they survive crashes: once the send returns, the message is stored on at least one machine and is not deleted from one store until it has been forwarded to and stored in the next — until a receiver acknowledges it.

## Store-and-forward, hop by hop

Each machine running the messaging system has its own local data store. The sender's send operation does not complete successfully until the message is safely stored in the sender's store; the message is then not deleted from one store until it is successfully forwarded to and stored in the next store on its path. Once the send succeeds, the message is on disk on at least one computer until it is delivered and acknowledged by the receiver. This is a chain of local guarantees — not an end-to-end application protocol. In RabbitMQ it means **durable queues plus persistent messages** (both, not either); in Kafka, durability comes from the replicated commit log and acks settings; in JMS it means persistent delivery mode with a transactional or client-acknowledge session.

```d2
direction: right
s: "Sender" {
  width: 150
  height: 55
  style.fill: "#e3f2fd"
}
st1: "Store 1\nsender side" {
  width: 160
  height: 65
  style.fill: "#fff3e0"
}
st2: "Store 2\nbroker side" {
  width: 160
  height: 65
  style.fill: "#fff3e0"
}
r: "Receiver\nack deletes" {
  width: 170
  height: 65
  style.fill: "#e8f5e9"
}
s -> st1: "send completes\nafter fsync"
st1 -> st2: "forward, then delete"
st2 -> r: "deliver"
r -> st2: "ack" {
  style.stroke-dash: 4
}```

**Fig. 1.** Each store keeps the message until the next hop confirms storage; the ack from the receiver is what finally removes it.

## JMS persistence knobs

```java
producer.setDeliveryMode(DeliveryMode.PERSISTENT); // write to store
producer.setTimeToLive(60_000);
producer.send(queue, textMessage);      // returns only after persist
session = connection.createSession(true, Session.SESSION_TRANSACTED);
// ... and commit() to make the send visible
```

**Listing 1.** Persistent delivery mode plus a transacted session: the message survives a broker crash, and the commit draws the transaction boundary for when it becomes visible.

> [!warning] Persistence is not a delivery guarantee to the application
> Guaranteed Delivery promises the message survives the messaging system's failures — it does **not** promise your handler succeeded, did not run twice, or ran exactly once. Crashes between receive and business-commit still need [[What is the Idempotent Receiver pattern]] semantics or coordinated [[What is the Transactional Client pattern]] sessions; persistence alone covers only the transport leg.

> [!tip] Interview answer
> Guaranteed Delivery means the messaging system persists messages to a local store at every hop: the send only succeeds after the store has it, and each store keeps the message until the next hop confirms. Combined with receiver acknowledgment, the message survives broker crashes. In RabbitMQ you need durable queues and persistent messages together; and note it says nothing about application-level effects — duplicates still happen.
