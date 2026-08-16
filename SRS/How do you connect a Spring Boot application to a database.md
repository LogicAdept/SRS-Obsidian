<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Boot #Java/Spring/Data #Java/JDBC #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Step 01**: application.properties Settings
```java
spring.datasource.url=jdbc:mysql://localhost:3306/springbootdb  
spring.datasource.username=root  
spring.datasource.password=mysql  
spring.jpa.hibernate.ddl-auto=create-drop  
```

**Step 02**: SpringBootJdbcApplication.java
```java
package com.learningzone;  

import org.springframework.boot.SpringApplication;  
import org.springframework.boot.autoconfigure.SpringBootApplication;  
@SpringBootApplication  
public class SpringBootJdbcApplication {  
    public static void main(String[] args) {  
        SpringApplication.run(SpringBootJdbcApplication.class, args);  
    }  
}
```

**Step 03**: SpringBootJdbcController.java
```java
package com.learningzone;
  
import org.springframework.web.bind.annotation.RequestMapping;  
import org.springframework.beans.factory.annotation.Autowired;  
import org.springframework.jdbc.core.JdbcTemplate;  
import org.springframework.web.bind.annotation.RestController;  
@RestController  
public class SpringBootJdbcController {  
    @Autowired  
    JdbcTemplate jdbc;
    @RequestMapping("/insert")  
    public String index(){  
        jdbc.execute("insert into user(name, email) values('Pradeep Kumar','pradeep.vwa@gmail.com')");  
        return "Record inserted Successfully";  
    }  
}  
```

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Spring Data — как работает?**

Интерфейс extends JpaRepository<Entity, ID>. Spring создаёт прокси в рантайме. Имя метода парсится: findByEmailAndStatus → JPQL. @Query для сложных запросов. Pageable → Page/Slice. JpaRepository добавляет flush(), saveAllAndFlush(), deleteAllInBatch() к CrudRepository.

**Как Spring Data создаёт реализацию репозитория?**

Через прокси, генерируемый в рантайме. Имя метода (findByEmailAndStatus) парсится и превращается в JPQL.

**Как Spring создаёт реализацию репозитория, если ты только написал интерфейс?**

Через прокси, который генерируется в рантайме. Имя метода (findByEmail) парсится и превращается в SQL/JPQL.
