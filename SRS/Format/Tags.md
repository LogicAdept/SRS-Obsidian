For tags, use the following rules:

1. The **#New** tag is placed on cards that are **not yet answered** (empty) or have an **incomplete / draft** answer; when the card is brought to the required level, remove **#New** from it. See item 7 for the position of **#New** in the tag line.
2. Tags are composite and may have 1 or more levels.
3. Tags define groups and relationships between topics; one document may have multiple tags.
4. Tags come immediately after the metadata.
5. Words in tags **start with capital letters**.
6. Abbreviations are written in **uppercase**.
7. The **#New** tag is placed at the end.
8. Every SRS flashcard note must have the **#SRS** tag (spaced repetition).

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
* `#Java/Collections`
* `#Java/Collections/List`
* `#Java/Collections/List/Vector`
* `#Java/Collections/Map`
* `#Java/Collections/Map/Hashtable`
* `#Java/Collections/Set`
* `#Java/Collections/Queues`
* `#Java/Collections/Queues/PriorityQueue`
* `#Java/Collections/Iteration`
* `#Java/Collections/Sorting`
* `#Java/Collections/Concurrency`
* `#Java/Streams`
* `#Java/HashCodeEquals`
* `#Java/OOP`
* `#Java/OOP/Initialization`
* `#Java/OOP/Constructors`
* `#Java/Concurrency`
* `#Java/Concurrency/Synchronization`
* `#Java/Concurrency/Synchronization/SynchronizedKeyword`
* `#Java/Concurrency/SchedulableUnit`
* `#Java/Parallelism`
* `#Java/Async`
* `#Java/Exceptions`
* `#Java/Language`
* `#Java/Language/Assert`
* `#Java/Language/Primitives`
* `#Java/Language/Primitives/ShortType`
* `#Java/Language/Wrappers`
* `#Java/Language/Reflection`
* `#Java/Arrays`
* `#Java/String`
* `#Java/StringBuilder`
* `#Java/StringJoiner`
* `#Java/Optional`
* `#Java/Library`
* `#Java/Library/Nashorn`
* `#Java/Library/Reactor`
* `#Java/Library/Reactor/Mono`
* `#Java/Library/Reactor/Flux`
* `#Java/Time`
* `#Java/Time/LocalDateTime`
* `#Java/Time/ZonedDateTime`
* `#Java/Lambdas`
* `#Java/MethodReferences`
* `#Java/FunctionalInterfaces`
* `#Java/Annotations`
* `#Java/Serialization`
* `#Java/Serialization/SerialVersionUID`
* `#Java/Serialization/SingletonSerializationProblem`
* `#Java/Generics`
* `#Java/Generics/TypeBounds`
* `#Java/Immutability`
* `#Java/IO`
* `#Java/NIO`
* `#Java/Networking`
* `#Java/Networking/UrlEncoding`
* `#Java/Logging`
* `#Java/JVM`
* `#Java/JVM/Memory`
* `#Java/JVM/GarbageCollector`
* `#Java/JVM/ClassLoaders`
* `#Java/JVM/Tuning`
* `#Java/Runtime`
* `#Java/Bytecode`
* `#Java/JMM`
* `#Java/Performance`
* `#Java/JDK`
* `#Java/Legacy`
* `#Java/Versions`
* `#Java/Versions/8`
* `#Java/Versions/11`
* `#Java/Versions/17`
* `#Java/Versions/21`
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
* `#Java/Security`
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
* `#Testing`
* `#Testing/Mocking`
* `#Testing/Integration`

### Kotlin
* `#Kotlin`

### Databases
* `#Databases`
* `#Databases/RelationalAlgebra`
* `#Databases/SQL`
* `#Databases/SQL/DDL`
* `#Databases/SQL/DML`
* `#Databases/SQL/DCL`
* `#Databases/SQL/Transactions`
* `#Databases/SQL/DataTypes`
* `#Databases/Indexes`
* `#Databases/Partitioning`
* `#Databases/Replication`
* `#Databases/Keys`
* `#Databases/NormalForms`
* `#Databases/Transactions`
* `#Databases/MySQL`
* `#Databases/PostgreSQL`
* `#Databases/Oracle`
* `#Databases/MSSQL`

### NoSQL
* `#NoSQL`

### Serialization
* `#Serialization`

### DataFormats
* `#DataFormats`
* `#DataFormats/XML`
* `#DataFormats/JSON`

### Security
* `#Security`
* `#Security/Authentication`
* `#Security/Authorization`
* `#Security/Cryptography`
* `#Security/JWT`
* `#Security/AppSec`
* `#Security/AppSec/Injection`

### Problems
* `#Problems`
* `#Problems/Persistence`
* `#Problems/Concurrency`
* `#Problems/Optimization`
* `#Persistence`
* `#Persistence/ORM`
* `#Persistence/Caching`

### Internationalization
* `#Internationalization`
* `#Localization`

### Math
* `#Math`
* `#Math/Probability`
* `#Math/Optimization`
* `#Math/Optimization/LinearProgramming`
* `#Math/Optimization/LinearProgramming/SimplexMethod`
* `#Math/Optimization/Combinatorial`
* `#Math/Norm`

### UML
* `#UML`

### DSA
* `#DSA/Algorithms`
* `#DSA/Algorithms/Search`
* `#DSA/Algorithms/String`
* `#DSA/Algorithms/String/RabinKarp`
* `#DSA/Algorithms/ErrorCorrection`
* `#DSA/Algorithms/Greedy`
* `#DSA/Algorithms/Randomized`
* `#DSA/Algorithms/Selection`
* `#DSA/Algorithms/Sorting`
* `#DSA/Algorithms/Sorting/Timsort`
* `#DSA/Algorithms/DynamicProgramming`
* `#DSA/Algorithms/Mathematical`
* `#DSA/Algorithms/DynamicProgramming/PartitionProblem`
* `#DSA/Algorithms/DynamicProgramming/RodCuttingProblem`
* `#DSA/Algorithms/DynamicProgramming/RodCuttingProblem`
* `#DSA/Algorithms/LinearProgramming`
* `#DSA/Algorithms/SweepLine`
* `#DSA/Algorithms/TwoPointersTechnique`
* `#DSA/Complexity`
* `#DSA/DataStructures`
* `#DSA/DataStructures/Graph`
* `#DSA/Algorithms/Graph/ShortestPath`
* `#DSA/Algorithms/Graph/ReverseDelete`
* `#DSA/DataStructures/LinkedList`
* `#DSA/DataStructures/Set`
* `#DSA/DataStructures/Tree`
* `#DSA/DataStructures/UnionFind`
* `#DSA/Problems`

### MachineLearning
* `#MachineLearning`
* `#MachineLearning/UnsupervisedLearning`

### Simulation
* `#Simulation`

### ComputerArchitecture
* `#ComputerArchitecture`
* `#ComputerArchitecture/Registers`

### Methods
* `#Methods`
* `#Methods/Simulation`
* `#Methods/Simulation/AgentBased`
* `#Methods/Simulation/MonteCarlo`

### Paradigms
* `#Paradigms/OOP`
* `#Paradigms/Functional`
* `#Paradigms/Procedural`
* `#Paradigms/Async`
* `#Paradigms/Parallelism`
* `#Paradigms/Reactive`

### DataAndState
* `#DataAndState`
* `#DataAndState/Values`
* `#DataAndState/Objects`
* `#DataAndState/State`
* `#DataAndState/Mutability`
* `#DataAndState/Mutability/Mutable`
* `#DataAndState/Mutability/Immutable`
* `#DataAndState/ValueSemantics`
* `#DataAndState/ReferenceSemantics`
* `#DataAndState/MemoryManagement`
* `#DataAndState/Hashing`

### DistributedSystems
* `#DistributedSystems`
* `#DistributedSystems/Communication`
* `#DistributedSystems/Consensus`
* `#DistributedSystems/Consensus/LeaderElection`
* `#DistributedSystems/MapReduce`

### Messaging
* `#Messaging`
* `#Messaging/Async`
* `#Messaging/Tools`
* `#Messaging/Tools/Kafka`
* `#Messaging/Tools/RabbitMQ`
* `#Messaging/Tools/Flume`
* `#Messaging/Tools/Flink`
* `#Messaging/Bus`
* `#Messaging/Channel`
* `#Messaging/Dispatcher`
* `#Messaging/Endpoint`
* `#Messaging/Expiration`
* `#Messaging/Filter`
* `#Messaging/History`
* `#Messaging/Message`
* `#Messaging/Message/Simple`
* `#Messaging/Router`
* `#Messaging/Sequence`
* `#Messaging/Store`
* `#Messaging/Translator`
* `#Messaging/Bridge`
* `#Messaging/Gateway`
* `#Messaging/Mapper`
* `#Messaging/PollingConsumer`
* `#Messaging/Broker`
* `#Messaging/RequestReply`
* `#Messaging/Resequencer`
* `#Messaging/ReturnAddress`

### Networking
* `#Networking`
* `#Networking/TCP`
* `#Networking/UDP`
* `#Networking/DNS`
* `#Networking/Web`
* `#Networking/Web/HTML`
* `#Networking/Web/CSS`
* `#Networking/Web/Protocols`
* `#Networking/Web/Protocols/HTTP`
* `#Networking/Web/Protocols/TLS`
* `#Networking/Web/Protocols/FTP`
* `#Networking/Web/Protocols/WebSocket`
* `#Networking/Web/Cookies`
* `#Networking/Web/UrlEncoding`
* `#Networking/Web/Caching`

### API
* `#API/REST`
* `#API/OpenAPI`
* `#API/SOAP`
* `#API/GraphQL`
* `#API/GRPC`
* `#API/RPC`
* `#API/Gateway`
* `#API/Webhooks`
* `#API/Contracts`
* `#API/Idempotency`

### Patterns
* `#Patterns/AntiPatterns`
* `#Patterns/GoF`
* `#Patterns/GoF/Creational`
* `#Patterns/GoF/Structural`
* `#Patterns/GoF/Behavioral`
* `#Patterns/GoF/Behavioral/Strategy`
* `#Patterns/GoF/Behavioral/Observer`
* `#Patterns/GRASP`
* `#Patterns/Enterprise`
* `#Patterns/Enterprise/Integration`
* `#Patterns/Enterprise/Integration/Channels`
* `#Patterns/Enterprise/Integration/Channels/PublishSubscribe`
* `#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel`
* `#Patterns/Enterprise/Integration/Messages`
* `#Patterns/Enterprise/Integration/Messages/EnvelopeWrapper`
* `#Patterns/Enterprise/Integration/Messages/EventMessage`
* `#Patterns/Enterprise/Integration/Messages/FormatIndicator`
* `#Patterns/Enterprise/Integration/Messages/TestMessage`
* `#Patterns/Enterprise/Integration/TransactionalClient`
* `#Patterns/Enterprise/Integration/WireTap`
* `#Patterns/Enterprise/Integration/Routing`
* `#Patterns/Enterprise/Integration/Routing/RoutingSlip`
* `#Patterns/Enterprise/Integration/Routing/DynamicRouter`
* `#Patterns/Enterprise/Integration/Transformation`
* `#Patterns/Enterprise/Integration/Transformation/Normalizer`
* `#Patterns/Enterprise/Integration/Transformation/PipesAndFilters`
* `#Patterns/Enterprise/Integration/Endpoints`
* `#Patterns/Enterprise/Integration/Endpoints/SelectiveConsumer`
* `#Patterns/Enterprise/Integration/Endpoints/EventDrivenConsumer`
* `#Patterns/Enterprise/Integration/Endpoints/ServiceActivator`
* `#Patterns/Enterprise/Integration/SmartProxy`
* `#Patterns/Enterprise/Integration/Management`
* `#Patterns/Enterprise/Integration/Management/ProcessManager`
* `#Patterns/Enterprise/Integration/Messaging`
* `#Patterns/Enterprise/Integration/Messaging/Splitter`
* `#Patterns/Enterprise/Integration/Messaging/ScatterGather`
* `#Patterns/Enterprise/Integration/Messaging/DurableSubscriber`
* `#Patterns/Enterprise/Integration/Messaging/GuaranteedDelivery`
* `#Patterns/DistributedSystems`
* `#Patterns/Cloud`
* `#Patterns/Architecture/UI`
* `#Patterns/Architecture/UI/MicroFrontends`
* `#Patterns/Architecture/Monolith`
* `#Patterns/Architecture/Microservices`
* `#Patterns/Architecture/Microservices/ServiceBoundaries`
* `#Patterns/Architecture/Microservices/CrossCuttingConcerns`
* `#Patterns/Architecture/Microservices/CommunicationStyles`
* `#Patterns/Architecture/Microservices/ExternalAPI`
* `#Patterns/Architecture/Microservices/ServiceDiscovery`
* `#Patterns/Architecture/Microservices/Deployment`
* `#Patterns/Architecture/Microservices/Sidecar`
* `#Patterns/Architecture/Microservices/Observability`

### Methodologies
* `#Methodologies/DDD`
* `#Methodologies/BDD`
* `#Methodologies/BDUF`
* `#Methodologies/TDD`
* `#Methodologies/DesignByContract`
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

### ProjectManagement
* `#ProjectManagement`
* `#ProjectManagement/Agile`
* `#ProjectManagement/Planning`
* `#ProjectManagement/Estimation`
* `#ProjectManagement/Delivery`

### EngineeringLeadership
* `#EngineeringLeadership`
* `#EngineeringLeadership/TechLead`
* `#EngineeringLeadership/Architect`
* `#EngineeringLeadership/CTO`
* `#EngineeringLeadership/DecisionMaking`

### Career
* `#Career`
* `#Career/Interview`
* `#Career/Interview/Exercises`
* `#Career/Experience`
* `#Career/Java`
* `#Career/Behavioral`

### Build
* `#Build/Tools`
* `#Build/Tools/Maven`
* `#Build/Tools/Gradle`
* `#Build/Tools/Ant`
* `#Build/Tools/CMake`
* `#Build/Dependencies`
* `#Build/ArtifactRepositories`
* `#Build/ArtifactRepositories/Nexus`

### DevOps
* `#DevOps/Tools/Docker`
* `#DevOps/Tools/Kubernetes`
* `#DevOps/VCS`
* `#DevOps/VCS/Git`
* `#DevOps/Shell`
* `#DevOps/Containerisation`
* `#DevOps/Virtualisation`
* `#DevOps/Orchestration`
* `#DevOps/Configuration`
* `#DevOps/Cloud`
* `#DevOps/Deployment`
* `#DevOps/Deployment/Strategies`
* `#DevOps/CICD`

### Debugging
* `#Debugging`

### OperatingSystems
* `#OperatingSystems`
* `#OperatingSystems/MemoryHierarchy`
* `#OperatingSystems/MemoryHierarchy/VirtualMemory`
* `#OperatingSystems/IO`
* `#OperatingSystems/IO/Buffered`
* `#OperatingSystems/IO/Streams`
* `#OperatingSystems/IO/Files`
* `#OperatingSystems/Concurrency`
* `#OperatingSystems/Concurrency/NonBlocking`
* `#OperatingSystems/Concurrency/LockFree`
* `#OperatingSystems/Linux`

### Caching
* `#Caching`

### Logging
* `#Logging`

### Observability
* `#Observability`

### SystemDesign
* `#SystemDesign`
* `#SystemDesign/Scalability`
* `#SystemDesign/Reliability`
* `#SystemDesign/Performance`
* `#SystemDesign/Availability`
* `#SystemDesign/Consistency`
* `#SystemDesign/PartitionTolerance`
* `#SystemDesign/Architecture`
* `#SystemDesign/Microservices`
* `#SystemDesign/Tradeoffs`
* `#SystemDesign/Atomicity`

### ORM
* `#ORM`

### System
* `#SRS`
* `#New`

### ProgrammingLanguages
* `#ProgrammingLanguages`
* `#ProgrammingLanguages/Compilation`
* `#ProgrammingLanguages/Interpretation`
* `#ProgrammingLanguages/ExecutionModel`
