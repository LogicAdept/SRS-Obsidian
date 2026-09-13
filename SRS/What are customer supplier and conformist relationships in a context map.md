<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What are customer-supplier and conformist relationships in a context map?

> [!abstract] Short answer
> Both patterns describe an upstream context feeding a downstream one. Customer-supplier: the upstream team treats the downstream as a customer - the two teams negotiate the contract, and upstream accepts work requests that serve downstream's model. Conformist: the downstream drops ambition to translate and simply adopts the upstream's model as-is. The difference is who bends: negotiated contract versus downstream conformity.

## Customer-supplier: negotiated integration

The relationship fits when both sides matter to the business and both teams control their own models: the upstream exposes what downstream needs through a negotiated interface, and changes go through the negotiation instead of breaking it. The upstream team plans its roadmap partly around downstream requests - that commitment is what distinguishes the pattern from "downstream hopes upstream is stable". The negotiated contract typically becomes an explicit protocol with its own versioning, which is why customer-supplier pairs naturally with an open host service on the upstream side ([[What are the open host service and published language patterns]]). Failure mode: upstream without incentive drifts its internal model, the "negotiated" contract rots into breaking changes, and the downstream discovers it was never really a customer.

## Conformist: deliberate adoption

Conformist is the decision to not translate at all: the downstream model adopts the upstream's vocabulary, fields, and even its naming quirks, so no mapping layer exists. This is rational when the upstream is a platform or an industry standard you cannot influence, when its model is actually good enough for your domain, or when the translation cost exceeds the modeling benefit. The saving is real: zero mapping code, zero drift between representations, instant access to upstream changes. The cost is equally real: the downstream's ubiquitous language now has a landlord, and if the upstream renames a field, the rename propagates straight into your model.

```java
// Upstream published contract.
record UpstreamCustomerDto(String first_name, String last_name, String status_code) {}

// Conformist downstream: upstream vocabulary appears unchanged in local code.
String render(UpstreamCustomerDto dto) {
    return dto.first_name() + " " + dto.last_name() + " [" + dto.status_code() + "]";
}

// Translated downstream: a small mapper keeps the model in its own language.
LocalCustomer local = Translator.toLocal(dto);   // -> name + Standing.TRUSTED
```

**Listing 1.** Verified on JDK 21.0.12.1: the conformist path echoes `status_code` verbatim, while the translated path converts it to a local `Standing` - the trade is mapping code versus vocabulary leakage.

```d2
direction: right
up: "Upstream team\nowns its model" {
  width: 230
  height: 80
  style.fill: "#e3f2fd"
}
down: "Downstream team\nowns its model" {
  width: 230
  height: 80
  style.fill: "#e8f5e9"
}
up -> down: "customer-supplier:\nnegotiated contract"
plat: "Platform upstream\nnot negotiable" {
  width: 230
  height: 80
  style.fill: "#fff3e0"
}
conf: "Conformist downstream\nadopts upstream model" {
  width: 230
  height: 80
  style.fill: "#ffebee"
}
plat -> conf: "conformity\nno translation"
```

**Fig. 1.** Customer-supplier keeps two models and negotiates the seam; conformist collapses the seam by letting one model rule both sides.

## Choosing between them

Ask the leverage question: can the downstream team influence the upstream's model? With influence and mutual interest, negotiate - customer-supplier. Without influence, the honest options are conformist (accept their world) or an anti-corruption layer (translate at the edge, [[What is the anti-corruption layer pattern]]); pick conformist when their model is tolerable and the integration is broad, translate when their model would poison yours. Both patterns are decisions to record on the context map ([[What is context mapping in DDD]]), because the worst outcome is conformism by accident - no one decided, the mapping layer just never got written.

> [!warning] Accidental conformism
> The dangerous state is not chosen conformity but unexamined conformity: a consumer starts deserializing upstream DTOs straight into the domain because it was fastest that sprint, and five years later the "temporary" vocabulary is load-bearing. If the upstream model must not leak, the mapping layer has to exist from the first week - it can be ten lines, but it must exist.

> [!tip] Interview answer
> Customer-supplier means the upstream team serves the downstream: two autonomous models, a negotiated contract, changes through agreement. Conformist means the downstream gives up translation and adopts the upstream model as-is - cheaper integration, but your vocabulary follows theirs. Choose by leverage: negotiate when you can influence upstream, conform when you cannot and their model is tolerable, and put an anti-corruption layer between when it is not.

