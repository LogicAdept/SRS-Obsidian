<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Messaging/ScatterGather #SRS

# What is the Scatter-Gather pattern?

> [!abstract] Short answer
> **Scatter-Gather** broadcasts one request to **multiple recipients** and then **aggregates their replies** back into a single response message — best quote wins, worst terms are ignored. Scatter and gather are two coupled halves: a distribution mechanism plus an [[What is the Aggregator pattern]].

## Broadcast the request, distill the responses

An order needs a quote; several suppliers could fill it, at different prices and dates; the best terms should win. The scatter-gather routes the request to all of them, then collects responses into one result. Two distribution variants exist. **Distribution via a recipient list**: the scatter-gather computes the recipient set and sends a copy to each — it controls exactly who is asked, at the cost of knowing each recipient's channel. **Auction**: the request is published on a publish-subscribe channel and everyone subscribed may answer — recipients self-select, the sender does not enumerate them. The gather half is an aggregator with a completeness strategy; in bidding scenarios a **timeout** or **first-best** strategy usually fits better than wait-for-all, because slow suppliers should not delay the answer. Both halves inherit their machinery: distribution from the recipient-list/pub-sub mechanics of [[What is the Publish-Subscribe Channel pattern]], collection from the [[What is the Aggregator pattern]] with [[What is the Correlation Identifier pattern]] keys.

```d2
direction: down
req: "Quote request" {
  width: 190
  height: 55
  style.fill: "#e3f2fd"
}
sc: "Scatter\nrecipient list or pub-sub" {
  width: 270
  height: 70
  style.fill: "#fff3e0"
}
s1: "Supplier 1" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}
s2: "Supplier 2" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}
s3: "Supplier 3" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}
ga: "Gather\naggregate + pick best" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
res: "Single response" {
  width: 180
  height: 55
  style.fill: "#e8f5e9"
}
req -> sc
sc -> s1
sc -> s2
sc -> s3
s1 -> ga
s2 -> ga
s3 -> ga
ga -> res```

**Fig. 1.** One request fans out to suppliers; replies converge into one distilled answer.

## The gather side is where it fails

```text
Strategy         Wait              Use when
---------------  ----------------  ----------------------------------
Wait for all     every reply       completeness matters, latency does not
Timeout          fixed window      approximate best is acceptable
First best       first reply       speed critical, quality secondary
Override         early good reply  stop waiting once score is high enough
```

**Listing 1.** The completeness table of the aggregator, applied to bids: pick deliberately — "wait for all" plus one dead supplier equals one stalled order.

> [!warning] Replies outlive the request
> Late replies arrive after the gather concluded and the state is gone; under at-least-once delivery the same quote may land twice. The gather side needs correlation keys, dedup, and a policy for stragglers — otherwise the second-best supplier silently fulfills an order priced by the first.

> [!tip] Interview answer
> Scatter-Gather broadcasts a request to multiple recipients and aggregates the replies into one response. The scatter is either a computed recipient list or an auction over a publish-subscribe channel; the gather is an aggregator whose completeness strategy — usually timeout or first-best for bids — decides latency and quality. Correlation and dedup matter because duplicates and late replies are routine.
