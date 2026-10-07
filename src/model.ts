/**
 * dsh-permit-report-check — table shape and material contract.
 *
 * The plugin is data-only: this file declares which columns the material may use
 * and how they map onto canonical field names; the shared kit supplies the reader
 * and the check engine, and the rule pack declares every check. Adding a check
 * that fits an existing kind is a rule-pack edit, not a code change.
 */

import { canonicaliseRow, parseTable, type TableSpec } from './shared/table.ts'
import { runTableCheck, type TableCheckOptions, type TableInput } from './shared/rows.ts'
import type { Ruleset } from './shared/rules.ts'

/** Tool id exposed to the model, and the row id in `cordis.patch.yml`. */
export const TOOL_NAME = 'permit_report_check'

/** The register's column aliases, declared once so both the spec and the guard see them. */
const COLUMNS = {
  reportNo: ['序号', '报告编号', '编号', 'reportNo'],
  permitType: ['许可事项', '许可类型', '事项', 'permitType'],
  issuingAuthority: ['许可机关', '审批机关', '发证机关', 'issuingAuthority'],
  legalBasis: ['法定依据', '法律依据', '依据', 'legalBasis'],
  requiredItems: ['申请材料', '材料清单', '提交材料', 'requiredItems'],
  submittedItems: ['已提交材料', '提交情况', '实交材料', 'submittedItems'],
  acceptedAt: ['受理日期', '收件日期', 'acceptedAt'],
  legalDays: ['法定时限', '法定期限天数', 'legalDays'],
  dueAt: ['承诺办结日', '应办结日期', 'dueAt'],
  decidedAt: ['决定日期', '办结日期', 'decidedAt'],
  decision: ['决定结果', '办理结果', '决定', 'decision'],
  certificateNo: ['许可证号', '批文号', '证件编号', 'certificateNo'],
  handler: ['承办人', '经办人', 'handler'],
} as const

/** How the material declares its table. */
export const SPEC: TableSpec = {
  rowKeys: ['rows', 'items', 'reports', '报告'],
  columns: COLUMNS,
  header: {
  applicant: ['applicant', '申请人', '申请单位'],
  matter: ['matter', '申请事项', '项目名称'],
  window: ['window', '受理窗口', '办理窗口'],
  checkedAt: ['checkedAt', '核对日期'],
  },
}

/** Fields the material must carry somewhere for the reader to accept it. */
export const REQUIRE_ANY_OF = [
  '许可事项',
  'permitType',
  '申请材料',
  'requiredItems',
  '决定结果',
  'decision',
  '报告编号',
  'reportNo',
]

/**
 * Parse the material and attach its canonical field names.
 * @param source - JSON or YAML text.
 * @param target - description of where the material came from.
 * @returns the normalized table, with each row's aliases resolved to field names.
 */
export function parseMaterial(source: string, target: string): TableInput {
  const table = parseTable(source, target, {
    ...SPEC,
    ...(REQUIRE_ANY_OF === undefined ? {} : { requireAnyOf: REQUIRE_ANY_OF }),
  })
  for (const row of table.rows) canonicaliseRow(row, SPEC)
  return table
}

/**
 * Run the rule pack against the material.
 * @param input - normalized table.
 * @param ruleset - validated rule pack.
 * @param options - plugin identity, clock value, rule selection and overrides.
 * @returns the report.
 */
export function runCheck(input: TableInput, ruleset: Ruleset, options: TableCheckOptions) {
  return runTableCheck(input, ruleset, options)
}

export type { TableCheckOptions, TableInput }
