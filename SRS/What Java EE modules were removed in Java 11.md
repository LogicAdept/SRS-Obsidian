<!--
reps: 0
priority: 0
-->
#Java/Versions/11 #SRS

# What Java EE modules were removed in Java 11

> [!abstract] Short answer
> **JEP 320 removed six Java EE and CORBA modules from the JDK in Java 11: `java.xml.bind` (JAXB), `java.xml.ws` (JAX-WS), `java.activation` (JAF), `java.transaction`, `java.xml.ws.annotation` (Common Annotations), and `java.corba`.** Core XML parsing stayed (`java.xml`: SAX/DOM/StAX/XSLT), as did `java.sql`. The replacement is explicit dependencies — the Jakarta EE / Glassfish artifacts (`jakarta.xml.bind`, `jakarta.xml.ws`) or their `javax.xml.bind` ancestors for pre-3.0 stacks. This is the #1 concrete break when moving from 8 to 11/17 ([[What are the typical problems when upgrading from Java 8 to 17]]).

## What left, what stayed, why

The modules were **deprecated in Java 9** (JEP 320 marked them deprecated-for-removal; JEP 261 had already made them non-default) and **removed in 11**: Oracle would not evolve Java EE APIs inside the JDK while Java EE itself moved to the Eclipse Foundation (becoming Jakarta EE). Binding/WS frameworks version faster than the JDK and belong on the classpath with the app. `java.xml` parsing (SAX/DOM/StAX), `java.sql` (including `java.sql.Date`) and `java.naming` stayed — only the *EE* API surface left.

The failure mode: code that compiled on 8 with `javax.xml.bind.JAXB` compiles on 11 **only if a dependency provides it**, and libraries that reflectively load JAXB classes fail at **runtime** with `ClassNotFoundException`/`NoClassDefFoundError` — typically during marshalling, not at startup. Pre-Jakarta artifacts (`javax.xml.bind:jaxb-api` + a runtime like `org.glassfish.jaxb`) bridge old code; new code should target `jakarta.xml.bind` namespaces.

```d2
direction: down
j8: "JDK 8\njavax.xml.bind, javax.xml.ws,\njavax.activation, javax.transaction,\njava.corba all inside" {
  width: 380
  height: 90
  style.fill: "#fff8e1"
}
j11: "JDK 11 (JEP 320)\nEE + CORBA modules removed" {
  width: 320
  height: 70
  style.fill: "#ffcdd2"
}
dep: "add dependencies:\njaxb-api / jakarta.xml.bind + runtime" {
  width: 400
  height: 70
  style.fill: "#e8f5e9"
}
stay: "stayed: java.xml (SAX/DOM/StAX), java.sql, java.naming" {
  width: 440
  height: 60
  style.fill: "#e3f2fd"
}
j8 -> j11
j11 -> dep
j11 -> stay
```

**Fig. 1.** The EE surface left the JDK in two steps (deprecated 9, removed 11); parsing, SQL, and naming stayed. The fix is classpath dependencies, not JVM flags.

```java
public class V17_EeRemoved {
    public static void main(String[] args) {
        try {
            Class.forName("javax.xml.bind.JAXB");
            System.out.println("JAXB loaded (an explicit jar provides it)");
        } catch (ClassNotFoundException e) {
            System.out.println("ClassNotFoundException: " + e.getMessage());
        }
        // Core XML parsing stayed in the JDK (java.xml), only binding frameworks left:
        System.out.println("javax.xml.parsers still present: "
                + (javax.xml.parsers.DocumentBuilderFactory.class.getModule().getName()));
    }
}
```

**Listing 1.** Verified on JDK 21 (V17_EeRemoved in empirics): `ClassNotFoundException: javax.xml.bind.JAXB`, `javax.xml.parsers still present: java.xml` — JAXB is absent from the runtime while core XML parsing survives in `java.xml` (out/V17_EeRemoved.txt).

> [!warning] The failure is at runtime, inside a library, not in your imports
> The trap pattern: your code compiles fine because the build already had a JAXB jar transitively — or because nothing referenced JAXB — then a library (old Hibernate Validator, Jackson XML, SOAP clients) does `Class.forName("javax.xml.bind.DatatypeConverter")` deep inside a request and the stack trace surfaces in production. Second trap: `javax`→`jakarta` is an **ecosystem** boundary, not a JDK rule — the JDK never contained `jakarta.*`; Spring Boot 3/Tomcat 10 moved to Jakarta namespaces, but that is their packaging choice. Third: `--add-modules java.xml.bind` does **not** bring it back on 11+ — the module is gone, not hidden ([[What is the Java Platform Module System]]).

> [!tip] Interview answer
> **Java 11 removed the Java EE and CORBA modules — JAXB, JAX-WS, activation, transaction, common annotations, CORBA — deprecated in 9, gone in 11 (JEP 320).** Parsing (java.xml), SQL, and naming stayed. Migration means adding the JAXB/Jakarta dependencies explicitly, and the classic failure is a runtime ClassNotFoundException from a library, not a compile error.
