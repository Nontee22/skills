# Java Learning Taxonomy

Use this taxonomy to classify points and build learning paths. Do not add facts only because they appear in this taxonomy; taxonomy is for organization.

## Core Java

- Java syntax, object model, generics, annotations, reflection, exceptions.
- Collections, `HashMap`, `ConcurrentHashMap`, iterators, fail-fast, sorting.
- IO, NIO, serialization, date/time, streams, lambda, optional.

## JVM

- class loading, parent delegation, linking, initialization.
- bytecode, JIT, escape analysis, method dispatch.
- runtime memory areas, heap, stack, metaspace, direct memory.
- GC algorithms, collectors, tuning flags, allocation, promotion, pause analysis.
- Java Memory Model, happens-before, visibility, ordering.

## Concurrency

- thread lifecycle, synchronization, lock semantics.
- `volatile`, `synchronized`, CAS, AQS, `ReentrantLock`, read-write locks.
- thread pools, queues, rejection policies, sizing, lifecycle.
- `CompletableFuture`, fork/join, concurrent containers.
- deadlock, livelock, starvation, visibility bugs, race conditions.

## Spring Ecosystem

- IoC container, dependency injection, Bean lifecycle, scopes.
- AOP proxy model, JDK dynamic proxy, CGLIB, advice chain.
- transaction management, propagation, isolation, rollback rules, failure cases.
- Spring MVC request lifecycle, argument resolution, return handling, exception handling.
- Spring Boot startup, auto-configuration, condition evaluation, starter dependencies.
- configuration binding, profiles, events, validation.

## Persistence

- JDBC, connection pools, transactions, batch operations.
- MyBatis mapper proxy, executor, statement handling, result mapping, plugin chain.
- JPA/Hibernate entity lifecycle, dirty checking, lazy loading, N+1, transaction boundary.
- SQL design, indexes, execution plans, lock behavior, isolation levels.
- MySQL/InnoDB MVCC, redo/undo log, binlog, gap locks, next-key locks.

## Cache And Middleware

- Redis data structures, expiration, eviction, persistence, cluster.
- cache penetration, breakdown, avalanche, consistency, distributed lock.
- MQ semantics, delivery guarantee, idempotency, ordering, retry, dead-letter queues.
- Kafka partitioning, consumer groups, offset, rebalance, exactly-once caveats.
- RabbitMQ and RocketMQ routing, ack, retry, delay messages.

## Distributed Systems

- RPC, HTTP, REST, serialization, timeout, retry, circuit breaking, rate limiting.
- service discovery, configuration center, gateway, load balancing.
- distributed transaction, Saga, TCC, eventual consistency.
- idempotency, distributed lock, clock, snowflake IDs.
- observability, tracing, metrics, logs, alerting.

## Network And Framework Internals

- Netty event loop, channel pipeline, byte buffer, codec.
- servlet container, Tomcat connector, thread model.
- HTTP protocol, connection reuse, TLS, gRPC when relevant.

## Engineering Practice

- Maven/Gradle dependencies, packaging, deployment.
- Docker, Kubernetes, CI/CD.
- testing, mocks, integration tests, contract tests.
- troubleshooting, profiling, logging, monitoring, production diagnostics.

## Classification Fields

For each point, assign:

- `primary_category`: one taxonomy category.
- `secondary_tags`: optional keywords.
- `depth`: `basic`, `intermediate`, `advanced`, or `source-code`.
- `learning_priority`: `high`, `medium`, or `low`.
- `interview_value`: `high`, `medium`, or `low`.
- `source_dive`: `yes`, `optional`, or `no`.

## Deep-Dive Signal

Prefer source-code deep dive when the article discusses:

- framework behavior that depends on proxies, interceptors, filters, handlers, or lifecycle callbacks;
- "why it fails" cases such as Spring transaction self-invocation;
- runtime dispatch, class loading, lock acquisition, transaction commit/rollback, SQL execution, or message consumption;
- performance tuning or production troubleshooting;
- annotations or configuration that trigger hidden framework behavior.
