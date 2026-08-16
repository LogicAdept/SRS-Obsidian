<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**BeanFactory vs ApplicationContext?**

BeanFactory: basic IoC, lazy by default, no AOP/events/i18n out of the box. ApplicationContext extends it: eager singleton pre-instantiation, internationalization, event publication, AOP, Environment, automatic BeanPostProcessor registration. Boot always uses ApplicationContext (AnnotationConfigServletWebServerApplicationContext in web). Interview: you almost never inject BeanFactory in an app.
