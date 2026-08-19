<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Instrumentation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps put `META-INF/aop.xml` on the classpath so AspectJ LTW knows which packages to weave and which aspect classes to apply.

Dump shape:

```xml
<aspectj>
    <weaver>
        <include within="com.example..*" />
    </weaver>
    <aspects>
        <aspect name="com.example.aspect.LoggingAspect" />
    </aspects>
</aspectj>
```

The same file shows up in dumps for `@Configurable` LTW, listing `AnnotationBeanConfigurerAspect`.

> [!warning] Unverified traps from the dump
> - Without `aop.xml`, `@EnableLoadTimeWeaving` alone may weave nothing.
> - `include within` that is too wide or too narrow is a dump-style misconfig: either nothing is woven, or the weaver touches the wrong packages.
