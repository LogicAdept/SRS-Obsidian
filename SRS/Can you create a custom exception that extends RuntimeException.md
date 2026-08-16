<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Можно ли создать свой exception от RuntimeException?**

Да, и это типовая практика. Большинство современных проектов делают свои исключения от RuntimeException — не загромождают сигнатуру методов throws. От Error не рекомендуется наследоваться — это «системные» ошибки JVM, бизнес-код их трогать не должен.

**Как написать собственное («пользовательское») исключение?**

Необходимо унаследоваться от базового класса требуемого типа исключений (например от `Exception` или `RuntimeException`).

```java
class CustomException extends Exception {
    public CustomException() {
        super();
    }

    public CustomException(final String string) {
        super(string + " is invalid");
    }

    public CustomException(final Throwable cause) {
        super(cause);
    }
}
```
