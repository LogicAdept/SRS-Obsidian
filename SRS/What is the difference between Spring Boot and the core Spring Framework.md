<!--
reps: 0
priority: 0
-->
#Java/Spring/Core #Java/Spring/Framework/Boot #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

|Basis of Differentiation | Spring |Spring Boot |
|---------------------------|-------------------------|--------------------------------------------------|
|**Configuration** |In order to design any Spring based application, the developer has to take recourse to the annual setup feature on the Hibernate data source. Session Factory, entity Manager, Transaction Management, etc. have to be configured as well. | The common set up and features of Spring Boot do not have to be designed by the developer individually. The Spring Boot Configuration annotation is well-equipped to handle everything at the time of deployment. |
|**XML** |In Spring MVC applications, some XML definitions are to be managed mandatorily.| In the configuration of Spring Boot applications, nothing has to be managed manually. The annotations are capable of managing all that is needed.|
|**Controlling** | As the configuration can be easily handled manually, Spring or Spring Boot need not load some unwanted default features for specific applications. |In Spring Boot, the controls are automatically handled during the default loading part. As such, developers do not have the option of not loading unusable components belonging to the default Spring Boot features.|
|**Use** |Better to use if characteristics or application type are purely defined.|Better to use in cases where the application type of functionality of future use is not properly defined. As the task of integrating any Spring-specific feature is auto-configured in this case, there is no necessity of any additional configuration.

**Framework toolkit vs Boot opinions?**

You can use Spring without Boot (war + XML). Boot is not a different IoC — it auto-wires the Framework.
