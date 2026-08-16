<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**When does @Transactional roll back?**

Default: rollback on RuntimeException and Error; commit on checked Exception. Override: rollbackFor=Exception.class, noRollbackFor=.... rollbackFor does nothing if the method wasn't proxied (private/self-invoke). Checked exceptions that you swallow inside the method also won't roll back.
