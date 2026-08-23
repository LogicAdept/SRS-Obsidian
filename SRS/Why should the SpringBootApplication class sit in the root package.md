<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #Java/Annotations #SRS

# Why should the SpringBootApplication class sit in the root package?

> [!abstract] Short answer
> **`@SpringBootApplication`** meta-annotates **`@ComponentScan`** with default attributes, so scanning starts at **the package of the main class** and includes **only that package and its sub-packages**. Placing the main class in a **root application package** above controllers, services, and repositories ensures all project components are discovered without scanning every class on the classpath.

## What `@SpringBootApplication` scans

`@SpringBootApplication` combines:

- **`@EnableAutoConfiguration`** — pulls in Boot auto-config from the classpath (not tied to your package layout)
- **`@ComponentScan`** — registers `@Component`, `@Service`, `@Repository`, `@Controller`, and related stereotypes **from the main class’s package downward**
- **`@SpringBootConfiguration`** — marks the class as a configuration entry point

With no custom `scanBasePackages`, **`@ComponentScan` uses the package of the annotated class** as the base search package. Sub-packages are included; **sibling packages are not**.

```d2
direction: right
root: "com.example.myapplication\n@SpringBootApplication" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
customer: "customer.*\n(scanned)" {
  width: 160
  height: 70
  style.fill: "#e8f5e9"
}
order: "order.*\n(scanned)" {
  width: 160
  height: 70
  style.fill: "#e8f5e9"
}
web: "web.* sibling\n(not scanned)" {
  width: 180
  height: 70
  style.fill: "#fce4ec"
}

root -> customer
root -> order
root -> web: "outside\nsubtree"
```

**Fig. 1.** Recommended layout: main class at `com.example.myapplication`; feature packages live underneath.

## What goes wrong in a nested package

If the main class sits in **`com.acme.app.web`**, component scan covers **`com.acme.app.web.*`** only. A `@Service` in **`com.acme.app.service`** is a **sibling package**, so it is **not** registered — a common “my bean is not found” failure when `main` is moved into a feature sub-package.

The same base package also anchors **`@Entity`** scan (for JPA) and related “search package” behavior described in the Boot reference.

```java
// Recommended
package com.example.myapplication;

@SpringBootApplication
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

**Listing 1.** Root-package main class; `customer`, `order`, and other sub-packages are picked up automatically.

> [!warning] Default package and overly broad scans
> Classes with **no `package` declaration** sit in the default package. With `@SpringBootApplication`, that can make Spring read **classes from every JAR** on the classpath — slow startup and accidental bean registration. Boot recommends a reversed-domain root such as **`com.example.project`**. If the main class must stay nested, set an explicit scan base: `@SpringBootApplication(scanBasePackages = "com.acme.app")` or `scanBasePackageClasses`.

See [[What is Spring Boot]] and [[How does Spring Boot find auto-configuration classes]] — auto-configuration is classpath-driven; **component scan** is what the main-class package controls.

> [!tip] Interview answer
> @SpringBootApplication turns on @ComponentScan from the main class’s package and its sub-packages only. Put the application class in the root package above your features so services and repositories are discovered; a main class buried in com.acme.app.web will miss com.acme.app.service unless you override scanBasePackages.
