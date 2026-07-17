# Skills-Tools 索引 (INDEX)

> 本仓库分类与命名规范见 [CONVENTIONS.md](./CONVENTIONS.md)。
> 本文件由 `scripts/gen_index.py` 遍历 `skills/` 与 `packages/` 全部 SKILL.md 自动生成，修改结构后请重跑脚本以免再次脱节。

## 目录结构

```
Skills-Tools/
├── skills/                # 独立 skill（最小可调用单元），按领域分桶
│   ├── agent-ops/         # 智能体运作 / 系统工具
│   ├── content/           # 文档处理 (markitdown-skill)
│   ├── design/            # 设计 / 原型 / 可视化 / 前端
│   ├── engineering/       # 工程方法论 (superpowers 套件)
│   ├── pm/                # 产品管理（9 个中文子分类，见下）
│   └── supply-chain/      # 供应链 (WMS/OMS/TMS/关务)
├── packages/              # 多 skill 套件（含 manifest）
├── tools/                 # 通用脚本/CLI（非 skill 形态）
├── experts/               # 角色/专家人设
├── assets/                # 共享二进制资源
│   └── fonts/
├── intro/                 # 工作区 HTML 介绍/预览页
├── _trash_20260717/       # 重分类回收站（可恢复，非最终删除）
├── CONVENTIONS.md
└── INDEX.md
```

## Skill 清单（skills/）

### agent-ops（智能体运作/系统工具）

| 名称 (name) | 路径 | 说明 |
|---|---|---|
| `calicat-cli-operator` | `agent-ops/calicat-cli-operator/SKILL.md` | Use when an AI agent needs to operate the local Calicat CLI to |
| `teach` | `agent-ops/teach/SKILL.md` | Teach the user a new skill or concept, within this workspace. |
| `web-access` | `agent-ops/web-access/SKILL.md` | 所有联网操作必须通过此 skill 处理，包括：搜索、网页抓取、登录后操作、网络交互等。 |
| `wiki-lint` | `agent-ops/wiki-lint/SKILL.md` | Lint / health-check a Karpathy-style LLM Wiki. Runs link-graph |

### content（文档处理）

| 名称 (name) | 路径 | 说明 |
|---|---|---|
| `markitdown-skill` | `content/markitdown-skill/SKILL.md` | Convert documents to Markdown using Microsoft's MarkItDown CLI |

### design（设计/原型/可视化/前端）

| 名称 (name) | 路径 | 说明 |
|---|---|---|
| `ant-design` | `design/antd-skill/skills/ant-design/SKILL.md` | Decision guide for antd 6.x, Ant Design Pro 5/ProComponents, Ant Design X v2, and the offline `@ant-design/cli`. Use for component selection, theming/… |
| `antd` | `design/antd-skill/skills/antd/SKILL.md` | > |
| `archify` | `design/archify/SKILL.md` | Create professional architecture, workflow, sequence, data-flow, |
| `ardot-ant-icons-import` | `design/ardot-ant-icons-import/SKILL.md` | Import Ant Design icons into Ardot prototypes by converting SVGs to |
| `code-first-design-system` | `design/code-first-design-system/SKILL.md` | 用于为 code-first（产品直接出 HTML / AI 生成 UI）团队交付设计系统。产出包含：Ardot 画布规范看板、给 |
| `mermaid-diagram` | `design/mermaid-diagram/SKILL.md` | 生成 Mermaid 图表。用于产品经理或开发需要画流程图、泳道图、系统架构图、时序图、脑图，把文本描述或 PRD |
| `pencil-design` | `design/pencil-design/SKILL.md` | > |
| `pm-html-presentation` | `design/pm-html-presentation/SKILL.md` | HTML 演示/幻灯片生成 skill（fork of pakco-html）：生成静态 deck、网页、社媒卡片，并提供可视化风格选择器。单文件 / 内联 / 零外部依赖 / 响应式。 |
| `style-dictionary-token-build` | `design/style-dictionary-token-build/SKILL.md` | 用 style-dictionary v5 把单一 Token 源编译到 CSS/SCSS/JS/JSON 等多端。覆盖 v5 的 |
| `zhp-html-prototype` | `design/zhp-html-prototype/SKILL.md` | 生成静态 HTML |

### engineering（工程方法论）

#### engineering（其他）

| 名称 (name) | 路径 | 说明 |
|---|---|---|
| `superpowers` | `engineering/superpowers/SKILL.md` | > |
| `superpowers-brainstorming` | `engineering/superpowers/superpowers-brainstorming/SKILL.md` | Use before any creative work - creating features, building components, adding functionality, or modifying behavior - guides through exploration, quest… |
| `dispatching-parallel-agents` | `engineering/superpowers/superpowers-dispatching-parallel-agents/SKILL.md` | Use when facing 2+ independent tasks that can be worked on without |
| `executing-plans` | `engineering/superpowers/superpowers-executing-plans/SKILL.md` | Use when you have a written implementation plan to execute in a |
| `finishing-a-development-branch` | `engineering/superpowers/superpowers-finishing-a-development-branch/SKILL.md` | Use when implementation is complete, all tests pass, and you need |
| `receiving-code-review` | `engineering/superpowers/superpowers-receiving-code-review/SKILL.md` | Use when receiving code review feedback, before implementing |
| `requesting-code-review` | `engineering/superpowers/superpowers-requesting-code-review/SKILL.md` | Use when completing tasks, implementing major features, or before |
| `subagent-driven-development` | `engineering/superpowers/superpowers-subagent-driven-development/SKILL.md` | Use when executing implementation plans with independent tasks in |
| `systematic-debugging` | `engineering/superpowers/superpowers-systematic-debugging/SKILL.md` | Use when encountering any bug, test failure, or unexpected |
| `test-driven-development` | `engineering/superpowers/superpowers-test-driven-development/SKILL.md` | Use when implementing any feature or bugfix, before writing implementation code |
| `using-git-worktrees` | `engineering/superpowers/superpowers-using-git-worktrees/SKILL.md` | Use when starting feature work that needs isolation from current |
| `verification-before-completion` | `engineering/superpowers/superpowers-verification-before-completion/SKILL.md` | Use when about to claim work is complete, fixed, or passing, before |
| `superpowers-writing-plans` | `engineering/superpowers/superpowers-writing-plans/SKILL.md` | Use when you have a spec or requirements for a multi-step task, before touching code - guides writing comprehensive implementation plans with bite-siz… |
| `writing-skills` | `engineering/superpowers/superpowers-writing-skills/SKILL.md` | Use when creating new skills, editing existing skills, or verifying |
| `using-superpowers` | `engineering/superpowers/using-superpowers/SKILL.md` | Use when starting any conversation - establishes how to find and |

#### engineering/superpowers（Anthropic superpowers 方法论套件）

| 名称 (name) | 路径 | 说明 |
|---|---|---|

### pm（产品管理）

#### pm/AI上线

| 名称 (name) | 路径 | 说明 |
|---|---|---|
| `intended-vs-implemented` | `pm/AI上线/intended-vs-implemented/SKILL.md` | The method for finding the gap between what a system is supposed to do and what the code actually does — the class of bug generic scanners miss becaus… |
| `shipping-artifacts` | `pm/AI上线/shipping-artifacts/SKILL.md` | The durable documentation set that makes an AI-built (vibe-coded) app reviewable before shipping. A small core every app needs — architecture, user/pe… |

#### pm/产品发现

| 名称 (name) | 路径 | 说明 |
|---|---|---|
| `beachhead-segment` | `pm/产品发现/beachhead-segment/SKILL.md` | Identify the first beachhead market segment for a product launch. Evaluates segments against burning pain, willingness to pay, winnable market share, … |
| `brainstorm-experiments-new` | `pm/产品发现/brainstorm-experiments-new/SKILL.md` | Design lean startup experiments (pretotypes) for a new product. Creates XYZ hypotheses and suggests low-effort validation methods like landing pages, … |
| `brainstorm-ideas-new` | `pm/产品发现/brainstorm-ideas-new/SKILL.md` | Brainstorm feature ideas for a new product in initial discovery from PM, Designer, and Engineer perspectives. Use when starting product discovery for … |
| `identify-assumptions-new` | `pm/产品发现/identify-assumptions-new/SKILL.md` | Identify risky assumptions for a new product idea across 8 risk categories including Go-to-Market, Strategy, and Team. Use when evaluating startup ris… |
| `opportunity-solution-tree` | `pm/产品发现/opportunity-solution-tree/SKILL.md` | Build an Opportunity Solution Tree (OST) to structure product discovery — map a desired outcome to opportunities, solutions, and experiments. Based on… |

#### pm/产品执行

| 名称 (name) | 路径 | 说明 |
|---|---|---|
| `brainstorm-okrs` | `pm/产品执行/brainstorm-okrs/SKILL.md` | Brainstorm team-level OKRs aligned with company objectives — qualitative objectives with measurable key results. Use when setting quarterly OKRs, alig… |
| `create-prd` | `pm/产品执行/create-prd/SKILL.md` | Create a Product Requirements Document using a comprehensive 8-section template covering problem, objectives, segments, value propositions, solution, … |
| `dummy-dataset` | `pm/产品执行/dummy-dataset/SKILL.md` | Generate realistic dummy datasets for testing with customizable columns, constraints, and output formats (CSV, JSON, SQL, Python script). Use when cre… |
| `job-stories` | `pm/产品执行/job-stories/SKILL.md` | Create job stories using the 'When [situation], I want to [motivation], so I can [outcome]' format with detailed acceptance criteria. Use when writing… |
| `outcome-roadmap` | `pm/产品执行/outcome-roadmap/SKILL.md` | Transform an output-focused roadmap into an outcome-focused one that communicates strategic intent. Rewrites initiatives as outcome statements reflect… |
| `release-notes` | `pm/产品执行/release-notes/SKILL.md` | Generate user-facing release notes from tickets, PRDs, or changelogs. Creates clear, engaging summaries organized by category (new features, improveme… |
| `sprint-plan` | `pm/产品执行/sprint-plan/SKILL.md` | Plan a sprint with capacity estimation, story selection, dependency mapping, and risk identification. Use when preparing for sprint planning, estimati… |
| `test-scenarios` | `pm/产品执行/test-scenarios/SKILL.md` | Create comprehensive test scenarios from user stories with test objectives, starting conditions, user roles, step-by-step actions, and expected outcom… |
| `user-stories` | `pm/产品执行/user-stories/SKILL.md` | Create user stories following the 3 C's (Card, Conversation, Confirmation) and INVEST criteria with descriptions, design links, and acceptance criteri… |
| `wwas` | `pm/产品执行/wwas/SKILL.md` | Create product backlog items in Why-What-Acceptance format — independent, valuable, testable items with strategic context. Use when writing structured… |

#### pm/产品策略

| 名称 (name) | 路径 | 说明 |
|---|---|---|
| `ansoff-matrix` | `pm/产品策略/ansoff-matrix/SKILL.md` | Generate an Ansoff Matrix analysis mapping growth strategies across market penetration, market development, product development, and diversification. … |
| `business-model` | `pm/产品策略/business-model/SKILL.md` | Generate a Business Model Canvas with all 9 building blocks. Use when creating a business model, documenting how a business creates value, or analyzin… |
| `competitor-analysis` | `pm/产品策略/competitor-analysis/SKILL.md` | Analyze competitors with strengths, weaknesses, and differentiation opportunities. Identifies direct competitors and maps the competitive landscape. U… |
| `ideal-customer-profile` | `pm/产品策略/ideal-customer-profile/SKILL.md` | Identify the Ideal Customer Profile (ICP) from research data with demographics, behaviors, JTBD, and needs. Use when defining your ICP, analyzing PMF … |
| `lean-canvas` | `pm/产品策略/lean-canvas/SKILL.md` | Generate a Lean Canvas with problem, solution, metrics, cost structure, UVP, unfair advantage, channels, segments, and revenue. Use when exploring a l… |
| `market-segments` | `pm/产品策略/market-segments/SKILL.md` | Identify 3-5 potential customer segments with demographics, JTBD, and product fit analysis. Use when exploring market segments, identifying target aud… |
| `market-sizing` | `pm/产品策略/market-sizing/SKILL.md` | Estimate market size using TAM, SAM, and SOM with top-down and bottom-up approaches. Use when sizing a market opportunity, estimating addressable mark… |
| `pestle-analysis` | `pm/产品策略/pestle-analysis/SKILL.md` | Perform a PESTLE analysis covering Political, Economic, Social, Technological, Legal, and Environmental factors. Use when assessing the macro environm… |
| `porters-five-forces` | `pm/产品策略/porters-five-forces/SKILL.md` | Perform Porter's Five Forces analysis — competitive rivalry, supplier power, buyer power, threat of substitutes, and threat of new entrants. Use when … |
| `positioning-ideas` | `pm/产品策略/positioning-ideas/SKILL.md` | Brainstorm product positioning ideas differentiated from competitors. Identifies top competitors and generates positioning statements with rationale. … |
| `pricing-strategy` | `pm/产品策略/pricing-strategy/SKILL.md` | Analyze and design pricing strategies including pricing models, competitive pricing analysis, willingness-to-pay estimation, and price elasticity. Use… |
| `product-strategy` | `pm/产品策略/product-strategy/SKILL.md` | Create a comprehensive product strategy using the 9-section Product Strategy Canvas — vision, segments, costs, value propositions, trade-offs, metrics… |
| `product-vision` | `pm/产品策略/product-vision/SKILL.md` | Brainstorm an inspiring, achievable, and emotional product vision that motivates teams and aligns stakeholders. Use when defining or refining a produc… |
| `startup-canvas` | `pm/产品策略/startup-canvas/SKILL.md` | Generate a Startup Canvas combining Product Strategy (9 sections) and Business Model (costs + revenue) for a new product. An alternative to BMC and Le… |
| `swot-analysis` | `pm/产品策略/swot-analysis/SKILL.md` | Perform a detailed SWOT analysis — strengths, weaknesses, opportunities, and threats with actionable recommendations. Use when doing strategic assessm… |
| `value-prop-statements` | `pm/产品策略/value-prop-statements/SKILL.md` | Generate value proposition statements for marketing, sales, and onboarding from existing value propositions. Use when writing marketing copy, creating… |
| `value-proposition` | `pm/产品策略/value-proposition/SKILL.md` | Design a detailed value proposition using a 6-part JTBD template — Who, Why, What before, How, What after, Alternatives. Use when creating a value pro… |

#### pm/市场研究

| 名称 (name) | 路径 | 说明 |
|---|---|---|
| `customer-journey-map` | `pm/市场研究/customer-journey-map/SKILL.md` | Create an end-to-end customer journey map with stages, touchpoints, emotions, pain points, and opportunities. Use when mapping the customer experience… |
| `interview-script` | `pm/市场研究/interview-script/SKILL.md` | Create a structured customer interview script with JTBD probing questions, warm-up, core exploration, and wrap-up sections. Follows The Mom Test princ… |
| `sentiment-analysis` | `pm/市场研究/sentiment-analysis/SKILL.md` | Analyze user feedback data to identify segments with sentiment scores, JTBD, and product satisfaction insights. Use when analyzing user feedback at sc… |
| `summarize-interview` | `pm/市场研究/summarize-interview/SKILL.md` | Summarize a customer interview transcript into a structured template with JTBD, satisfaction signals, and action items. Use when processing interview … |
| `summarize-meeting` | `pm/市场研究/summarize-meeting/SKILL.md` | Summarize a meeting transcript into structured notes with date, participants, topic, key decisions, summary points, and action items. Use when process… |
| `user-personas` | `pm/市场研究/user-personas/SKILL.md` | Create refined user personas from research data — 3 personas with JTBD, pains, gains, and unexpected insights. Use when building personas from survey … |
| `user-segmentation` | `pm/市场研究/user-segmentation/SKILL.md` | Segment users from feedback data based on behavior, JTBD, and needs. Identifies at least 3 distinct user segments. Use when segmenting a user base, an… |

#### pm/市场进入

| 名称 (name) | 路径 | 说明 |
|---|---|---|
| `growth-loops` | `pm/市场进入/growth-loops/SKILL.md` | Identify growth loops (flywheels) for sustainable traction. Evaluates 5 loop types: Viral, Usage, Collaboration, User-Generated, and Referral. Use whe… |
| `gtm-motions` | `pm/市场进入/gtm-motions/SKILL.md` | Identify the best GTM motions and tools across 7 motion types: Inbound, Outbound, Paid Digital, Community, Partners, ABM, and PLG. Use when selecting … |
| `gtm-strategy` | `pm/市场进入/gtm-strategy/SKILL.md` | Create a go-to-market strategy covering marketing channels, messaging, success metrics, and launch timeline. Use when planning a product launch, creat… |
| `metrics-dashboard` | `pm/市场进入/metrics-dashboard/SKILL.md` | Define and design a product metrics dashboard with key metrics, data sources, visualization types, and alert thresholds. Use when creating a metrics d… |
| `stakeholder-map` | `pm/市场进入/stakeholder-map/SKILL.md` | Build a stakeholder map using a power/interest grid, identify communication strategies per quadrant, and generate a communication plan. Use when manag… |

#### pm/数据分析

| 名称 (name) | 路径 | 说明 |
|---|---|---|
| `ab-test-analysis` | `pm/数据分析/ab-test-analysis/SKILL.md` | Analyze A/B test results with statistical significance, sample size validation, confidence intervals, and ship/extend/stop recommendations. Use when e… |
| `cohort-analysis` | `pm/数据分析/cohort-analysis/SKILL.md` | Perform cohort analysis on user engagement data — retention curves, feature adoption trends, and segment-level insights. Use when analyzing user reten… |
| `sql-queries` | `pm/数据分析/sql-queries/SKILL.md` | Generate SQL queries from natural language descriptions. Supports BigQuery, PostgreSQL, MySQL, and other dialects. Reads database schemas from uploade… |

#### pm/营销增长

| 名称 (name) | 路径 | 说明 |
|---|---|---|
| `marketing-ideas` | `pm/营销增长/marketing-ideas/SKILL.md` | Generate 5 creative, cost-effective marketing ideas with channels, messaging, and engagement rationale. Use when brainstorming marketing campaigns, pl… |
| `monetization-strategy` | `pm/营销增长/monetization-strategy/SKILL.md` | Brainstorm 3-5 monetization strategies with audience fit, risks, and validation experiments. Use when exploring revenue models, evaluating pricing str… |
| `north-star-metric` | `pm/营销增长/north-star-metric/SKILL.md` | Define a North Star Metric and 3-5 supporting input metrics that form a metrics constellation. Classify the business game (Attention, Transaction, Pro… |
| `product-name` | `pm/营销增长/product-name/SKILL.md` | Brainstorm 5 unique, memorable product names with rationale aligned to brand values and target audience. Use when naming a new product, rebranding, or… |

#### pm/通用工具

| 名称 (name) | 路径 | 说明 |
|---|---|---|
| `analyze-feature-requests` | `pm/通用工具/analyze-feature-requests/SKILL.md` | Analyze and prioritize a list of feature requests by theme, strategic alignment, impact, effort, and risk. Use when reviewing customer feature request… |
| `brainstorm-experiments-existing` | `pm/通用工具/brainstorm-experiments-existing/SKILL.md` | Design experiments to test assumptions for an existing product — prototypes, A/B tests, spikes, and other low-effort validation methods. Use when vali… |
| `brainstorm-ideas-existing` | `pm/通用工具/brainstorm-ideas-existing/SKILL.md` | Brainstorm product ideas for an existing product using multi-perspective ideation from PM, Designer, and Engineer viewpoints. Use when generating new … |
| `competitive-battlecard` | `pm/通用工具/competitive-battlecard/SKILL.md` | Create sales-ready competitive battlecards comparing your product against a specific competitor — positioning, feature comparison, objection handling,… |
| `draft-nda` | `pm/通用工具/draft-nda/SKILL.md` | Draft a detailed Non-Disclosure Agreement between two parties covering information types, jurisdiction, and clauses needing legal review. Use when cre… |
| `grammar-check` | `pm/通用工具/grammar-check/SKILL.md` | Identify grammar, logical, and flow errors in text and suggest targeted fixes without rewriting the entire text. Use when proofreading content, checki… |
| `identify-assumptions-existing` | `pm/通用工具/identify-assumptions-existing/SKILL.md` | Identify risky assumptions for a feature idea in an existing product across Value, Usability, Viability, and Feasibility. Uses multi-perspective devil… |
| `pre-mortem` | `pm/通用工具/pre-mortem/SKILL.md` | Run a pre-mortem risk analysis on a PRD or launch plan. Categorizes risks as Tigers (real problems), Paper Tigers (overblown concerns), and Elephants … |
| `prioritization-frameworks` | `pm/通用工具/prioritization-frameworks/SKILL.md` | Reference guide to 9 prioritization frameworks with formulas, when-to-use guidance, and templates — RICE, ICE, Kano, MoSCoW, Opportunity Score, and mo… |
| `prioritize-assumptions` | `pm/通用工具/prioritize-assumptions/SKILL.md` | Prioritize assumptions using an Impact × Risk matrix and suggest experiments for each. Use when triaging a list of assumptions, deciding what to test … |
| `prioritize-features` | `pm/通用工具/prioritize-features/SKILL.md` | Prioritize a backlog of feature ideas based on impact, effort, risk, and strategic alignment with top 5 recommendations. Use when prioritizing a featu… |
| `privacy-policy` | `pm/通用工具/privacy-policy/SKILL.md` | Draft a detailed privacy policy covering data types, jurisdiction, GDPR and compliance considerations, and clauses needing legal review. Use when crea… |
| `retro` | `pm/通用工具/retro/SKILL.md` | Facilitate a structured sprint retrospective — what went well, what didn't, and prioritized action items with owners and deadlines. Use when running a… |
| `review-resume` | `pm/通用工具/review-resume/SKILL.md` | Comprehensive PM resume review and tailoring against 10 best practices including XYZ+S formula, keyword optimization, job-specific tailoring, and stru… |
| `strategy-red-team` | `pm/通用工具/strategy-red-team/SKILL.md` | Red-team a PRD, roadmap, or strategy by attacking its load-bearing assumptions before reality does. Steelmans then attacks each claim, ranks failure m… |

### supply-chain（供应链 WMS/OMS/TMS/关务）

| 名称 (name) | 路径 | 说明 |
|---|---|---|
| `prd-writer` | `supply-chain/PRD-writer/SKILL.md` | PRD产品需求文档撰写专家。当用户提到"写PRD"、"撰写需求"、"产品需求"、"功能设计"、"撰写产品需求文档"时，必须使用此skill。按照10段式标准模板（功能定义→业务规则→流程说明→数据来源→页面交互→操作后发生什么→约束与限制→状态机→用例→数据字典）输出专业文档。支持Mermaid流程… |
| `customs-classification` | `supply-chain/customs-classification/SKILL.md` | 使用 HS 六准则、类注、章注和品目文字辅助海关商品归类；当用户要求归类商品、比较候选税号、解释归类依据，或将归类规则整理成培训、SOP、案例、汇报材料时使用。 |
| `supply-chain-prd-writer` | `supply-chain/supply-chain-prd-writer/SKILL.md` | 扮演专业供应链产品经理，面向WMS/OMS/TMS等供应链后台管理系统，按四阶段门禁（需求分析 → Plan → HTML原型 → PRD）输出产品需求文档；终点交付物是PRD（产品需求文档），全程只关注业务目标、用户场景、功能边界、交互逻辑和验收标准，不关心技术实现；当用户提到写PRD、需求分析、… |

## 套件（packages/）

> `packages/` 内存放多 skill 套件。注意 `pm-flow-kit` 有两份平台变体套件（codex / workbuddy），skill 清单一致，仅触发词不同，均合法保留。

### 套件 · pm-flow-kit-codex

| 名称 (name) | 路径 | 说明 |
|---|---|---|
| `humanizer` | `skills/humanizer/SKILL.md` | Polish product writing without changing facts, scope, metrics, requirements, decisions, acceptance criteria, or source meaning. Use when Codex needs t… |
| `pm-boundary` | `skills/pm-boundary/SKILL.md` | Define boundary-stage product scope for pm-flow-kit. Use when Codex needs to create boundary.md with scope, non-scope, stakeholders, roles, permission… |
| `pm-context-contract` | `skills/pm-context-contract/SKILL.md` | Define and validate context contracts for product work. Use when Codex needs to organize domain rules, knowledge-base entry points, CONTEXT_MANIFEST.m… |
| `pm-flow` | `skills/pm-flow/SKILL.md` | End-to-end product management workflow controller for workspace binding, knowledge-base path confirmation, staged context confirmation, research, boun… |
| `pm-html-prototype` | `skills/pm-html-prototype/SKILL.md` | Generate offline HTML product prototypes with local assets, device frames, design-token usage, font constraints, component-library mapping, and self-c… |
| `pm-mermaid-diagram` | `skills/pm-mermaid-diagram/SKILL.md` | Generate standalone Mermaid diagrams for product management work. Use when Codex needs to turn requirement analysis, scenario catalogs, use cases, PRD… |
| `pm-metrics-definition` | `skills/pm-metrics-definition/SKILL.md` | Define product success metrics before PRD, prototype, or review output. Use when Codex needs to convert product goals into business metrics, user beha… |
| `pm-prd` | `skills/pm-prd/SKILL.md` | Create right-sized product requirements documents. Use when Codex needs to write, review, resize, or refactor PRDs using L1/L2/L3 depth, requirement-a… |
| `pm-prototype-review` | `skills/pm-prototype-review/SKILL.md` | Create prototype review artifacts that connect UI elements to requirement rules. Use when requirement analysis says a separate review artifact is need… |
| `pm-requirement-analysis` | `skills/pm-requirement-analysis/SKILL.md` | Analyze product requirements before downstream output. Use when Codex needs to convert rough or direct user requests into requirement analysis, scenar… |
| `pm-research` | `skills/pm-research/SKILL.md` | Produce research-stage product context for pm-flow-kit. Use when Codex needs to complete opportunity, user, market, competitor, benchmark, metric cont… |
| `pm-review` | `skills/pm-review/SKILL.md` | Perform independent product artifact reviews for pm-flow-kit. Use when Codex needs to review requirement analysis, metrics, boundary, PRDs, prototypes… |

### 套件 · pm-flow-kit-workbuddy

| 名称 (name) | 路径 | 说明 |
|---|---|---|
| `humanizer` | `skills/humanizer/SKILL.md` | Polish product writing without changing facts, scope, metrics, requirements, decisions, acceptance criteria, or source meaning. Use when you need to r… |
| `pm-boundary` | `skills/pm-boundary/SKILL.md` | Define boundary-stage product scope for pm-flow-kit. Use when you need to create boundary.md with scope, non-scope, stakeholders, roles, permissions, … |
| `pm-context-contract` | `skills/pm-context-contract/SKILL.md` | Define and validate context contracts for product work. Use when you need to organize domain rules, knowledge-base entry points, CONTEXT_MANIFEST.md, … |
| `pm-flow` | `skills/pm-flow/SKILL.md` | End-to-end product management workflow controller for staged context confirmation, requirement analysis, metrics definition, scenario and use-case cov… |
| `pm-html-prototype` | `skills/pm-html-prototype/SKILL.md` | Generate offline HTML product prototypes with local assets, device frames, design-token usage, font constraints, component-library mapping, and self-c… |
| `pm-mermaid-diagram` | `skills/pm-mermaid-diagram/SKILL.md` | Generate standalone Mermaid diagrams for product management work. Use when you need to turn requirement analysis, scenario catalogs, use cases, PRDs, … |
| `pm-metrics-definition` | `skills/pm-metrics-definition/SKILL.md` | Define product success metrics before PRD, prototype, or review output. Use when you need to convert product goals into business metrics, user behavio… |
| `pm-prd` | `skills/pm-prd/SKILL.md` | Create right-sized product requirements documents. Use when you need to write, review, resize, or refactor PRDs using L1/L2/L3 depth, requirement-anal… |
| `pm-prototype-review` | `skills/pm-prototype-review/SKILL.md` | Create prototype review artifacts that connect UI elements to requirement rules. Use when requirement analysis says a separate review artifact is need… |
| `pm-requirement-analysis` | `skills/pm-requirement-analysis/SKILL.md` | Analyze product requirements before downstream output. Use when you need to convert rough or direct user requests into requirement analysis, scenario … |
| `pm-research` | `skills/pm-research/SKILL.md` | Produce research-stage product context for pm-flow-kit. Use when you need to complete opportunity, user, market, competitor, benchmark, metric context… |
| `pm-review` | `skills/pm-review/SKILL.md` | Perform independent product artifact reviews for pm-flow-kit. Use when you need to review requirement analysis, metrics, boundary, PRDs, prototypes, d… |

## 工具 (tools/)

| 工具组 | 内容 |
|---|---|
| `doc-convert` | `doc_to_md`、`md_to_docx`、`wx2md`（纯脚本；`batch-doc-convert` 已迁为 `skills/content/markitdown-skill`） |
| `image-process` | `md2png` |

## 专家 (experts/)

| 文件 | 说明 |
|---|---|
| `solution-owner.md` | 角色/人设定义 |
| `supply-chain-solution-expert.md` | 角色/人设定义 |

## 资源 (assets/)

| 目录 | 内容 |
|---|---|
| `assets/fonts/` | `钉钉进步体` |

## 介绍页 (intro/)

| 文件 | 说明 |
|---|---|
| `pm-flow-kit.html` | 工作区/套件 HTML 介绍页 |

---
> 本索引由脚本自动生成。手工编辑后若结构变动，请运行 `python scripts/gen_index.py` 重新生成。
