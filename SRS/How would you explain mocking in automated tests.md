<!--
reps: 0
priority: 0
-->
#Testing/Mocking #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

Mockito is a mocking framework, JAVA-based library that is used for effective unit testing of JAVA applications. Mockito is used to mock interfaces so that a dummy functionality can be added to a mock interface that can be used in unit testing. 

**Spring Boot - mockito and junit – unit test service layer Example** 

* **Maven Dependencies** 
The spring-boot-starter-test dependency includes all required dependencies to create and execute tests.
```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-test</artifactId>
</dependency>
```
* **MockitoJUnitRunner class**: It automatically initialize all the objects annotated with `@Mock` and `@InjectMocks` annotations.
```java
@RunWith(MockitoJUnitRunner.class)
public class TestEmployeeManager {
     
    @InjectMocks
    EmployeeManager manager;
     
    @Mock
    EmployeeDao dao;
     
    //tests 
}
```
* **JUnit tests using Mockito** 

Here `getAllEmployees()` which will return list of EmployeeVO objects, `getEmployeeById(int id)` to return a employee by given id; and `createEmployee()` which will add an employee object and return void.

* **Service layer tests** ( TestEmployeeManager.java )

```java
import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
 
import java.util.ArrayList;
import java.util.List;
 
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.mockito.junit.MockitoJUnitRunner;
 
import com.javaexample.demo.dao.EmployeeDao;
import com.javaexample.demo.model.EmployeeVO;
import com.javaexample.demo.service.EmployeeManager;
 
public class TestEmployeeManager {
     
    @InjectMocks
    EmployeeManager manager;
     
    @Mock
    EmployeeDao dao;
 
    @Before
    public void init() {
        MockitoAnnotations.initMocks(this);
    }
     
    @Test
    public void getAllEmployeesTest()
    {
        List<EmployeeVO> list = new ArrayList<EmployeeVO>();
        EmployeeVO empOne = new EmployeeVO(1, "John", "John", "javaexample@gmail.com");
        EmployeeVO empTwo = new EmployeeVO(2, "Alex", "kolenchiski", "alexk@yahoo.com");
        EmployeeVO empThree = new EmployeeVO(3, "Steve", "Waugh", "swaugh@gmail.com");
         
        list.add(empOne);
        list.add(empTwo);
        list.add(empThree);
         
        when(dao.getEmployeeList()).thenReturn(list);
         
        //test
        List<EmployeeVO> empList = manager.getEmployeeList();
         
        assertEquals(3, empList.size());
        verify(dao, times(1)).getEmployeeList();
    }
     
    @Test
    public void getEmployeeByIdTest()
    {
        when(dao.getEmployeeById(1)).thenReturn(new EmployeeVO(1,"Lokesh","Gupta","user@email.com"));
         
        EmployeeVO emp = manager.getEmployeeById(1);
         
        assertEquals("Lokesh", emp.getFirstName());
        assertEquals("Gupta", emp.getLastName());
        assertEquals("user@email.com", emp.getEmail());
    }
     
    @Test
    public void createEmployeeTest()
    {
        EmployeeVO emp = new EmployeeVO(1,"Lokesh","Gupta","user@email.com");
         
        manager.addEmployee(emp);
         
        verify(dao, times(1)).addEmployee(emp);
    }
}
```
**Service layer class** ( EmployeeManager.java )

```java
import java.util.List;
 
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
 
import com.javaexample.demo.dao.EmployeeDao;
import com.javaexample.demo.model.EmployeeVO;
 
@Service
public class EmployeeManager 
{
    @Autowired
    EmployeeDao dao;
     
    public List<EmployeeVO> getEmployeeList() {
        return dao.getEmployeeList();
    }
     
    public EmployeeVO getEmployeeById(int id) {
        return dao.getEmployeeById(id);
    }
     
    public void addEmployee(EmployeeVO employee) {
        dao.addEmployee(employee);
    }
}
```
**Dao layer class** ( EmployeeDao.java ) 
```java
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
 
import org.springframework.stereotype.Repository;
 
import com.javaexample.demo.model.EmployeeVO;
 
@Repository
public class EmployeeDao {
     
    private Map<Integer, EmployeeVO> DB = new HashMap<>();
     
    public List<EmployeeVO> getEmployeeList() 
    {
        List<EmployeeVO> list = new ArrayList<>();
        if(list.isEmpty()) {
            list.addAll(DB.values());
        }
        return list;
    }
     
    public EmployeeVO getEmployeeById(int id) {
        return DB.get(id);
    }
     
    public void addEmployee(EmployeeVO employee) {
        employee.setEmployeeId(DB.keySet().size() + 1);
        DB.put(employee.getEmployeeId(), employee);
    }
     
    public void updateEmployee(EmployeeVO employee) {
        DB.put(employee.getEmployeeId(), employee);
    }

    public void deleteEmployee(int id) {
        DB.remove(id);
    }
}
```

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Mockito: mock vs spy.**

mock() — пустой объект, все методы возвращают default (null, 0, false). spy() — обёртка над реальным объектом, методы вызываются по-настоящему, если не заmock'ать.

**Mockito: Mock vs Spy — в чём разница?**

Mock: полностью пустой объект, все методы возвращают default (null, 0, false). Spy: обёртка над реальным объектом, методы вызываются по-настоящему, если не замоканы. Для Spy: doReturn().when(spy).method() (не when(spy.method()) — иначе вызовется реальный метод).

**Что такое Mockito?**

Библиотека для создания моков (имитаций) объектов в тестах. Позволяет «подменить» зависимость тестируемого класса фейком, который ведёт себя так, как тебе нужно.

**Базовый набор Mockito?**

@Mock — создать мок. @InjectMocks — создать тестируемый объект и подставить в него моки. @ExtendWith(MockitoExtension.class) — активировать. when(mock.method(...)).thenReturn(...) — задать поведение. verify(mock).method(...) — проверить, что метод был вызван. ArgumentCaptor — захватить аргументы, с которыми звали мок. @ExtendWith(MockitoExtension.class) class UserServiceTest { @Mock UserRepository repo; @InjectMocks UserService service;
