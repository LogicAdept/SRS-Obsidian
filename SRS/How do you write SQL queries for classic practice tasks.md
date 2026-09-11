<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Напишите запрос...**

```sql
CREATE TABLE table (
  id BIGINT(20) NOT NULL AUTO_INCREMENT,
  created TIMESTAMP NOT NULL DEFAULT 0,
  PRIMARY KEY (id)
);
```

Требуется написать запрос, который вернет максимальное значение `id` и значение `created` для этого `id`:

```sql
SELECT id, created FROM table where id = (SELECT MAX(id) FROM table);
```

---

```sql
CREATE TABLE track_downloads (
  download_id BIGINT(20) NOT NULL AUTO_INCREMENT,
  track_id INT NOT NULL,
  user_id BIGINT(20) NOT NULL,
  download_time TIMESTAMP NOT NULL DEFAULT 0,
  PRIMARY KEY (download_id)
);
```

Напишите SQL-запрос, возвращающий все пары `(download_count, user_count)`, удовлетворяющие следующему условию: `user_count` — общее ненулевое число пользователей, сделавших ровно `download_count` скачиваний `19 ноября 2010 года`:

```sql
SELECT DISTINCT download_count, COUNT(*) AS user_count
FROM (
    SELECT COUNT(*) AS download_count
    FROM track_downloads WHERE download_time="2010-11-19"
    GROUP BY user_id)
AS download_count
GROUP BY download_count;
```

# Источники
+ [Википедия](https://ru.wikipedia.org/wiki/SQL)
+ [Quizful](http://www.quizful.net/interview/sql)
