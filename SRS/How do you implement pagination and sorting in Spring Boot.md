<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Boot #Java/Spring/Data #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

* **JPA Entity**: 

**EmployeeEntity.java** 
```java
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;
 
@Entity
@Table(name="TBL_EMPLOYEES")
public class EmployeeEntity {
 
    @Id
    @GeneratedValue
    private Long id;
     
    @Column(name="first_name")
    private String firstName;
     
    @Column(name="last_name")
    private String lastName;
     
    @Column(name="email", nullable=false, length=200)
    private String email;
     
    //Setters and getters
 
    @Override
    public String toString() {
        return "EmployeeEntity [id=" + id + ", firstName=" + firstName +
                ", lastName=" + lastName + ", email=" + email   + "]";
    }
}
```
* **PagingAndSortingRepository** 
PagingAndSortingRepository is an extension of CrudRepository to provide additional methods to retrieve entities using the pagination and sorting abstraction. It provides two methods :

 * **Page findAll(Pageable pageable)** – returns a Page of entities meeting the paging restriction provided in the Pageable object.
 * **Iterable findAll(Sort sort)** – returns all entities sorted by the given options. No paging is applied here.

**EmployeeRepository.java** 
```java
import org.springframework.data.repository.PagingAndSortingRepository;
import org.springframework.stereotype.Repository;
import com.springbatchexample.demo.entity.EmployeeEntity;
 
@Repository
public interface EmployeeRepository
        extends PagingAndSortingRepository<EmployeeEntity, Long> {
 
}
```
* **Accepting paging and sorting parameters** 
In below spring mvc controller, we are accepting paging and sorting parameters using pageNo, pageSize and sortBy query parameters. Also, by default '10' employees will be fetched from database in page number '0', and employee records will be sorted based on 'id' field.

**EmployeeController.java** 
```java
@RestController
@RequestMapping("/employees")
public class EmployeeController
{
    @Autowired
    EmployeeService service;
 
    @GetMapping
    public ResponseEntity<List<EmployeeEntity>> getAllEmployees(
                        @RequestParam(defaultValue = "0") Integer pageNo,
                        @RequestParam(defaultValue = "10") Integer pageSize,
                        @RequestParam(defaultValue = "id") String sortBy)
    {
        List<EmployeeEntity> list = service.getAllEmployees(pageNo, pageSize, sortBy);
 
        return new ResponseEntity<List<EmployeeEntity>>(list, new HttpHeaders(), HttpStatus.OK);
    }
}
```
To perform pagination and/or sorting, we must create org.springframework.data.domain.Pageable or org.springframework.data.domain.Sort instances are pass to the findAll() method.

**EmployeeService.java**
```java
@Service
public class EmployeeService
{
    @Autowired
    EmployeeRepository repository;
     
    public List<EmployeeEntity> getAllEmployees(Integer pageNo, Integer pageSize, String sortBy)
    {
        Pageable paging = PageRequest.of(pageNo, pageSize, Sort.by(sortBy));
 
        Page<EmployeeEntity> pagedResult = repository.findAll(paging);
         
        if(pagedResult.hasContent()) {
            return pagedResult.getContent();
        } else {
            return new ArrayList<EmployeeEntity>();
        }
    }
}
```
* **Pagination and sorting techniques**
 * **Paging WITHOUT sorting**: To apply only pagination in result set, we shall create Pageable object without any Sort information.
```java
Pageable paging = PageRequest.of(pageNo, pageSize);
Page<EmployeeEntity> pagedResult = repository.findAll(paging);
```
 * **Paging WITH sorting**: To apply only pagination in result set, we shall create Pageable object with desired Sort column name.
```java
Pageable paging = PageRequest.of(pageNo, pageSize, Sort.by("email"));
Page<EmployeeEntity> pagedResult = repository.findAll(paging);
```
 * **Sorting only**: If there is no need to page, and only sorting is required, we can create Sort object for that.
```java
Sort sortOrder = Sort.by("email");
List<EmployeeEntity> list = repository.findAll(sortOrder);
```

**PageRequest vs keyset?**

Spring Pageable → OFFSET. Fine until deep pages. For feeds, keyset on indexed (sort,id). Don't COUNT(*) every page. Sort property must match an index or you sort 1e8 rows.
