<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS

# How do you register a JDBC driver?

> [!abstract] Short answer
> A JDBC **`Driver`** must be **registered with `DriverManager`**. The driver class is supposed to **construct an instance and call `registerDriver` when the class is loaded**, so **`Class.forName("vendor.Driver")`** is the documented application call. You can also pass an instance to **`DriverManager.registerDriver(driver)`**. `DriverManager` **also** registers whatever it finds in **`jdbc.drivers`** (colon-separated class names, **system** class loader) and in **`java.sql.Driver` service providers** (lookup uses the **thread context class loader** of the thread that first initializes `DriverManager`). After that, `getConnection` can pick a driver for the URL.

## What “register” means

`Driver` is the interface **every** JDBC driver class implements. `DriverManager` loads as many drivers as it can, then on `getConnection` asks each one to connect to the URL ([[Why must you load a JDBC database driver]]).

When a `Driver` class is **loaded**, it should **create an instance of itself and register it**. That is why `Class.forName("foo.bah.Driver")` both loads the class and, via that static setup, registers it. `DriverManager.registerDriver(Driver)` is the method that actually puts the instance on the list. If that instance is **already** registered, `registerDriver` does nothing. `deregisterDriver` removes it; if a `DriverAction` was supplied (Java 8 `registerDriver(Driver, DriverAction)`), its deregister hook runs first.

Initialization of `DriverManager` is **lazy** and also tries:

| Source | How classes are loaded |
| --- | --- |
| `jdbc.drivers` system property | Colon-separated FQCNs; **system** class loader |
| `java.sql.Driver` service providers | Service-provider loader; **TCCL** of the initializing thread |

```d2
direction: right
forName: "Class.forName\nloads Driver class" {
  width: 230
  height: 75
  style.fill: "#fff3e0"
}
spi: "SPI / jdbc.drivers\nauto at DriverManager init" {
  width: 270
  height: 75
  style.fill: "#e3f2fd"
}
list: "DriverManager\nregistered drivers" {
  width: 230
  height: 75
  style.fill: "#e8f5e9"
}
get: "getConnection(url)" {
  width: 200
  height: 75
  style.fill: "#f3e5f5"
}

forName -> list
spi -> list
list -> get
```

**Fig. 1.** Registration fills `DriverManager`’s list. Connecting is a later step ([[How do you establish a database connection in Java]]).

```java
import java.sql.Connection;
import java.sql.Driver;
import java.sql.DriverManager;
import java.sql.SQLException;

public final class RegisterDriver {
    public static void byClassName(String fqcn) throws ClassNotFoundException {
        Class.forName(fqcn);
    }

    public static void byInstance(Driver driver) throws SQLException {
        DriverManager.registerDriver(driver);
    }

    public static Connection connect(String url, String user, String password)
            throws SQLException {
        return DriverManager.getConnection(url, user, password);
    }
}
```

**Listing 1.** `forName` is enough if the driver registers in its class initializer. `registerDriver` needs a live `Driver`. Service-provider jars often need **neither** in application code.

A **`DataSource`** is still the **preferred** way to obtain connections; it does not replace the vendor driver, but application code often never names the driver class ([[How do you integrate a database with a Java application]]).

> [!warning] `Class.forName(…).newInstance()` is extra
> The `Driver` contract is register **on class load**. `forName` already initializes the class. `newInstance()` is not the documented user call.

> [!warning] The wrong class loader hides the driver
> Service providers are found with the **TCCL** of the thread that first touches `DriverManager`. `jdbc.drivers` uses the **system** class loader. In a servlet container those are often different from the webapp loader — `getConnection` then fails even though the jar is in `WEB-INF/lib`.

> [!warning] Registration is not `getConnection`
> A successful `forName` / `registerDriver` does not open a session. `null` URL still throws `SQLException` at `getConnection`. Duplicate user/password in URL and `Properties` is **implementation-defined** ([[How do you establish a database connection in Java]]).

> [!tip] Interview answer
> You register a JDBC driver with `DriverManager`. Drivers should register themselves when loaded, so `Class.forName("vendor.Driver")` is the classic line; `registerDriver(instance)` is the explicit API. JDBC also auto-loads `jdbc.drivers` and `java.sql.Driver` service providers, so many apps never call `forName` before `getConnection`.

## See also

- [[How do you close a database connection properly]]
- [[What is JDBC]]
- [[What is JDBC, an implementation or a specification]]
