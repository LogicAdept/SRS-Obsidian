<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA/Mapping #Databases/Relational #SRS

# What is an example of a one to many relationship in databases or JPA?

> [!abstract] Short answer
> **Department → employees** (or **Customer → orders**): one parent row, many children. In SQL the **FK lives on the many table** (`EMPLOYEE.DEPARTMENT_id`) and is **not** unique. In JPA that is **`@ManyToOne` on `Employee.department`** (owning side) and **`@OneToMany(mappedBy = "department")` on `Department.employees`**. One-to-one uses a **unique** FK instead: [[What is a one to one relationship in databases or JPA]].

## Department and employees

Jakarta Persistence cardinalities include one-to-many / many-to-one. For a bidirectional pair, **the many side must own** the relationship: it maps the foreign key. The one side is inverse (`mappedBy`). Default table mapping: `EMPLOYEE` has `DEPARTMENT_{pk}` with the same type as `DEPARTMENT`’s primary key — **no unique constraint** (several employees may share one department).

The JPA JavaDoc’s Customer / `Set<Order>` example is the same shape: FK `CUST_ID` on `Order`. What JPA is: [[What is the Java Persistence API JPA]].

```d2
direction: down
dept: "DEPARTMENT\nPK" {
  width: 160
  height: 40
  style.fill: "#e3f2fd"
}
emp: "EMPLOYEE\nPK + FK department_id\n(not unique)" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
dept -> emp: "one department, many employees"
```

**Fig. 1.** One-to-many in the database is a non-unique FK on the child table.

```java
@Entity
public class Department {
    @Id
    private Long id;

    @OneToMany(mappedBy = "department")
    private Set<Employee> employees = new HashSet<>();

    protected Department() {}

    public void addEmployee(Employee employee) {
        employees.add(employee);
        employee.setDepartment(this);
    }
}

@Entity
public class Employee {
    @Id
    private Long id;

    @ManyToOne
    @JoinColumn(name = "DEPARTMENT_ID")
    private Department department;

    protected Employee() {}

    void setDepartment(Department department) {
        this.department = department;
    }
}
```

**Listing 1.** Spec default: `Employee` owns the FK. `addEmployee` updates both sides; flush uses the `@ManyToOne`.

Unidirectional `@OneToMany` (no `mappedBy`) defaults to a **join table** `A_B`, not a FK on `B`. To put the FK on the child without a `ManyToOne`, use `@JoinColumn` on the `@OneToMany` (JavaDoc example: `@JoinColumn(name = "CUST_ID")` on `Customer.orders`).

`@OneToMany` defaults to **`fetch = LAZY`**; `@ManyToOne` to **EAGER**: [[What are JPA fetch types for entity associations]]. `cascade = REMOVE` and `orphanRemoval` are portable on `@OneToMany`: [[How would you explain CascadeType.ALL]].

> [!warning] The collection is not the owner
> Clearing `department.getEmployees()` without nulling `employee.department` does not clear `EMPLOYEE.DEPARTMENT_ID`. Persist and update follow the many-to-one.

> [!warning] Bare @OneToMany implies a join table
> `@OneToMany` with no `mappedBy` and no `@JoinColumn` creates `DEPARTMENT_EMPLOYEE`-style extra table. That is still one-to-many, but it is not the usual FK-on-child schema.

> [!tip] Interview answer
> A department has many employees: the employee table holds a non-unique foreign key to department. In JPA, Employee has ManyToOne to Department, and Department has OneToMany mappedBy that field. Customer and orders is the same pattern. One-to-one looks similar except the foreign key is unique.
