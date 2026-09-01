<!--
reps: 0
priority: 0
-->
#Java/OOP #Java/Language/Modifiers/Static #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**В чем разница между членом экземпляра класса и статическим членом класса?**

Модификатор `static` говорит о том, что данный метод или поле принадлежат самому классу и доступ к ним возможен даже без создания экземпляра класса. Поля помеченные `static` инициализируются при инициализации класса. На методы, объявленные как `static`, накладывается ряд ограничений:

+ Они могут вызывать только другие статические методы.
+ Они должны осуществлять доступ только к статическим переменным.
+ Они не могут ссылаться на члены типа `this` или `super`.

в отличие от статических, поля экземпляра класса принадлежат конкретному объекту и могут иметь разные значения для каждого. Вызов метода экземпляра возможен только после предварительного создания объекта класса.

Пример:
```java
public class MainClass {

	public static void main(String args[]) {
		System.out.println(TestClass.v);
		new TestClass().a();
		System.out.println(TestClass.v);
	}

}
```

```java
public class TestClass {

	public static String v = "Initial val";

	{
		System.out.println("!!! Non-static initializer");
		v = "Val from non-static";
	}

	static {
		System.out.println("!!! Static initializer");
		v = "Some val";
	}

	public void a() {
		System.out.println("!!! a() called");
	}

}
```

Результат:

```
!!! Static initializer
Some val
!!! Non-static initializer
!!! a() called
Val from non-static

```
