<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**What is OSIV and why is it dangerous?**

Open Session In View: Hibernate Session stays open until the view/JSON is rendered, so lazy loads in the controller/Jackson work. Boot often enables spring.jpa.open-in-view=true by default (warning in logs). Hides missing fetch plans, holds DB connections during HTTP write, classic LazyInitializationException when you turn it off. Senior answer: disable OSIV, map DTO in @Transactional service.
