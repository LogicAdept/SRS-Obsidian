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

**SQL in the tree:** topics of the **SQL language** should be tagged only with **`#Databases/SQL`** and child paths (for example, **`#Databases/SQL/Transactions`**); there is **no `#SQL` root** in the vault. SQL is the language, not the relational store family.

**Relational in the tree:** classic RDBMS products live under **`#Databases/Relational`** and child paths (for example **`#Databases/Relational/PostgreSQL`**). Comparison cards (relational vs NoSQL **store types**) carry **`#Databases/Relational`** and **`#Databases/NoSQL`** (or the product leaves). Do not put **`#Databases`** next to **`#Databases/Relational`** on the same card.

**NoSQL in the tree:** non-relational stores (document, key-value, wide-column, graph, vector, search) live under **`#Databases/NoSQL`** and child paths (for example **`#Databases/NoSQL/Redis`**). There is **no `#NoSQL` root**. Comparison cards (relational vs NoSQL store types) carry **`#Databases/Relational`** and **`#Databases/NoSQL`** (or the product leaves). Do not put **`#Databases`** next to **`#Databases/NoSQL`** on the same card.

**OLAP in the tree:** analytical / columnar engines live under **`#Databases/OLAP`** and child paths (for example **`#Databases/OLAP/ClickHouse`**). Do not put them under Relational or NoSQL. OLTP vs OLAP cards carry **`#Databases/Relational`** and **`#Databases/OLAP`** (or the product leaves). Do not put **`#Databases`** next to **`#Databases/OLAP`** on the same card.

**Messaging in the tree:** protocols and brokers live under **`#Messaging`** (`#Messaging/AMQP`, `#Messaging/MQTT`, `#Messaging/Tools/Kafka`, …). Hohpe/Woolf **EIP pattern names** (Message Bus, Channel, Broker, Request-Reply, …) live under **`#Patterns/Enterprise/Integration/...`**, not as `#Messaging/Bus` and similar. A pattern card that is also about messaging carries **`#Messaging`** plus the Patterns leaf — do not duplicate the pattern name under Messaging.

**Indexes in the tree:** **`#Databases/Indexes`** is the index idea (when to index, B-tree vs hash/GIN/GiST, clustered vs not, plans). **Covering** is INCLUDE / index-only covering. **Partial** is `WHERE` on the index. **Functional** is expression / function-based indexes (`lower(email)`, JSON path). **Composite** is a multi-column key (leftmost prefix). Comparison of composite vs INCLUDE carries **Covering** and **Composite**. Do not put **`#Databases/Indexes`** next to a more specific **`#Databases/Indexes/...`** child on the same card.

**Spring in the tree:** **`#Java/Spring/Framework/...`** is for **Spring Framework** modules (Web MVC, WebFlux, AOP, Cache, DataAccess, Testing, …). **Spring Boot** and **Spring Security** are separate projects: **`#Java/Spring/Boot`** and **`#Java/Spring/Security`**, not under Framework. Spring Data / Cloud / Batch / Integration / AMQP / Kafka stay as siblings under **`#Java/Spring`**. Java-language crypto and auth concepts stay **`#Java/Security`**, not Spring Security. **`#Java/Spring/Core`** is framework identity, versions, and ecosystem. The IoC container, beans, DI, `BeanFactory`/`ApplicationContext`, `FactoryBean`, circular dependencies, and context events live under **`#Java/Spring/Core/IoC`**. Bean **scopes** (including scoped proxies / `@Lookup`), **lifecycle** (`@PostConstruct` / destroy / `BeanPostProcessor`), **stereotypes** (`@Component` / `@Service` / `@Repository` / `@Controller`), **configuration** (XML vs Java vs annotations, `@Bean`, `@ComponentScan`, `@Profile`, `@Import`), and **SpEL** (`@Value`, `@PropertySource`, `Environment`) live under the matching **`#Java/Spring/Core/IoC/...`** child. **`#Java/Spring/Boot`** is Boot identity (what Boot is, Initializr, DevTools, AOT, Modulith, version deltas, `SpringApplication` / runners) and Boot-flavored how-tos that already carry another honest leaf. **Auto-configuration** (starters, `ConditionalOn*`, custom starters, `@SpringBootApplication` and its default component-scan package) is **`#Java/Spring/Boot/AutoConfiguration`**. **Externalized config** (`application.properties`/`yml`, property order, `@ConfigurationProperties`, Boot profiles) is **`#Java/Spring/Boot/Properties`**. **Embedded servlet container**, jar vs WAR as a *runtime* choice (external container, `SpringBootServletInitializer`), and server SSL/compression are **`#Java/Spring/Boot/Embedded`**. **Build** (Maven/Gradle parent, BOM, fat/executable JAR, how you ship the app) is **`#Java/Spring/Boot/Build`**. **Actuator** and **Admin** stay their leaves. **Filter chain** (`FilterChainProxy`, `SecurityFilterChain`, `HttpSecurity`, named servlet filters, `addFilterBefore`/`After`) is **`#Java/Spring/Security/FilterChain`**. **Method security** (`@PreAuthorize`, `@Secured`, `@EnableMethodSecurity` / `@EnableGlobalMethodSecurity`, `@PreFilter`/`@PostFilter`) is **`#Java/Spring/Security/MethodSecurity`**. **Authentication** (`UserDetails` / `UserDetailsService`, `AuthenticationManager` / `AuthenticationProvider`, form login, HTTP Basic, remember-me, principal vs credentials, `AuthenticationEntryPoint` / `AccessDeniedHandler`) is **`#Java/Spring/Security/Authentication`**. **SecurityContext** (`SecurityContextHolder`, strategies, repository, async propagation) is **`#Java/Spring/Security/SecurityContext`**. **PasswordEncoder** (`PasswordEncoder`, `DelegatingPasswordEncoder`, BCrypt/Argon2/PBKDF2, encode vs matches) is **`#Java/Spring/Security/PasswordEncoder`** (dual-tag **`#Security/Cryptography`** when the cue is hashing/encoders). **CSRF** (`CsrfToken`, repositories, AJAX/JSON token, CSRF vs CORS, CSRF off for JWT APIs) is **`#Java/Spring/Security/CSRF`**. **Session management** (`SessionCreationPolicy`, fixation, `maximumSessions`) is **`#Java/Spring/Security/SessionManagement`**, not **`#Java/Spring/Session`** (the Spring Session project). **OAuth2** (`oauth2Login` / `oauth2Client` / `oauth2ResourceServer`, grants, `JwtDecoder` / `NimbusJwtDecoder` / opaque introspection, Keycloak as an OIDC broker) is **`#Java/Spring/Security/OAuth2`**; still dual-tag **`#Security/OAuth2`**, **`#Security/JWT`**, **`#Security/OIDC`**, **`#Security/Keycloak`** as they apply. **SAML** (`saml2Login`) stays on **`#Java/Spring/Security`** plus **`#Security/SAML`**. Tests dual-tag **`#Java/Spring/Framework/Testing`**. **Reactive HTTP security** (`SecurityWebFilterChain`, `ServerHttpSecurity`, `authorizeExchange`, `pathMatchers`, `@EnableWebFluxSecurity`) is **`#Java/Spring/Security/WebFlux`**; dual-tag **`#Java/Spring/Framework/WebFlux`**, not FilterChain. **`#Java/Spring/Transactions`** is Spring transaction management (`PlatformTransactionManager` / `TransactionTemplate`, `@Transactional`, default rollback). **Propagation** (`REQUIRED`, `REQUIRES_NEW`, `NESTED`, and the other `Propagation` values) is **`#Java/Spring/Transactions/Propagation`**. **Calls between `@Transactional` methods** (proxy self-invocation versus a cross-bean call, and how that interacts with propagation and rollback) is **`#Java/Spring/Transactions/SelfInvocation`**. Test-level `@Transactional` dual-tags **`#Java/Spring/Framework/Testing`**. AOP as the interceptor mechanism dual-tags **`#Java/Spring/Framework/AOP`**. Do not put **`#Java/Spring`** next to a more specific **`#Java/Spring/...`** child, **`#Java/Spring/Core`** next to **`#Java/Spring/Core/IoC`**, **`#Java/Spring/Core/IoC`** next to a more specific **`#Java/Spring/Core/IoC/...`** child, **`#Java/Spring/Boot`** next to a more specific **`#Java/Spring/Boot/...`** child, **`#Java/Spring/Security`** next to a more specific **`#Java/Spring/Security/...`** child, or **`#Java/Spring/Transactions`** next to a more specific **`#Java/Spring/Transactions/...`** child.

**Spring in the tree:** **`#Java/Spring/Framework/...`** is for **Spring Framework** modules (Web MVC, WebFlux, AOP, Cache, DataAccess, Testing, …). **Spring Boot** and **Spring Security** are separate projects: **`#Java/Spring/Boot`** and **`#Java/Spring/Security`**, not under Framework. Spring Data / Cloud / Batch / Integration / AMQP / Kafka stay as siblings under **`#Java/Spring`**. Java-language crypto and auth concepts stay **`#Java/Security`**, not Spring Security. **`#Java/Spring/Core`** is framework identity, versions, and ecosystem. The IoC container, beans, `BeanFactory`/`ApplicationContext`, `FactoryBean`, circular dependencies, and context events live under **`#Java/Spring/Core/IoC`**. **Dependency injection** (constructor / setter / field / method injection, wiring versus `new` or a locator, interface injection, why constructor injection) is **`#Java/Spring/Core/IoC/DI`**. Bean **autowiring** (`@Autowired`, `@Qualifier`, `@Primary`, XML `autowire` modes, `@Resource` vs `@Inject` matching) is **`#Java/Spring/Core/IoC/Autowiring`**. Bean **scopes** (including scoped proxies / `@Lookup`), **lifecycle** (`@PostConstruct` / destroy / `BeanPostProcessor`), **stereotypes** (`@Component` / `@Service` / `@Repository` / `@Controller`), **configuration** (XML vs Java vs annotations, `@Bean`, `@ComponentScan`, `@Profile`, `@Import`), and **SpEL** (`@Value`, `@PropertySource`, `Environment`) live under the matching **`#Java/Spring/Core/IoC/...`** child. **`#Java/Spring/Boot`** is Boot identity (what Boot is, `@SpringBootApplication`, Initializr, DevTools, AOT, Modulith, version deltas) and Boot-flavored how-tos that already carry another honest leaf. **Auto-configuration** (starters, `ConditionalOn*`, custom starters) is **`#Java/Spring/Boot/AutoConfiguration`**. **Externalized config** (`application.properties`/`yml`, property order, `@ConfigurationProperties`, Boot profiles) is **`#Java/Spring/Boot/Properties`**. **Embedded servlet container**, jar vs WAR as a *runtime* choice (external container, `SpringBootServletInitializer`), and server SSL/compression are **`#Java/Spring/Boot/Embedded`**. **Build** (Maven/Gradle parent, BOM, fat/executable JAR, how you ship the app) is **`#Java/Spring/Boot/Build`**. **Actuator** and **Admin** stay their leaves. **Filter chain** (`FilterChainProxy`, `SecurityFilterChain`, `HttpSecurity`, named servlet filters, `addFilterBefore`/`After`) is **`#Java/Spring/Security/FilterChain`**. **Method security** (`@PreAuthorize`, `@Secured`, `@EnableMethodSecurity` / `@EnableGlobalMethodSecurity`, `@PreFilter`/`@PostFilter`) is **`#Java/Spring/Security/MethodSecurity`**. **Authentication** (`UserDetails` / `UserDetailsService`, `AuthenticationManager` / `AuthenticationProvider`, form login, HTTP Basic, remember-me, principal vs credentials, `AuthenticationEntryPoint` / `AccessDeniedHandler`) is **`#Java/Spring/Security/Authentication`**. **SecurityContext** (`SecurityContextHolder`, strategies, repository, async propagation) is **`#Java/Spring/Security/SecurityContext`**. **PasswordEncoder** (`PasswordEncoder`, `DelegatingPasswordEncoder`, BCrypt/Argon2/PBKDF2, encode vs matches) is **`#Java/Spring/Security/PasswordEncoder`** (dual-tag **`#Security/Cryptography`** when the cue is hashing/encoders). **CSRF** (`CsrfToken`, repositories, AJAX/JSON token, CSRF vs CORS, CSRF off for JWT APIs) is **`#Java/Spring/Security/CSRF`**. **Session management** (`SessionCreationPolicy`, fixation, `maximumSessions`) is **`#Java/Spring/Security/SessionManagement`**, not **`#Java/Spring/Session`** (the Spring Session project). **OAuth2** (`oauth2Login` / `oauth2Client` / `oauth2ResourceServer`, grants, `JwtDecoder` / `NimbusJwtDecoder` / opaque introspection, Keycloak as an OIDC broker) is **`#Java/Spring/Security/OAuth2`**; still dual-tag **`#Security/OAuth2`**, **`#Security/JWT`**, **`#Security/OIDC`**, **`#Security/Keycloak`** as they apply. **SAML** (`saml2Login`) stays on **`#Java/Spring/Security`** plus **`#Security/SAML`**. Tests dual-tag **`#Java/Spring/Framework/Testing`**. **Reactive HTTP security** (`SecurityWebFilterChain`, `ServerHttpSecurity`, `authorizeExchange`, `pathMatchers`, `@EnableWebFluxSecurity`) is **`#Java/Spring/Security/WebFlux`**; dual-tag **`#Java/Spring/Framework/WebFlux`**, not FilterChain. **`#Java/Spring/Transactions`** is Spring transaction management (`PlatformTransactionManager` / `TransactionTemplate`, `@Transactional`, default rollback). **Propagation** (`REQUIRED`, `REQUIRES_NEW`, `NESTED`, and the other `Propagation` values) is **`#Java/Spring/Transactions/Propagation`**. **Calls between `@Transactional` methods** (proxy self-invocation versus a cross-bean call, and how that interacts with propagation and rollback) is **`#Java/Spring/Transactions/SelfInvocation`**. Test-level `@Transactional` dual-tags **`#Java/Spring/Framework/Testing`**. AOP as the interceptor mechanism dual-tags **`#Java/Spring/Framework/AOP`**. Do not put **`#Java/Spring`** next to a more specific **`#Java/Spring/...`** child, **`#Java/Spring/Core`** next to **`#Java/Spring/Core/IoC`**, **`#Java/Spring/Core/IoC`** next to a more specific **`#Java/Spring/Core/IoC/...`** child, **`#Java/Spring/Boot`** next to a more specific **`#Java/Spring/Boot/...`** child, **`#Java/Spring/Security`** next to a more specific **`#Java/Spring/Security/...`** child, or **`#Java/Spring/Transactions`** next to a more specific **`#Java/Spring/Transactions/...`** child.

**Annotations in the tree:** **`#Java/Annotations`** is the Java annotation mechanism (declaration, retention, repeatable, records, marker-interface replacement). A card about a **Spring-specific annotation** (`@Autowired`, `@Bean`, `@Transactional`, `@SpringBootApplication`, …) carries the honest **`#Java/Spring/...`** leaf **and** **`#Java/Annotations`**. Do not put **`#Java/Annotations`** on Spring cards that are not about an annotation (container identity, scopes, circular dependencies, XML-only wiring). JPA / JUnit annotation cards likewise carry their persistence or testing leaf **and** **`#Java/Annotations`**.

**Records in the tree:** **`#Java/Language/Records`** is the record type (header versus class, generated members, restrictions, versus Lombok `@Value`). **Constructors** is the canonical constructor, the compact form, and extra constructors that must `this(...)` into the canonical one. Do not put **`#Java/Language/Records`** next to **`#Java/Language/Records/Constructors`** on the same card. Compact constructors stay here, not **`#Java/OOP/Constructors`**. JPA / Jackson / Java serialization / reflection / annotation-on-component cards dual-tag those leaves. Record-generated `equals`/`hashCode` dual-tags **`#Java/HashCodeEquals`**.

**Concurrency in the tree:** **`#Java/Concurrency`** is the Java threading model. Child leaves: **`Threads`** (lifecycle, `Thread`/`Runnable`, join/sleep/interrupt/daemon), **`Executors`** (pools, `Future`/`Callable`/`CompletableFuture`, ForkJoin), **`Synchronizers`** (`CountDownLatch`, `CyclicBarrier`, `Phaser`, `Semaphore`, `Exchanger`), **`Atomics`** (`java.util.concurrent.atomic`, CAS), **`VirtualThreads`**, **`Synchronization`** (monitors, wait/notify, intrinsic locks). **`Synchronization/SynchronizedKeyword`** is the `synchronized` keyword (methods, blocks, `this` vs `Class` monitor, private mutex objects). **`Synchronization/Locks`** is `java.util.concurrent.locks` (`Lock`, `ReentrantLock`, `ReadWriteLock`, `StampedLock`, `Condition`). Concurrent collections stay **`#Java/Collections/Concurrency`**. The Java Memory Model stays **`#Java/JMM`**. Do not put **`#Java/Concurrency`** next to a more specific **`#Java/Concurrency/...`** child, or **`#Java/Concurrency/Synchronization`** next to a more specific **`#Java/Concurrency/Synchronization/...`** child, on the same card.

**Collections in the tree:** **`#Java/Collections`** is the framework (interfaces, `Collection` vs `Collections`, unmodifiable views). Implementations live under **`List`**, **`Map`**, **`Set`**, **`Queues`**. List impls: **`ArrayList`**, **`LinkedList`**, **`Vector`**. Set impls: **`HashSet`**, **`LinkedHashSet`**, **`TreeSet`**, **`EnumSet`**. Queue impls: **`ArrayDeque`**, **`PriorityQueue`**, **`BlockingQueue`**. Concurrent collections stay **`#Java/Collections/Concurrency`**. Iterators stay **`#Java/Collections/Iteration`**. Do not put **`#Java/Collections`** or a family tag (`List`/`Set`/`Map`/`Queues`) next to a more specific child on the same card. Comparison cards carry both implementation leaves.

**Exceptions in the tree:** **`#Java/Exceptions`** is the Java exception model (handling practices, custom types, `throw`/propagation). **Hierarchy** is `Throwable` and the Exception/Error/RuntimeException tree. **Checked** is checked exceptions (`throws`, wrapping, the checked-exception debate). **Unchecked** is `RuntimeException` and common kinds (NPE, CCE). **Error** is `java.lang.Error` and JVM errors (OOM, StackOverflowError, ExceptionInInitializerError, AssertionError). **TryCatch** is try/catch/finally, multi-catch, catch order, and which try forms are legal. **TryWithResources** (under TryCatch) is try-with-resources, `AutoCloseable`, suppressed exceptions on `close`, and TWR vs try-finally when both throw. Catalog-of-try-forms cards stay on **TryCatch**. Checked vs unchecked comparison cards carry **Checked** and **Unchecked**. Error vs Exception comparison carries **Error** and **Hierarchy**. Do not put **`#Java/Exceptions`** next to a more specific **`#Java/Exceptions/...`** child, or **`#Java/Exceptions/TryCatch`** next to **`#Java/Exceptions/TryCatch/TryWithResources`**, on the same card.

**Assert in the tree:** **`#Java/Language/Assert`** is the Java `assert` keyword (`assert cond;` / `assert cond : detail;`), runtime enable/disable (`-ea` / `-da` / `-esa` / `-dsa`, package and class filters), and `AssertionError` from a failed `assert`. Test-library assertions (JUnit `assertEquals` / `assertThrows` / `assertAll`, AssertJ, Hamcrest, JSONAssert, hard vs soft) stay **`#Java/Testing/...`**, not Language/Assert. `AssertionError` cards dual-tag **`#Java/Exceptions/Error`**. Do not put **`#Java/Language`** next to **`#Java/Language/Assert`** on the same card.

**Runtime in the tree:** **`#Java/Runtime`** is the process-level API (`java.lang.Runtime`, `java.lang.System`: standard streams, `System.exit`, environment and properties, `Runtime.exec` / shutdown hooks). The **JRE product** (JVM + libraries, no compiler) is **`#Java/JRE`**, not Runtime. JVM internals (memory regions, GC, class loaders, JIT, launch flags, VM startup) stay **`#Java/JVM/...`**. Compile-time vs runtime **language** semantics (dynamic dispatch / polymorphism) stay **`#Java/OOP`** and **`#Java/Language`**. Do not put **`#Java/Runtime`** next to a more specific **`#Java/Runtime/...`** child on the same card.

**Optional in the tree:** **`#Java/Language/Optional`** is `java.util.Optional` (what it is versus `null`, factories `of` / `ofNullable` / `empty`, `map` / `flatMap` / `filter` / `stream`, `isPresent` / `ifPresent` / `or` / `orElseThrow` / `get`, primitive `OptionalInt` / `OptionalLong` / `OptionalDouble`). **Usage** is intended-use rules: return type not field or parameter, never return a null `Optional`, do not wrap a collection, avoid `get()`, allocation cost, not `Serializable`. Primitive optionals dual-tag **`#Java/Language/Primitives`**. Stream bridging dual-tags **`#Java/Streams`**. Serialization of Optional dual-tags **`#Java/Serialization`**. Do not put **`#Java/Language/Optional`** next to **`#Java/Language/Optional/Usage`** on the same card.

---

## Tree (prefixes in cards)

### Java
* `#Java`
* `#Java/Collections`
* `#Java/Collections/List`
* `#Java/Collections/List/ArrayList`
* `#Java/Collections/List/LinkedList`
* `#Java/Collections/List/Vector`
* `#Java/Collections/Map`
* `#Java/Collections/Map/ConcurrentHashMap`
* `#Java/Collections/Map/EnumMap`
* `#Java/Collections/Map/HashMap`
* `#Java/Collections/Map/Hashtable`
* `#Java/Collections/Map/IdentityHashMap`
* `#Java/Collections/Map/LinkedHashMap`
* `#Java/Collections/Map/TreeMap`
* `#Java/Collections/Map/WeakHashMap`
* `#Java/Collections/Set`
* `#Java/Collections/Set/HashSet`
* `#Java/Collections/Set/LinkedHashSet`
* `#Java/Collections/Set/TreeSet`
* `#Java/Collections/Set/EnumSet`
* `#Java/Collections/Queues`
* `#Java/Collections/Queues/ArrayDeque`
* `#Java/Collections/Queues/PriorityQueue`
* `#Java/Collections/Queues/BlockingQueue`
* `#Java/Collections/Iteration`
* `#Java/Collections/Sorting`
* `#Java/Collections/Concurrency`
* `#Java/Streams`
* `#Java/HashCodeEquals`
* `#Java/OOP`
* `#Java/OOP/Initialization`
* `#Java/OOP/Constructors`
* `#Java/Concurrency`
* `#Java/Concurrency/Threads`
* `#Java/Concurrency/Executors`
* `#Java/Concurrency/Synchronizers`
* `#Java/Concurrency/Atomics`
* `#Java/Concurrency/VirtualThreads`
* `#Java/Concurrency/Synchronization`
* `#Java/Concurrency/Synchronization/SynchronizedKeyword`
* `#Java/Concurrency/Synchronization/Locks`
* `#Java/Parallelism`
* `#Java/Async`
* `#Java/Exceptions`
* `#Java/Exceptions/Hierarchy`
* `#Java/Exceptions/Checked`
* `#Java/Exceptions/Unchecked`
* `#Java/Exceptions/Error`
* `#Java/Exceptions/TryCatch`
* `#Java/Exceptions/TryCatch/TryWithResources`
* `#Java/Language`
* `#Java/Language/Assert`
* `#Java/Language/Enum`
* `#Java/Language/Optional`
* `#Java/Language/Optional/Usage`
* `#Java/Language/Primitives`
* `#Java/Language/Primitives/ShortType`
* `#Java/Language/Records`
* `#Java/Language/Records/Constructors`
* `#Java/Language/Reflection`
* `#Java/Language/Wrappers`
* `#Java/Arrays`
* `#Java/String`
* `#Java/StringBuilder`
* `#Java/StringJoiner`
* `#Java/Library`
* `#Java/Library/JAXP`
* `#Java/Library/Log4j`
* `#Java/Library/Lombok`
* `#Java/Library/Nashorn`
* `#Java/Library/Reactor`
* `#Java/Library/Reactor/Mono`
* `#Java/Library/Reactor/Flux`
* `#Java/Library/RxJava`
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
* `#Java/JVM/JIT`
* `#Java/JVM/Tuning`
* `#Java/Runtime`
* `#Java/Bytecode`
* `#Java/JMM`
* `#Java/Performance`
* `#Java/JDK`
* `#Java/JRE`
* `#Java/Legacy`
* `#Java/Versions`
* `#Java/Versions/5`
* `#Java/Versions/8`
* `#Java/Versions/9`
* `#Java/Versions/11`
* `#Java/Versions/16`
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
* `#Java/Spring/Core/IoC/DI`
* `#Java/Spring/Core/IoC/Autowiring`
* `#Java/Spring/Core/IoC/Scopes`
* `#Java/Spring/Core/IoC/Lifecycle`
* `#Java/Spring/Core/IoC/Stereotypes`
* `#Java/Spring/Core/IoC/Configuration`
* `#Java/Spring/Core/IoC/SpEL`
* `#Java/Spring/Framework/AOP`
* `#Java/Spring/Framework/Cache`
* `#Java/Spring/Framework/DataAccess`
* `#Java/Spring/Framework/WebMvc`
* `#Java/Spring/Framework/WebSocket`
* `#Java/Spring/Framework/WebFlux`
* `#Java/Spring/Framework/Testing`
* `#Java/Spring/Framework/Instrumentation`
* `#Java/Spring/Boot`
* `#Java/Spring/Boot/Actuator`
* `#Java/Spring/Boot/Admin`
* `#Java/Spring/Boot/AutoConfiguration`
* `#Java/Spring/Boot/Properties`
* `#Java/Spring/Boot/Embedded`
* `#Java/Spring/Boot/Build`
* `#Java/Spring/Transactions`
* `#Java/Spring/Transactions/Propagation`
* `#Java/Spring/Transactions/SelfInvocation`
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
* `#Java/Spring/Security/FilterChain`
* `#Java/Spring/Security/MethodSecurity`
* `#Java/Spring/Security/Authentication`
* `#Java/Spring/Security/SecurityContext`
* `#Java/Spring/Security/PasswordEncoder`
* `#Java/Spring/Security/CSRF`
* `#Java/Spring/Security/SessionManagement`
* `#Java/Spring/Security/OAuth2`
* `#Java/Spring/Security/WebFlux`
* `#Java/Spring/Batch`
* `#Java/Spring/Integration`
* `#Java/Spring/AMQP`
* `#Java/Spring/Kafka`
* `#Java/Spring/Session`
* `#Java/Spring/AI`
* `#Java/JDBC`
* `#Java/Persistence`
* `#Java/Persistence/JPA`
* `#Java/Persistence/Hibernate`
* `#Java/Persistence/JOOQ`
* `#Java/Quarkus`
* `#Java/Testing`
* `#Java/Testing/JUnit`
* `#Java/Testing/Mockito`
* `#Java/Testing/Testcontainers`
* `#Java/Testing/WireMock`
* `#Java/Testing/Cucumber`
* `#Java/Testing/Gherkin`

### Testing
* `#Testing`
* `#Testing/Mocking`
* `#Testing/Integration`
* `#Testing/Performance`

### Kotlin
* `#Kotlin`
* `#Kotlin/Coroutines`

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
* `#Databases/Indexes/Covering`
* `#Databases/Indexes/Partial`
* `#Databases/Indexes/Functional`
* `#Databases/Indexes/Composite`
* `#Databases/Partitioning`
* `#Databases/Sharding`
* `#Databases/Replication`
* `#Databases/Keys`
* `#Databases/NormalForms`
* `#Databases/Transactions`
* `#Databases/Relational`
* `#Databases/Relational/MySQL`
* `#Databases/Relational/PostgreSQL`
* `#Databases/Relational/Oracle`
* `#Databases/Relational/MSSQL`
* `#Databases/Relational/CockroachDB`
* `#Databases/OLAP`
* `#Databases/OLAP/ClickHouse`
* `#Databases/OLAP/Snowflake`
* `#Databases/OLAP/Druid`
* `#Databases/OLAP/Pinot`
* `#Databases/NoSQL`
* `#Databases/NoSQL/Redis`
* `#Databases/NoSQL/MongoDB`
* `#Databases/NoSQL/Cassandra`
* `#Databases/NoSQL/Elasticsearch`
* `#Databases/NoSQL/ScyllaDB`
* `#Databases/NoSQL/Vector`

### Serialization
* `#Serialization`

### DataFormats
* `#DataFormats`
* `#DataFormats/XML`
* `#DataFormats/JSON`
* `#DataFormats/Protobuf`
* `#DataFormats/CloudEvents`
* `#DataFormats/Iceberg`

### Security
* `#Security`
* `#Security/Authentication`
* `#Security/Authorization`
* `#Security/Cryptography`
* `#Security/JWT`
* `#Security/OAuth2`
* `#Security/OIDC`
* `#Security/SAML`
* `#Security/Keycloak`
* `#Security/ActiveDirectory`
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

### Machine Learning
* `#MachineLearning`
* `#MachineLearning/Supervised`
* `#MachineLearning/Unsupervised`
* `#MachineLearning/Reinforcement`
* `#MachineLearning/Metrics`
* `#MachineLearning/Optimization`
* `#MachineLearning/Regularization`
* `#MachineLearning/Ensembles`
* `#MachineLearning/DeepLearning`
* `#MachineLearning/DeepLearning/CNN`
* `#MachineLearning/DeepLearning/RNN`
* `#MachineLearning/DeepLearning/Transformers`
* `#MachineLearning/LLM`
* `#MachineLearning/LLM/GPT`
* `#MachineLearning/Embeddings`
* `#MachineLearning/RAG`
* `#MachineLearning/RAG/Retrieval`
* `#MachineLearning/MLOps`
* `#MachineLearning/MLOps/MLflow`
* `#MachineLearning/Tools`
* `#MachineLearning/Tools/PyTorch`
* `#MachineLearning/Tools/HuggingFace`

### UML
* `#UML`

### DSA
* `#DSA/Algorithms`
* `#DSA/Algorithms/Hashing`
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
* `#DSA/Algorithms/NP`
* `#DSA/DataStructures`
* `#DSA/DataStructures/Heap`
* `#DSA/DataStructures/Graph`
* `#DSA/Algorithms/Graph/ShortestPath`
* `#DSA/Algorithms/Graph/ReverseDelete`
* `#DSA/DataStructures/LinkedList`
* `#DSA/DataStructures/Set`
* `#DSA/DataStructures/Tree`
* `#DSA/DataStructures/Tree/BTree`
* `#DSA/DataStructures/Tree/RedBlack`
* `#DSA/DataStructures/Tree/AVL`
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
* `#DistributedSystems/Spark`
* `#DistributedSystems/Hadoop`

### Messaging
* `#Messaging`
* `#Messaging/Async`
* `#Messaging/AMQP`
* `#Messaging/MQTT`
* `#Messaging/Tools`
* `#Messaging/Tools/Kafka`
* `#Messaging/Tools/RabbitMQ`
* `#Messaging/Tools/ActiveMQ`
* `#Messaging/Tools/Artemis`
* `#Messaging/Tools/Flume`
* `#Messaging/Tools/Flink`

### Networking
* `#Networking`
* `#Networking/OSI`
* `#Networking/TCP`
* `#Networking/UDP`
* `#Networking/DNS`
* `#Networking/Modbus`
* `#Networking/Web`
* `#Networking/Web/HTML`
* `#Networking/Web/CSS`
* `#Networking/Web/MIME`
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
* `#Patterns/Enterprise/BPM`
* `#Patterns/Enterprise/BPM/Camunda`
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
* `#Patterns/Architecture/UI/MVC`
* `#Patterns/Architecture/UI/MVVM`
* `#Patterns/Architecture/UI/MicroFrontends`
* `#Patterns/Architecture/CQRS`
* `#Patterns/Architecture/Monolith`
* `#Patterns/Architecture/SOA`
* `#Patterns/Architecture/EventDriven`
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
* `#DevOps/Tools/Docker/Compose`
* `#DevOps/Tools/Kubernetes`
* `#DevOps/Tools/Helm`
* `#DevOps/Tools/OpenShift`
* `#DevOps/Tools/Nginx`
* `#DevOps/Tools/Terraform`
* `#DevOps/VCS`
* `#DevOps/VCS/Git`
* `#DevOps/VCS/BitBucket`
* `#DevOps/Shell`
* `#DevOps/Containerisation`
* `#DevOps/Virtualisation`
* `#DevOps/Orchestration`
* `#DevOps/Configuration`
* `#DevOps/Cloud`
* `#DevOps/Cloud/AWS`
* `#DevOps/Deployment`
* `#DevOps/Deployment/Strategies`
* `#DevOps/Deployment/Strategies/BlueGreen`
* `#DevOps/Deployment/Strategies/Canary`
* `#DevOps/Deployment/Strategies/Rolling`
* `#DevOps/CICD`
* `#DevOps/CICD/Jenkins`
* `#DevOps/CICD/GitLab`
* `#DevOps/CICD/TeamCity`

### Debugging
* `#Debugging`
* `#Debugging/Profiling`

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
* `#Caching/Infinispan`

### Logging
* `#Logging`

### Observability
* `#Observability`
* `#Observability/Prometheus`
* `#Observability/Grafana`

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
* `#ProgrammingLanguages/CSharp`
* `#ProgrammingLanguages/Python`
* `#ProgrammingLanguages/Go`
* `#ProgrammingLanguages/Compilation`
* `#ProgrammingLanguages/Interpretation`
* `#ProgrammingLanguages/ExecutionModel`
