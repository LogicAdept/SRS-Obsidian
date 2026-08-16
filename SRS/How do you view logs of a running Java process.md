<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Как посмотреть логи запущенного Java-процесса?**

tail -f /var/log/app.log, или journalctl -u service-name -f, или через docker logs -f container.
