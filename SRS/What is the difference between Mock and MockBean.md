<!--
reps: 0
priority: 0
-->
#Testing/Mocking #Java/Spring/Framework/Testing #Java/Annotations #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

@Mock используется для создания заглушек (моков) в unit-тестах, не требуя контекста Spring, тогда как @MockBean добавляет мок в контекст Spring (ApplicationContext), заменяя существующий бин, что необходимо для интеграционных тестов. @Mock быстрее, а @MockBean позволяет тестировать взаимодействие компонентов.

**@Mock vs @MockBean?**

@Mock (Mockito): plain unit test, no Spring. @MockBean: replaces a bean in the Spring test context. Mixing them wrong is a common fail.
