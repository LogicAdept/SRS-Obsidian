<!--
reps: 0
priority: 0
-->
#Java/Testing/JUnit #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Какие assertions используются?**

assertEquals(expected, actual) — равенство. assertTrue / assertFalse — для boolean. assertNotNull / assertNull. assertThrows(Exception.class, () -> ...) — проверка, что код бросает исключение. AssertJ (отдельная либа) даёт fluent API: assertThat(value).isEqualTo(...).isNotNull(). @Test @DisplayName("Деление на ноль бросает ArithmeticException") void divideByZero() { Calculator c = new Calculator(); assertThrows(ArithmeticException.class, () -> c.divide(10, 0)); }
