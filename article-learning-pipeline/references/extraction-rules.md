# Extraction Rules

Use these rules for every technical article extraction across Vue2/Vue3, WeChat Mini Program frontend, AI Agent systems, Java, and similar engineering domains.

## Point Types

Use one or more of these point types:

- `concept`: definition, term, mental model, or distinction.
- `mechanism`: runtime behavior, internal process, lifecycle, dispatch path, transaction flow, memory model, thread interaction, or framework mechanism.
- `api`: class, interface, method, annotation, enum, command, dependency, or library API.
- `configuration`: property, XML/YAML item, JVM flag, Maven/Gradle dependency, annotation attribute, or runtime option.
- `code-behavior`: what a code block does, why it works, why it fails, or what output it produces.
- `sequence`: ordered steps, request path, startup path, initialization path, or source-code call chain.
- `comparison`: difference between two concepts, APIs, implementations, or scenarios.
- `tradeoff`: advantage, disadvantage, cost, performance impact, maintainability impact, or design decision.
- `caveat`: warning, pitfall, boundary condition, invalid scenario, or common misunderstanding.
- `failure-mode`: exception, bug, data inconsistency, deadlock, timeout, transaction failure, cache failure, or production incident pattern.
- `troubleshooting`: diagnosis method, log signal, metric, reproduction path, or fix.
- `interview`: point likely to become an interview question or follow-up.

## Must Extract

Extract these whenever present:

- definitions and "what is X" statements;
- "why" explanations and root causes;
- numbered workflows, lifecycle phases, request chains, startup chains, and call chains;
- language/runtime/framework/platform details, including Java/JVM, Vue2/Vue3 runtime, WeChat Mini Program lifecycle/API constraints, Agent orchestration, tool calling, memory, planning, retrieval, and evaluation behavior;
- Spring, Spring Boot, Spring MVC, Spring AOP, transaction, IoC, Bean lifecycle, and auto-configuration mechanisms;
- MyBatis, JPA, JDBC, connection pool, SQL, transaction isolation, lock, index, and query optimization details;
- Redis, cache consistency, distributed lock, MQ, Kafka, RabbitMQ, RocketMQ, Dubbo, Netty, HTTP, RPC, and microservice details;
- class names, method names, annotations, configuration keys, dependencies, commands, and code snippets;
- conditions under which a mechanism succeeds or fails;
- version constraints, environment requirements, or compatibility notes;
- performance, memory, concurrency, transaction, security, and reliability implications;
- warnings introduced by words such as "注意", "核心", "关键", "必须", "不要", "不建议", "坑", "原理", "本质", "源码", "异常", "失败", "性能", "安全", "并发", "事务", "配置".

## Can Compress

Compress but still account for these in the internal coverage ledger:

- repeated motivation or background;
- repeated examples that support the same point;
- personal commentary with no technical content;
- introductory transitions;
- marketing or non-technical wording.

Mark compressed content as `background`, `duplicate`, or `example-only`.

## Atomicity

One point should contain one learning claim. Split a sentence into multiple points when it contains multiple independent claims.

Bad:

`Spring transactions use AOP, support multiple propagation behaviors, and may fail with self-invocation or swallowed exceptions.`

Good:

- `Spring declarative transactions usually rely on AOP proxy interception.`
- `Spring transaction propagation controls how an inner transaction participates in an outer transaction.`
- `Self-invocation can bypass the proxy and prevent transactional advice from running.`
- `Catching and not rethrowing an exception can prevent rollback.`

## Evidence Rules

Every article-derived point must include source IDs. If the point combines multiple parts of the article, include every relevant source ID.

Use these labels:

- `direct`: explicitly stated by the article.
- `synthesized`: combines multiple article fragments.
- `inferred`: reasonable inference from the article, not directly stated.
- `external-suggestion`: useful learning direction or source-code entry point not stated by the article.
- `supplemental-suggestion`: related key knowledge missing from the article, current enough to recommend, and clearly separated from extracted content.

Only `direct` and `synthesized` points count as extracted article content.

## Supplemental Suggestion Rules

Preserve every article core point first. Add supplemental suggestions only after extraction and omission audit show the article-derived point list is complete.

Use `SUP-001`, `SUP-002`, etc. for supplemental suggestions. Do not use `P-xxx` IDs for supplements.

Include a supplemental suggestion only when all are true:

- it is directly related to the article topic, prerequisite chain, source-code mechanism, production scenario, or interview follow-up path;
- it is not already covered by the article-derived points;
- it materially improves learning or prevents a likely misunderstanding;
- it is not known to be obsolete;
- it is stable engineering knowledge, or it has been checked against current official documentation/source material when version-sensitive.

Do not include supplements that are merely interesting, speculative, too broad, or weakly related.

For each supplement, include:

- `ID`: `SUP-xxx`;
- `补充建议`: concise statement;
- `关联原文`: related `P-xxx` IDs or source units;
- `为什么补充`: why the article would be incomplete for learning without noticing it;
- `时效状态`: `stable`, `verified-current`, or `needs-verification`;
- `验证说明`: official source/date when checked, or why it is stable;
- `学习/面试价值`: how it helps learning, source-code reading, or interview preparation.

If currentness cannot be verified for a version-sensitive claim, place it under low-confidence or human-confirmation items instead of the confirmed supplemental suggestions table.

Supplemental suggestions must not affect coverage status. A source unit cannot be marked covered because of a supplement.

## Source-Code Deep Dive Rules

When a point has source-code learning value, create a deep-dive direction inside that point's AI prompt card. Include concrete entry points when they are known and relevant, but label them as suggestions if they are not present in the article.

Examples:

- Spring transaction: `TransactionInterceptor`, `TransactionAspectSupport`, `PlatformTransactionManager`, `AbstractPlatformTransactionManager`, `AnnotationTransactionAttributeSource`.
- Spring IoC / Bean lifecycle: `AbstractApplicationContext`, `DefaultListableBeanFactory`, `AbstractAutowireCapableBeanFactory`, `BeanPostProcessor`.
- Spring MVC: `DispatcherServlet`, `HandlerMapping`, `HandlerAdapter`, `HandlerMethodArgumentResolver`, `HandlerExceptionResolver`.
- Spring Boot auto-configuration: `SpringApplication`, `AutoConfigurationImportSelector`, `ConfigurationClassPostProcessor`.
- MyBatis: `SqlSession`, `Executor`, `MappedStatement`, `StatementHandler`, `ParameterHandler`, `ResultSetHandler`.
- JDK concurrency: `ThreadPoolExecutor`, `AbstractQueuedSynchronizer`, `ReentrantLock`, `ConcurrentHashMap`, `CompletableFuture`.
- JVM class loading: `ClassLoader`, parent delegation, verification, preparation, resolution, initialization.

Do not pretend the article mentioned these entry points unless source IDs prove it.

Do not create a standalone source-code deep-dive checklist table. Put `源码入口` and `深挖方向` directly into each `P-xxx` or `SUP-xxx` prompt card, and repeat that content in the copy-pasteable prompt text.

## Code And Configuration Output Rules

Still detect code blocks, annotations, commands, dependencies, configuration keys, and snippets during extraction. They often carry important mechanism, failure-mode, or source-code entry information.

Do not output a standalone code/configuration table, and do not paste raw code/configuration snippets as a separate section. Instead:

- if the code or configuration expresses a core learning point, create a normal `P-xxx` AI prompt card for it;
- describe the behavior, purpose, risk, source IDs, source-code entry, and deep-dive direction in that card;
- include exact names such as class names, method names, annotation names, or property keys only when they are needed for learning or source navigation;
- mark code/config-only source units as `example-only`, `background`, or `duplicate` in the internal coverage ledger when they do not add a new learning point.

## Interview Rules

Mark a point as interview-worthy when it has at least one of these traits:

- it explains "why" instead of only "what";
- it involves failure conditions or boundary cases;
- it has source-code or implementation depth;
- it connects to production incidents;
- it has common misconceptions;
- it can become a scenario question;
- it requires comparing two mechanisms.

For interview follow-ups, include:

- basic check question;
- deeper mechanism question;
- source-code or implementation question;
- production scenario question when applicable.

## Omission Audit

After extraction, inspect the source units again and verify:

- every heading is reflected in the learning map;
- every paragraph has a coverage status;
- every list item is either extracted or marked repetitive;
- every table row is represented or summarized with source IDs;
- every code block has behavior, purpose, or non-essential status;
- every warning/caveat/failure case has at least one point;
- every important class, method, annotation, and configuration item appears in the relevant AI prompt card as a topic detail, source-code entry, or deep-dive direction.
