<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Messages/EnvelopeWrapper #SRS

# What is the Envelope Wrapper pattern?

> [!abstract] Short answer
> An **Envelope Wrapper** wraps application data in an envelope that satisfies the **messaging infrastructure's requirements** — mandatory header fields, encryption, signatures — and unwraps it at the destination, so endpoints never see infrastructure fields and infrastructure never sees raw app data.

## Two worlds with different format demands

Most messaging systems split messages into header and body, and the header carries fields the infrastructure needs to manage flow. Endpoint systems frequently have no idea these fields exist — or actively reject them as malformed because they violate the application's expected format. Conversely, routing middleware may treat a message without proper header fields as invalid. The wrapper bridges both directions: on the sending side it builds the envelope around application data (adding headers, encrypting, signing); on the receiving side it strips the envelope, leaving the application exactly the format it expects. The wrapping process is symmetric — wrap, transport, unwrap — which is why it pairs naturally with an [[What is the Format Indicator pattern]] (the envelope says what is inside) and a [[What is the Message Translator pattern]] (which may run inside the envelope conversion). Unlike a translator, the wrapper does not touch the payload's meaning: it adds or removes **layers**, not fields.

```d2
direction: right
app: "App data\nprivate format" {
  width: 180
  height: 60
  style.fill: "#e3f2fd"
}
w: "Envelope Wrapper\nadd headers, encrypt" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
ch: "Channel\ninfrastructure reads envelope" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
u: "Envelope Unwrapper\nstrip, decrypt" {
  width: 210
  height: 70
  style.fill: "#fff3e0"
}
app2: "Receiver app\nprivate format" {
  width: 180
  height: 60
  style.fill: "#e8f5e9"
}
app -> w -> ch -> u -> app2```

**Fig. 1.** The payload is unchanged; everything the middleware requires lives in the added layer.

## What wrapping adds, what unwrapping removes

```text
Layer                Added by wrapper            Removed by unwrapper
-------------------  --------------------------  ---------------------------
Transport headers    message id, TTL, priority   all infrastructure fields
Security             encryption, signature       envelope, after verify
Routing metadata     reply address, slip         before app deserialization
App payload          passed through untouched    passed through untouched
```

**Listing 1.** The invariant row is the last one: wrapping never alters the application payload — that is the translator's territory.

> [!warning] Wrapped systems need matching versions of both envelopes
> The sender's wrapper and receiver's unwrapper are a distributed pair with no shared build; when one side upgrades header layout or crypto, the other fails closed on every message. Version the envelope, negotiate or dual-read during migration, and monitor unwrap failures — they are format regressions, not application errors.

> [!tip] Interview answer
> An Envelope Wrapper adds whatever the messaging infrastructure demands — headers, encryption, routing metadata — around application data, and unwraps it at the destination, so apps keep their private formats and middleware keeps its contract. It differs from a translator: the payload's meaning is untouched, only layers are added or removed. Both ends must agree on the envelope version.
