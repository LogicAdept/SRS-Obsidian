<!--
reps: 0
priority: 0
-->
#Java/Concurrency #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Напишите минимальный неблокирующий стек (всего два метода — `push()` и `pop()`).**

```java
class NonBlockingStack<T> {
    private final AtomicReference<Element> head = new AtomicReference<>(null);

    Stack<T> push(final T value) {
        final Element current = new Element();
        current.value = value;
        Element recent;
        do {
            recent = head.get();
            current.previous = recent;
        } while (!head.compareAndSet(recent, current));
        return this;
    }

    T pop() {
        Element result;
        Element previous;
        do {
            result = head.get();
            if (result == null) {
                return null;
            }
            previous = result.previous;
        } while (!head.compareAndSet(result, previous));
        return result.value;
    }

    private class Element {
        private T value;
        private Element previous;
    }
}
```

**Напишите минимальный неблокирующий стек (всего два метода — `push()` и `pop()`) с использованием `Semaphore`.**

```java
class SemaphoreStack<T> {
    private final Semaphore semaphore = new Semaphore(1);
    private Node<T> head = null;

    SemaphoreStack<T> push(T value) {
        semaphore.acquireUninterruptibly();
        try {
            head = new Node<>(value, head);
        } finally {
            semaphore.release();
        }

        return this;
    }

    T pop() {
        semaphore.acquireUninterruptibly();
        try {
            Node<T> current = head;
            if (current != null) {
                head = head.next;
                return current.value;
            }
            return null;
        } finally {
            semaphore.release();
        }
    }

    private static class Node<E> {
        private final E value;
        private final Node<E> next;

        private Node(E value, Node<E> next) {
            this.value = value;
            this.next = next;
        }
    }
}
```
