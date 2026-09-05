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

**Spring in the tree:** **`#Java/Spring/Framework/...`** is for **Spring Framework** modules (Web MVC, WebFlux, AOP, Cache, DataAccess, Testing, …). **Spring Boot** and **Spring Security** are separate projects: **`#Java/Spring/Boot`** and **`#Java/Spring/Security`**, not under Framework. Spring Data / Cloud / Batch / Integration / AMQP / Kafka stay as siblings under **`#Java/Spring`**. Java-language crypto and auth concepts stay **`#Java/Security`**, not Spring Security. **`#Java/Spring/Core`** is framework identity, versions, and ecosystem. The IoC container, beans, `BeanFactory`/`ApplicationContext`, `FactoryBean`, circular dependencies, and context events live under **`#Java/Spring/Core/IoC`**. **Dependency injection** (constructor / setter / field / method injection, wiring versus `new` or a locator, interface injection, why constructor injection) is **`#Java/Spring/Core/IoC/DI`**. Bean **autowiring** (`@Autowired`, `@Qualifier`, `@Primary`, XML `autowire` modes, `@Resource` vs `@Inject` matching) is **`#Java/Spring/Core/IoC/Autowiring`**. Bean **scopes** (including scoped proxies / `@Lookup`), **lifecycle** (`@PostConstruct` / destroy / `BeanPostProcessor`), **stereotypes** (`@Component` / `@Service` / `@Repository` / `@Controller`), **configuration** (XML vs Java vs annotations, `@Bean`, `@ComponentScan`, `@Profile`, `@Import`), and **SpEL** (`@Value`, `@PropertySource`, `Environment`) live under the matching **`#Java/Spring/Core/IoC/...`** child. **`#Java/Spring/Boot`** is Boot identity (what Boot is, Initializr, DevTools, AOT, Modulith, version deltas, `SpringApplication` / runners) and Boot-flavored how-tos that already carry another honest leaf. **Auto-configuration** (starters, `ConditionalOn*`, custom starters, `@SpringBootApplication` and its default component-scan package) is **`#Java/Spring/Boot/AutoConfiguration`**. **Externalized config** (`application.properties`/`yml`, property order, `@ConfigurationProperties`, Boot profiles) is **`#Java/Spring/Boot/Properties`**. **Embedded servlet container**, jar vs WAR as a *runtime* choice (external container, `SpringBootServletInitializer`), and server SSL/compression are **`#Java/Spring/Boot/Embedded`**. **Build** (Maven/Gradle parent, BOM, fat/executable JAR, how you ship the app) is **`#Java/Spring/Boot/Build`**. **Actuator** and **Admin** stay their leaves. **Filter chain** (`FilterChainProxy`, `SecurityFilterChain`, `HttpSecurity`, named servlet filters, `addFilterBefore`/`After`) is **`#Java/Spring/Security/FilterChain`**. **Method security** (`@PreAuthorize`, `@Secured`, `@EnableMethodSecurity` / `@EnableGlobalMethodSecurity`, `@PreFilter`/`@PostFilter`) is **`#Java/Spring/Security/MethodSecurity`**. **Authentication** (`UserDetails` / `UserDetailsService`, `AuthenticationManager` / `AuthenticationProvider`, form login, HTTP Basic, remember-me, principal vs credentials, `AuthenticationEntryPoint` / `AccessDeniedHandler`) is **`#Java/Spring/Security/Authentication`**. **SecurityContext** (`SecurityContextHolder`, strategies, repository, async propagation) is **`#Java/Spring/Security/SecurityContext`**. **PasswordEncoder** (`PasswordEncoder`, `DelegatingPasswordEncoder`, BCrypt/Argon2/PBKDF2, encode vs matches) is **`#Java/Spring/Security/PasswordEncoder`** (dual-tag **`#Security/Cryptography`** when the cue is hashing/encoders). **CSRF** (`CsrfToken`, repositories, AJAX/JSON token, CSRF vs CORS, CSRF off for JWT APIs) is **`#Java/Spring/Security/CSRF`**. **Session management** (`SessionCreationPolicy`, fixation, `maximumSessions`) is **`#Java/Spring/Security/SessionManagement`**, not **`#Java/Spring/Session`** (the Spring Session project). **OAuth2** (`oauth2Login` / `oauth2Client` / `oauth2ResourceServer`, grants, `JwtDecoder` / `NimbusJwtDecoder` / opaque introspection, Keycloak as an OIDC broker) is **`#Java/Spring/Security/OAuth2`**; still dual-tag **`#Security/OAuth2`**, **`#Security/JWT`**, **`#Security/OIDC`**, **`#Security/Keycloak`** as they apply. **SAML** (`saml2Login`) stays on **`#Java/Spring/Security`** plus **`#Security/SAML`**. Tests dual-tag **`#Java/Spring/Framework/Testing`**. **Reactive HTTP security** (`SecurityWebFilterChain`, `ServerHttpSecurity`, `authorizeExchange`, `pathMatchers`, `@EnableWebFluxSecurity`) is **`#Java/Spring/Security/WebFlux`**; dual-tag **`#Java/Spring/Framework/WebFlux`**, not FilterChain. **`#Java/Spring/Transactions`** is Spring transaction management (`PlatformTransactionManager` / `TransactionTemplate`, `@Transactional`, default rollback). **Propagation** (`REQUIRED`, `REQUIRES_NEW`, `NESTED`, and the other `Propagation` values) is **`#Java/Spring/Transactions/Propagation`**. **Calls between `@Transactional` methods** (proxy self-invocation versus a cross-bean call, and how that interacts with propagation and rollback) is **`#Java/Spring/Transactions/SelfInvocation`**. Test-level `@Transactional` dual-tags **`#Java/Spring/Framework/Testing`**. AOP as the interceptor mechanism dual-tags **`#Java/Spring/Framework/AOP`**. Do not put **`#Java/Spring`** next to a more specific **`#Java/Spring/...`** child, **`#Java/Spring/Core`** next to **`#Java/Spring/Core/IoC`**, **`#Java/Spring/Core/IoC`** next to a more specific **`#Java/Spring/Core/IoC/...`** child, **`#Java/Spring/Boot`** next to a more specific **`#Java/Spring/Boot/...`** child, **`#Java/Spring/Security`** next to a more specific **`#Java/Spring/Security/...`** child, or **`#Java/Spring/Transactions`** next to a more specific **`#Java/Spring/Transactions/...`** child.

**Annotations in the tree:** **`#Java/Annotations`** is the Java annotation mechanism (declaration, retention, repeatable, records, marker-interface replacement). A card about a **Spring-specific annotation** (`@Autowired`, `@Bean`, `@Transactional`, `@SpringBootApplication`, …) carries the honest **`#Java/Spring/...`** leaf **and** **`#Java/Annotations`**. Do not put **`#Java/Annotations`** on Spring cards that are not about an annotation (container identity, scopes, circular dependencies, XML-only wiring). JPA / JUnit annotation cards likewise carry their persistence or testing leaf **and** **`#Java/Annotations`**.

**Records in the tree:** **`#Java/Language/Records`** is the record type (header versus class, generated members, restrictions, versus Lombok `@Value`). **Constructors** is the canonical constructor, the compact form, and extra constructors that must `this(...)` into the canonical one. Do not put **`#Java/Language/Records`** next to **`#Java/Language/Records/Constructors`** on the same card. Compact constructors stay here, not **`#Java/OOP/Constructors`**. JPA / Jackson / Java serialization / reflection / annotation-on-component cards dual-tag those leaves. Record-generated `equals`/`hashCode` dual-tags **`#Java/HashCodeEquals`** (or **Contract** / **Implementation** when those own the cue).

**Concurrency in the tree:** **`#Java/Concurrency`** is the Java threading model. Child leaves: **`Threads`** (lifecycle, `Thread`/`Runnable`, join/sleep/interrupt/daemon), **`Executors`** (pools, `Future`/`Callable`/`CompletableFuture`, ForkJoin), **`Synchronizers`** (`CountDownLatch`, `CyclicBarrier`, `Phaser`, `Semaphore`, `Exchanger`), **`Atomics`** (`java.util.concurrent.atomic`, CAS), **`VirtualThreads`**, **`Synchronization`** (monitors, wait/notify, intrinsic locks). **`Synchronization/SynchronizedKeyword`** is the `synchronized` keyword (methods, blocks, `this` vs `Class` monitor, private mutex objects). **`Synchronization/Locks`** is `java.util.concurrent.locks` (`Lock`, `ReentrantLock`, `ReadWriteLock`, `StampedLock`, `Condition`). Concurrent collections stay **`#Java/Collections/Concurrency`**. **`CopyOnWrite`** (`CopyOnWriteArrayList` / `CopyOnWriteArraySet`, snapshot iterators, write-copy cost) is **`#Java/Collections/Concurrency/CopyOnWrite`**. The Java Memory Model stays **`#Java/JMM`**. Do not put **`#Java/Concurrency`** next to a more specific **`#Java/Concurrency/...`** child, **`#Java/Concurrency/Synchronization`** next to a more specific **`#Java/Concurrency/Synchronization/...`** child, or **`#Java/Collections/Concurrency`** next to **`#Java/Collections/Concurrency/CopyOnWrite`**, on the same card.

**Collections in the tree:** **`#Java/Collections`** is the framework (interfaces, `Collection` vs `Collections`, hierarchy surveys). **Unmodifiable** is unmodifiable views and factories (`Collections.unmodifiable*`, `emptyList` / `emptySet` / `emptyMap`, `List.of` / `Set.of` / `Map.of` / `copyOf`, optional mutators / `UnsupportedOperationException`). Dual-tag **`#Java/Immutability`** when the cue is immutable versus unmodifiable. Implementations live under **`List`**, **`Map`**, **`Set`**, **`Queues`**. List impls: **`ArrayList`**, **`LinkedList`**, **`Vector`**. Set impls: **`HashSet`**, **`LinkedHashSet`**, **`TreeSet`**, **`EnumSet`**. Queue impls: **`ArrayDeque`**, **`PriorityQueue`**, **`BlockingQueue`**. Concurrent collections stay **`#Java/Collections/Concurrency`**. Iterators stay **`#Java/Collections/Iteration`**. **FailFast** (under Iteration) is fail-fast vs fail-safe iterator behavior, `ConcurrentModificationException`, structural modification, and snapshot / weakly consistent contrast. **Sorting** is `Collections.sort` / `List.sort` / `Arrays.sort`, `Collections.reverse`, and sorted-map key order (dual-tag **`Map/TreeMap`** or **`Map`** when the cue is `SortedMap`). **Comparable** is `java.lang.Comparable` / `compareTo` / natural order. **Comparator** is `java.util.Comparator` / `compare` / `comparing*` / lambdas as sort order (dual-tag **`#Java/Lambdas`** when the cue is a lambda). Comparison of the two interfaces carries **Comparable** and **Comparator**. Array-algorithm cards dual-tag **`#Java/Arrays`**. Do not put **`#Java/Collections`** or a family tag (`List`/`Set`/`Map`/`Queues`) next to a more specific child on the same card, **`#Java/Collections`** next to **`#Java/Collections/Unmodifiable`**, **`#Java/Collections/Iteration`** next to **`#Java/Collections/Iteration/FailFast`**, or **`#Java/Collections/Sorting`** next to a more specific **`#Java/Collections/Sorting/...`** child. Comparison cards carry both implementation leaves.

**Streams in the tree:** **`#Java/Streams`** is the `java.util.stream` API (what a `Stream` is, vs `Collection`, sources/creation, pipeline internals / `Spliterator`, `Optional.stream()`). **Operations** is the two kinds (intermediate vs terminal) as a catalog, laziness, and when the pipeline starts. **Operations/Intermediate** is intermediate ops (`filter`, `map` / `flatMap`, `sorted`, `limit`, `distinct`, `peek`). **Operations/Terminal** is terminal ops (`collect` / `Collector`, `forEach` / `forEachOrdered`, `reduce`, `min` / `max` / `sum` / `average`, `count`). **Parallel** is `parallelStream()` / `parallel()`, sequential vs parallel, and ForkJoin / `Spliterator` backing (dual-tag **`#Java/Parallelism`**). Sequential vs parallel is a mode, not a third kind of operation. Byte/char IO streams stay **`#Java/IO`**. Reactive streams stay **`#Java/Library/Reactor`** / **`#Paradigms/Reactive`**. Do not put **`#Java/Streams`** next to a more specific **`#Java/Streams/...`** child, or **`#Java/Streams/Operations`** next to a more specific **`#Java/Streams/Operations/...`** child, on the same card.

**HashCodeEquals in the tree:** **`#Java/HashCodeEquals`** is `equals` / `hashCode` as hash-based collections use them (map/set keys, collisions, IdentityHashMap versus `equals`, TreeMap consistent-with-equals). **Contract** is `Object.equals` (the five properties, `==` versus `equals`, `null`) and `Object.hashCode` (equal objects share a hash, consistency with `equals`, default identity implementations). **Implementation** is how to override them (the `equals(Object)` signature, which fields, pitfalls, the `equals(MyClass)` overload trap, `hashCode` combiners). Do not put **`#Java/HashCodeEquals`** next to a more specific **`#Java/HashCodeEquals/...`** child on the same card. Collection cards dual-tag the collection leaf. Record-generated members dual-tag **`#Java/Language/Records`**. Default `Object` members dual-tag **`#Java/Language/Object`**. Enum `==` versus `equals` dual-tags **`#Java/Language/Enum`**.

**Exceptions in the tree:** **`#Java/Exceptions`** is the Java exception model (handling practices, custom types, `throw`/propagation). **Hierarchy** is `Throwable` and the Exception/Error/RuntimeException tree. **Checked** is checked exceptions (`throws`, wrapping, the checked-exception debate). **Unchecked** is `RuntimeException` and common kinds (NPE, CCE). **Error** is `java.lang.Error` and JVM errors (OOM, StackOverflowError, ExceptionInInitializerError, AssertionError). **TryCatch** is try/catch/finally, multi-catch, catch order, and which try forms are legal. **TryWithResources** (under TryCatch) is try-with-resources, `AutoCloseable`, suppressed exceptions on `close`, and TWR vs try-finally when both throw. Catalog-of-try-forms cards stay on **TryCatch**. Checked vs unchecked comparison cards carry **Checked** and **Unchecked**. Error vs Exception comparison carries **Error** and **Hierarchy**. Do not put **`#Java/Exceptions`** next to a more specific **`#Java/Exceptions/...`** child, or **`#Java/Exceptions/TryCatch`** next to **`#Java/Exceptions/TryCatch/TryWithResources`**, on the same card.

**Assert in the tree:** **`#Java/Language/Assert`** is the Java `assert` keyword (`assert cond;` / `assert cond : detail;`), runtime enable/disable (`-ea` / `-da` / `-esa` / `-dsa`, package and class filters), and `AssertionError` from a failed `assert`. Test-library assertions (JUnit `assertEquals` / `assertThrows` / `assertAll`, AssertJ, Hamcrest, JSONAssert, hard vs soft) stay **`#Java/Testing/...`**, not Language/Assert. `AssertionError` cards dual-tag **`#Java/Exceptions/Error`**. Do not put **`#Java/Language`** next to **`#Java/Language/Assert`** on the same card.

**Runtime in the tree:** **`#Java/Runtime`** is the process-level API (`java.lang.Runtime`, `java.lang.System`: standard streams, `System.exit`, environment and properties, `Runtime.exec` / shutdown hooks). The **JRE product** (JVM + libraries, no compiler) is **`#Java/JRE`**, not Runtime. JVM internals stay **`#Java/JVM/...`**. Compile-time vs runtime **language** semantics (dynamic dispatch / polymorphism) stay **`#Java/OOP`** and **`#Java/Language`**. Do not put **`#Java/Runtime`** next to a more specific **`#Java/Runtime/...`** child on the same card.

**JVM in the tree:** **`#Java/JVM`** is the virtual machine as a platform (what the JVM is, JRE vs JDK vs JVM, bytecode portability, other languages on the VM, startup, interpreter-plus-JIT as the execution engine, compiled vs interpreted). **Memory** is runtime data areas (heap, stacks / frames, Metaspace vs PermGen, string-pool *location*, off-heap, object layout / size, strong / weak / soft / phantom references). **GarbageCollector** is reachability, generations, collector algorithms (Serial / Parallel / CMS / G1 / ZGC / Shenandoah), and finalization as a GC hook. Do not add per-collector leaves. **ClassLoaders** is class loading, parent delegation, and the classpath (`Class.forName` / `getClass` dual-tag **`#Java/Language/Reflection/Class`**). **JIT** is just-in-time compilation, inlining, and escape analysis — not the whole execution engine. **Tuning** is launch flags, heap / thread dumps, and profilers. Dual-tag **`#Java/Bytecode`** for class-file / instruction encoding, **`#Java/JMM`** for the memory model, **`#Java/Runtime`** for `java.lang.Runtime` / `System`, **`#Java/String`** when the cue is the string *type* or intern API rather than the pool as a region, **`#Java/JRE`** / **`#Java/JDK`** on product comparisons. Do not put **`#Java/JVM`** next to a more specific **`#Java/JVM/...`** child on the same card. Memory-layout vs GC comparison cards carry **Memory** and **GarbageCollector**.

**Memory in the tree:** **`#Java/JVM/Memory`** is JVM run-time data areas as a whole (method area / Metaspace, off-heap/native, constant-pool metadata, region surveys). **Heap** is the Java object heap (instances/arrays, allocation, `-Xmx`, heap dumps, generational heap layout, interned `String` objects). **Stack** is per-thread JVM stacks and frames (`-Xss`, stack overflow). **References** is `java.lang.ref` reachability (strong/soft/weak/phantom, `ReferenceQueue`, `WeakHashMap` as a GC-aware map). Stack vs heap comparison cards carry **Heap** and **Stack**. GC algorithm cards stay **`#Java/JVM/GarbageCollector`** (dual-tag Heap when the cue is young/old layout or heap roots). Do not put **`#Java/JVM/Memory`** next to a more specific **`#Java/JVM/Memory/...`** child on the same card.

**GarbageCollector in the tree:** **`#Java/JVM/GarbageCollector`** is HotSpot garbage collection: reachability and tracing, generations, collector identity (Serial, Parallel, CMS, G1, ZGC, Shenandoah), and `System.gc`. Collector and reachability cards use this leaf, not **`#Java/JVM`**. Dual-tag **`#Java/JVM/Memory`** when the cue owns heap/stack/Metaspace regions; **`#Java/JVM/Tuning`** when it owns flags/ergonomics; **`#Java/Legacy`** for CMS or `finalize` history; **`#Java/Versions`** for default-collector-by-release surveys (stay on the Versions parent, not `/8` plus `/9`). `Object.finalize` / finalization dual-tags **`#Java/Language/Object/Finalize`**. `IDisposable` versus a finalizer dual-tags **`#ProgrammingLanguages/CSharp`**. Do not add per-collector children (`/G1`, `/ZGC`, …) for a single identity card. Do not put **`#Java/JVM`** next to **`#Java/JVM/GarbageCollector`** on the same card.

**Optional in the tree:** **`#Java/Language/Optional`** is `java.util.Optional` (what it is versus `null`, factories `of` / `ofNullable` / `empty`, `map` / `flatMap` / `filter` / `stream`, `isPresent` / `ifPresent` / `or` / `orElseThrow` / `get`, primitive `OptionalInt` / `OptionalLong` / `OptionalDouble`). **Usage** is intended-use rules: return type not field or parameter, never return a null `Optional`, do not wrap a collection, avoid `get()`, allocation cost, not `Serializable`. Primitive optionals dual-tag **`#Java/Language/Primitives`**. Stream bridging dual-tags **`#Java/Streams`**. Serialization of Optional dual-tags **`#Java/Serialization`**. Do not put **`#Java/Language/Optional`** next to **`#Java/Language/Optional/Usage`** on the same card.

**Wrappers in the tree:** **`#Java/Language/Wrappers`** is the eight `java.lang` boxing types (`Boolean`, `Byte`, `Character`, `Short`, `Integer`, `Long`, `Float`, `Double`): why they exist, immutability, null vs primitive defaults, collections/generics, parse/format APIs (`parseInt`, `toBinaryString`). **Autoboxing** is compiler boxing/unboxing (`valueOf` / `xxxValue`, when it occurs, NPE on unbox, overload-resolution phases, `++`/`+=` on a wrapper). **Cache** (under Autoboxing) is interned identity (`IntegerCache`, `-XX:AutoBoxCacheMax`, `Boolean.TRUE`/`FALSE`, which types cache, `valueOf` vs `new`). Identity/why-wrappers and parse/format cards stay on **Wrappers**. Survey cards that span unboxing and cache stay on **Wrappers**. Dual-tag **`#Java/Language/Primitives`** when the cue is primitive vs wrapper. Do not put **`#Java/Language/Wrappers`** next to a more specific **`#Java/Language/Wrappers/...`** child, or **`#Java/Language/Wrappers/Autoboxing`** next to **`#Java/Language/Wrappers/Autoboxing/Cache`**, on the same card.

**Primitives in the tree:** **`#Java/Language/Primitives`** is the Java primitive types (`boolean`, `byte`, `short`, `char`, `int`, `long`, `float`, `double`): identity, ranges, signedness, default/local initialization, not being `Object`. **NumericPromotion** is JLS binary/unary numeric promotion in arithmetic (why `byte + byte` is `int`, why `char + char` does not concatenate, why `int * int` overflows before a `long` assignment). **FloatingPoint** is IEEE 754 `float`/`double` (binary fractions, `float` vs `double`, `BigDecimal` for decimals, floating-point `/0`). Do not add per-type leaves (`ShortType`, `CharType`, …). Primitive vs wrapper comparison and autoboxing/unboxing cards carry **`#Java/Language/Wrappers`** and **`#Java/Language/Primitives`**. Integer overflow wrap, integer `/`, and numeric literals stay on **Primitives** unless a child owns the cue. Bit shifts (`<<`, `>>`, `>>>`) live under **`#Java/Language/Operators/Bitwise`**. Do not put **`#Java/Language/Primitives`** next to a more specific **`#Java/Language/Primitives/...`** child on the same card.

**Exercises in the tree:** **`#Career/Interview/Exercises`** is interview drills: predict-the-output / print-to-console / line-by-line tracing, and implement-this coding problems. A Java print-to-console snippet carries **Exercises** plus the honest topical leaf (Primitives, Autoboxing, Initialization, Lambdas, …). There is **no `#Java/CodeSnippet`** and no `#Exercise` root. Do not put **`#Career/Interview`** next to **`#Career/Interview/Exercises`** on the same card.

**Language in the tree:** **`#Java/Language`** is Java the language (identity, typing, `var`, source form, `instanceof`). Predict-the-output snippets stay **`#Career/Interview/Exercises`** plus a topical leaf, not on Language alone. **NestedClasses** is nested / inner / static nested / local / anonymous classes (enclosing instance, when to use each kind). **Modifiers** is the modifier catalog (`abstract`, `transient`, `volatile`, `synchronized` as a modifier — dual-tag **`#Java/JMM`**, **`#Java/Serialization`**, or **`#Java/Concurrency/Synchronization/SynchronizedKeyword`** as they apply). **Access** is `public` / `protected` / `private` / package-private. **Static** is the `static` keyword (members, `main`, which constructs may be `static`). **Final** is `final` on types, methods, and fields, and effectively-final. **Operators** is ternary, logical, and bitwise (not numeric promotion — that is **Primitives/NumericPromotion**; not `++` atomicity — that is **`#Java/JMM`**). **Parameters** is pass-by-value (the reference is copied). **Loops** is `for` / `while` / `do-while` and enhanced for-each (Iterable dual-tags **`#Java/Collections/Iteration`**). **Switch** is `switch` (strings in `switch`, arrow / `yield`, versus pattern matching). Record patterns in `switch` dual-tag **`#Java/Language/Records`**. **Object** is `java.lang.Object` (root type, generated / inherited members, `clone` / `Cloneable`, `finalize`). `equals` / `hashCode` stay **`#Java/HashCodeEquals`** (**Contract** / **Implementation** when those own the cue). `wait` / `notify` stay **`#Java/Concurrency/Synchronization`**. Constructors and initializer blocks stay **`#Java/OOP/Constructors`** and **`#Java/OOP/Initialization`**. Inheritance, polymorphism, and the `interface` type stay **`#Java/OOP/Inheritance`**, **`#Java/OOP/Polymorphism`**, and **`#Java/OOP/Interfaces`**. Do not put **`#Java/Language`** next to a more specific **`#Java/Language/...`** child, **`#Java/Language/Modifiers`** next to a more specific **`#Java/Language/Modifiers/...`** child, **`#Java/Language/Optional`** next to **`#Java/Language/Optional/Usage`**, **`#Java/Language/Primitives`** next to a more specific **`#Java/Language/Primitives/...`** child, **`#Java/Language/Records`** next to **`#Java/Language/Records/Constructors`**, **`#Java/Language/Wrappers`** next to a more specific **`#Java/Language/Wrappers/...`** child, **`#Java/Language/Wrappers/Autoboxing`** next to **`#Java/Language/Wrappers/Autoboxing/Cache`**, or **`#Java/Language/Reflection`** next to a more specific **`#Java/Language/Reflection/...`** child, on the same card.

**OOP in the tree:** **`#Java/OOP`** is object-oriented programming in Java (what OOP is, principle surveys, class vs object, abstraction as a principle, composition/aggregation, POJO/DTO surveys). **Encapsulation** is hiding state and publishing an API (`private` fields, package as a boundary, public mutable fields as the failure mode). Dual-tag **`#Java/Language/Modifiers/Access`** when the cue is an access modifier. The `abstract` keyword stays **`#Java/Language/Modifiers/Abstract`**. **Inheritance** is `extends`, inherited members, single class inheritance, and is-a. **Polymorphism** is subtype dispatch, overriding, overloading, and static vs dynamic binding. **Interfaces** is the `interface` type (members, default/static/private methods, marker interfaces, vs abstract class). **Constructors** and **Initialization** stay their leaves. Do not put **`#Java/OOP`** next to a more specific **`#Java/OOP/...`** child. Interface vs abstract class carries **Interfaces** and **`#Java/Language/Modifiers/Abstract`**. Multiple inheritance of type (class vs interface) carries **Inheritance** and **Interfaces**. Nested classes stay **`#Java/Language/NestedClasses`**. `java.lang.Object` as root dual-tags **`#Java/Language/Object`**.

**Reflection in the tree:** **`#Java/Language/Reflection`** is the reflection API as a whole (what it is, use cases, drawbacks, and lookup that spans `Class` and members). **Class** is `java.lang.Class` (how you obtain it, `forName` / `getClass`, array `Class`, superclass/interfaces, `ClassNotFoundException` versus `NoClassDefFoundError` as by-name lookup). **Members** is `Field` / `Method` / `Constructor` / `AccessibleObject` (`get` versus `getDeclared`, `invoke`, `newInstance`, static and `final` fields, `setAccessible`). **Proxy** is `java.lang.reflect.Proxy` / `InvocationHandler` (JDK dynamic proxies; Spring AOP dual-tags **`#Java/Spring/Framework/AOP`**). Runtime annotation lookup dual-tags **`#Java/Annotations`** and stays on **Reflection** when the cue is not Class-only or Members-only. Record reflection dual-tags **`#Java/Language/Records`**. Do not put **`#Java/Language/Reflection`** next to a more specific **`#Java/Language/Reflection/...`** child on the same card.

**Versions in the tree:** **`#Java/Versions/N`** is Java SE **N** (the marketing number: **5** not 1.5). Use the child that matches the release the cue is about. Survey / LTS-roadmap / “which versions have you used” cards stay on **`#Java/Versions`**. Introductions that have no child yet (1.2 Collections, 1.4 `assert`, Java 6 `NavigableMap`, and other one-off SE numbers) also stay on the parent — do not add `/1.2`, `/6`, `/10`, `/15`, or `/25` for a single card. A feature that *shipped* in 8 and was later removed still uses **`#Java/Versions/8`** unless the cue is the removal release and that leaf exists. Dual-tag sibling version leaves when the cue is two specific SE lines (17 and 21). Do not put **`#Java/Versions`** next to **`#Java/Versions/N`** on the same card.

---

## Tree (prefixes in cards)

### Java
* `#Java`
* `#Java/Collections`
* `#Java/Collections/Unmodifiable`
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
* `#Java/Collections/Queues/Deque`
* `#Java/Collections/Queues/PriorityQueue`
* `#Java/Collections/Queues/BlockingQueue`
* `#Java/Collections/Iteration`
* `#Java/Collections/Iteration/FailFast`
* `#Java/Collections/Sorting`
* `#Java/Collections/Sorting/Comparable`
* `#Java/Collections/Sorting/Comparator`
* `#Java/Collections/Concurrency`
* `#Java/Collections/Concurrency/CopyOnWrite`
* `#Java/Streams`
* `#Java/Streams/Operations`
* `#Java/Streams/Operations/Intermediate`
* `#Java/Streams/Operations/Terminal`
* `#Java/Streams/Parallel`
* `#Java/HashCodeEquals`
* `#Java/HashCodeEquals/Contract`
* `#Java/HashCodeEquals/Implementation`
* `#Java/OOP`
* `#Java/OOP/Encapsulation`
* `#Java/OOP/Initialization`
* `#Java/OOP/Constructors`
* `#Java/OOP/Inheritance`
* `#Java/OOP/Polymorphism`
* `#Java/OOP/Interfaces`
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
* `#Java/Language/Loops`
* `#Java/Language/Modifiers`
* `#Java/Language/Modifiers/Abstract`
* `#Java/Language/Modifiers/Access`
* `#Java/Language/Modifiers/Final`
* `#Java/Language/Modifiers/Static`
* `#Java/Language/Modifiers/Volatile`
* `#Java/Language/NestedClasses`
* `#Java/Language/Object`
* `#Java/Language/Object/Clone`
* `#Java/Language/Object/Finalize`
* `#Java/Language/Operators`
* `#Java/Language/Operators/Bitwise`
* `#Java/Language/Operators/Logical`
* `#Java/Language/Operators/Ternary`
* `#Java/Language/Optional`
* `#Java/Language/Optional/Usage`
* `#Java/Language/Parameters`
* `#Java/Language/Primitives`
* `#Java/Language/Primitives/Conversions`
* `#Java/Language/Primitives/FloatingPoint`
* `#Java/Language/Primitives/NumericPromotion`
* `#Java/Language/Records`
* `#Java/Language/Records/Constructors`
* `#Java/Language/Reflection`
* `#Java/Language/Reflection/Class`
* `#Java/Language/Reflection/Members`
* `#Java/Language/Reflection/Proxy`
* `#Java/Language/Switch`
* `#Java/Language/Wrappers`
* `#Java/Language/Wrappers/Autoboxing`
* `#Java/Language/Wrappers/Autoboxing/Cache`
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
* `#Java/JVM/Memory/Heap`
* `#Java/JVM/Memory/Stack`
* `#Java/JVM/Memory/References`
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
* `#Patterns/Enterprise/Integration/Channels/DatatypeChannel`
* `#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel`
* `#Patterns/Enterprise/Integration/Channels/DeadLetterChannel`
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
