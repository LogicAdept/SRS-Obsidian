<!--
reps: 0
priority: 0
-->
#Java/Time #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Как получить текущую дату с использованием Date Time API из Java 8?**

```java
LocalDate.now();
```

**Как добавить 1 неделю, 1 месяц, 1 год, 10 лет к текущей дате с использованием Date Time API?**

```java
LocalDate.now().plusWeeks(1);
LocalDate.now().plusMonths(1);
LocalDate.now().plusYears(1);
LocalDate.now().plus(1, ChronoUnit.DECADES);
```

**Как получить следующий вторник используя Date Time API?**

```java
LocalDate.now().with(TemporalAdjusters.next(DayOfWeek.TUESDAY));
```

**Как получить вторую субботу текущего месяца используя Date Time API?**

```java
LocalDate
    .of(LocalDate.now().getYear(), LocalDate.now().getMonth(), 1)
    .with(TemporalAdjusters.nextOrSame(DayOfWeek.SATURDAY))
    .with(TemporalAdjusters.next(DayOfWeek.SATURDAY));
```

**Как получить текущее время с точностью до миллисекунд используя Date Time API?**

```java
new Date().toInstant();
```

**Как получить текущее время по местному времени с точностью до миллисекунд используя Date Time API?**

```java
LocalDateTime.ofInstant(new Date().toInstant(), ZoneId.systemDefault());
```
