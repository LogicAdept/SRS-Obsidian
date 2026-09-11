<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration #SRS

# What is the Message Translator pattern?

> [!abstract] Short answer
> A **Message Translator** is a filter between systems or steps that **converts one data format into another** — field renaming, structure reshaping, value mapping — so applications with proprietary data models can exchange messages without knowing each other's formats.

## Every system speaks its own dialect

Integrated applications are built on proprietary data models: the accounting system keys customers by taxpayer id, the CRM by phone and address; each expects messages shaped like its internals. Standards (industry XML formats, EDI) add a third dialect. The translator is the messaging equivalent of the GoF Adapter: it converts the interface — here, the message format — so the same business data flows between incompatible shapes. What it can and cannot do is the boundary worth stating in an interview: it works with what is **in the message** — rename `zip` to `postalCode`, restructure a list, map `"M"` to `"MALE"`. When the target needs data the message does not carry, that is a different pattern, the [[What is the Content Enricher pattern]]. At scale, pairwise translation explodes, which is why translators usually target a [[What is the Canonical Data Model pattern]], and the [[What is the Normalizer pattern]] is their composition into a type-switch.

```d2
direction: right
a: "CRM\ncustomer: {name, phone}" {
  width: 210
  height: 70
  style.fill: "#e3f2fd"
}
t: "Message Translator\nrename + reshape" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
b: "Accounting\ncustomer: {taxId, address}" {
  width: 220
  height: 70
  style.fill: "#ffebee"
}
a -> t -> b```

**Fig. 1.** The translator is the only component that knows both shapes; neither endpoint changes.

## Translation, not invention

```java
// In:  {"name":"Ivanov","phone":"+7-900-..."}
// Out: {"surname":"Ivanov","contacts":[{"kind":"mobile","value":"+7-900-..."}]}
CustomerCrm c = mapper.readValue(in, CustomerCrm.class);
AccountingCustomer out = new AccountingCustomer(
        c.name(),
        List.of(new Contact("mobile", c.phone())));
producer.send(accountingChannel, mapper.writeValueAsBytes(out));
```

**Listing 1.** Every field in the output traces back to the input; the moment it does not, the component has become an enricher and needs an external data source.

> [!warning] Translators accumulate silently and die by schema drift
> Each system upgrade that touches a shared entity changes one side's dialect, and the translator — nobody's product — breaks in production first. Keep translators stateless, generated from schema mappings where possible, and tested against versioned sample messages on both sides; otherwise the integration layer becomes the least-maintained code in the estate.

> [!tip] Interview answer
> A Message Translator converts messages from one data format to another between systems with proprietary models — renaming fields, reshaping structures, mapping values. It is the messaging analogue of the Adapter pattern and it only reshapes what the message already contains; missing data is the Content Enricher's job. With many systems, translators should target a canonical model instead of pairwise dialects.
