<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What is the __consumer_offsets topic?**

Internal compacted topic storing committed offsets per group per partition. After restart the group resumes from the last commit.
Commit too early → loss; too late → duplicates. This is the reliability trade-off interviewers want.
