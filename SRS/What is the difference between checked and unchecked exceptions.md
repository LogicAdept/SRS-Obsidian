<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #Java/Language #Java/Exceptions/Unchecked #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Разница между checked и unchecked исключениями.**

Checked наследуются от Exception (но не RuntimeException) — компилятор требует обработки или throws. Unchecked — от RuntimeException и Error — обрабатывать необязательно.

**Назови несколько unchecked исключений.**

NullPointerException, ArrayIndexOutOfBoundsException, IllegalArgumentException, ClassCastException, NumberFormatException.

**Разница между checked и unchecked исключениями.**

Checked наследуются от Exception (но не RuntimeException) — компилятор требует throws или catch. Unchecked — от RuntimeException/Error — обрабатывать необязательно.

**Что такое checked и unchecked исключения?**

Checked — компилятор требует обработать (catch) или объявить в throws. Используются для ожидаемых внешних ошибок (IO, БД). Unchecked (RuntimeException и наследники) — обрабатывать не обязательно. Используются для ошибок программирования (NPE, IllegalArgumentException).

**Разница между checked и unchecked исключениями.**

Checked — от Exception (кроме RuntimeException), компилятор требует обработки. Unchecked — от RuntimeException/Error.
