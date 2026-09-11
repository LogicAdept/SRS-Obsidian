<!--
reps: 0
priority: 0
-->
#API/SOAP #SRS

# What is SOAP

> [!abstract] Short answer
> SOAP (Simple Object Access Protocol) is an XML-based messaging protocol standardized at W3C (SOAP 1.2): a message is an Envelope with an optional Header of processing directives and a mandatory Body carrying the payload or a Fault. It is transport-neutral — HTTP is the common binding, not a requirement — and its contract is described in WSDL.

## The envelope is the contract's runtime

Every SOAP message is a fixed XML envelope: the soap:Envelope wraps a soap:Header (zero or more header blocks, each addressed to a role — an intermediary that must process it — and optionally flagged mustUnderstand, meaning "reject the message if you cannot honor this block") and a soap:Body. The Body carries the application payload or, on failure, a soap:Fault with Code, Reason, Detail, and Role (1.2 structure; 1.1 used faultcode/faultstring). This header-block machinery is SOAP's real design idea: intermediaries process messages in standardized layers — security tokens (WS-Security), addressing (WS-Addressing), reliability (WS-ReliableMessaging) — without touching the payload. The HTTP binding maps a request-response exchange to POST with a SOAPAction header (1.1) or a media type (1.2), but nothing in the envelope assumes HTTP — SMTP bindings exist, which is why SOAP is called transport-neutral ([[What is WSDL used for]] for the static contract; [[What is the difference between an API and a web service]] for the era this defined).

```xml
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
  <soap:Header>
    <t:transaction xmlns:t="https://example.com/tx" soap:mustUnderstand="1">tx-42</t:transaction>
  </soap:Header>
  <soap:Body>
    <o:getOrder xmlns:o="https://example.com/orders">
      <id>7</id>
    </o:getOrder>
  </soap:Body>
</soap:Envelope>
```

**Listing 1.** The 1.2 envelope shape: a header block a router must understand, and the payload in the Body (conceptual, per W3C SOAP 1.2 Part 0 primer).

```d2
env: SOAP Envelope {
  hdr: Header (optional) {
    h1: block -> role: next intermediary
    h2: mustUnderstand=1 -> reject if not honored
  }
  body: Body (mandatory) {
    b1: application payload
    b2: Fault (Code, Reason, Detail) on failure
  }
}
http: HTTP binding (POST)
smtp: other bindings possible
env -> http: common carrier
env -> smtp: transport-neutral
```

**Fig. 1.** Header blocks carry processing directives for specific roles; the Body carries payload or Fault; the binding is swappable.

## Why it still exists, and where it does not

SOAP's strengths made it the enterprise standard of its era: a formal contract (WSDL), a rich WS-* standard library (security with signing and encryption at message level, reliable delivery, transactions), and transport independence. That same machinery is its weight: verbose XML envelopes, layered standards to implement correctly, tooling-sensitive interoperability (the history of WS-I profiles exists because stacks diverged). Modern designs reach the same goals over HTTP with OAuth2, TLS, idempotency keys, and OpenAPI contracts at a fraction of the complexity ([[How does SOAP differ from REST style web services]] for the head-to-head; [[How should you version a public API]] — WSDL fixed versioning formally). SOAP remains entrenched in banking, telecom, government, and ERP integrations — you will meet it as an integration obligation, rarely as a choice.

> [!warning] SOAP is not "XML over HTTP"
> The protocol lives in the envelope processing model — roles, mustUnderstand, the Fault structure, header blocks — not in the XML serialization. Treating a SOAP service like a plain XML HTTP endpoint ignores exactly the machinery enterprises adopted it for.

> [!tip] Interview answer
> SOAP is a W3C XML messaging protocol: a fixed Envelope with an optional Header of role-addressed, mustUnderstand-capable blocks and a mandatory Body holding payload or a structured Fault. It is transport-neutral — HTTP is just the common binding — and contracted via WSDL, with the WS-* family layering security and reliability on top. Heavy but formal: still an integration reality in banking and government, not a greenfield choice.
