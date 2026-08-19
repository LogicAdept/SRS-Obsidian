<!--
reps: 0
priority: 0
-->
#Methodologies/Principles/IoC #Java/Spring/Core/IoC #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

* **DI(Dependency Injection)**

Dependency injection is a pattern used to create instances of objects that other objects rely upon without knowing at compile time which class will be used to provide that functionality or simply the way of injecting properties to an object is called dependency injection.

There are 3 types of Dependency injection

1. Constructor Injection
1. Setter/Getter Injection
1. Interface Injection 
Spring support only Constructor Injection and Setter/Getter Injection.

* **IOC(Inversion Of Control)**

Giving control to the container to create and inject instances of objects that your application depend upon, means instead of you are creating an object using the new operator, let the container do that for you. Inversion of control relies on dependency injection because a mechanism is needed in order to activate the components providing the specific functionality

The two concepts work together in this way to allow for much more flexible, reusable, and encapsulated code to be written. As such, they are important concepts in designing object-oriented solutions.
