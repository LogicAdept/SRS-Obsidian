<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #SRS

# What is Spring AOT and GraalVM native image support?

> [!abstract] Short answer
> **Spring AOT** is **build-time** processing of your **bean definitions**: it emits **Java sources**, **proxy bytecode**, an **`ApplicationContextInitializer`**, and GraalVM **JSON hints** under **`META-INF/native-image`**. A **GraalVM native image** is a **platform-specific executable** built from that closed-world analysis — **no JVM in the box**, **faster start**, **smaller RSS**. AOT is **required for native**; you can also run AOT code **on the JVM** with **`-Dspring.aot.enabled=true`**. It is **not** Java 25’s **AOT cache** / CDS.

## Closed world, then generate

Native images **statically analyze from `main`**. Unreachable code is **stripped**. Reflection, resources, serialization, and JDK proxies need **hints**. The **classpath is frozen**. Spring Boot auto-config is **runtime-dynamic**, so native mode assumes a **closed world** and **restricts** that dynamism ([[What changed in Spring Boot 3]]).

```java
@Configuration(proxyBeanMethods = false)
public class MyConfiguration {

	@Bean
	public MyBean myBean() {
		return new MyBean();
	}
}
```

**Listing 1.** On the JVM, `@Configuration` is **parsed at startup** and `@Bean` methods run via **reflection**. AOT **does not create bean instances**; it walks definitions and writes equivalent **`MyConfiguration__BeanDefinitions`** (plus initializer) GraalVM can see. Maven sources: `target/spring-aot/main/sources`; Gradle: `build/generated/aotSources`. Hints: `resource-config.json`, `reflect-config.json`, `serialization-config.json`, `proxy-config.json`, `jni-config.json`. Extra hints if generated ones are not enough.

```bash
mvn -Pnative package
java -Dspring.aot.enabled=true -jar myapplication.jar
```

**Listing 2.** AOT **on the JVM** (log: `Starting AOT-processed …`). Gradle: `org.springframework.boot.aot` plugin. Native executable: Boot **buildpacks** (`bootBuildImage`) or GraalVM **`native-image`** on an AOT-processed JAR ([[What is an executable JAR in Spring Boot]]).

Closed-world **Spring** limits (native **and** `spring.aot.enabled`):

- **`@Profile`** / profile-specific config have **limitations**
- **`@ConditionalOnProperty`** and other “create this bean if a property says so” switches are **not supported** ([[What is ConditionalOnProperty in Spring Boot]], [[What is a Spring profile]])

```d2
direction: down
aot: "Spring AOT\nsources + proxies + hints" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
jvm: "JVM + spring.aot.enabled" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
nat: "GraalVM native executable\nno JRE, fast start, low RSS" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

aot -> jvm
aot -> nat
```

**Fig. 1.** Native: **no lazy class loading** (everything in the binary is loaded at start). Suited to **containers / FaaS**. Docs do **not** claim native wins **peak throughput** for long-lived JVMs. Tracing agent can fill missing hints; Spring relies on **GraalVM reachability metadata** for many third-party libs.

> [!warning] Spring AOT ≠ HotSpot AOT cache
> Java **25+** **AOT cache** (`-XX:AOTCache`) / older **CDS** is a **JVM** training-run cache. Docs say it can be **combined** with Spring AOT. It is **not** `native-image`. Boot’s “no code generation” goal **excepts native image** ([[What is Spring Boot]]).

> [!warning] AOT JAR is not automatically faster
> Packaging with `-Pnative` only **includes** generated init code. The JVM still uses the **old** refresh path unless **`spring.aot.enabled=true`**. `@ConditionalOnProperty` that **flips beans after build** will not match native/AOT reality.

> [!tip] Interview answer
> Spring AOT runs at build time, writes bean-definition source, proxies, and GraalVM hints. A native image is a closed-world binary with fast startup and a small RSS. I use native for scale-to-zero and containers. I can also run that AOT code on the JVM with spring.aot.enabled. Profiles and property conditions that change the bean graph are limited.
