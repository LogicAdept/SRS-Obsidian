<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #Java/Exceptions/Checked #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**checked vs unchecked исключения.**

Checked: от Exception (не RuntimeException) — компилятор требует throws/catch. Примеры: IOException, SQLException. Unchecked: от RuntimeException и Error. Примеры: NullPointerException, IllegalArgumentException, ClassCastException. Современные фреймворки (Spring, Hibernate) предпочитают unchecked.

**Checked vs Unchecked исключения.**

Checked: от Exception (не RuntimeException) — компилятор требует обработки. IOException, SQLException. Unchecked: от RuntimeException — не обязательно ловить. NullPointerException, IllegalArgumentException. try-with-resources: ресурс реализует AutoCloseable.
