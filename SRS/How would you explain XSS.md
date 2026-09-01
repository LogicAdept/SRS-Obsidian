<!--
reps: 0
priority: 0
-->
#Security/AppSec #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**XSS — что это и как проверить?**

Cross-Site Scripting: вставка JavaScript в данные. <script>alert(1)</script> в поле имени → если отобразится без экранирования — XSS. Stored XSS: скрипт сохраняется в БД. Reflected: в URL-параметре. Защита: экранирование вывода, Content-Security-Policy.
