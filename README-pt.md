# dsh-permit-report-check — Verificação de completude e coerência de datas do registo de pedidos de autorização administrativa

`dsh-permit-report-check` lê um registo de tramitação de autorizações administrativas (行政许可办理台账) —o cabeçalho do requerente mais uma linha por pedido— e verifica o fecho e a coerência interna desse registo: que cada item listado na coluna 申请材料 registe se foi entregue, que a 受理日期 não seja posterior à 决定日期, que a 决定日期 fique entre a 受理日期 e a 承诺办结日 que o próprio registo indica, que a 决定结果 venha do repertório de valores que configurar, que um registo cuja 决定结果 indique deferimento traga o seu 许可证号, que o cabeçalho declare 申请人 e 申请事项, e que nenhum 许可事项 fique registado duas vezes na tabela.

## O que ele responde

| Você pergunta | O que ele responde |
|---|---|
| Uma linha lista materiais em 申请材料, mas 已提交材料 está vazia — isso é reportado? | Sim. `PR-001` exige um valor `submittedItems` em todas as linhas cuja célula 申请材料 esteja preenchida e assinala a linha quando a coluna de entrega está vazia. Lê a coluna de materiais do próprio registo e verifica apenas se a entrega ficou registada: não compara essa lista com o guia de serviço do pedido nem julga se os materiais entregues estão completos ou são conformes. Se nenhuma linha tiver 申请材料 preenchido, a regra passa a `skipped`. |
| A 受理日期 é posterior à 决定日期 — isso é detetado? | Sim. `PR-002` compara as duas datas que o próprio registo contém, `acceptedAt` com `decidedAt`, considera que o mesmo dia não é posterior e assinala a linha em que a aceitação vem depois da decisão. Compara apenas essas duas datas: não julga se a aceitação foi legal nem se o pedido devia ser aceite. Uma data que não consegue analisar é reportada como achado próprio, não é ignorada em silêncio. |
| O que acontece se a coluna 承诺办结日 estiver vazia — e há alguma regra que leia a coluna 法定时限? | `PR-003` passa a `skipped`: não há qualquer contagem de dias incorporada, porque os prazos legais contam-se em dias úteis, podem ser prorrogados e podem excluir o tempo de audiência ou de parecer técnico, pelo que a única referência é a 承诺办结日 (`dueAt`) que o registo declara. Nenhuma regra lê a coluna 法定时限 (`legalDays`). Com `dueAt` preenchido, a regra verifica se a 决定日期 fica entre a 受理日期 e essa data; um achado significa que a decisão não concorda com o prazo que registou, nunca que tenha havido atraso. |
| Escrevi 补正后准予 em 决定结果. Isso é aceite? | `PR-004` confronta a 决定结果 com o repertório do seu parâmetro `values`, e esse parâmetro vem vazio — tal como é entregue, a regra passa a `skipped` em vez de julgar a sua redação. Preencha `values` com os resultados que a sua instituição regista (por exemplo 不予受理) e qualquer valor fora da lista é reportado. A regra verifica apenas se o valor consta da lista; não julga se a decisão está correta ou é legal. |
| Uma linha diz 准予, mas a coluna 许可证号 está vazia. | `PR-005` reporta-a: quando a 决定结果 coincide com um marcador de deferimento —`conditionValues`, por omissão 准予 / 准予许可 / 通过 / 同意 / 已办结 / 批准— a linha tem de trazer o seu 许可证号 (`certificateNo`). Verifica apenas se o número está preenchido, não se o certificado é autêntico, válido ou foi notificado. Se nenhuma linha coincidir com um marcador de deferimento, a regra passa a `skipped`. |
| O mesmo 许可事项 aparece em duas linhas. | `PR-007` reporta a linha posterior e indica a linha com que se repete, porque dois registos do mesmo assunto tornam ambíguo o controlo de prazos. Verifica apenas a unicidade, e um achado exige confirmação humana: um projeto que pede vários assuntos pode coincidir legitimamente, pelo que deve distingui-lo na coluna de materiais em vez de apagar a linha. As diferenças de espaços são ignoradas; sem coluna 许可事项, a regra passa a `skipped`. |

## Normas que segue

| Documento | Número | Regras que o citam |
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

| Superfície | Estado |
|---|---|
| Harness | Faixa de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificada para aceitar tanto `0.2.0-rc.2` quanto `0.2.1-alpha.1`. **`engines.dsh` não é declarado**: não tem leitor e não pode recusar nenhum host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sem código nativo, sem rede, sem chamada ao modelo) |
| Modo de ferramenta | Funciona em `native`, `ptc` e `both`; para um diretório inteiro use `ptc` |

## What it does

A tabela de regras, os campos e o comportamento detalhado estão em [README.md](README.md#what-it-does) (versão principal em inglês). O plugin apenas lista divergências literais frente às cláusulas citadas e indica em `skipped` cada verificação que não pôde ser executada.

## Install

```sh
dsh plugin --profile <name> add dsh-permit-report-check
dsh --profile <name> --dump-config | grep 'dsh-permit-report-check'
```

## Configuration

Todos os parâmetros ajustáveis ficam no esquema Schemastery de `src/config.ts`, portanto mudam pelo `cordis.yml` sem editar código; os limites por regra ficam no pacote de regras sob `rules/`.

| Chave | Tipo | Padrão | Descrição |
|---|---|---|---|
| `rulesFile` | string | `rules/permit-report-check.yaml` | Caminho do pacote de regras, relativo à raiz do pacote |
| `disabledRules` | string[] | `[]` | Ids de regras a desativar; cada uma aparece em `skipped` |
| `onlyRules` | string[] | `[]` | Executar apenas estas regras; vazio executa todas |
| `skipNotes` | string | `""` | Nota acrescentada a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Orçamento de tempo limite cooperativo da ferramenta |

## Material format

Aceita JSON ou YAML. O exemplo completo de campos está em [README.md](README.md#material-format) (versão principal em inglês). Os campos são opcionais na camada de leitura e validados pelo motor, de modo que uma exportação parcial gera achados sobre o que falta em vez de falhar.

## Rule sources

Os dados das regras ficam separados do código: cada regra traz documento, número, cláusula na numeração própria da fonte, trecho literal e URL de origem. O carregador impõe que o trecho seja citação real de pelo menos oito caracteres e que uma verificação baseada apenas em princípio geral (`kind: derived-from-principle`, teto `warn`) ou em política local (`kind: institutional-configuration`, teto `info`) nunca seja declarada `error`.

Os limites verificados e as conclusões deliberadamente **não** afirmadas estão em [README.md](README.md#rule-sources) (versão principal em inglês) e em `rules/evidence/`.

## Troubleshooting

- **O plugin instala mas a ferramenta não aparece**: confirme que `main` resolve para `lib/index.mjs` e que `pnpm run build` o gerou.
- **`dsh plugin add` recusa o pacote**: a faixa de peers cobre `0.1.x` e `0.2.x`; fora dela, conceda isenção explícita com `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Uma regra não executou**: leia o arranjo `skipped`.
- **`check` informa `manifest-peers` como falha**: problema conhecido do `dsh-plugin-dev`; o runtime aplica a compatibilidade na instalação.
- **Os horários parecem deslocados**: toda a aritmética é de hora local sobre as cadeias fornecidas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-permit-report-check
```

O último comando copia o kit compartilhado de `../_shared` para `src/shared/`; execute-o novamente após cada alteração compartilhada.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-permit-report-check contributors.
