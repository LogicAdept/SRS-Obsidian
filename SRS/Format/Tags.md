For tags, use the following rules:

1. The **#New** tag is placed on cards that are **not yet answered** (empty) or have an **incomplete / draft** answer; when the card is brought to the required level, remove **#New** from it. See item 7 for the position of **#New** in the tag line.
2. Tags are composite and may have 1 or more levels.
3. Tags define groups and relationships between topics; one document may have multiple tags.
4. Tags come immediately after the metadata.
5. Words in tags **start with capital letters**.
6. Abbreviations are written in **uppercase**.
7. The **#New** tag is placed at the end.
8. All cards in the root of the vault have the **#SRS** tag (spaced repetition).

---

## Tag model

Tags are **composite paths** (`Root/.../Leaf`) plus, when necessary, **multiple paths** on one card: this defines both the topic hierarchy and intersections (for example, microservices and observability). On the tag line, **thematic** tags come first, then **`#SRS`**, then **`#New`**. Cards that **compare** two entities must carry **both** corresponding thematic tags (or an equivalent by meaning), so that selections by either side are complete. **Do not** put a parent and child tag with the same prefix next to each other (for example, do not use `#Patterns/Architecture/Microservices` and `#Patterns/Architecture/Microservices/Observability` — the leaf `.../Microservices/Observability` is sufficient).

**Incomplete path (not a leaf):** it is acceptable to specify a tag **shorter** than the deepest known prefix in the tree below if there is **no child tag** that would be noticeably more appropriate by meaning. If a suitable leaf already exists in the tree, prefer it (and do not duplicate it together with its parent on the same card, see the paragraph above).

**Extension:** new notes should, where possible, **extend this tree** (new subtags under already accepted roots), rather than introduce **parallel tags that are synonyms** of the same concept. If a path is already established for an entity (for example, Kubernetes only as `#DevOps/Tools/Kubernetes`), do not add a second root without a reason (`#Kubernetes` alongside the same meaning). For different API types, use the **`#API/`** prefix and the leaf **`#API/<Type>`** (for example, `#API/REST`), rather than separate roots such as `#REST` or a branch under `Patterns`.

**New tag if the topic does not fit:** if there is **no suitable leaf** in the tree for a card (there is no point in forcing the topic under an “almost suitable” tag), **do not stretch** the nearest similar tag to fit. Add a new prefix under a **logical root** in the **“Tree”** section of `Tags.md` (or a new root, for example **`#Databases/SQL/...`** for the SQL language in the “database → SQL” model), and then use this tag on the card. The tree and tag selections must honestly reflect the subject.

**SQL in the tree:** topics of the **SQL language** should be tagged only with **`#Databases/SQL`** and child paths (for example, **`#Databases/SQL/Transactions`**); there is **no `#SQL` root** in the vault.

**`#NoSQL`:** **non-relational** stores and models (document, key-value, wide-column, graph, etc.); for a hybrid with a relational part, **`#Databases/SQL`** and **`#NoSQL`** may be used together.

---

## Tree (prefixes in cards)

### Java
<<<<<<< HEAD
=======

>>>>>>> a74789d1f0acc3e218739fc9ab48c7ab107ec9b2
* `#Java/Collections`
* `#Java/Collections/List`
* `#Java/Collections/Map`
* `#Java/Collections/Set`
* `#Java/Collections/Queues`
* `#Java/Collections/Iteration`
* `#Java/Collections/Concurrency`
* `#Java/Streams`
* `#Java/HashCodeEquals`
* `#Java/OOP`
* `#Java/Concurrency`
* `#Java/Exceptions`
* `#Java/Language`
* `#Java/Generics`
* `#Java/Immutability`
* `#Java/IO`
* `#Java/JVM`
* `#Java/JVM/GarbageCollector`
* `#Java/JDK`
* `#Java/Tooling`
* `#Java/Tooling/Maven`
* `#Java/Tooling/Gradle`
* `#Java/JavaEE`
* `#Java/Servlet`
* `#Java/CGI`
* `#Java/Listeners`
* `#Java/JSP`
* `#Java/JSP/JSTL`
* `#Java/Spring`
* `#Java/Spring/Core`
* `#Java/Spring/Core/IoC`
* `#Java/Spring/Framework/AOP`
* `#Java/Spring/Framework/DataAccess`
* `#Java/Spring/Framework/WebMvc`
* `#Java/Spring/Framework/WebSocket`
* `#Java/Spring/Framework/WebFlux`
* `#Java/Spring/Framework/Testing`
* `#Java/Spring/Framework/Instrumentation`
* `#Java/Spring/Boot`
* `#Java/Spring/Transactions`
* `#Java/Spring/Cloud`
* `#Java/Spring/Cloud/Gateway`
* `#Java/Spring/Cloud/Config`
* `#Java/Spring/Cloud/Stream`
* `#Java/Spring/Cloud/CircuitBreaker`
* `#Java/Spring/Data`
* `#Java/Spring/Data/JPA`
* `#Java/Spring/Data/MongoDB`
* `#Java/Spring/Data/Redis`
* `#Java/Spring/Security`
* `#Java/Spring/Batch`
* `#Java/Spring/Integration`
* `#Java/Spring/Session`
* `#Java/Spring/AI`
* `#Java/JDBC`
* `#Java/Persistence`
* `#Java/Persistence/JPA`
* `#Java/Persistence/Hibernate`

### Testing
<<<<<<< HEAD
* `#Testing`

### Kotlin
* `#Kotlin`

### Databases
=======

* `#Testing`

### Kotlin

* `#Kotlin`

### Databases

>>>>>>> a74789d1f0acc3e218739fc9ab48c7ab107ec9b2
* `#Databases`
* `#Databases/SQL`
* `#Databases/SQL/Transactions`
* `#Databases/Indexes`
* `#Databases/Transactions`

### NoSQL
<<<<<<< HEAD
* `#NoSQL`

### Problems
* `#Problems/Persistence`

### DSA
=======

* `#NoSQL`

### Problems

* `#Problems/Persistence`

### DSA

>>>>>>> a74789d1f0acc3e218739fc9ab48c7ab107ec9b2
* `#DSA/Algorithms/Search`
* `#DSA/DataStructures/Graph`

### Paradigms
<<<<<<< HEAD
* `#Paradigms/OOP`

### DistributedSystems
* `#DistributedSystems/Communication`

### Networking
=======

* `#Paradigms/OOP`

### DistributedSystems

* `#DistributedSystems/Communication`

### Networking

>>>>>>> a74789d1f0acc3e218739fc9ab48c7ab107ec9b2
* `#Networking`
* `#Networking/TCP`
* `#Networking/UDP`
* `#Networking/DNS`
* `#Networking/Web`
* `#Networking/Web/Protocols`
* `#Networking/Web/Protocols/HTTP`
* `#Networking/Web/Protocols/TLS`
* `#Networking/Web/Cookies`
* `#Networking/Web/Caching`

### API
<<<<<<< HEAD
=======

>>>>>>> a74789d1f0acc3e218739fc9ab48c7ab107ec9b2
* `#API/REST`
* `#API/SOAP`
* `#API/GraphQL`
* `#API/GRPC`
* `#API/RPC`
* `#API/Gateway`
* `#API/Webhooks`

### Patterns
<<<<<<< HEAD
=======

>>>>>>> a74789d1f0acc3e218739fc9ab48c7ab107ec9b2
* `#Patterns/GoF`
* `#Patterns/GoF/Creational`
* `#Patterns/GoF/Structural`
* `#Patterns/GoF/Behavioral`
* `#Patterns/GRASP`
* `#Patterns/Enterprise`
* `#Patterns/Enterprise/Integration`
* `#Patterns/Enterprise/Integration/Channels`
* `#Patterns/Enterprise/Integration/Messages`
* `#Patterns/Enterprise/Integration/Routing`
* `#Patterns/Enterprise/Integration/Transformation`
* `#Patterns/Enterprise/Integration/Endpoints`
* `#Patterns/Enterprise/Integration/Management`
* `#Patterns/DistributedSystems`
* `#Patterns/Cloud`
* `#Patterns/Architecture/UI`
* `#Patterns/Architecture/Monolith`
* `#Patterns/Architecture/Microservices`
* `#Patterns/Architecture/Microservices/ServiceBoundaries`
* `#Patterns/Architecture/Microservices/CrossCuttingConcerns`
* `#Patterns/Architecture/Microservices/CommunicationStyles`
* `#Patterns/Architecture/Microservices/ExternalAPI`
* `#Patterns/Architecture/Microservices/ServiceDiscovery`
* `#Patterns/Architecture/Microservices/Deployment`
* `#Patterns/Architecture/Microservices/Observability`

### Methodologies
<<<<<<< HEAD
=======

>>>>>>> a74789d1f0acc3e218739fc9ab48c7ab107ec9b2
* `#Methodologies/DDD`
* `#Methodologies/Principles`
* `#Methodologies/Principles/SOLID`
* `#Methodologies/Principles/DRY`
* `#Methodologies/Principles/KISS`
* `#Methodologies/Principles/IoC`
* `#Methodologies/Principles/DependencyInjection`
* `#Methodologies/Principles/YAGNI`
* `#Methodologies/Principles/SeparationOfConcerns`
* `#Methodologies/Principles/TellDontAsk`
* `#Methodologies/Principles/LawOfDemeter`

### Career
<<<<<<< HEAD
=======

>>>>>>> a74789d1f0acc3e218739fc9ab48c7ab107ec9b2
* `#Career`
* `#Career/Interview`
* `#Career/Experience`
* `#Career/Java`
* `#Career/Behavioral`

### Build
<<<<<<< HEAD
=======

>>>>>>> a74789d1f0acc3e218739fc9ab48c7ab107ec9b2
* `#Build/Tools`
* `#Build/Tools/Maven`
* `#Build/Tools/Gradle`
* `#Build/Tools/Ant`
* `#Build/Tools/CMake`

### DevOps
<<<<<<< HEAD
=======

>>>>>>> a74789d1f0acc3e218739fc9ab48c7ab107ec9b2
* `#DevOps/Tools/Docker`
* `#DevOps/Tools/Kubernetes`
* `#DevOps/Containerisation`
* `#DevOps/Virtualisation`
* `#DevOps/Orchestration`
* `#DevOps/Configuration`
* `#DevOps/Cloud`
* `#DevOps/Deployment`
* `#DevOps/Deployment/Strategies`

### SystemDesign
<<<<<<< HEAD
* `#SystemDesign`
* `#SystemDesign/Scalability`
* `#SystemDesign/Reliability`
* `#SystemDesign/Performance`
* `#SystemDesign/Availability`
* `#SystemDesign/Consistency`
* `#SystemDesign/Architecture`

### System
=======

* `#SystemDesign`
* `#SystemDesign/Scalability`
* `#SystemDesign/Reliability`
* `#SystemDesign/Performance`
* `#SystemDesign/Availability`
* `#SystemDesign/Consistency`
* `#SystemDesign/Architecture`

### System

>>>>>>> a74789d1f0acc3e218739fc9ab48c7ab107ec9b2
* `#SRS`
* `#New`