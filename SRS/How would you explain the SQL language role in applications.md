<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How would you explain the SQL language role in applications?

> [!abstract] Short answer
> In an application, SQL is the **boundary language between app code and data**: the application owns the UI, business rules, and orchestration, while SQL expresses every read and write against the database. Even when you never type SQL yourself — an ORM, a query builder, or a reporting tool generates it — the statement that finally executes is still SQL, which is why backend engineers are expected to read, review, and tune it.

The layered reality is: Java/C# code → data-access API (JDBC, ODBC, or the driver protocol) → SQL text sent to the engine → parsed, planned, executed → result set returned. ORMs such as Hibernate or JPA sit on top and translate object operations into SQL, but they do not remove the boundary — they only generate it ([[How would you explain @Query JPQL vs native SQL]]). A developer who cannot read the generated SQL cannot diagnose the slow endpoints, because performance problems surface as specific statements and specific plans ([[How do you systematically diagnose a slow SQL query]]).

Three practical consequences follow. First, **SQL is the integration point for every stack** — the same skill transfers between Java, Python, and Go services, because the database part is identical. Second, **the app and the DB share responsibility for correctness**: application code controls transaction boundaries (`commit`, `rollback`) and levels like read-committed, while SQL semantics (constraints, isolation) enforce the rest — you cannot fix a concurrency bug purely in either layer alone ([[How do you handle transaction isolation anomalies]]). Third, **SQL injection happens exactly at this boundary**: when user input is concatenated into the SQL text instead of being bound as parameters, data becomes code ([[How would you explain SQL injection attacks and defenses]]).

```sql
-- Same boundary shown twice: hand-written SQL vs generated SQL.
-- 1) Hand-written through a driver (JDBC would send exactly this text):
SELECT d.name AS department, COUNT(*) AS people
FROM emp e JOIN dept d ON d.id = e.dept_id
WHERE e.salary > :min_salary            -- :name = bind parameter
GROUP BY d.name ORDER BY people DESC;

-- 2) ORM-generated shape (what Hibernate typically emits for the same need):
SELECT d.name, COUNT(e.id) AS people
FROM department d
LEFT OUTER JOIN employee e ON e.department_id = d.id
GROUP BY d.name
ORDER BY COUNT(e.id) DESC;
```

**Listing 1.** Conceptual (bind-parameter syntax is driver-specific; shape verified on SQLite 3.53.1 with `?` placeholders). Both statements cross the same boundary; the ORM version is just another way to produce SQL, not a replacement for it.

```d2
direction: right
app: "Application code\nJava / C# / Python" {width: 190; height: 90}
api: "Data-access API\nJDBC / ODBC / ORM" {width: 200; height: 90}
sql: "SQL text\nparsed, planned" {width: 160; height: 90}
db: "Engine\nrows out" {width: 140; height: 90}
app -> api -> sql -> db
```

**Fig. 1.** Every layer in front of the engine ends as SQL text — ORMs and drivers generate the boundary, they do not remove it.

> [!warning] "The ORM hides SQL" is the reason juniors ship slow endpoints
> Hiding the syntax does not hide the cost: a lazy-association loop becomes the N+1 pattern, a wide `SELECT *` becomes a fat result set, and none of it is visible in Java code review. Reviewers must be able to see the SQL the ORM will emit, or the first production traffic spike finds it ([[What is the N plus 1 problem in SQL]]).

> [!tip] Interview answer
> SQL is the interface between an application and its relational data: the app holds business logic and sends statements through a driver or ORM, and those statements — hand-written or generated — are what the engine parses, plans, and executes. Knowing SQL means you can review what the ORM produces, tune the slow statements, and keep the correctness split right: transaction boundaries and constraints, not just Java code. It also puts SQL injection on your radar, since input becomes code exactly at this boundary if you concatenate instead of binding.
