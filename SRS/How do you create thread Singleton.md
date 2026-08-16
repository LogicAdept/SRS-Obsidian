<!--
reps: 0
priority: 0
-->
#Java/Concurrency #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Как создать потокобезопасный Singleton?**

+ __Static field__

```java
public class Singleton {
	public static final Singleton INSTANCE = new Singleton();
}
```

+ __Enum__

```java
public enum Singleton {
	INSTANCE;
}
```

+ __Synchronized Accessor__

```java
public class Singleton {
	private static Singleton instance;

	public static synchronized Singleton getInstance() {
		if (instance == null) {
			instance = new Singleton();
		}
		return instance;
	}
}
```

+ __Double Checked Locking & `volatile`__

```java
public class Singleton {
        private static volatile Singleton instance;

        public static Singleton getInstance() {
		Singleton localInstance = instance;
		if (localInstance == null) {
			synchronized (Singleton.class) {
				localInstance = instance;
				if (localInstance == null) {
					instance = localInstance = new Singleton();
				}
			}
		}
		return localInstance;
	}
}
```

+ __On Demand Holder Idiom__

```java
public class Singleton {

	public static class SingletonHolder {
		public static final Singleton HOLDER_INSTANCE = new Singleton();
	}

	public static Singleton getInstance() {
		return SingletonHolder.HOLDER_INSTANCE;
	}
}
```
