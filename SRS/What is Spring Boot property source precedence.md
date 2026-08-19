<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Properties #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The same property can be set in many places. Highest wins (dump’s simplified order):

1. Command-line arguments (`--server.port=8081`)
2. `SPRING_APPLICATION_JSON` / environment variables (`SERVER_PORT=8081`)
3. `application-{profile}.yml`
4. `application.yml`
5. `@PropertySource` on `@Configuration`
6. Defaults on `@ConfigurationProperties` types

That is why one artifact can run in every environment: env vars / CLI override packaged YAML without a rebuild (twelve-factor config).

> [!warning] Unverified traps from the dump
> - The real Boot order is longer (servlet config, random, test properties, …). Treat this list as interview-level, not the full `ConfigDataEnvironment` table.
> - Profile-specific files override the base file; they do not replace the whole stack.
