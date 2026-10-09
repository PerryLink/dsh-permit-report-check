# dsh-permit-report-check — 行政许可办理核对

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-permit-report-check` 读取一份行政许可办理台账——申请人表头加每条申请一行——核对这份台账自身的闭环与自洽：申请材料栏列出的每一项是否记录了提交情况、受理日期是否不晚于决定日期、决定日期是否落在受理日期与该台账自己写的承诺办结日之间、决定结果是否取自你配置的取值口径、决定结果表示已办结的记录是否填写了许可证号、表头是否声明了申请人与申请事项、许可事项是否在表内重复登记。

## 实际输出长什么样

![Terminal demo of dsh-permit-report-check: real output over its PR-002 fixture](https://raw.githubusercontent.com/PerryLink/dsh-permit-report-check/main/docs/assets/dsh-permit-report-check-demo.png)

本插件对自己 `PR-002` 测试夹具的**真实输出**，不是示意图。规则库不伪造引文，因此每条发现都会同时写明所引条款，以及该条款原文本次未取得。

## 它回答什么问题

| 你会问 | 它怎么答 |
|---|---|
| 某行的申请材料栏列了材料，已提交材料栏却空着，会被报出吗？ | 会。`PR-001` 要求凡申请材料栏填了内容的行都必须填写 `submittedItems`，提交情况栏为空即报出该行。它读的是台账自己列的申请材料栏，只核对是否记录了提交情况：不拿这份清单与该事项的办事指南比对，也不判断已提交的材料是否齐全、是否符合要求。若没有任何一行填了申请材料，本条进入 `skipped`，而不是静默通过。 |
| 受理日期晚于决定日期，能查出来吗？ | 能。`PR-002` 拿台账自己写的两个日期相比（`acceptedAt` 与 `decidedAt`），同一天视为不晚于，受理晚于决定时逐行报出。它只比较这两个日期：不判断受理是否合法、是否应当受理。解析不了的日期会单独报出，不会静默跳过。 |
| 承诺办结日这一栏是空的会怎样？法定时限那一栏又有没有规则在读？ | `PR-003` 会进入 `skipped`：本插件不内置任何期限天数——法定期限按工作日计算，可依法延长，听证、专家评审等所需时间还可能不计入，唯一可靠的基准就是台账自己写的承诺办结日（`dueAt`）。没有任何规则读法定时限（`legalDays`）栏。`dueAt` 填写后，本条核对决定日期是否落在受理日期与该日之间；命中只表示「与你写在台账里的期限不一致」，不表示已经超期。 |
| 决定结果我填了「补正后准予」，会被接受吗？ | `PR-004` 拿决定结果与你配置的 `values` 取值清单比对，而该清单出厂为空——因此按出厂配置，本条进入 `skipped`，而不是评判你的写法。把本机构实际记录的结果填进 `values`（例如「不予受理」）后，凡不在册的取值都会被报出。本条只核对取值是否在册，不判断该决定是否正确、是否合法。 |
| 某条记录写的是「准予」，许可证号栏却空着。 | `PR-005` 会报出：当决定结果命中准予标记（`conditionValues`，默认为 准予 / 准予许可 / 通过 / 同意 / 已办结 / 批准）时，该记录必须填写许可证号（`certificateNo`）。它只核对证件号是否填写，不判断该证件是否真实有效、是否已送达。台账里没有任何一行命中准予标记时，本条进入 `skipped`。 |
| 同一个许可事项出现在两行里。 | `PR-007` 会报出后出现的那一行，并指出它与哪一行重复，因为同一事项登记两次会让时限核对无从判断。它只核对唯一性，且命中需要人工确认：一个项目同时申请多个事项时，事项名称相同是可能的，此时应在材料名称栏加以区分，而不是简单删除该行。值内部的空白差异会被忽略；台账没有许可事项栏时，本条进入 `skipped`。 |

## 依据的标准

| 文件 | 文号 | 引用它的规则 |
|---|---|---|
| 《中华人民共和国行政许可法》 | 现行版本与条号本次未核实 | PR-001, PR-002, PR-005, PR-006, PR-007 |
| 各事项办事指南与承诺时限（本机构配置） | 无统一标准（本条依据为台账写明的承诺办结日）—— ⚠️ 法定上限见《行政许可法》第四十二条，本条不引用该条 | PR-003 |
| 本机构许可办理管理口径（本机构配置） | 无统一标准（本条依据为本机构配置的结果口径）—— ⚠️ 法定决定类型见《行政许可法》第三十八条，本条不引用该条 | PR-004 |

**Boundary:** this plugin checks an **行政许可办理台账** for the closed loop a register can be held to — that each
application item records its submission, that acceptance does not follow the decision, that the decision falls
between acceptance and the promised completion date, that the decision outcome comes from your vocabulary, that a
grant records its certificate number, that the register names its applicant and matter, and that matters are not
double-registered. It does **not** decide whether a permit decision was lawful, whether the materials were
complete or compliant, whether an application should be accepted, or whether a permit should be granted.

> ### ⚠️ What this plugin deliberately does not judge
>
> **It does not check whether the materials list is complete.** It reads the register's **own** 申请材料 column
> and checks that each listed item records whether it was submitted — **not** whether that list matches the
> matter's service guide. Verifying the list means comparing it against the guide, which this plugin does not do.
>
> **No statutory period is built in — and the statute says why that is the right call.**
> 《中华人民共和国行政许可法》was read verbatim (see `rules/evidence/clause-verification.md`), and three of its
> provisions make a built-in number unusable: **article 82 requires statutory periods to be counted in working
> days, excluding public holidays**; article 42 sets twenty days with a ten-day extension (forty-five plus
> fifteen for joint handling); and article 45 excludes time needed for hearings, testing, inspection and expert
> review from the period altogether. A register normally records calendar dates, so `PR-003` compares the decision
> date against the **promised completion date written in the register**, and reports itself in `skipped` when that
> column is empty. A finding means "this disagrees with the deadline you recorded", never "this was late".
>
> ⚠️ **The text read was the 2003 promulgation**; a 2019 amendment exists and **was not obtained**, so the pack
> keeps the note 「现行版本与条号本次未核实」 on every rule and claims no article is current law.
>
> **The outcome vocabulary ships empty.** Wording for grants, refusals and terminations varies by institution
> and matter, so `PR-004` reports itself in `skipped` until you configure it, and `PR-005` (which requires a
> certificate number once a grant is recorded) uses a configurable set of grant marker values rather than a
> built-in list.
>
> **Every `excerpt` in the rule pack says, in so many words, that the clause text was not obtained.** The
> regime lives in 《中华人民共和国行政许可法》 and in each matter's service guide. The verification pass could
> not retrieve verbatim clause text, so the pack states the gap in the `excerpt` field itself and keeps every
> rule at `warn` or `info`. **When the texts are in hand, replace each `excerpt` with the real clause and
> raise `kind` to `direct`.**

## Compatibility

| 项目 | 状态 |
|---|---|
| Harness | 对等版本范围 `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` —— 已实测同时接受 `0.2.0-rc.2` 与 `0.2.1-alpha.1`。**刻意不声明 `engines.dsh`**：它没有任何读取者，也无法拒装任何宿主 |
| Node | `^22.19.0 || >=24.0.0` |
| 平台 | 全平台（纯 ESM；无原生代码、无联网、不调用模型） |
| 工具模式 | `native` / `ptc` / `both` 均可；批量校验整个目录时建议 `ptc`，schema 成本只付一次 |

## What it does

规则表、字段说明与行为细节见 [README.md](README.md#what-it-does)（英文主版本）。本插件只列出材料与所引条款之间的字面差异，并对无法执行的检查在 `skipped` 中逐项说明。

## Install

```sh
dsh plugin --profile <name> add dsh-permit-report-check
dsh --profile <name> --dump-config | grep 'dsh-permit-report-check'
```

## Configuration

全部可调参数都在 `src/config.ts` 的 Schemastery schema 中，只改 `cordis.yml` 即可生效，无需改代码；逐条阈值在 `rules/` 下的规则库文件里。

| 键 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `rulesFile` | string | `rules/permit-report-check.yaml` | 规则库文件路径，相对插件包根目录 |
| `disabledRules` | string[] | `[]` | 要停用的规则 id 列表；每条都会出现在 `skipped` 中 |
| `onlyRules` | string[] | `[]` | 只执行这些规则 id；留空表示执行全部规则 |
| `skipNotes` | string | `""` | 附加到每条 `skipped` 说明后的备注 |
| `timeoutMs` | number | `120000` | 工具协作式超时预算（毫秒） |

## Material format

支持 JSON 与 YAML。完整字段示例见 [README.md](README.md#material-format)（英文主版本）。字段在读取层是可选的，由检查引擎校验，因此部分导出的材料会产生"缺项"类差异，而不是让程序崩溃。

## Rule sources

规则数据与代码分离，每条规则都带文件名、文号、按原文自身编号体系的条款号、逐字摘录与来源地址。加载期强制：摘录必须是真实引文且不少于八个字符；依据仅为原则性条款（`kind: derived-from-principle`，严重级上限 `warn`）或本机构配置（`kind: institutional-configuration`，上限 `info`）的检查不得标为 `error`。夸大依据的规则库会在加载期失败，而不会产出一份看起来很有底气的报告。

核验中确认的边界与"刻意没有作出的结论"见 [README.md](README.md#rule-sources)（英文主版本）与随包的 `rules/evidence/` 目录。

## Troubleshooting

- **插件装上了但工具不出现**：确认 `main` 指向 `lib/index.mjs` 且 `pnpm run build` 已生成该文件；`main` 写错会让加载器静默跳过该条目。
- **`dsh plugin add` 报版本不兼容**：peer 范围覆盖 `0.1.x` 与 `0.2.x`；若运行时在其之外，可显式豁免：`dsh plugin --profile <name> allow-version <包名@版本> --dsh-version <runtime> --accept-risk`
- **某条规则没有执行**：查看 `skipped` 数组，其中写明了规则 id 与原因。
- **`check` 报 `manifest-peers` 失败**：静态检查器比对的是一份早于 0.2 世代的硬编码 peer 范围；安装期的 peer 校验以运行时为准。这是 `dsh-plugin-dev` 的已知上游问题。
- **时间看起来偏移**：全部计算都是对输入字符串做墙上时钟运算，不做时区换算。

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-permit-report-check
```

第 4 项把 `../_shared` 的共享件同步进 `src/shared/`；每次改动共享件后都要重跑。

## License

[Apache License 2.0](LICENSE) © 2026 dsh-permit-report-check contributors.
