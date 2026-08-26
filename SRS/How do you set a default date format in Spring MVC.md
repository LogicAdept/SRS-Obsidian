<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS

# How do you set a default date format in Spring MVC?

> [!abstract] Short answer
> For **`java.util.Date` form binding**, register a **`CustomDateEditor`** or **`DateFormatter`** on the **`WebDataBinder`** in **`@InitBinder`**, or add a **`Formatter`/`Converter`** via **`WebMvcConfigurer.addFormatters`**. For **`java.time`** (and also `Date`/`Calendar`), put **`@DateTimeFormat(pattern = "…")`** on the field or handler parameter. Style-based `@DateTimeFormat` without a pattern is **locale-sensitive** (JDK 20+ warning).

## Three official knobs

Spring MVC `@InitBinder` docs show a controller-local `SimpleDateFormat` + **`CustomDateEditor`** on `Date.class`, or **`binder.addCustomFormatter(new DateFormatter("yyyy-MM-dd"))`**. Empty `@InitBinder` `value` applies to **all** command attributes on that controller; `@ControllerAdvice` can make it global — [[What is the InitBinder annotation in Spring MVC]].

`WebMvcConfigurer.addFormatters` registers converters/formatters **in addition to defaults** on the shared **`FormattingConversionService`** — app-wide form (and some conversion) formatting without repeating `@InitBinder`.

`@DateTimeFormat` javadoc: parse/print **Date, Calendar, Long timestamps, and JSR-310 `java.time` types**. Use **`pattern`**, **`iso`**, or **`style`** (mutually exclusive; `pattern` wins). Default with no attributes is style **`SS`**. ISO formatting of `Date` uses **UTC**; `pattern`/`style` use the **JVM default zone**.

```java
@Controller
public class FormController {

    @InitBinder
    public void initBinder(WebDataBinder binder) {
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        dateFormat.setLenient(false);
        binder.registerCustomEditor(Date.class, new CustomDateEditor(dateFormat, false));
    }
}

public class Booking {
    @DateTimeFormat(iso = DateTimeFormat.ISO.DATE)
    private LocalDate start;
}
```

**Listing 1.** Conceptual `Date` binder from Spring’s `@InitBinder` reference, plus field-level `@DateTimeFormat` for `java.time`. Binding pipeline: [[How does form binding work in Spring MVC]].

```d2
direction: down
field: "Form field\n2026-08-26" {
  width: 200
  height: 60
  style.fill: "#e3f2fd"
}
fmt: "@InitBinder editor /\n@DateTimeFormat /\naddFormatters" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
prop: "Date or LocalDate\non command object" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

field -> fmt -> prop
```

**Fig. 1.** HTTP JSON dates are **`HttpMessageConverter` / Jackson** config, not `@InitBinder` — [[How do you configure message converters in Spring MVC]].

> [!warning] `CustomDateEditor` is `java.util.Date` only
> It does **not** parse `LocalDate`. Use `@DateTimeFormat` or a `Formatter<LocalDate>`.

> [!warning] Lenient `SimpleDateFormat`
> Official sample calls **`setLenient(false)`**. Default lenient parsing accepts nonsense dates.

> [!warning] Style patterns vs JDK 20+
> `@DateTimeFormat` **style** uses locale `FormatStyle` patterns that **changed on JDK 20+**. Prefer **`iso` or an explicit `pattern`** you control.

> [!tip] Interview answer
> **Default `Date` form format: `@InitBinder` + `CustomDateEditor`/`DateFormatter`, or global `addFormatters`.** For `java.time`, **`@DateTimeFormat` on the field.** That is binding/formatting, not Jackson JSON. Don’t use `CustomDateEditor` for `LocalDate`.
