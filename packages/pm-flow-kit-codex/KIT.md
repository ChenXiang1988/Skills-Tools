# pm-flow-kit（PM 流程套件）

`pm-flow-kit` 是一组协同工作的 PM skill。入口是 `pm-flow`，其他 skill 只提供插件内的专项能力，不依赖包外能力路由。

## 包含内容

英文目录名是给系统识别用的；你看中文名称和作用即可。

| skill 目录名 | 中文名称 | 作用 |
|---|---|---|
| `pm-flow` | PM 流程总控 | 流程总控：阶段、状态、产物、决策、门禁 |
| `pm-context-contract` | 上下文契约 | 领域规范、知识库、输入约束、上下文读取规则 |
| `pm-research` | 研究阶段 | 机会、用户、市场、竞品、标杆、指标上下文、来源风险、假设和开放问题 |
| `pm-requirement-analysis` | 需求分析 | 把口语化需求转成需求分析结论、场景覆盖清单、产物计划 |
| `pm-boundary` | 边界定义 | 范围、非范围、利益相关方、角色权限、端面、系统归属、约束、依赖、风险和决策 |
| `pm-prd` | PRD 写作 | PRD 量级判定、L1/L2/L3 模板、字段字典、验收标准、自检 |
| `pm-html-prototype` | HTML 原型 | 离线 HTML 原型、设备框、字体、设计规范引用、组件库映射 |
| `pm-prototype-review` | 原型评审 | 界面和规则联动评审件、评审会议材料；仅在需求分析判定需要评审件时使用 |
| `pm-metrics-definition` | 指标定义 | 定义业务指标、用户行为指标、输入指标、护栏指标、基线、数据源和判断阈值 |
| `pm-mermaid-diagram` | 图表生成 | Mermaid 流程图、泳道图、状态机、时序图专项输出，默认外置到图表目录 |
| `pm-review` | 综合评审 | 对需求分析、边界、指标、PRD、原型、图表、风险、决策和就绪度做独立评审 |
| `humanizer` | 文档去 AI 味 | PRD 和产品文档表达润色，只改表达，不改事实 |

## 设计系统

通用 Codex 版内置一个中性的 `design-system/`，用于 HTML 原型默认视觉和 token。它不绑定具体业务域。

原型脚手架的设计系统选择顺序：

1. `PM_FLOW_DESIGN_SYSTEM`
2. 项目根目录 `design-system/`
3. 项目根目录 `.pm-flow/design-system/`
4. 插件内置通用 `design-system/`

生成原型时，实际使用的设计系统会被快照到 `prototypes/assets/design-system/`，保证原型离线可打开。

## 使用方式

1. 安装并启用 `pm-flow-kit`。
2. 使用 `pm-flow` 作为入口 skill。
3. 首次介入时先确认项目工作区位置，并写入 `.pm-flow/project_config.json`。
4. 首次介入时同时确认知识库边界：知识库目录、确认的文件清单，或明确“不使用外部知识库”的原因。
5. 工作区和知识库已确认后，后续任务复用，不重复询问。
6. 每轮先读 `pm-flow/USAGE.md`，再运行 `pm-flow/controller.py status --root <项目目录>`。
7. 先完成知识库引入确认，再用 `pm-requirement-analysis` 生成 `requirement_analysis.md`、`scenario-catalog.md`、`artifact-plan.md`。
8. 根据当前阶段和产物计划调用 `pm-research`、`pm-boundary`、`pm-metrics-definition`、`pm-prd`、`pm-html-prototype`、`pm-prototype-review`、`pm-mermaid-diagram`、`pm-review` 或 `humanizer`。
9. PRD 内容确认后，可用 `humanizer` 去 AI 味，但不能改变需求事实、范围、规则或验收标准。

## 工作区规则

- human 只需要提供工作区位置，不需要先整理成标准文档。
- 插件只创建 `.pm-flow/`、`.pm-flow/work/` 和 `project_config.json` 映射的产物，不重排 human 已有目录。
- 如果 human 明确要求变更工作区，使用 `workspace rebind --confirm` 重新绑定。
- 如果发现当前目录和已绑定目录不一致，agent 必须停止工作，先和 human 明确工作区结构。

## 知识库规则

- 知识库是 agent 读取的资料边界，不是插件内部内容。
- 首次介入时必须确认知识库路径；如果没有外部知识库，也要记录“不使用”的原因。
- 知识库确认后，后续任务不重复询问。
- 如果 human 要变更知识库，使用 `knowledge rebind --confirm` 重新绑定。
- 如果知识库目录、manifest 或已确认来源文件不存在、移动或不一致，agent 必须停止工作，先找 human 确认。
- 插件只在 `.pm-flow/project_config.json` 记录知识库绑定，不把公司资料复制进插件。

## 核心流程

`pm-flow` 保持五个阶段不变；知识库引入确认和需求分析是所有阶段前的全局前置门禁，不新增为阶段：

```text
research -> boundary -> prototype -> prd -> review
```

四种流程路径：

| 类型 | 阶段 |
|---|---|
| `new-platform` | research -> boundary -> prototype -> prd -> review |
| `iteration` | boundary -> prototype -> prd -> review |
| `iteration-lite` | boundary -> prd -> review |
| `micro` | prd -> review |

## 关键约束

- 工作区位置必须先确认；确认后不得重复询问，除非 human 要变更。
- 工作区目录发生变更时必须停止，不允许继续写产物。
- 知识库边界必须先确认；确认后不得重复询问，除非 human 要变更。
- 知识库路径、manifest 或来源文件异常时必须停止，不允许假装已经引用知识库。
- 不新增 `discovery`、`validation`、`shipping` 等阶段。
- 不依赖包外能力路由；插件内每个 skill 都必须自包含。
- 有上下文时按 manifest 读取；没有上下文时记录假设，不把假设写成事实。
- PRD、HTML 原型、图表、原型评审件、humanizer 输出前，都必须先完成需求分析。
- research 阶段使用 `pm-research`；boundary 阶段使用 `pm-boundary`；review 阶段使用 `pm-review`。
- 不默认套用 Ant Design；只有项目规范或用户明确指定时才启用。
- HTML 原型使用 `pm-html-prototype`；原型评审件使用 `pm-prototype-review`，二者不是同一个分支。
- `humanizer` 只用于表达润色，不得改变范围、规则、验收标准或决策。
