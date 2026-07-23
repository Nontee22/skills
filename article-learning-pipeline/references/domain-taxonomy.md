# Domain Taxonomy

Use this taxonomy to classify extracted `P-xxx` points across supported engineering domains. Pick one primary category and add secondary tags when helpful.

## Common Dimensions

- `concept`: definition, mental model, architecture role, or terminology.
- `mechanism`: runtime behavior, lifecycle, scheduling, dispatch, dependency tracking, state transition, or orchestration flow.
- `api`: API, hook, component option, annotation, class, method, tool interface, protocol, command, or SDK method.
- `configuration`: config file, build option, manifest field, project setting, dependency, runtime flag, or platform switch.
- `code-behavior`: what a code block does, why it works, why it fails, or what output/side effect it produces.
- `sequence`: ordered lifecycle, request path, rendering path, startup path, tool-call path, or source-code call chain.
- `comparison`: differences between versions, APIs, mechanisms, or design choices.
- `tradeoff`: cost, benefit, maintainability, reliability, performance, or compatibility decision.
- `caveat`: boundary condition, pitfall, invalid scenario, platform constraint, or common misunderstanding.
- `failure-mode`: bug, exception, stale state, race condition, render issue, transaction issue, tool-call failure, hallucination, timeout, or production incident.
- `troubleshooting`: diagnosis path, log/metric/snapshot signal, reproduction method, or fix.
- `interview`: point likely to become a basic, mechanism, source, or scenario interview follow-up.

## Frontend Vue2 / Vue3

- `frontend-vue/concept`: data-driven UI, component model, MVVM, Composition API mental model.
- `frontend-vue/reactivity`: Vue2 `Object.defineProperty`, Vue3 `Proxy`, `ref`, `reactive`, dependency tracking, `computed`, `watch`, `nextTick`.
- `frontend-vue/rendering`: template compilation, virtual DOM, diff, patch flags, block tree, slots, directives.
- `frontend-vue/component`: props, emits, provide/inject, v-model, lifecycle, Teleport, async component, keep-alive.
- `frontend-vue/router-state`: Vue Router, navigation guards, route lazy loading, Vuex, Pinia.
- `frontend-vue/performance`: bundle splitting, render optimization, list rendering, key, virtualization, SSR/SSG/prerender.
- `frontend-vue/source`: Vue core packages, runtime-core, reactivity, compiler, scheduler, renderer.

## WeChat Mini Program Frontend

- `frontend-miniprogram/concept`: app/page/component model, host environment, WXML/WXSS/JS split, platform limits.
- `frontend-miniprogram/lifecycle`: App/Page/Component lifecycle, route stack, tab/page navigation.
- `frontend-miniprogram/state-render`: `setData`, data diff, render bridge, custom component state, observers.
- `frontend-miniprogram/api`: wx APIs, login, authorization, storage, network, payment, sharing, open capability.
- `frontend-miniprogram/performance`: package size, subpackage loading, image optimization, list rendering, bridge-call reduction.
- `frontend-miniprogram/build`: project config, app.json/page.json, npm package handling, cloud development, CI upload.
- `frontend-miniprogram/failure`: auth failure, data not updating, route stack overflow, package oversize, API compatibility.

## AI Agent Systems

- `agent/concept`: agent loop, role/task decomposition, tool use, memory, planning, reflection, evaluation.
- `agent/orchestration`: single-agent, multi-agent, supervisor/worker, planner/executor, routing, handoff.
- `agent/tooling`: function calling, MCP/tool schema, tool result parsing, retries, sandboxing, permissions.
- `agent/context-memory`: prompt construction, context window, retrieval, summarization, vector memory, episodic memory.
- `agent/rag`: query rewriting, retrieval, reranking, grounding, citation, chunking, freshness.
- `agent/evaluation`: task success criteria, traces, regression evals, human review, hallucination checks.
- `agent/failure`: tool misuse, prompt injection, stale context, infinite loops, over-delegation, unsafe action.

## Java / Backend

- `java/core`: syntax, object model, generics, annotations, reflection, exceptions.
- `java/jvm`: class loading, bytecode, memory areas, GC, JIT, JVM flags.
- `java/concurrency`: threads, locks, JMM, volatile, CAS, thread pools, CompletableFuture.
- `java/spring`: IoC, Bean lifecycle, AOP, transaction, Spring MVC, Spring Boot auto-configuration.
- `java/persistence`: JDBC, MyBatis, JPA, transaction isolation, locks, index/query optimization.
- `java/distributed`: Redis, MQ, RPC, Dubbo, Netty, HTTP, cache consistency, distributed lock.
- `java/production`: logging, metrics, tracing, performance tuning, reliability, security, deployment.

## Classification Rules

- Use the domain prefix when the point is clearly domain-specific.
- Use common dimensions when the article is cross-domain or the domain is unclear.
- Do not add facts only because they appear in this taxonomy. The taxonomy organizes extracted facts; it is not evidence.
- Put version-sensitive claims into low-confidence items unless the source or an official reference supports the exact version.
