<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #Java/Spring/Framework/DataAccess #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**What connection pool does Boot use?**

HikariCP is the default DataSource pool. Tune maximum-pool-size, connection-timeout, leak-detection. Pool exhaustion + OSIV + slow queries is a classic outage. Actuator/hikari metrics. Don't create extra DataSources without a reason.
