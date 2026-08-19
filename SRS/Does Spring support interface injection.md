<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Classic IoC lists three injection styles:

- constructor injection (Pico, Spring)
- setter / JavaBean property injection (Spring)
- **interface injection** (Avalon): the container calls a method on an interface the component implements

Dumps state: **Spring supports only constructor and setter injection.**

> [!warning] Unverified traps from the dump
> - Field `@Autowired` exists in Spring and is missing from that older three-way list.
> - “Spring has no interface injection” does not mean you cannot inject an interface **type**; it means the Avalon-style “container calls `injectXxx` on an interface you implement” is not a Spring DI mode.
