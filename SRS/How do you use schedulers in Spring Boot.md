<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

Spring Boot internally uses the `TaskScheduler` interface for scheduling the annotated methods for execution. The @Scheduled annotation is added to a method along with some information about when to execute it, and Spring Boot takes care of the rest.
**Enable Scheduling**
```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class SchedulerDemoApplication {

	public static void main(String[] args) {
		SpringApplication.run(SchedulerDemoApplication.class, args);
	}
}
```
**Scheduling a Task with Fixed Rate**
```java
@Scheduled(fixedRate = 2000)
public void scheduleTaskWithFixedRate() {
    logger.info("Fixed Rate Task :: Execution Time - {}", dateTimeFormatter.format(LocalDateTime.now()) );
}
```
Sample Output
```
Fixed Rate Task :: Execution Time - 10:26:58
Fixed Rate Task :: Execution Time - 10:27:00
Fixed Rate Task :: Execution Time - 10:27:02
....
....
```
**Scheduling a Task using Cron Expression**
```java
@Scheduled(cron = "0 * * * * ?")
public void scheduleTaskWithCronExpression() {
    logger.info("Cron Task :: Execution Time - {}", dateTimeFormatter.format(LocalDateTime.now()));
}
```
Sample Output
```
Cron Task :: Execution Time - 11:03:00
Cron Task :: Execution Time - 11:04:00
Cron Task :: Execution Time - 11:05:00
```
