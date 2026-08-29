<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/AutoConfiguration #Java/Spring/Boot/Properties #SRS

# How do you send email from a Spring Boot application?

> [!abstract] Short answer
> Add **`spring-boot-starter-mail`** and set **`spring.mail.host`** (plus port / credentials as needed). Boot’s **`MailSenderAutoConfiguration`** then creates a **`JavaMailSender`** if you did not define one. Inject it and **`send`** a **`SimpleMailMessage`** (plain text) or a **`MimeMessage`** via **`MimeMessageHelper`** (HTML, attachments). Jakarta Mail is on the classpath (`org.eclipse.angus:angus-mail`). Put **SMTP timeouts** in **`spring.mail.properties`** — the JavaMail defaults are **infinite**.

## Auto-config a `JavaMailSender`, then `send`

The starter is “Java Mail and Spring Framework’s email sending support” ([[Which common Spring Boot starters do you know]]). Condition: **host** is set, the mail libraries are present, and **no** `JavaMailSender` bean exists yet. Bindings live on **`MailProperties`** (`spring.mail`). **`spring.mail.jndi-name`** (a Jakarta Mail `Session`) **wins** over host/username/password.

```properties
spring.mail.host=smtp.example.com
spring.mail.port=587
spring.mail.username=${SMTP_USER}
spring.mail.password=${SMTP_PASSWORD}
spring.mail.properties[mail.smtp.auth]=true
spring.mail.properties[mail.smtp.starttls.enable]=true
spring.mail.properties[mail.smtp.connectiontimeout]=5000
spring.mail.properties[mail.smtp.timeout]=3000
spring.mail.properties[mail.smtp.writetimeout]=5000
```

**Listing 1.** Appendix keys: `protocol` defaults to **`smtp`**, `default-encoding` to **`UTF-8`**. YAML must quote dotted JavaMail keys (`"[mail.smtp.timeout]"`). Implicit SSL: **`spring.mail.ssl.enabled`** / **`spring.mail.ssl.bundle`** (hostname verification default **`true`**). **`spring.mail.test-connection=true`** probes SMTP at startup (default **`false`**).

```java
@Service
public class OrderMailService {

	private final JavaMailSender mailSender;

	public OrderMailService(JavaMailSender mailSender) {
		this.mailSender = mailSender;
	}

	public void sendPlain(String to) {
		SimpleMailMessage msg = new SimpleMailMessage();
		msg.setTo(to);
		msg.setSubject("Your order");
		msg.setText("Thank you for placing an order.");
		mailSender.send(msg);
	}
}
```

**Listing 2.** `JavaMailSender` extends **`MailSender`**. Failures are **`MailException`** (unchecked hierarchy). `setTo` accepts several addresses. Do **not** send from `CommandLineRunner.run` as the production design — that fires on **every** start.

```java
MimeMessage mime = mailSender.createMimeMessage();
MimeMessageHelper helper = new MimeMessageHelper(mime, true);
helper.setTo(to);
helper.setText("<p>See attachment</p>", true);
helper.addAttachment("report.pdf", new ClassPathResource("report.pdf"));
mailSender.send(mime);
```

**Listing 3.** Second constructor argument **`true`** = multipart. HTML is **`setText(html, true)`**. **Inline** images: add the HTML **first**, then **`addInline(contentId, resource)`** — reverse order does not work. Packages: **`jakarta.mail`**, not `javax.mail`.

```d2
direction: down
starter: "spring-boot-starter-mail\nspring.mail.host" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
bean: "JavaMailSender\nMailSenderAutoConfiguration" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
send: "SimpleMailMessage or\nMimeMessageHelper" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

starter -> bean -> send
```

**Fig. 1.** Boot wires the sender. You still write the message. Actuator’s **mail** health check is on by default (`management.health.mail.enabled`) ([[How does the Actuator health endpoint aggregate status]]). Complex HTML bodies belong in a **template** (Framework: FreeMarker), not string-concatenated markup.

> [!warning] JavaMail timeouts default to forever
> Official Boot note: without `mail.smtp.connectiontimeout` / `timeout` / `writetimeout`, a dead SMTP server can **block a thread indefinitely**. Do not commit SMTP passwords. `jndi-name` **ignores** the other session properties.

> [!warning] Gmail-in-`application.properties` dumps are stale
> Boot **2.1** POMs with Maven `xmlns` URLs, `javax.mail`, and a raw mailbox password are not current Boot **4**. Implicit SSL is **`spring.mail.ssl.*`**, not a hand-copied `socketFactory` class name. A user `@Bean` `JavaMailSender` **replaces** auto-config ([[How do ConditionalOn annotations drive auto-configuration]]).

> [!tip] Interview answer
> I add spring-boot-starter-mail, set spring.mail.host, and inject JavaMailSender. Plain text is SimpleMailMessage; HTML and attachments use MimeMessageHelper with multipart true. I always set SMTP timeouts because the JavaMail defaults are infinite, keep credentials out of git, and I use jakarta.mail. If the app already has a mail Session in JNDI, spring.mail.jndi-name wins.
