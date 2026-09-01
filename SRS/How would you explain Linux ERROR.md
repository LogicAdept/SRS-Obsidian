<!--
reps: 0
priority: 0
-->
#OperatingSystems/Linux #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Linux: найти все ERROR за сегодня и посчитать.**

grep "$(date +%Y-%m-%d)" app.log | grep -c "ERROR". find: find . -name "*.log" -mtime -1 (файлы за сутки). Уникальные IP: grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' access.log | sort -u. tail -f app.log | grep ERROR — мониторинг в реальном времени.
