<!--
reps: 0
priority: 0
-->
#Java/Versions/8 #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Как определить повторяемую аннотацию?**

Чтобы определить повторяемую аннотацию, необходимо создать аннотацию-контейнер для списка повторяемых аннотаций и обозначить повторяемую мета-аннотацией `@Repeatable`:

```java
@interface Schedulers
{
    Scheduler[] value();
}

@Repeatable(Schedulers.class)
@interface Scheduler
{
    String birthday() default "Jan 8 1935";
}
```
