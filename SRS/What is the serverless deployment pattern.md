<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/Deployment #SRS

# What is the serverless deployment pattern

> [!abstract] Short answer
> Serverless deployment: package the service's code, upload it to a managed runtime - AWS Lambda, Google Cloud Functions, Azure Functions - and let the platform run and scale it without exposing any server, VM or container to you. Billing is per invocation; scaling is automatic; in exchange you accept a constrained runtime: stateless functions, limited languages, restricted input sources and cold-start latency.

## Mechanism: code in, events in, no servers out

You ship a ZIP (for Java, a JAR) containing the handler, declare memory and timeout limits, and wire the function to its triggers. AWS Lambda - the worked example - supports four invocation routes: an event from another AWS service (S3 object created, DynamoDB item changed, Kinesis record available), an HTTP request routed through API Gateway, a direct call via the Lambda API, and a cron-like periodic schedule. On invocation, the platform finds a warm instance of the function or launches one; under the hood it isolates instances with containers on EC2 - but those details are deliberately invisible. The unit you manage is the function, not the fleet: no OS patching, no instance sizing, no autoscaler configuration. Cost follows usage - billed per invocation, in 100 ms time increments and memory consumed - which makes serverless the pay-per-request end of the deployment spectrum, opposite the always-on end where [[What is the service per VM pattern]] and [[What is the service per container pattern]] live.

```d2
direction: right
dev: "Developer
packages handler + limits" {style.fill: "#e8f5e9"}
fn: "AWS Lambda function
stateless handler" {style.fill: "#fff3e0"}
ev: "Event sources
S3, DynamoDB, Kinesis" {style.fill: "#eceff1"}
gw: "API Gateway" {style.fill: "#eceff1"}
cron: "Schedule" {style.fill: "#eceff1"}
dev -> fn: upload ZIP
ev -> fn: invoke
gw -> fn: HTTP invoke
cron -> fn: invoke
```

**Fig. 1.** The function is the only artifact the developer owns; the platform owns instances, scaling and isolation beneath it.

The strategic benefit is operational, not financial: all infrastructure below the function - OSes, VMs, container scheduling - is someone else's responsibility, so a small team ships a whole service without a platform crew. This is also the deepest expression of the deployment-platform idea: [[What is the service deployment platform pattern]] names the general abstraction (a named, load-balanced set of instances), and serverless is its most aggressive implementation.

## The constraints that shape architecture

The drawback list is architectural, and interviewers expect it. Language and runtime limits: the platform supports a fixed set of runtimes and versions. Statelessness is mandatory: long-running or stateful workloads - a database, a message broker, anything with in-memory sessions - do not fit the model. Input sources are restricted: a Lambda cannot, say, subscribe to RabbitMQ the way a real service can, so serverless couples you to the provider's event ecosystem. Startup latency: cold starts (provision an instance, initialize the runtime - notoriously slow for JVM-based functions) punish spiky, latency-sensitive traffic, and the platform can only react to load, never pre-provision for it. And quick startup is a requirement: a service that takes minutes to boot is useless as a function. These constraints push real designs toward hybrids - API Gateway plus Lambda for sporadic endpoints and event processors, containers for the core long-lived services.

> [!warning] Serverless is someone else's ops team
> The convenience is real but so is the coupling: provider-specific event formats, IAM integration, limits and quotas leak into your design, and moving a deeply-integrated function fleet to another provider is a rewrite of its glue, not a redeploy. Second trap: hidden state or long-running work inside a function - a 15-minute timeout kills the batch job mid-write; design functions as small, retryable, idempotent steps, because at-least-once invocation is the platform's contract.

> [!tip] Interview answer
> Serverless deployment means uploading packaged code to a managed runtime like AWS Lambda and letting the platform run, scale and isolate it - invoked by events, HTTP via API Gateway, API calls or schedules, billed per invocation. It removes all infrastructure work and scales automatically, but forces stateless, quick-starting functions, limited runtimes and input sources, and cold-start latency. I use it for event-driven and spiky workloads, containers for long-lived core services.
