<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump recommendation:

Keys: always StringRedisSerializer (readable in redis-cli). Values: GenericJackson2JsonRedisSerializer for debugging, class evolution, and some cross-language use. Hash keys: StringRedisSerializer. Hash values: GenericJackson2JsonRedisSerializer. Avoid JDK serialization in production.

Serializer table from the dump:

- StringRedisSerializer: UTF-8, readable, fastest, strings only
- JdkSerializationRedisSerializer: Java binary, not readable, Java-only, fragile serialVersionUID
- Jackson2JsonRedisSerializer: JSON for a declared type
- GenericJackson2JsonRedisSerializer: JSON plus @class metadata
> [!warning] Unverified traps from the dump
> - GenericJackson2Json stores @class; Jackson2JsonRedisSerializer is typed to one class.
> - JDK serialization is the historical default and the dump's security and evolution warning.
