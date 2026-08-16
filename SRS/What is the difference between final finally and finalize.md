<!--
reps: 0
priority: 0
-->
#Java/Language #Java/Exceptions #Java/JVM/GarbageCollector #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**final, finally, finalize — три разных слова.**

final: класс (нельзя наследовать), метод (нельзя переопределить), поле (нельзя переприсвоить). finally: блок try-catch-finally, выполняется ВСЕГДА. finalize(): метод Object, вызывается GC перед удалением. Deprecated с Java 9. Для ресурсов — try-with-resources.

**В чём разница final, finally, finalize?**

final — модификатор. final class / method / field. finally — блок в try-catch-finally, выполняется ВСЕГДА (даже при исключении или return). Используется для освобождения ресурсов. finalize() — метод Object, который раньше вызывал GC перед удалением объекта. Deprecated с Java 9, использовать нельзя. Сейчас для очистки используют try-with-resources и Cleaner.

**Чем отличаются `final`, `finally` и `finalize()`?**

Модификатор `final`:

+ Класс не может иметь наследников;
+ Метод не может быть переопределен в классах наследниках;
+ Поле не может изменить свое значение после инициализации;
+ Локальные переменные не могут быть изменены после присвоения им значения;
+ Параметры методов не могут изменять своё значение внутри метода.

Оператор `finally` гарантирует, что определенный в нём участок кода будет выполнен независимо от того, какие исключения были возбуждены и перехвачены в блоке `try-catch`.

Метод `finalize()` вызывается перед тем как сборщик мусора будет проводить удаление объекта.

Пример:
```java

public class MainClass {

	public static void main(String args[]) {
		TestClass a = new TestClass();
		System.out.println("result of a.a() is " + a.a());
		a = null;
		System.gc(); // Принудительно зовём сборщик мусора
		a = new TestClass();
		System.out.println("result of a.a() is " + a.a());
		System.out.println("!!! done");
	}

}
```

```java
public class TestClass {

	public int a() {
		try {
			System.out.println("!!! a() called");
			throw new Exception("");
		} catch (Exception e) {
			System.out.println("!!! Exception in a()");
			return 2;
		} finally {
			System.out.println("!!! finally in a() ");
		}
	}

	@Override
	protected void finalize() throws Throwable {
		System.out.println("!!! finalize() called");
		super.finalize();
	}
}
```

Результат выполнения:

```
!!! a() called
!!! Exception in a()
!!! finally in a()
result of a.a() is 2
!!! a() called
!!! Exception in a()
!!! finally in a()
!!! finalize() called
result of a.a() is 2
!!! done
```
