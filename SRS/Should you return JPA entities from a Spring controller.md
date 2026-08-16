<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**Entity vs DTO in the API?**

Don't return entities: Jackson triggers lazy loads, leaks internals, couples API to schema, OSIV/LIE. Map to DTO (or record) inside the transactional service while the session is open, or use interface/class projections / JOIN FETCH. Interview staple 2026.
