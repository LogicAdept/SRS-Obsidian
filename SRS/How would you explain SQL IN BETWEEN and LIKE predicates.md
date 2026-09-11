<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Для чего используются операторы `IN`, `BETWEEN`, `LIKE`?**

`IN` - определяет набор значений.

```sql
SELECT * FROM Persons WHERE name IN ('Ivan','Petr','Pavel');
```

`BETWEEN` определяет диапазон значений. В отличие от `IN`, `BETWEEN` чувствителен к порядку, и первое значение в предложении должно быть первым по алфавитному или числовому порядку.

```sql
SELECT * FROM Persons WHERE age BETWEEN 20 AND 25;
```

`LIKE` применим только к полям типа `CHAR` или `VARCHAR`, с которыми он используется чтобы находить подстроки. В качестве условия используются _символы шаблонизации (wildcards_) - специальные символы, которые могут соответствовать чему-нибудь:

+ `_` замещает любой одиночный символ. Например, `'b_t'` будет соответствовать словам `'bat'` или `'bit'`, но не будет соответствовать `'brat'`.

+ `%` замещает последовательность любого числа символов. Например `'%p%t'` будет соответствовать словам `'put'`, `'posit'`, или `'opt'`, но не `'spite'`.

```sql
SELECT * FROM UNIVERSITY WHERE NAME LIKE '%o';
```

**IN BETWEEN LIKE performance?**

IN: small lists or semi-join; huge IN may hash. BETWEEN: sargable range. LIKE: prefix uses B-tree; leading % does not — trigram/FTS. NOT IN + NULL trap.
