<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #DevOps/Containerisation #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

A Docker is a tool that makes it very easy to deploy and run an application using **containers**. A container allows a developer to create an all-in-one package of the developed application with all its dependencies. For example, a Java application requires Java libraries, and when we deploy it on any system or VM, we need to install Java first. But, in a container, everything is kept together and shipped as one package, such as in a Docker container.

Step 01: **Create a simple Spring Boot Application**
```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class Application {

    @RequestMapping("/")
    public String home() {
        return "Hello Docker World";
    }

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```
To run the application, use the following Maven command from the project root folder:
```
cmd> mvn spring-boot:run
```
Step 02: **Dockerizing using Dockerfile** 

* **Dockerfile** – Specifying a file that contains native Docker commands to build the image
* **Maven** – Using a Maven plugin to build the image 

A Dockerfile is just a regular `.txt` file that includes native Docker commands that are used to specify the layers of an image. The content of the file itself can look something like this:
```
FROM java:8-jdk-alpine

COPY ./target/demo-docker-0.0.1-SNAPSHOT.jar /usr/app/

WORKDIR /usr/app

RUN sh -c 'touch demo-docker-0.0.1-SNAPSHOT.jar'

ENTRYPOINT ["java","-jar","demo-docker-0.0.1-SNAPSHOT.jar"]
```

* **FROM** – The keyword FROM tells Docker to use a given base image as a build base. We have used 'java' with tag '8-jdk-alpine'. Think of a tag as a version. The base image changes from project to project. You can search for images on docker-hub.
* **COPY** - This tells Docker to copy files from the local file-system to a specific folder inside the build image. Here, we copy our .jar file to the build image (Linux image) inside /usr/app.
* **WORKDIR** - The WORKDIR instruction sets the working directory for any RUN, CMD, ENTRYPOINT, COPY and ADD instructions that follow in the Dockerfile. Here we switched the workdir to /usr/app so as we don't have to write the long path again and again.
* **RUN** - This tells Docker to execute a shell command-line within the target system. Here we practically just "touch" our file so that it has its modification time updated (Docker creates all container files in an "unmodified" state by default).
* **ENTRYPOINT** - This allows you to configure a container that will run as an executable. It's where you tell Docker how to run your application. We know we run our spring-boot app as java -jar.jar, so we put it in an array.

Step 03: **Create Docker image** 

Generate a Spring Boot `.jar` file using `mvn clean install` command. This file will be used to create the Docker image.
Let's build the image using this Dockerfile. To do so, move to the root directory of the application and run this command:
```
cmd> docker build -t greeting-app 
```
We built the image using `docker build`. We gave it a name with the `-t` flag and specified the current directory where the Dockerfile is. The image is built and stored in our local docker registry. 

Let's check our image: 
```
cmd> docker images
```
And finally, let's run our image:
```
cmd> docker run -p 8090:8080 greeting-app 
```
We can run Docker images using the `docker run` command. 

Each container is an isolated environment in itself and we have to map the port of the host operating system - 8090 and the port inside the container - 8080, which is specified as the -p 8090:8080 argument.
Now, we can access the endpoint on `http://localhost:8080/greet/Pradeep`

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Чем образ (image) отличается от контейнера (container)?**

Образ — шаблон, неизменяемый снимок (как класс). Контейнер — запущенный экземпляр образа (как объект). Из одного образа можно запустить много контейнеров.

**Что такое Dockerfile?**

Текстовый файл с инструкциями для сборки образа: FROM (базовый образ), COPY, RUN, CMD/ENTRYPOINT и т.д.

**Какие команды Docker ты знаешь?**

docker build, docker run, docker ps, docker logs, docker exec, docker stop, docker rm, docker images, docker pull/push.

**Что такое docker-compose?**

Инструмент для запуска нескольких связанных контейнеров одной командой через yaml-файл. Обычно: приложение + БД + Redis.

**Зачем нужны Docker-образы в CI/CD?**

Чтобы среда сборки была одинаковая на всех машинах. И на проде запускается тот же образ, что был протестирован.

**Образ (image) vs контейнер (container).**

Образ — неизменяемый шаблон (как класс). Контейнер — запущенный экземпляр образа (как объект). Из одного образа — много контейнеров.

**Dockerfile: основные инструкции.**

FROM (базовый образ), COPY/ADD, RUN, WORKDIR, EXPOSE, ENV, CMD/ENTRYPOINT, VOLUME, USER.

**docker-compose.**

Инструмент для запуска нескольких связанных контейнеров одной командой через yaml. Типовой сценарий: приложение + БД + Redis + Kafka.

**Docker: образ vs контейнер. CMD vs ENTRYPOINT.**

Образ: шаблон (класс). Контейнер: запущенный экземпляр (объект). CMD: аргументы по умолчанию (легко переопределить). ENTRYPOINT: основная команда (сложнее). docker-compose: несколько контейнеров (Postgres + Kafka + сервис). Testcontainers: Docker из Java-кода для тестов.
