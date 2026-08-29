<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Properties #SRS

# How do profile-specific property files work in Spring Boot?

> [!abstract] Short answer
> Boot also loads **`application-{profile}`** files (`.properties` and YAML variants) from the **same locations** as `application.properties`. They **overlay** the non-profile file: both are considered, and overlapping keys in the profile file **win**. The name is `application-dev.properties`, not `dev-application.properties`. If no profile is activated, the Environment’s default profile **`default`** is on, so **`application-default`** is considered.

## Naming and overlay

Activate `dev` (for example `--spring.profiles.active=dev` or `spring.profiles.active=dev` in the **base** file) and Boot considers both `application.properties` / `application.yaml` **and** `application-dev.properties` / `application-dev.yaml`. Profile-specific documents **always override** the non-specific ones at that location. Keys you do not repeat keep the base value — the profile file does **not** replace the whole file.

The basename follows `spring.config.name` (default `application`). A custom name `myproject` looks for `myproject-{profile}` as well.

```properties
# application.properties
server.port=8080
logging.level.root=INFO
```

```properties
# application-dev.properties
server.port=9090
```

**Listing 1.** With `--spring.profiles.active=dev`, `server.port` becomes `9090`; `logging.level.root` stays `INFO`.

```d2
direction: right
base: "application.properties\n(or .yaml / .yml)" {
  width: 210
  height: 70
  style.fill: "#e3f2fd"
}
profile: "application-dev.properties\nsame search locations" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
env: "Environment\noverlapping keys: profile wins" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

base -> env
profile -> env
```

**Fig. 1.** Both files load; the profile document overlays matching keys ([[What is Spring Boot property source precedence]]).

Inside a jar, profile-specific packaged files override packaged `application.*`. **Outside** the jar, the same pair is searched again (current directory, `config/`, `config/*/`, and so on), and those profile-specific files override the packaged ones. Prefer one format: if `.properties` and YAML sit in the **same** location, **`.properties` wins**.

## Several profiles and the implicit `default`

`spring.profiles.active=prod,live` uses **last-wins**: `application-live.*` overrides `application-prod.*` for the same key. That last-wins rule is applied **per location group** (`spring.config.location` commas vs `;` groups are not the same).

If you set **no** active profile, Boot enables default profiles **`[default]`** (rename with `spring.profiles.default`). Then `application-default.properties` / `application-default.yaml` are considered — the same overlay rules, not a special format. Activating `dev` turns **`default` off**, so `application-default.*` is **not** loaded unless `default` is also active. Set `spring.profiles.default=none` if you want no implicit profile file.

Activate profiles from the base document or the command line ([[How do you activate a Spring profile]]). Profile groups and `spring.profiles.include` can add more names, each of which can have its own `application-{profile}` file.

> [!warning] Overlay, not replace — and not a free-form filename
> `application-dev.properties` **adds** a PropertySource on top of `application.properties`; missing keys still come from the base file (and from higher sources such as OS env and CLI). `dev-application.properties` is **not** a profile file. A profile-specific file is loaded **once**; importing it again does not merge it a second time.

> [!warning] Do not put `spring.profiles.active` in the profile file
> `spring.profiles.active`, `spring.profiles.default`, `spring.profiles.include`, and `spring.profiles.group` are valid only in **non-profile-specific** documents. They **cannot** be placed in `application-{profile}.*` or in documents gated by `spring.config.activate.on-profile` — that document is invalid. Put `spring.profiles.active=dev` in `application.properties` or pass `--spring.profiles.active=dev`.

> [!tip] Interview answer
> Profile files follow application-{profile}, same locations as application.properties, and overlay the base file instead of replacing it. With spring.profiles.active=dev you get application.properties plus application-dev.properties, and colliding keys take the profile value. If nothing is activated, the default profile default loads application-default. Last active profile wins when several are listed, and you must not set spring.profiles.active inside a profile-specific file.
