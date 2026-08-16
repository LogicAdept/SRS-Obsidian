<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**What are test slices (@WebMvcTest, @DataJpaTest)?**

@SpringBootTest: almost full context, slow, Testcontainers/DB. @WebMvcTest: web slice, MockMvc, controllers, security optionally; @MockBean collaborators. @DataJpaTest: JPA slice, embedded/Testcontainers DB, @Transactional rollback. @JsonTest, @RestClientTest. Prefer slices for fast unit-ish tests; BootTest for wiring.
