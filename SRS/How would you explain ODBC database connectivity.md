<!--
reps: 0
priority: 0
-->
#Databases #SRS

# How would you explain ODBC database connectivity

> [!abstract] Short answer
> **ODBC (Open Database Connectivity) is a standard C-level API that lets one application talk to many different DBMS products through per-database drivers.** The application codes against one interface — connection, SQL execution, result fetching — and a driver manager routes calls to the vendor driver installed for the target database.

## How the pieces fit

ODBC comes from Microsoft (early 1990s) and is built on the SQL Call-Level Interface that was later standardized as ISO/IEC 9075-3 (SQL/CLI). It is deliberately low-level and relational: you open a connection, prepare and execute SQL statements, bind columns or fetch rows by position. The **Driver Manager** (on Windows it ships with the OS; unixODBC and iODBC play this role on Unix) loads the right **driver** for the DSN — Data Source Name — the app connects to. Each vendor ships a driver that translates the ODBC calls into that DBMS's wire protocol: the PostgreSQL ODBC driver speaks PostgreSQL's protocol, the SQL Server driver speaks TDS.

The payoff is interoperability: one reporting tool can query Oracle, SQL Server, and PostgreSQL without being rewritten, because the application is written against the API, not against a product. Configuration lives in the DSN — server address, database, credentials — so switching environments is a registry or `odbc.ini` change, not a code change.

```d2
direction: right
app: "Application\n(one C API, one SQL dialect)" {
  width: 240
  height: 90
  style.fill: "#e3f2fd"
}
dm: "Driver Manager\nresolves DSN to driver" {
  width: 230
  height: 90
  style.fill: "#fff3e0"
}
d1: "PostgreSQL driver" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}
d2: "SQL Server driver" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}
app -> dm: "SQLConnect / SQLExecDirect"
dm -> d1
dm -> d2
```

**Fig. 1.** The application targets one stable API; the driver manager picks the vendor driver named by the DSN, and each driver speaks its database's wire protocol.

## Where you meet it today

ODBC is the plumbing under most BI tools (Tableau, Power BI connectors), Excel imports, and language bridges: Java's JDBC is the same idea with a Java API, and many non-JDBC data sources are reached via a JDBC-ODBC bridge. When someone "sets up a DSN" for Excel to pull from Postgres, ODBC is the layer doing the work. Its design also explains its limits: it is C-centric (pointers, handles), synchronous, and row-oriented, so ORMs and language-native drivers rather than raw ODBC dominate application code.

> [!warning] ODBC is an interface, not a query translator
> The driver passes your SQL to the server; it does **not** make dialects interchangeable. A query using PostgreSQL's `LIMIT` fails on SQL Server (`TOP`) through a perfectly working ODBC driver. Portability across DBMSs through ODBC covers the API surface, not the SQL text — cross-database SQL still needs ANSI-only statements or a translation layer.

For the Java-side equivalent see [[How do JDBC interface types such as Statement and PreparedStatement differ]]-style drill on the Java side, via [[How do you configure a DataSource in Spring]], and compare the DBMS role itself in [[How would you explain what a database management system provides]].

> [!tip] Interview answer
> ODBC is a Microsoft-originated, CLI-standardized C API for database access. An application uses one interface; a driver manager loads the vendor driver for the configured data source, and that driver speaks the DBMS's native protocol. It gives maximum interoperability for tools and BI — one program, many databases — while JDBC is its Java counterpart.
