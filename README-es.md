# dsh-permit-report-check — Comprobación de completitud y coherencia de fechas del registro de solicitudes de autorización administrativa

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-permit-report-check` lee un registro de tramitación de autorizaciones administrativas (行政许可办理台账) —la cabecera del solicitante más una fila por solicitud— y comprueba el cierre y la coherencia interna de ese registro: que cada partida enumerada en la columna 申请材料 registre si se presentó, que la 受理日期 no sea posterior a la 决定日期, que la 决定日期 quede entre la 受理日期 y la 承诺办结日 que el propio registro indica, que la 决定结果 proceda del repertorio de valores que usted configure, que un registro cuya 决定结果 indique concesión lleve su 许可证号, que la cabecera declare 申请人 y 申请事项, y que ningún 许可事项 quede registrado dos veces en la tabla.

## Cómo se ve la salida

![Terminal demo of dsh-permit-report-check: real output over its PR-002 fixture](https://raw.githubusercontent.com/PerryLink/dsh-permit-report-check/main/docs/assets/dsh-permit-report-check-demo.png)

Salida real de este plugin sobre su propio fixture de prueba `PR-002` — no es un montaje. El paquete de reglas no inventa citas, así que cada hallazgo nombra la cláusula aplicada y advierte que su texto no se obtuvo.

## Qué responde

| Usted pregunta | Qué responde |
|---|---|
| Una fila enumera materiales en 申请材料, pero 已提交材料 está vacía, ¿se informa de ello? | Sí. `PR-001` exige un valor `submittedItems` en toda fila cuya celda 申请材料 esté rellena y señala la fila cuando la columna de presentación está vacía. Lee la columna de materiales del propio registro y comprueba solo si la presentación queda registrada: no compara esa lista con la guía de servicio del trámite ni juzga si los materiales presentados están completos o son conformes. Si ninguna fila tiene 申请材料 relleno, la regla pasa a `skipped`. |
| La 受理日期 es posterior a la 决定日期, ¿se detecta? | Sí. `PR-002` compara las dos fechas que el propio registro contiene, `acceptedAt` frente a `decidedAt`, considera que el mismo día no es posterior y señala la fila en la que la aceptación va después de la decisión. Solo compara esas dos fechas: no juzga si la aceptación fue legal ni si la solicitud debía aceptarse. Una fecha que no puede analizar se informa como hallazgo propio, no se omite en silencio. |
| ¿Qué ocurre si la columna 承诺办结日 está vacía, y hay alguna regla que lea la columna 法定时限? | `PR-003` pasa a `skipped`: no hay ningún cómputo de días incorporado, porque los plazos legales se cuentan en días hábiles, pueden prorrogarse y pueden excluir el tiempo de audiencia o de dictamen pericial, de modo que la única referencia es la 承诺办结日 (`dueAt`) que el registro declara. Ninguna regla lee la columna 法定时限 (`legalDays`). Con `dueAt` relleno, la regla comprueba que la 决定日期 quede entre la 受理日期 y esa fecha; un hallazgo significa que la decisión no concuerda con el plazo que usted registró, nunca que haya habido retraso. |
| He escrito 补正后准予 en 决定结果. ¿Se acepta? | `PR-004` contrasta la 决定结果 con el repertorio de su parámetro `values`, y ese parámetro viene vacío: tal como se entrega, la regla pasa a `skipped` en lugar de enjuiciar su redacción. Rellene `values` con los resultados que registra su institución (por ejemplo 不予受理) y se informará de cualquier valor que no figure en la lista. La regla solo comprueba si el valor está en la lista; no juzga si la decisión es correcta o legal. |
| Una fila dice 准予, pero la columna 许可证号 está vacía. | `PR-005` lo informa: cuando la 决定结果 coincide con un marcador de concesión —`conditionValues`, por defecto 准予 / 准予许可 / 通过 / 同意 / 已办结 / 批准— la fila debe llevar su 许可证号 (`certificateNo`). Solo comprueba que el número esté relleno, no que el certificado sea auténtico, válido o esté notificado. Si ninguna fila coincide con un marcador de concesión, la regla pasa a `skipped`. |
| El mismo 许可事项 aparece en dos filas. | `PR-007` informa de la fila posterior y nombra la fila con la que se duplica, porque dos registros de un mismo asunto hacen ambiguo el control de plazos. Solo comprueba la unicidad, y un hallazgo requiere confirmación humana: un proyecto que solicita varios asuntos puede coincidir legítimamente, así que distíngalo en la columna de materiales en lugar de borrar la fila. Las diferencias de espacios se ignoran; sin columna 许可事项, la regla pasa a `skipped`. |

## Normas que sigue

| Documento | Número | Reglas que lo citan |
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

| Superficie | Estado |
|---|---|
| Harness | Rango de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificado para aceptar tanto `0.2.0-rc.2` como `0.2.1-alpha.1`. **No se declara `engines.dsh`**: no tiene lector y no puede rechazar ningún host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sin código nativo, sin red, sin llamada al modelo) |
| Modo de herramienta | Funciona en `native`, `ptc` y `both`; para un directorio completo use `ptc` |

## What it does

La tabla de reglas, los campos y el comportamiento detallado están en [README.md](README.md#what-it-does) (versión principal en inglés). El plugin sólo enumera divergencias literales frente a las cláusulas citadas e indica en `skipped` cada comprobación que no pudo ejecutarse.

## Install

```sh
dsh plugin --profile <name> add dsh-permit-report-check
dsh --profile <name> --dump-config | grep 'dsh-permit-report-check'
```

## Configuration

Todos los parámetros ajustables viven en el esquema Schemastery de `src/config.ts`, por lo que se cambian desde `cordis.yml` sin tocar el código; los umbrales por regla están en el paquete de reglas bajo `rules/`.

| Clave | Tipo | Predeterminado | Descripción |
|---|---|---|---|
| `rulesFile` | string | `rules/permit-report-check.yaml` | Ruta del paquete de reglas, relativa a la raíz del paquete |
| `disabledRules` | string[] | `[]` | Ids de reglas que se dejan de ejecutar; cada una aparece en `skipped` |
| `onlyRules` | string[] | `[]` | Ejecutar solo estas reglas; vacío ejecuta todas |
| `skipNotes` | string | `""` | Nota añadida a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Presupuesto de tiempo de espera cooperativo de la herramienta |

## Material format

Acepta JSON o YAML. El ejemplo completo de campos está en [README.md](README.md#material-format) (versión principal en inglés). Los campos son opcionales en la capa de lectura y los valida el motor, de modo que una exportación parcial produce hallazgos sobre lo que falta en lugar de un fallo.

## Rule sources

Los datos de las reglas están separados del código: cada regla lleva documento, número, cláusula en la numeración propia de la fuente, extracto literal y URL de origen. El cargador impone que el extracto sea una cita real de al menos ocho caracteres y que una comprobación basada sólo en un principio general (`kind: derived-from-principle`, tope `warn`) o en una política local (`kind: institutional-configuration`, tope `info`) nunca se declare `error`.

Los límites verificados y las conclusiones deliberadamente **no** afirmadas están en [README.md](README.md#rule-sources) (versión principal en inglés) y en `rules/evidence/`.

## Troubleshooting

- **El plugin se instala pero la herramienta no aparece**: compruebe que `main` resuelve a `lib/index.mjs` y que `pnpm run build` lo generó.
- **`dsh plugin add` rechaza el paquete**: la faixa de peers cubre `0.1.x` y `0.2.x`; fuera de ella, conceda una exención explícita con `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Una regla no se ejecutó**: lea el arreglo `skipped`.
- **`check` informa `manifest-peers` como fallo**: es un problema conocido de `dsh-plugin-dev`; el runtime aplica la compatibilidad al instalar.
- **Los horarios parecen desplazados**: toda la aritmética es de hora local sobre las cadenas entregadas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-permit-report-check
```

El último comando copia el kit compartido de `../_shared` a `src/shared/`; vuelva a ejecutarlo tras cada cambio compartido.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-permit-report-check contributors.
