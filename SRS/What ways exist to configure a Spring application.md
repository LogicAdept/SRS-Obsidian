<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Какие способы конфигурирование Spring существуют?**

+ __XML конфигурация__ — `ClassPathXmlApplicationContext(“context.xml”)`. Используется класс — `XmlBeanDefinitionReader`, который реализует интерфейс `BeanDefinitionReader`. Тут все достаточно прозрачно. `XmlBeanDefinitionReader` получает InputStream и загружает Document через `DefaultDocumentLoader`. Далее обрабатывается каждый элемент документа и если он является бином, то создается `BeanDefinition` на основе заполненных данных (id, name, class, alias, init-method, destroy-method и др.). Каждый `BeanDefinition` помещается в Mindmap. Mindmap хранится в классе `DefaultListableBeanFactory`.

+ __Аннотация/JavaConfig__ — с указанием пакета для сканирования — `AnnotationConfigApplicationContext(“package.name”)` или через аннотации с указанием класса (или массива классов) помеченного аннотацией `@Configuration` - `AnnotationConfigApplicationContext(JavaConfig.class)`. Внутри `AnnotationConfigApplicationContext`, то можно увидеть два поля.

````java
    private final AnnotatedBeanDefinitionReader reader;

    private final ClassPathBeanDefinitionScanner scanner;
````

`ClassPathBeanDefinitionScanner` сканирует указанный пакет на наличие классов помеченных аннотацией @Component (или любой другой аннотацией которая включает в себя `@Component`). Найденные классы разбираются и для них создаются BeanDefinition. Чтобы сканирование было запущено, в конфигурации должен быть указан пакет для сканирования. @ComponentScan({"package.name"}) или

`AnnotatedBeanDefinitionReader` работает в несколько этапов. Первый этап — это регистрация всех `@Configuration` для дальнейшего разбора. Если в конфигурации используются Conditional, то будут зарегистрированы только те конфигурации, для которых Condition вернет true. Аннотация Conditional появилась в четвертой версии Spring. Она используется в случае, когда на момент поднятия контекста нужно решить, создавать бин/конфигурацию или нет. Причем решение принимает специальный класс, который обязан реализовать интерфейс Condition. Второй этап — это регистрация специального `BeanFactoryPostProcessor`, а именно `BeanDefinitionRegistryPostProcessor`, который при помощи класса `ConfigurationClassParser` разбирает JavaConfig и создает BeanDefinition.

+ __Groovy конфигурация__ — `GenericGroovyApplicationContext(“context.groovy”)`. Данная конфигурация очень похожа на конфигурацию через Xml, за исключением того, что в файле не XML, а Groovy. Чтением и анализом groovy конфигурации занимается класс GroovyBeanDefinitionReader.
