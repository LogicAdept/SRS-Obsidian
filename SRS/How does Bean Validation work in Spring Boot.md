<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**How does @Valid / @Validated work?**

Jakarta Bean Validation (Hibernate Validator). @Valid on @RequestBody/@ModelAttribute triggers MethodValidation. ConstraintViolation → 400 via MethodArgumentNotValidException. Service layer: @Validated on class + @Valid params, needs a Spring proxy (same self-invocation caveat). Groups for create vs update. Don't validate only in the controller if other entry points exist.
