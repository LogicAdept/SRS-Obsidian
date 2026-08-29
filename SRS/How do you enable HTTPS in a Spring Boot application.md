<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Embedded #Java/Spring/Boot/Properties #SRS

# How do you enable HTTPS in a Spring Boot application?

> [!abstract] Short answer
> Set **`server.ssl.*`** on the embedded server (usually with **`server.port=8443`**) and point at trust material: a **Java KeyStore** (`server.ssl.key-store=classpath:…`), **PEM** cert/key files, or an **SSL bundle** (`server.ssl.bundle=…`). That **replaces** the plain HTTP connector — Boot does **not** give you 8080+8443 from properties alone.

## Declarative SSL on the embedded server

`server.ssl.*` is wired in `application.properties` / YAML. `classpath:` loads a keystore from `src/main/resources`. Appendix keys include `key-store`, `key-store-password`, `key-store-type`, and a separate **`key-password`** for the private key inside the store.

```properties
server.port=8443
server.ssl.key-store=classpath:keystore.jks
server.ssl.key-store-password=secret
server.ssl.key-password=another-secret
```

**Listing 1.** Official KeyStore shape. For PKCS12 use `server.ssl.key-store=classpath:keystore.p12` and `server.ssl.key-store-type=PKCS12` (`key-store-type` is the store format).

PEM alternative (prefer PKCS#8 keys): `server.ssl.certificate`, `server.ssl.certificate-private-key`, optional `server.ssl.trust-certificate`.

```properties
server.port=8443
server.ssl.bundle=mybundle
spring.ssl.bundle.jks.mybundle.key.alias=application
spring.ssl.bundle.jks.mybundle.keystore.location=classpath:application.p12
spring.ssl.bundle.jks.mybundle.keystore.password=secret
spring.ssl.bundle.jks.mybundle.keystore.type=PKCS12
```

**Listing 2.** Named bundle, then apply it with `server.ssl.bundle`. **Do not** mix `server.ssl.bundle` with discrete `server.ssl.key-store` / PEM properties. Ciphers/protocols then live under `spring.ssl.bundle…options`, not `server.ssl.ciphers`.

Tomcat and Netty can map host names to bundles for **SNI**; Jetty does not take that mapping the same way. Reloadable PEM bundles (`reload-on-update`) work with Tomcat/Netty only.

```d2
direction: right
material: "KeyStore / PEM / bundle" {
  width: 200
  height: 60
  style.fill: "#e3f2fd"
}
props: "server.port=8443\nserver.ssl.*" {
  width: 180
  height: 60
  style.fill: "#fff3e0"
}
https: "Embedded server\nHTTPS only" {
  width: 180
  height: 60
  style.fill: "#e8f5e9"
}

material -> props -> https
```

**Fig. 1.** One connector. Dual HTTP+HTTPS needs a **programmatic** extra connector; Boot recommends keeping **HTTPS** in properties ([[How do you change the port of the embedded server]], [[Which embedded containers are supported by Spring Boot]]).

> [!warning] Properties cannot run HTTP 8080 and HTTPS 8443 together
> Configuring `server.ssl.*` **drops** the plain HTTP connector on 8080. Spring Boot **does not** support both connectors through `application.properties`. If you need both, configure **one** programmatically (HTTP is the easier one). `management.server.ssl.*` is a **different** server when Actuator uses its own port.

> [!warning] Store password is not the key password, and it is a secret
> `key-store-password` opens the store; `key-password` opens the key entry — they can differ. Do not commit either. Bind them from the environment (`SERVER_SSL_KEY_STORE_PASSWORD`, and so on) ([[What is Spring Boot property source precedence]]). `server.ssl.bundle` cannot be combined with the discrete KeyStore/PEM keys under `server.ssl`.

> [!tip] Interview answer
> I enable HTTPS on the embedded server with server.ssl and usually server.port=8443, pointing key-store at a classpath PKCS12 or JKS, plus key-store-password and key-password. PEM files or a spring.ssl.bundle plus server.ssl.bundle are the other official shapes. That setup is HTTPS-only — Boot will not give you 8080 and 8443 from properties; a second connector is programmatic. Passwords belong in the environment, not in git.
