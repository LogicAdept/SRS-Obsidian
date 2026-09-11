<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #DataFormats/XML #SRS

# How do you use XML or EDI validators with an Invalid Message Channel

> [!abstract] Short answer
> Validators turn "the receiver could not process it" from a crash into a **classification**: run the XML Schema or EDI check first, and on failure route the message — with the reason attached — to the invalid channel. The pattern only pays off if invalidity is detected precisely, and validators are how you do that.

## Structured detection before parking

The Java standard tool for the XML half is `javax.xml.validation.Validator` — the API documentation defines it as "a processor that checks an XML document against `Schema`", loaded from a `SchemaFactory` for W3C XML Schema, invoked with `validate(source)`, and reporting failures through a supplied `ErrorHandler` or a thrown `SAXException`. The Javadoc's operational constraint matters in consumers: a validator object is **not thread-safe and not reentrant**, so each consuming thread holds its own. For EDI (EDIFACT/X12 documents), commercial integration suites ship dedicated validators — SAP Integration Suite, for example, lets an exception subprocess catch a failed step and put the message on a JMS queue such as `InvalidMessages` with a receiver adapter, and documents XML Validator and EDI Validator as the checks you can place ahead of the parking decision. Custom checks — body length, required headers — slot into the same pre-parking stage; the reason attached at this point is what later makes triage possible ([[How does an error handler consume from the Invalid Message Channel]]).

```java
Validator v = schemaFactory.newSchema(xsd).newValidator();  // Conceptual
try {
    v.validate(new StreamSource(bytes));
    process(bytes);
} catch (SAXException e) {
    parkOnInvalidChannel(bytes, e.getMessage());   // reason travels with payload
}
```

**Listing 1.** Conceptual receiver flow: schema validation gates processing; a failed validation parks the message with its reason instead of crashing.

> [!warning] Weak identification starves the quarantine
> A receiver that parks everything with the reason "parse failed" forces triage to re-derive what was wrong from raw bytes. The tooling note behind this card rates the pattern by the ability to create the invalid channel, not by how good the identification is — but the diagnostic value comes from the validator, and "an invalid field value" can also be a business failure rather than a messaging one, the boundary in [[Why should you not treat an application error as an invalid message]].

> [!tip] Interview answer
> Put structured validation before the parking decision: XML Schema validation with `javax.xml.validation.Validator` (one validator per thread — the class is not thread-safe), EDI validators where the suite provides them, custom header and length checks otherwise. On failure, route the message to the invalid channel with the validator's reason attached, so the error handler gets a diagnosis, not just a corpse.
