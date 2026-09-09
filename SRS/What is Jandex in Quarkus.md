<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

# What is Jandex in Quarkus

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.
Draft cue: Jandex is the class index library Quarkus uses for bean discovery — it builds a compact index of annotations/classes/methods/fields from bytecode instead of runtime classpath scanning.
ArC bean discovery, extension build steps and many integrations consume the index; annotations like @RegisterForReflection relate to it indirectly.
