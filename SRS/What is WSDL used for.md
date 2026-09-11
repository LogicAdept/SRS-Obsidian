<!--
reps: 0
priority: 0
-->
#API/SOAP #SRS

# What is WSDL used for

> [!abstract] Short answer
> WSDL (Web Services Description Language) is the XML contract document for a SOAP web service: it declares the message types (via XSD), the abstract operations, the concrete binding (protocol and message style), and the endpoint address. Tooling turns a WSDL into client stubs and server skeletons, which is why it enabled formal, cross-organization integration.

## The four sections, top to bottom

A WSDL 1.1 document reads in four layers. types holds XML Schema definitions of every message part — the actual data model, reusable and validated. message (1.1 terminology) names the input/output envelopes; portType assembles them into abstract operations — request-response, one-way, notification — with no transport or wire detail. binding makes it concrete: which protocol (SOAP 1.1 HTTP), which style and encoding (document/literal wrapped is the interoperable norm; rpc/encoded is the legacy minefield), and how faults map. service and port pin the address — where and how to call. The design point: abstraction layers let the same interface ride different bindings. WSDL 2.0 reorganized this (interface/binding/service, no message element) but 1.1 remains the interoperability standard in practice ([[What is SOAP]] for the runtime the contract governs).

```xml
<definitions xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">
  <types>  <xs:schema> ... OrderType, GetOrderRequest ... </xs:schema> </types>
  <message name="GetOrderRequest"> <part element="o:GetOrderRequest"/> </message>
  <portType name="OrderPort">
    <operation name="GetOrder">
      <input message="o:GetOrderRequest"/>
      <output message="o:GetOrderResponse"/>
    </operation>
  </portType>
  <binding name="OrderSoap" type="o:OrderPort">   <!-- soap:binding, document/literal -->
    <soap:binding transport="http://schemas.xmlsoap.org/soap/http" style="document"/>
  </binding>
  <service name="OrderService">
    <port name="OrderPort" binding="o:OrderSoap">
      <soap:address location="https://api.example.com/orders"/>
    </port>
  </service>
</definitions>
```

**Listing 1.** WSDL 1.1 skeleton (abridged): XSD types, abstract portType operations, SOAP binding, addressed port (conceptual, per W3C WSDL 1.1 note).

```d2
w: WSDL document
w.types: types (XSD)
data model
w.pt: portType
abstract operations
w.bind: binding
SOAP + style
w.svc: service/port
endpoint URL
w.types -> w.pt: messages
w.pt -> w.bind: implemented as
w.bind -> w.svc: deployed at
gen: wsdl2java -> stubs + skeletons
w -> gen: tooling input
```

**Fig. 1.** The layered document: data model, abstract interface, concrete binding, address — and the codegen it feeds.

## What it buys and what replaced it

WSDL's value was mechanical: publish the contract, and partners generate correct clients in any language — no human-readable docs needed for the wire truth; versioning becomes contract governance (new WSDL, new target namespace). Its costs are the same XML-era weight: generated code is voluminous, the abstraction layers leak (style/encoding choices break interop), and iterating a design through XSD edits is slow. OpenAPI now fills the descriptive role for REST — lighter, human-readable, generative in the same way ([[What is OpenAPI and how does Swagger relate to it]]); gRPC's .proto is the closest spiritual successor — a strict interface definition feeding multi-language codegen, minus the XML ([[What is the difference between RPC and gRPC]]). In interviews, WSDL signals you can navigate legacy enterprise integration: reading one, spotting document/literal versus rpc/encoded, and knowing wsimport-style tooling flows.

> [!warning] The binding section is where interop dies
> Two conformant stacks can still fail to interoperate over style/encoding choices (rpc/encoded's type serialization was the notorious case). "It is in the WSDL" never meant "it works across stacks" — the WS-I profiles exist precisely because the standard left too much room.

> [!tip] Interview answer
> WSDL is the machine-readable contract of a SOAP service: XSD types define the data model, portType declares abstract operations, binding makes them concrete as SOAP with a style, and service/port pins the endpoint address. Tooling generates stubs and skeletons from it, which made formal cross-org integration possible. It is the ancestor of OpenAPI and proto in spirit — heavier, XML-native, and still widespread in enterprise estates.
