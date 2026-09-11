<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration #SRS

# What is the Claim Check pattern?

> [!abstract] Short answer
> The **Claim Check** replaces message content with a **unique key**: the payload is stored in a repository, the message carries only the claim check, and a receiver retrieves the content later using the key — big bodies travel out-of-band while channels stay light.

## What a baggage claim check really does

A large document or image does not need to ride through every middleware hop — often it cannot (broker size limits) or should not (bandwidth, memory, or sensitive content passing through an untrusted party). The sender stores the content in a repository — a database, object store, or a dedicated message store — and sends a message containing only the key. The receiver, when it is ready, redeems the check and gets the full content. Camel's implementation names the operations after exactly this lifecycle: `Set` (store with key), `Get` / `GetAndRemove` (redeem, optionally consuming it), plus `Push`/`Pop` stack variants for nested use. Two motivations coexist and should not be confused: **efficiency** (thin messages through the flow) and **confidentiality** (the body never crosses middleware you do not trust — only the key does). Related pieces: storage plumbing is a [[What is the Message Store pattern]], and the selective removal of data from the moving copy is the [[What is the Content Filter pattern]].

```d2
direction: right
s: "Sender\nbig payload" {
  width: 170
  height: 60
  style.fill: "#e3f2fd"
}
rep: "Repository\npayload stored" {
  width: 190
  height: 65
  style.fill: "#fff3e0"
}
ch: "Channel\nkey only" {
  width: 170
  height: 60
  style.fill: "#fff3e0"
}
r: "Receiver\nredeem claim check" {
  width: 200
  height: 65
  style.fill: "#e8f5e9"
}
s -> rep: "1. store"
s -> ch: "2. send key"
ch -> r: "3. receive"
r -> rep: "4. fetch" {
  style.stroke-dash: 4
}```

**Fig. 1.** The message hops stay small; the heavy hop happens once, between repository and final receiver.

## The four steps in order

```text
Step  Broker sees        Contents
----  -----------------  -------------------------------------
1     nothing            payload persisted, key generated
2     tiny message       header/body = claim check key
3     tiny message       receiver consumes key
4     nothing            key redeemed, payload loaded (maybe removed)
```

**Listing 1.** The flow is only safe if step 4 has an owner: keys nobody redeem, or payloads removed before a redelivered key arrives, are the pattern's two classic data-loss stories.

> [!warning] The repository inherits the messaging semantics you hoped to avoid
> Claims need TTL (a key is useless after the payload is evicted), consumers need idempotent redemption (at-least-once redelivery re-presents the same key), and retention rules must match the slowest legitimate consumer. A claim-check store is a production database with SLAs — treating it as a scratch space produces heisenbugs where messages "contain" nothing.

> [!tip] Interview answer
> A Claim Check stores a large or sensitive payload externally and sends just a unique key through the messaging system; the receiver redeems the key to fetch the content. It lightens channels, sidesteps broker size limits, and keeps bodies away from untrusted hops. The operational cost is a real repository with TTL, idempotent redemption, and retention aligned to consumers.
