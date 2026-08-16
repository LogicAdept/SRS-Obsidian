<!--
reps: 0
priority: 0
-->
#Java/Spring/Batch #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

Spring Batch is a lightweight, comprehensive batch framework that is designed for use in developing robust batch applications. 
**Why Is Spring Batch Useful** 
* Restartability
* Different readers and writers
* Chunk Processing
* Ease Of Transaction Management
* Ease of parallel processing

**Project Structure** 
In this project, we will create a simple job with 2 step tasks and execute the job to observe the logs. Job execution flow will be –

1. Start job
1. Execute task one
1. Execute task two
1. Finish job

* **Maven Dependencies**

**pom.xml** 
```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd;">
    <modelVersion>4.0.0</modelVersion>
 
    <groupId>com.springbatchexample</groupId>
    <artifactId>App</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <packaging>jar</packaging>
 
    <name>App</name>
    <url>http://maven.apache.org</url>
 
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.0.3.RELEASE</version>
    </parent>
 
    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>
 
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-batch</artifactId>
        </dependency>
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>runtime</scope>
        </dependency>
    </dependencies>
 
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
 
    <repositories>
        <repository>
            <id>repository.spring.release</id>
            <name>Spring GA Repository</name>
            <url>http://repo.spring.io/release</url>
        </repository>
    </repositories>
</project>
```

* **Add Tasklets**

**TaskOne.java**
```java
import org.springframework.batch.core.StepContribution;
import org.springframework.batch.core.scope.context.ChunkContext;
import org.springframework.batch.core.step.tasklet.Tasklet;
import org.springframework.batch.repeat.RepeatStatus;
 
public class TaskOne implements Tasklet {
 
    public RepeatStatus execute(StepContribution contribution, ChunkContext chunkContext) throws Exception
    {
        System.out.println("TaskOne start..");
        // ... some code
        System.out.println("TaskOne done..");
        return RepeatStatus.FINISHED;
    }   
}
```

**TaskTwo.java**
```java
import org.springframework.batch.core.StepContribution;
import org.springframework.batch.core.scope.context.ChunkContext;
import org.springframework.batch.core.step.tasklet.Tasklet;
import org.springframework.batch.repeat.RepeatStatus;
 
public class TaskTwo implements Tasklet {
 
    public RepeatStatus execute(StepContribution contribution, ChunkContext chunkContext) throws Exception 
    {
        System.out.println("TaskTwo start..");
        // ... some code
        System.out.println("TaskTwo done..");
        return RepeatStatus.FINISHED;
    }   
}
```
* **Spring Batch Configuration** 
This is major step where you define all the job related configurations and it’s execution logic. 

**BatchConfig.java** 
```java
import org.springframework.batch.core.Job;
import org.springframework.batch.core.Step;
import org.springframework.batch.core.configuration.annotation.EnableBatchProcessing;
import org.springframework.batch.core.configuration.annotation.JobBuilderFactory;
import org.springframework.batch.core.configuration.annotation.StepBuilderFactory;
import org.springframework.batch.core.launch.support.RunIdIncrementer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
 
import com.springbatchexample.demo.tasks.TaskOne;
import com.springbatchexample.demo.tasks.TaskTwo;
 
@Configuration
@EnableBatchProcessing
public class BatchConfig {
     
    @Autowired
    private JobBuilderFactory jobs;
 
    @Autowired
    private StepBuilderFactory steps;
     
    @Bean
    public Step stepOne(){
        return steps.get("stepOne")
                .tasklet(new TaskOne())
                .build();
    }
     
    @Bean
    public Step stepTwo() {
        return steps.get("stepTwo")
                .tasklet(new TaskTwo())
                .build();
    }  
     
    @Bean
    public Job demoJob() {
        return jobs.get("demoJob")
                .incrementer(new RunIdIncrementer())
                .start(stepOne())
                .next(stepTwo())
                .build();
    }
}
```
* **Demo** 
Now our simple job 'demoJob' is configured and ready to be executed. I am using CommandLineRunner interface to execute the job automatically, with JobLauncher, when the application is fully started.

**App.java**
```java
import org.springframework.batch.core.Job;
import org.springframework.batch.core.JobParameters;
import org.springframework.batch.core.JobParametersBuilder;
import org.springframework.batch.core.launch.JobLauncher;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
 
@SpringBootApplication
public class App implements CommandLineRunner {
    @Autowired
    JobLauncher jobLauncher;
     
    @Autowired
    Job job;
     
    public static void main(String[] args) {
        SpringApplication.run(App.class, args);
    }
 
    @Override
    public void run(String... args) throws Exception {
        JobParameters params = new JobParametersBuilder()
                    .addString("JobID", String.valueOf(System.currentTimeMillis()))
                    .toJobParameters();
        jobLauncher.run(job, params);
    }
}
```
Console Logs
```
o.s.b.c.l.support.SimpleJobLauncher      : Job: [SimpleJob: [name=demoJob]] launched with
the following parameters: [{JobID=1530697766768}]
 
o.s.batch.core.job.SimpleStepHandler     : Executing step: [stepOne]
TaskOne start..
TaskOne done..
 
o.s.batch.core.job.SimpleStepHandler     : Executing step: [stepTwo]
TaskTwo start..
TaskTwo done..
 
o.s.b.c.l.support.SimpleJobLauncher      : Job: [SimpleJob: [name=demoJob]] completed with
the following parameters: [{JobID=1530697766768}] and the following status: [COMPLETED]
```
