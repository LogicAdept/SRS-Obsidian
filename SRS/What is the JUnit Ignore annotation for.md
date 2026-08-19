<!--
reps: 0
priority: 0
-->
#Java/Testing/JUnit #Java/Annotations #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**JUnit 5 — основные аннотации.**

@Test, @BeforeEach, @AfterEach, @BeforeAll, @AfterAll, @DisplayName, @Disabled, @ParameterizedTest, @Nested, @ExtendWith.

**JUnit 5: основные аннотации.**

@Test — тестовый метод. @BeforeEach/@AfterEach — до/после каждого теста. @BeforeAll/@AfterAll — до/после всех (static). @DisplayName — читаемое имя. @Disabled — пропустить. @Tag — категория (smoke, regression). @ParameterizedTest — параметризация.

**Параметризация тестов в JUnit 5.**

@ParameterizedTest + источник данных: @ValueSource(strings = {"a", "b"}), @CsvSource({"1, true", "2, false"}), @MethodSource("dataProvider"), @CsvFileSource(resources = "/data.csv"). Для AQA: параметризация status-кодов, валидных/невалидных данных, endpoint'ов.

**Какие базовые аннотации JUnit 5?**

@Test — обозначает тестовый метод. @BeforeEach / @AfterEach — выполняется перед/после каждого теста. @BeforeAll / @AfterAll — один раз перед/после всех тестов класса (метод должен быть static). @DisplayName — человекочитаемое имя теста. @ParameterizedTest — запуск теста с разными входными параметрами. @Disabled — отключить.
