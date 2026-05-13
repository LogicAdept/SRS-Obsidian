Для тегов следующие правила:
1. Новые файлы и те файлы которые подлежат редактированию или улучшению имеют тег #New
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

**Расширение:** новые заметки по возможности **расширяют это дерево** (новые подтеги под уже принятыми корнями), а не вводят **параллельные теги-синонимы** одного и того же понятия. Если для сущности уже закреплён путь (например Kubernetes только как `#DevOps/Tools/Kubernetes`), не добавлять второй корень без причины (`#Kubernetes` рядом с тем же смыслом). Для разных видов API используй префикс **`#API/`** и лист **`#API/<Вид>`** (например `#API/REST`), а не отдельные корни вроде `#REST` и не ветку под `Patterns`.

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
- `#Java/Spring`
- `#Java/JDBC`
- `#Java/Persistence`
- `#Java/Persistence/JPA`
- `#Java/Persistence/Hibernate`

### DSA
- `#DSA/Algorithms/Search`
- `#DSA/DataStructures/Graph`

### DistributedSystems
- `#DistributedSystems/Communication`

### API
- `#API/REST`
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
- `#Patterns/Concurrency`
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
