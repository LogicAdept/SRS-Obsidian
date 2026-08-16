<!--
reps: 0
priority: 0
-->
#Networking/Web/HTML #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что такое `DOCTYPE` и зачем он нужен?**

Элемент `<!DOCTYPE>` предназначен для указания типа текущего документа. Это необходимо, чтобы браузер понимал согласно какого стандарта необходимо интерпретировать данную web-страницу.

Существует несколько видов `<!DOCTYPE>`, различающихся версией языка, на который они ориентированы:

__HTML 4.01__

+ `<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
"http://www.w3.org/TR/html4/strict.dtd">`: строгий синтаксис HTML;

+ `<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">`: переходный синтаксис HTML;

+ `<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN"
"http://www.w3.org/TR/html4/frameset.dtd">`: HTML с фреймами.

__HTML 5__

+ `<!DOCTYPE html>`: для всех документов.

__XHTML 1.0__

+ `<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">`: строгий синтаксис XHTML;

+ `<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">`: переходный синтаксис XHTML;

+ `<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">`: XHTML с фреймами.

__XHTML 1.1__

+ `<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">`: для всех документов.
