<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Properties #SRS

# What configuration file names does Spring Boot use?

> [!abstract] Short answer
> Config data defaults to basename **`application`**: **`application.properties`** and **`application.yaml`** (YAML also as **`.yml`**). Profile files are **`application-{profile}`** in the same formats. Search (low → high): classpath root, classpath **`/config`**, current directory, **`./config/`**, then **immediate children of `./config/`**. Rename the basename with **`spring.config.name`**. **`bootstrap.*`** is Cloud bootstrap, not this list.

## Names, then locations

Official loader: **`application.properties`** and **`application.yaml`**. Same location: **`.properties` wins** over YAML ([[What is the difference between application.properties and application.yml]]). Profiles: **`application-prod.yaml`** overlays **`application.yaml`** (last active profile wins) ([[How do profile-specific property files work in Spring Boot]]). If nothing is active, **`application-default`** is considered.

```text
application.properties
application.yaml
application.yml
application-{profile}.properties
application-{profile}.yaml
```

**Listing 1.** Default basenames. Change the word `application` with an **environment** property (CLI / system / OS — too early for `application.properties` itself): `--spring.config.name=myproject` loads `myproject.properties` / `myproject.yaml` / `myproject-{profile}`.

Default search (later **overrides** earlier):

1. Classpath root (`classpath:/`)
2. Classpath `config` package (`classpath:/config/`)
3. Current directory (`file:./`)
4. `config/` under the current directory (`file:./config/`)
5. Immediate subdirectories of that `config/` (`file:./config/*/`)

`spring.config.location` **replaces** that list (directories must end in `/`). `spring.config.additional-location` **appends**. Missing extra files: prefix **`optional:`** or the start fails. Import more files with **`spring.config.import`** (including **`configtree:`** for extensionless Kubernetes-style trees). Full Environment order is wider than these files ([[What is Spring Boot property source precedence]]).

```d2
direction: down
names: "application(.properties|.yaml)\n+ application-{profile}" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
where: "classpath:/ then /config\nthen ./ then ./config/ then ./config/*/" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
env: "Environment\n(later location wins)" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}

names -> where -> env
```

**Fig. 1.** Multi-document YAML uses `---`; properties uses `#---` / `!---`. `@PropertySource` still does **not** load YAML.

> [!warning] `application.properties` is not the only file and not the highest source
> Dump answers that stop at that one filename miss YAML, profiles, `./config/`, and CLI/env. `spring.config.name` / `location` / `additional-location` **cannot** be set inside the file they are meant to find.

> [!warning] `bootstrap.properties` is not a Boot core name
> It belongs to **Spring Cloud**’s bootstrap context (or legacy `spring-cloud-starter-bootstrap`). Boot 2.4+ prefers **`spring.config.import`** ([[What is the difference between application.properties and bootstrap.properties]]). `logback-spring.xml` / `banner.txt` are **not** Environment config-data files.

> [!tip] Interview answer
> Boot looks for application.properties and application.yaml, plus application-profile variants, on the classpath, in ./config, and in the working directory. I rename the basename with spring.config.name. bootstrap is Cloud, not the default Boot list.
