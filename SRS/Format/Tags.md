Для тегов следующие правила:
1. Тег **#New** ставят на карточках, которые **ещё без ответа** (пустые) или с ответом **неполным / черновым**; когда карточка доведена до нужного уровня, **#New** с неё убирают. К позиции **#New** в строке тегов см. п. 7.
2. Теги - композитные, могут быть 1 и больше уровней
3. Теги задают группы и связи между темами; один документ может иметь несколько тегов
4. Теги идут сразу после метаинформации
5. Слова в тегах Начинаются с больших букв
6. Аббревиатуры - пишутся большими
7. Тег #New - ставится в конце
8. Все карточки в корне хранилища имеют тег #SRS (интервальное повторение)

---

## Модель тегов

Теги — это **композитные пути** (`Корень/.../Лист`) плюс при необходимости **несколько путей** на одной карточке: так задаются и иерархия темы, и пересечения (например микросервисы и наблюдаемость). На строке тегов сначала идут **тематические** теги, затем **`#SRS`**, затем **`#New`**. Карточки, которые **сравнивают** две сущности, должны нести **оба** соответствующих тематических тега (или эквивалент по смыслу), чтобы выборки по любой стороне были полными. **Не** ставить подряд родителя и дочерний тег с тем же префиксом (например не `#Patterns/Architecture/Microservices` и `#Patterns/Architecture/Microservices/Observability` — достаточно листа `.../Microservices/Observability`).

**Неполный путь (не лист):** допустимо указать тег **короче**, чем самый глубокий известный префикс в дереве ниже, если **нет дочернего тега**, который по смыслу подошёл бы заметно лучше. Если подходящий лист уже есть в дереве — предпочитай его (и не дублируй вместе с его родителем на одной карточке, см. абзац выше).

**Расширение:** новые заметки по возможности **расширяют это дерево** (новые подтеги под уже принятыми корнями), а не вводят **параллельные теги-синонимы** одного и того же понятия. Если для сущности уже закреплён путь (например Kubernetes только как `#DevOps/Tools/Kubernetes`), не добавлять второй корень без причины (`#Kubernetes` рядом с тем же смыслом). Для разных видов API используй префикс **`#API/`** и лист **`#API/<Вид>`** (например `#API/REST`), а не отдельные корни вроде `#REST` и не ветку под `Patterns`.

**Новый тег, если тема не влезает:** если для карточки **нет подходящего листа** в дереве (нет смысла маскировать тему под «почти подходящий» тег), **не натягивай** ближайший похожий. Добавь в **`Tags.md`** в раздел **«Дерево»** новый префикс под **логичным корнем** (или новый корень, например **`#SQL/...`** для языка SQL вне JVM) и затем используй этот тег на карточке. Дерево и выборки по тегам должны отражать предмет честно.

---

## Дерево (префиксы в карточках)

### Java
- `#Java/Collections`
- `#Java/Collections/List`
- `#Java/Collections/Map`
- `#Java/Collections/Set`
- `#Java/Collections/Queues`
- `#Java/Collections/Iteration`
- `#Java/Collections/Concurrency`
- `#Java/Streams`
- `#Java/OOP`
- `#Java/Concurrency`
- `#Java/Exceptions`
- `#Java/IO`
- `#Java/Tooling`
- `#Java/Tooling/Maven`
- `#Java/JavaEE`
- `#Java/Servlet`
- `#Java/CGI`
- `#Java/Listeners`
- `#Java/JSP`
- `#Java/JSP/JSTL`
- `#Java/Spring`
- `#Java/Spring/Core`
- `#Java/Spring/Core/IoC`
- `#Java/Spring/Framework/AOP`
- `#Java/Spring/Framework/DataAccess`
- `#Java/Spring/Framework/WebMvc`
- `#Java/Spring/Framework/WebSocket`
- `#Java/Spring/Framework/WebFlux`
- `#Java/Spring/Framework/Testing`
- `#Java/Spring/Framework/Instrumentation`
- `#Java/Spring/Boot`
- `#Java/Spring/Transactions`
- `#Java/Spring/Cloud`
- `#Java/Spring/Cloud/Gateway`
- `#Java/Spring/Cloud/Config`
- `#Java/Spring/Cloud/Stream`
- `#Java/Spring/Cloud/CircuitBreaker`
- `#Java/Spring/Data`
- `#Java/Spring/Data/JPA`
- `#Java/Spring/Data/MongoDB`
- `#Java/Spring/Data/Redis`
- `#Java/Spring/Security`
- `#Java/Spring/Batch`
- `#Java/Spring/Integration`
- `#Java/Spring/Session`
- `#Java/Spring/AI`
- `#Java/JDBC`
- `#Java/Persistence`
- `#Java/Persistence/JPA`
- `#Java/Persistence/Hibernate`

### SQL
- `#SQL`
- `#SQL/Transactions`

### Databases
- `#Databases`
- `#Databases/Transactions`

### Problems
- `#Problems/Persistence`

### DSA
- `#DSA/Algorithms/Search`
- `#DSA/DataStructures/Graph`

### Paradigms
- `#Paradigms/OOP`

### DistributedSystems
- `#DistributedSystems/Communication`

### Networking
- `#Networking`
- `#Networking/TCP`
- `#Networking/UDP`
- `#Networking/DNS`
- `#Networking/Web`
- `#Networking/Web/Protocols`
- `#Networking/Web/Protocols/HTTP`
- `#Networking/Web/Protocols/TLS`
- `#Networking/Web/Cookies`
- `#Networking/Web/Caching`

### API
- `#API/REST`
- `#API/SOAP`
- `#API/GraphQL`
- `#API/GRPC`
- `#API/RPC`
- `#API/Gateway`
- `#API/Webhooks`

### Patterns
- `#Patterns/GoF`
- `#Patterns/GoF/Creational`
- `#Patterns/GoF/Structural`
- `#Patterns/GoF/Behavioral`
- `#Patterns/GRASP`
- `#Patterns/Enterprise`
- `#Patterns/Enterprise/Integration`
- `#Patterns/Enterprise/Integration/Channels`
- `#Patterns/Enterprise/Integration/Messages`
- `#Patterns/Enterprise/Integration/Routing`
- `#Patterns/Enterprise/Integration/Transformation`
- `#Patterns/Enterprise/Integration/Endpoints`
- `#Patterns/Enterprise/Integration/Management`
- `#Patterns/DistributedSystems`
- `#Patterns/Cloud`
- `#Patterns/Architecture/UI`
- `#Patterns/Architecture/Monolith`
- `#Patterns/Architecture/Microservices`
- `#Patterns/Architecture/Microservices/ServiceBoundaries`
- `#Patterns/Architecture/Microservices/CrossCuttingConcerns`
- `#Patterns/Architecture/Microservices/CommunicationStyles`
- `#Patterns/Architecture/Microservices/ExternalAPI`
- `#Patterns/Architecture/Microservices/ServiceDiscovery`
- `#Patterns/Architecture/Microservices/Deployment`
- `#Patterns/Architecture/Microservices/Observability`

### Methodologies
- `#Methodologies/DDD`
- `#Methodologies/Principles`
- `#Methodologies/Principles/SOLID`
- `#Methodologies/Principles/DRY`
- `#Methodologies/Principles/KISS`
- `#Methodologies/Principles/IoC`
- `#Methodologies/Principles/DependencyInjection`
- `#Methodologies/Principles/YAGNI`
- `#Methodologies/Principles/SeparationOfConcerns`
- `#Methodologies/Principles/TellDontAsk`
- `#Methodologies/Principles/LawOfDemeter`

### Career
- `#Career`
- `#Career/Interview`
- `#Career/Experience`
- `#Career/Behavioral`

### Build
- `#Build/Tools`
- `#Build/Tools/Maven`
- `#Build/Tools/Gradle`
- `#Build/Tools/Ant`
- `#Build/Tools/CMake`

### DevOps
- `#DevOps/Tools/Docker`
- `#DevOps/Tools/Kubernetes`
- `#DevOps/Containerisation`
- `#DevOps/Virtualisation`
- `#DevOps/Orchestration`
- `#DevOps/Configuration`
- `#DevOps/Deployment`
- `#DevOps/Deployment/Strategies`

### SystemDesign
- `#SystemDesign`
- `#SystemDesign/Scalability`
- `#SystemDesign/Reliability`
- `#SystemDesign/Performance`
- `#SystemDesign/Availability`
- `#SystemDesign/Consistency`
- `#SystemDesign/Architecture`

### Системные
- `#SRS`
- `#New`
