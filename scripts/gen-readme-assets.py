#!/usr/bin/env python3
"""Generate the README visuals for dsh-permit-report-check.

Outputs (idempotent overwrite, all under docs/assets/):
  dsh-permit-report-check-hero-{zh,en}-{light,dark}.webp   1440x576, Pillow
  dsh-permit-report-check-flow-v5-{light,dark}.svg          1100x660, hand-written

Hero right panel: one real ledger row lifted onto a *proportional* date axis
(accepted 2026-03-02 -> decided 2026-04-20 -> promised due 2026-04-30), then the
three outcomes that row really produces: PR-001 -> issues[] (warn), PR-004 ->
skipped[] (values unset), PR-005 ran clean; PR-002/003/006/007 ran clean.
Counts are samples/quickstart/expected/result.json: error 0 / warn 1 / info 0,
issueCount 1, skippedCount 1. No invented data.

Flow grammar (1100x660): a tri-state dispatch board, not a five-node chain.
  left column   input -> alias normalisation -> config gates
  centre         the seven-rule pack, one row per rule, severity + fields read
  right         three exits: issues[] | skipped[] | ran-and-found-nothing
  bottom        the one report the two named channels converge on, plus the
                human boundary and the evidence cap
Every label is a real token or reason string from src/shared/rows.ts and
rules/permit-report-check.yaml.

Run: python scripts/gen-readme-assets.py
Requires: Pillow (hero), msyh.ttc / msyhbd.ttc / consola.ttf / consolab.ttf.
"""
from __future__ import annotations

import math
import os
import sys
from datetime import date

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")
NAME = "dsh-permit-report-check"

# ---------------------------------------------------------------------------
# fonts: fail loudly rather than render tofu boxes
# ---------------------------------------------------------------------------
FONTS = {
    "cjk": r"C:\Windows\Fonts\msyh.ttc",
    "cjk_bold": r"C:\Windows\Fonts\msyhbd.ttc",
    "mono": r"C:\Windows\Fonts\consola.ttf",
    "mono_bold": r"C:\Windows\Fonts\consolab.ttf",
}
for kind, path in FONTS.items():
    if not os.path.exists(path):
        sys.exit(f"FATAL: missing font {kind}: {path}")

_MEASURE = ImageDraw.Draw(Image.new("RGB", (8, 8)))
_CACHE: dict[tuple[str, float], ImageFont.FreeTypeFont] = {}


def font(size: float, kind: str = "cjk") -> ImageFont.FreeTypeFont:
    key = (kind, round(size, 2))
    if key not in _CACHE:
        _CACHE[key] = ImageFont.truetype(FONTS[kind], int(round(size)))
    return _CACHE[key]


def measure(text: str, size: float, kind: str = "cjk") -> float:
    return _MEASURE.textlength(text, font=font(size, kind))


def require_w(text: str, size: float, kind: str, max_w: float, what: str) -> None:
    width = measure(text, size, kind)
    if width > max_w:
        raise SystemExit(f"FATAL: {what} overflows: {width:.1f}px > {max_w:.1f}px: {text!r}")


def fit(text: str, kind: str, max_w: float, start: float, floor: float) -> float:
    size = start
    while size > floor and measure(text, size, kind) > max_w:
        size -= 0.5
    require_w(text, size, kind, max_w, "fitted text")
    return size


def fit_lines(lines: list[str], kind: str, max_w: float, start: float, floor: float) -> float:
    size = start
    while size > floor and any(measure(line, size, kind) > max_w for line in lines):
        size -= 0.5
    for line in lines:
        require_w(line, size, kind, max_w, "fitted title line")
    return size


# ---------------------------------------------------------------------------
# palettes
# ---------------------------------------------------------------------------
SKIN = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        card="#ffffff", band="#f4f1fb", edge="#e6e2ef", grid="#ece8f5",
        text="#141419", sub="#4d5261", faint="#8f94a4", rule="#4B67B4",
        accent="#4B67B4", accent_soft="#ece7f9",
        warn="#b45309", warn_bg="#fbf1e4",
        skip="#6b5aa8", skip_bg="#f0ecfa",
        ok="#2f855a", ok_bg="#e8f4ec",
        shadow="#2b2440", shadow_alpha=34,
        glow_alpha=26, line_alpha=8, dots="#cfc8e2",
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        card="#182032", band="#1e2941", edge="#2c3852", grid="#26324a",
        text="#f2f4fb", sub="#b7c0d4", faint="#8b96ad", rule="#8496f5",
        accent="#8496f5", accent_soft="#242f4e",
        warn="#f0b35e", warn_bg="#3a2c1c",
        skip="#b8a6f0", skip_bg="#2a2747",
        ok="#6ddba0", ok_bg="#1e3329",
        shadow="#000000", shadow_alpha=120,
        glow_alpha=38, line_alpha=10, dots="#2b3856",
    ),
}


def hx(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))  # type: ignore[return-value]


def gradient(w: int, h: int, top: str, bottom: str) -> Image.Image:
    base = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(base)
    first, last = hx(top), hx(bottom)
    for y in range(h):
        f = y / max(1, h - 1)
        draw.line([(0, y), (w, y)], fill=tuple(int(first[i] + (last[i] - first[i]) * f) for i in range(3)))
    return base.convert("RGBA")


def glow(img: Image.Image, cx: float, cy: float, r: float, color: str, alpha: int) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hx(color) + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(r * 0.55))
    img.alpha_composite(layer)
    return img


def ledger_rules(img: Image.Image, s: dict, step: int = 38, x0: int = 596, alpha: int = 9) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for y in range(58, img.height, step):
        draw.line([(x0, y), (img.width - 20, y)], fill=hx(s["rule"]) + (alpha,), width=1)
    layer = layer.filter(ImageFilter.GaussianBlur(0.4))
    img.alpha_composite(layer)
    return img


def card(img: Image.Image, box: tuple[int, int, int, int], s: dict,
         radius: int = 20, shadow: int = 22, fill: str | None = None,
         border: str | None = None) -> Image.Image:
    x0, y0, x1, y1 = box
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.rounded_rectangle([x0 + 2, y0 + max(4, shadow // 2), x1 + 2, y1 + max(5, shadow // 2)],
                           radius=radius, fill=hx(s["shadow"]) + (s["shadow_alpha"],))
    layer = layer.filter(ImageFilter.GaussianBlur(shadow / 2))
    img.alpha_composite(layer)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(box, radius=radius, fill=hx(fill or s["card"]),
                           outline=hx(border or s["edge"]), width=1)
    return img


def pill(img: Image.Image, xy: tuple[float, float], text: str, s: dict, size: float = 17,
         fg: str | None = None, bg: str | None = None, pad: float = 18,
         kind: str = "cjk_bold") -> float:
    x, y = xy
    height = size + 19
    width = measure(text, size, kind) + pad * 2
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([x, y, x + width, y + height], radius=height / 2, fill=hx(bg or s["accent_soft"]))
    draw.text((x + pad, y + height / 2), text, font=font(size, kind), fill=hx(fg or s["accent"]), anchor="lm")
    return width


def chip_right(img: Image.Image, right: float, y: float, text: str, fg: str, bg: str,
               size: float = 12, height: float = 24, kind: str = "cjk_bold") -> float:
    width = measure(text, size, kind) + 20
    x = right - width
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([x, y, right, y + height], radius=height / 2, fill=hx(bg))
    draw.text((x + 10, y + height / 2), text, font=font(size, kind), fill=hx(fg), anchor="lm")
    return x


def chip(img: Image.Image, x: float, y: float, text: str, s: dict, size: float = 11.5,
         height: float = 24, fg: str | None = None, bg: str | None = None,
         border: str | None = None, kind: str = "mono") -> float:
    width = measure(text, size, kind) + 18
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([x, y, x + width, y + height], radius=height / 2,
                           fill=hx(bg or s["band"]), outline=hx(border or s["edge"]), width=1)
    draw.text((x + 9, y + height / 2), text, font=font(size, kind), fill=hx(fg or s["sub"]), anchor="lm")
    return width


def check_badge(img: Image.Image, cx: float, cy: float, r: float, fg: str, bg: str) -> None:
    draw = ImageDraw.Draw(img)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hx(bg))
    draw.line([(cx - r * 0.44, cy + r * 0.02), (cx - r * 0.08, cy + r * 0.38), (cx + r * 0.48, cy - r * 0.34)],
              fill=hx(fg), width=max(2, int(round(r * 0.34))), joint="curve")


def rich_line(img: Image.Image, x: float, y: float, runs: list[tuple[str, str, str]], size: float) -> float:
    draw = ImageDraw.Draw(img)
    cursor = x
    for text, color, kind in runs:
        draw.text((cursor, y), text, font=font(size, kind), fill=hx(color), anchor="ls")
        cursor += measure(text, size, kind)
    return cursor


# ---------------------------------------------------------------------------
# hero copy — every figure below is real (see the module docstring)
# ---------------------------------------------------------------------------
HERO = {
    "zh": dict(
        kicker="DeepSeek Harness 插件 · 行政许可台账核对",
        title=["dsh-permit-", "report-check"],
        value=["把许可台账逐行核一遍，", "哪一行、哪一栏、差什么，列清。"],
        sub="日期、提交、证件号只报差异；许可决定交给人。",
        meta=[("permit_report_check", "accent", "mono_bold"),
              (" · ", "faint", "mono"),
              ("7 条规则", "faint", "cjk"),
              (" · PR-001..PR-007", "faint", "mono")],
        foot="Apache-2.0 · 只读材料 · 不联网 · 不调用模型 · 不写文件",
        card_title=("rows[0]", "台账第 1 行"),
        card_sub_label="样例",
        card_sub_path="samples/quickstart/input/PR-001-unsafe.json",
        chip_warn="warn 1",
        chip_skip="skipped 1",
        section="日期闭环 · 一条申请记录",
        section_right="PR-002 · PR-003",
        p3="PR-003 决定落在受理日与承诺办结日之间 · 早 10 天",
        accepted="受理 2026-03-02",
        decided="决定 2026-04-20",
        due="承诺办结日 2026-04-30",
        p2="PR-002 受理 ≤ 决定 · 49 天",
        row1=("PR-001", "已提交材料（空）", "warn · issues[]",
              "申请材料有值，submittedItems 为空"),
        row2=("PR-004", "决定结果 values = []", "skipped",
              "本机构口径未配置 → 本条不执行"),
        row3=("PR-005", "许可证号 某环审〔2026〕18 号", "未命中",
              "准予标记命中 → certificateNo 已填写"),
        quiet="已跑·未命中",
        quiet_right="两栏都不进",
        summary="error 0 · warn 1 · info 0",
        summary_right="issueCount 1 · skippedCount 1 · ruleset 2026.1",
    ),
    "en": dict(
        kicker="DEEPSEEK HARNESS PLUGIN · PERMIT LEDGER CHECK",
        title=["dsh-permit-", "report-check"],
        value=["Check a permit ledger row by row —", "name the row, the field, the gap."],
        sub="Differences only; the decision stays human.",
        meta=[("permit_report_check", "accent", "mono_bold"),
              (" · 7 rules · PR-001..PR-007", "faint", "mono")],
        foot="Apache-2.0 · read-only · no network · no model calls · no file writes",
        card_title=("rows[0]", "ledger row 1"),
        card_sub_label="sample",
        card_sub_path="samples/quickstart/input/PR-001-unsafe.json",
        chip_warn="warn 1",
        chip_skip="skipped 1",
        section="date loop · one ledger row",
        section_right="PR-002 · PR-003",
        p3="PR-003 decision inside acceptance → promised due · 10 days early",
        accepted="accepted 2026-03-02",
        decided="decided 2026-04-20",
        due="promised due 2026-04-30",
        p2="PR-002 accepted ≤ decided · 49 days",
        row1=("PR-001", "submitted items (blank)", "warn · issues[]",
              "requiredItems has a value, submittedItems is empty"),
        row2=("PR-004", "decision values = []", "skipped",
              "institution vocabulary unset → this check does not run"),
        row3=("PR-005", "cert. no. 某环审〔2026〕18 号", "no hit",
              "grant marker matched → certificateNo filled"),
        quiet="ran · no hit",
        quiet_right="neither list",
        summary="error 0 · warn 1 · info 0",
        summary_right="issueCount 1 · skippedCount 1 · ruleset 2026.1",
    ),
}

# proportional date axis: 2026-03-02 -> 2026-04-20 -> 2026-04-30
ACCEPTED = date(2026, 3, 2)
DECIDED = date(2026, 4, 20)
DUE = date(2026, 4, 30)
DECIDED_FRAC = (DECIDED - ACCEPTED).days / (DUE - ACCEPTED).days


def hero(lang: str, skin: str) -> None:
    s, h = SKIN[skin], HERO[lang]
    W, H = 1440, 576
    img = gradient(W, H, s["bg_from"], s["bg_to"])
    img = ledger_rules(img, s, alpha=s["line_alpha"])
    img = glow(img, 1180, 10, 380, s["accent"], s["glow_alpha"])
    img = glow(img, 140, 580, 300, s["accent"], max(8, s["glow_alpha"] // 3))

    # ---- left copy column ---------------------------------------------------
    m, col_w = 64, 556
    pill(img, (m, 44), h["kicker"], s, size=18)
    d = ImageDraw.Draw(img)

    title_size = fit_lines(list(h["title"]), "cjk_bold", col_w, 92, 76)
    baseline_one = 176
    baseline_two = baseline_one + int(round(title_size * 1.04))
    d.text((m - 2, baseline_one), h["title"][0], font=font(title_size, "cjk_bold"),
           fill=hx(s["text"]), anchor="ls")
    d.text((m - 2, baseline_two), h["title"][1], font=font(title_size, "cjk_bold"),
           fill=hx(s["accent"]), anchor="ls")

    value_size = fit_lines(list(h["value"]), "cjk_bold", col_w, 34, 27)
    for index, line in enumerate(h["value"]):
        d.text((m, 322 + index * 42), line, font=font(value_size, "cjk_bold"),
               fill=hx(s["text"]), anchor="ls")

    sub_size = fit(h["sub"], "cjk", col_w, 25, 20)
    d.text((m, 406), h["sub"], font=font(sub_size, "cjk"), fill=hx(s["sub"]), anchor="ls")

    meta_runs = [(text, s[color], kind) for text, color, kind in h["meta"]]
    meta_end = rich_line(img, m + 1, 450, meta_runs, 20)
    if meta_end > m + col_w:
        raise SystemExit(f"FATAL: hero meta overflows ({meta_end:.0f}px)")

    d = ImageDraw.Draw(img)
    d.line([m + 1, 474, m + col_w - 2, 474], fill=hx(s["grid"]), width=2)
    foot_size = fit(h["foot"], "cjk", col_w, 16, 13)
    d.text((m + 1, 502), h["foot"], font=font(foot_size, "cjk"), fill=hx(s["faint"]), anchor="ls")

    # ---- right panel: one row on a proportional date axis -------------------
    cx0, cy0, cx1, cy1 = 664, 40, 1392, 536
    img = card(img, (cx0, cy0, cx1, cy1), s, radius=22, shadow=28)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([cx0, cy0, cx1, cy0 + 78], radius=22, fill=hx(s["band"]))
    d.rectangle([cx0, cy0 + 56, cx1, cy0 + 78], fill=hx(s["band"]))
    d.line([cx0, cy0 + 78, cx1, cy0 + 78], fill=hx(s["edge"]), width=1)

    d.text((cx0 + 28, cy0 + 42), h["card_title"][0], font=font(25, "mono_bold"),
           fill=hx(s["text"]), anchor="ls")
    title_w = measure(h["card_title"][0], 25, "mono_bold")
    d.text((cx0 + 36 + title_w, cy0 + 44), h["card_title"][1], font=font(20, "cjk_bold"),
           fill=hx(s["accent"]), anchor="ls")
    label_kind = "cjk" if lang == "zh" else "mono"
    label_w = measure(h["card_sub_label"], 12, label_kind)
    require_w(h["card_sub_path"], 12, "mono", 470 - label_w - 7, "hero card subtitle")
    d.text((cx0 + 28, cy0 + 64), h["card_sub_label"], font=font(12, label_kind),
           fill=hx(s["faint"]), anchor="ls")
    d.text((cx0 + 28 + label_w + 7, cy0 + 64), h["card_sub_path"], font=font(12, "mono"),
           fill=hx(s["faint"]), anchor="ls")

    x = chip_right(img, cx1 - 24, cy0 + 16, h["chip_skip"], s["skip"], s["skip_bg"], size=12)
    chip_right(img, x - 8, cy0 + 16, h["chip_warn"], s["warn"], s["warn_bg"], size=12)

    # section label
    d = ImageDraw.Draw(img)
    d.text((cx0 + 28, 146), h["section"], font=font(13.5, "cjk_bold"), fill=hx(s["sub"]), anchor="ls")
    d.text((cx1 - 28, 146), h["section_right"], font=font(11.5, "mono"), fill=hx(s["faint"]), anchor="rs")

    # the PR-003 window and its green check
    check_badge(img, cx0 + 36, 170, 8, s["ok"], s["ok_bg"])
    require_w(h["p3"], 12.5, "cjk", 620, "hero PR-003 line")
    d.text((cx0 + 52, 174), h["p3"], font=font(12.5, "cjk"), fill=hx(s["sub"]), anchor="ls")

    tx0, tx1 = cx0 + 28, cx1 - 28
    band_top, band_bottom, axis_y = 214, 242, 228
    x_decided = tx0 + int(round((tx1 - tx0) * DECIDED_FRAC))

    d.rounded_rectangle([tx0, band_top, tx1, band_bottom], radius=14, fill=hx(s["accent_soft"]))
    d.line([(tx0 + 12, axis_y), (x_decided, axis_y)], fill=hx(s["ok"]), width=3)
    # dashed slack from decision to promised due
    cursor = x_decided + 12
    while cursor < tx1 - 12:
        d.line([(cursor, axis_y), (min(cursor + 7, tx1 - 12), axis_y)], fill=hx(s["faint"]), width=2)
        cursor += 13

    d.ellipse([tx0 - 7, axis_y - 7, tx0 + 7, axis_y + 7], fill=hx(s["accent"]))
    check_badge(img, x_decided, axis_y, 9, s["ok"], s["card"])
    d.ellipse([tx1 - 7, axis_y - 7, tx1 + 7, axis_y + 7], fill=hx(s["card"]),
              outline=hx(s["faint"]), width=2)

    accept_w = measure(h["accepted"], 13, "cjk_bold")
    dec_w = measure(h["decided"], 13, "cjk_bold")
    require_w(h["accepted"], 13, "cjk_bold", 300, "hero accepted label")
    require_w(h["decided"], 13, "cjk_bold", 300, "hero decided label")
    require_w(h["due"], 12.5, "cjk", 340, "hero due label")
    if tx0 + accept_w + 16 > x_decided - dec_w / 2:
        raise SystemExit("FATAL: hero date labels collide")
    d.text((tx0, 206), h["accepted"], font=font(13, "cjk_bold"), fill=hx(s["accent"]), anchor="ls")
    d.text((x_decided, 206), h["decided"], font=font(13, "cjk_bold"), fill=hx(s["ok"]), anchor="ms")
    d.text((tx1, 272), h["due"], font=font(12.5, "cjk"), fill=hx(s["sub"]), anchor="rs")

    # PR-002 bracket below the band
    d.line([(tx0, 284), (x_decided, 284)], fill=hx(s["accent"]), width=2)
    d.line([(tx0, 284), (tx0, 290)], fill=hx(s["accent"]), width=2)
    d.line([(x_decided, 284), (x_decided, 290)], fill=hx(s["accent"]), width=2)
    require_w(h["p2"], 12, "cjk", 380, "hero PR-002 line")
    check_badge(img, tx0 + 7, 301, 6.5, s["ok"], s["ok_bg"])
    d.text((tx0 + 20, 306), h["p2"], font=font(12, "cjk"), fill=hx(s["sub"]), anchor="ls")

    d.line([cx0 + 28, 320, cx1 - 28, 320], fill=hx(s["grid"]), width=1)

    # ---- three real outcomes for that row ----------------------------------
    def outcome_row(y: int, rule_id: str, label: str, chip_text: str, sub: str,
                    dot: str, dot_bg: str, chip_fg: str, chip_bg: str,
                    highlight: bool = False, ok_style: bool = False) -> None:
        nonlocal d
        if highlight:
            shot = Image.new("RGBA", img.size, (0, 0, 0, 0))
            sd = ImageDraw.Draw(shot)
            sd.rounded_rectangle([cx0 + 16, y, cx1 - 16, y + 44], radius=10,
                                 fill=hx(dot_bg) + (255,))
            img.alpha_composite(shot)
            d = ImageDraw.Draw(img)
        if ok_style:
            check_badge(img, cx0 + 32, y + 21, 8, s["ok"], s["ok_bg"])
        else:
            d.ellipse([cx0 + 26, y + 15, cx0 + 38, y + 27], fill=hx(dot))
        id_x = cx0 + 48
        d.text((id_x, y + 19), rule_id, font=font(13.5, "mono_bold"), fill=hx(s["accent"]), anchor="ls")
        label_x = id_x + measure(rule_id, 13.5, "mono_bold") + 10
        label_size = 13.2 if lang == "zh" else 12.6
        require_w(label, label_size, "cjk_bold", 430, f"hero row label {rule_id}")
        chip_x = chip_right(img, cx1 - 24, y + 10, chip_text, chip_fg, chip_bg, size=11)
        if label_x + measure(label, label_size, "cjk_bold") + 12 > chip_x:
            raise SystemExit(f"FATAL: hero {rule_id} label collides with its chip")
        d.text((label_x, y + 19), label, font=font(label_size, "cjk_bold"), fill=hx(s["text"]), anchor="ls")
        require_w(sub, 11.3, "cjk", cx1 - 24 - (cx0 + 48), f"hero row sub {rule_id}")
        d.text((cx0 + 48, y + 38), sub, font=font(11.3, "cjk"), fill=hx(s["faint"]), anchor="ls")

    outcome_row(330, *h["row1"], s["warn"], s["warn_bg"], s["warn"], s["warn_bg"], highlight=True)
    outcome_row(380, *h["row2"], s["skip"], s["skip_bg"], s["skip"], s["skip_bg"])
    outcome_row(430, *h["row3"], s["ok"], s["ok_bg"], s["ok"], s["ok_bg"], ok_style=True)

    # ---- the quiet exit -----------------------------------------------------
    d = ImageDraw.Draw(img)
    d.text((cx0 + 28, 500), h["quiet"], font=font(11.3, "cjk"), fill=hx(s["faint"]), anchor="ls")
    x_chip = cx0 + 28 + measure(h["quiet"], 11.3, "cjk") + 14
    for rule_id in ("PR-002", "PR-003", "PR-006", "PR-007"):
        width = chip(img, x_chip, 486, rule_id, s, size=11.2, height=22, kind="mono")
        x_chip += width + 6
    quiet_right_w = measure(h["quiet_right"], 11.3, "cjk")
    if x_chip + 10 > cx1 - 28 - quiet_right_w:
        raise SystemExit("FATAL: hero quiet chips collide with the note")
    d.text((cx1 - 28, 500), h["quiet_right"], font=font(11.3, "cjk"), fill=hx(s["faint"]), anchor="rs")

    require_w(h["summary"], 12.5, "mono_bold", 330, "hero summary")
    d.text((cx0 + 28, 524), h["summary"], font=font(12.5, "mono_bold"), fill=hx(s["text"]), anchor="ls")
    require_w(h["summary_right"], 11, "mono", 330, "hero summary right")
    d.text((cx1 - 28, 524), h["summary_right"], font=font(11, "mono"), fill=hx(s["faint"]), anchor="rs")

    d.rounded_rectangle([cx0, cy0, cx1, cy1], radius=22, outline=hx(s["edge"]), width=2)

    target = os.path.join(OUT, f"{NAME}-hero-{lang}-{skin}.webp")
    img.convert("RGB").save(target, "WEBP", quality=92, method=6)
    print(f"wrote {os.path.basename(target)} ({W}x{H})")


# ===========================================================================
# flow: tri-state dispatch board (1100x660), one hand-written SVG per skin
# ===========================================================================
SVG = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        card="#ffffff", band="#f5f2fb", edge="#e6e2ef", grid="#ece8f5",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", accent_soft="#ece7f9",
        warn="#b45309", warn_bg="#fbf1e4",
        skip="#6b5aa8", skip_bg="#f0ecfa",
        ok="#2f855a", ok_bg="#e8f4ec",
        shadow="#2b2440", shadow_op="0.14", dot="#cfc8e2",
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        card="#182032", band="#1e2941", edge="#2c3852", grid="#26324a",
        text="#f2f4fb", sub="#b7c0d4", faint="#8b96ad",
        accent="#8496f5", accent_soft="#242f4e",
        warn="#f0b35e", warn_bg="#3a2c1c",
        skip="#b8a6f0", skip_bg="#2a2747",
        ok="#6ddba0", ok_bg="#1e3329",
        shadow="#000000", shadow_op="0.55", dot="#2b3856",
    ),
}

MONO = "Consolas,'Microsoft YaHei',ui-monospace,monospace"
SANS = "'Microsoft YaHei','Segoe UI','PingFang SC','Noto Sans CJK SC',sans-serif"

# (id, title, severity, fields read; all copied from rules/permit-report-check.yaml)
RULES = [
    ("PR-001", "每条申请材料都应记录提交情况", "warn", "requiredItems → submittedItems"),
    ("PR-002", "受理日期不应晚于决定日期", "warn", "acceptedAt ≤ decidedAt"),
    ("PR-003", "决定日期不应晚于承诺办结日", "info", "acceptedAt ≤ decidedAt ≤ dueAt"),
    ("PR-004", "决定结果应使用本机构口径的取值", "info", "decision ∈ values[]（出厂空）"),
    ("PR-005", "表示已办结的记录应填写许可证号", "warn", "decision 准予 → certificateNo"),
    ("PR-006", "核对表应声明申请人与申请事项", "warn", "applicant + matter"),
    ("PR-007", "许可事项不应在表内重复登记", "warn", "permitType unique"),
]


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def est(text: str, size: float, kind: str = "sans") -> float:
    """Conservative width estimate; only used for layout guards and chip sizes."""
    width = 0.0
    for ch in text:
        code = ord(ch)
        if code >= 0x2E80:
            width += size
        elif ch == " ":
            width += size * 0.32
        else:
            width += size * (0.62 if kind == "mono" else 0.57)
    return width


def svg_text(x: float, y: float, text: str, size: float, fill: str, kind: str = "sans",
             weight: str | None = None, anchor: str | None = None, opacity: float | None = None) -> str:
    family = MONO if kind == "mono" else SANS
    attrs = [f'x="{x:g}"', f'y="{y:g}"', f'fill="{fill}"', f'font-family="{family}"', f'font-size="{size:g}"']
    if weight:
        attrs.append(f'font-weight="{weight}"')
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    if opacity is not None:
        attrs.append(f'opacity="{opacity:g}"')
    return f'<text {" ".join(attrs)}>{esc(text)}</text>'


def svg_rect(x: float, y: float, w: float, h: float, radius: float, fill: str,
             stroke: str | None = None, sw: float = 1, dash: str | None = None,
             shadow: bool = False, opacity: float | None = None) -> str:
    attrs = [f'x="{x:g}"', f'y="{y:g}"', f'width="{w:g}"', f'height="{h:g}"', f'rx="{radius:g}"',
             f'fill="{fill}"']
    if stroke:
        attrs += [f'stroke="{stroke}"', f'stroke-width="{sw:g}"']
    if dash:
        attrs.append(f'stroke-dasharray="{dash}"')
    if shadow:
        attrs.append('filter="url(#soft)"')
    if opacity is not None:
        attrs.append(f'opacity="{opacity:g}"')
    return f'<rect {" ".join(attrs)}/>'


def svg_pill(x_right: float, y: float, text: str, s: dict, size: float = 11,
             fg: str | None = None, bg: str | None = None, kind: str = "mono") -> tuple[str, float]:
    width = est(text, size, kind) + 22
    x = x_right - width
    return (svg_rect(x, y, width, 24, 12, bg or s["accent_soft"]) +
            svg_text(x + 11, y + 16.2, text, size, fg or s["accent"], kind), x)


def svg_chip(x: float, y: float, text: str, s: dict, size: float = 11,
             fg: str | None = None, bg: str | None = None, kind: str = "mono") -> tuple[str, float]:
    width = est(text, size, kind) + 18
    return (svg_rect(x, y, width, 23, 11.5, bg or s["band"], stroke=s["edge"], sw=1) +
            svg_text(x + 9, y + 15.6, text, size, fg or s["sub"], kind), width)


def svg_arrow(x1: float, y1: float, x2: float, y2: float, color: str, width: float = 1.5) -> str:
    angle = math.atan2(y2 - y1, x2 - x1)
    back = 8
    left = (x2 - back * math.cos(angle - 0.42), y2 - back * math.sin(angle - 0.42))
    right = (x2 - back * math.cos(angle + 0.42), y2 - back * math.sin(angle + 0.42))
    return (f'<path d="M{x1:g} {y1:g}L{x2 - 1:g} {y2:g}" fill="none" stroke="{color}" '
            f'stroke-width="{width:g}" stroke-linecap="round"/>'
            f'<path d="M{x2:g} {y2:g}L{left[0]:.1f} {left[1]:.1f}L{right[0]:.1f} {right[1]:.1f}Z" fill="{color}"/>')


def flow_svg(skin: str) -> str:
    s = SVG[skin]
    p: list[str] = []
    p.append('<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="660" viewBox="0 0 1100 660" '
             'role="img" aria-labelledby="title desc">')
    p.append('<title id="title">dsh-permit-report-check — 7 条规则、三种去向的分诊台</title>')
    p.append('<desc id="desc">'
             '左侧是输入与归一：file 或 material 二选一（JSON / YAML），表头与 rows[] 经别名匹配归一到 17 个规范栏目，'
             '不认得任何已知栏名就拒读；配置里的 disabledRules 与 onlyRules 直接改变出口。'
             '中央是随包的规则包 rules/permit-report-check.yaml（版本 2026.1，7 条规则 PR-001..PR-007，'
             '5 种 check：conditionalPresence、date、enum、headerPresence、unique），每条规则只走一个出口。'
             '右侧三个出口：命中的进 issues[]（本例 PR-001 一条 warn）；没能执行的进 skipped[]（本例 PR-004 因 values 未配置）；'
             '跑过而未命中的两栏都不进（PR-002、PR-003、PR-005、PR-006、PR-007）。'
             '两条有字的通道汇入同一份报告：error 0 · warn 1 · info 0，issueCount 1 · skippedCount 1，'
             '同时给出 markdown 与 reportJson，措辞守卫与免责声明恒常附带；许可决定留给审批人，报告不判合规、不判责任、不判是否应当准予。'
             '</desc>')
    p.append('<defs>')
    p.append(f'<linearGradient id="bg" x1="0" y1="0" x2="0.2" y2="1">'
             f'<stop offset="0" stop-color="{s["bg_from"]}"/><stop offset="1" stop-color="{s["bg_to"]}"/></linearGradient>')
    p.append(f'<filter id="soft" x="-30%" y="-30%" width="160%" height="180%">'
             f'<feDropShadow dx="0" dy="7" stdDeviation="9" flood-color="{s["shadow"]}" flood-opacity="{s["shadow_op"]}"/></filter>')
    p.append(f'<pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse">'
             f'<circle cx="1.2" cy="1.2" r="1.2" fill="{s["dot"]}"/></pattern>')
    p.append('</defs>')
    p.append(f'<rect width="1100" height="660" fill="url(#bg)"/>')
    p.append(f'<rect width="1100" height="660" fill="url(#dots)" opacity="0.5"/>')

    # ---- header -------------------------------------------------------------
    p.append(svg_text(44, 52, "dsh-permit-report-check", 27, s["text"], "mono", "700"))
    p.append(svg_text(44, 80, "一份行政许可台账，7 条规则、三种去向：命中进 issues[]，跑不了进 skipped[]，跑过未命中两栏都不进。",
                      13.5, s["sub"]))
    pill, _ = svg_pill(1056, 28, "rules/permit-report-check.yaml · v2026.1", s, size=11.5)
    p.append(pill)
    p.append(svg_text(44, 108, "TOOL · permit_report_check · file | material · JSON / YAML · 只读", 11, s["faint"], "mono"))
    p.append(svg_text(1056, 108, "OUT · summary · issues[] · skipped[] · markdown · reportJson", 11, s["faint"],
                      "mono", anchor="end"))
    p.append(f'<line x1="44" y1="122" x2="1056" y2="122" stroke="{s["grid"]}" stroke-width="1.4"/>')

    # ---- left column: input, normalisation, config gates --------------------
    p.append(svg_rect(44, 132, 286, 148, 18, s["card"], stroke=s["edge"], sw=1.5, shadow=True))
    p.append(svg_text(68, 162, "IN · 台账", 13, s["text"], weight="700"))
    pill, _ = svg_pill(318, 146, "file | material", s, size=11)
    p.append(pill)
    p.append(svg_text(68, 192, "JSON / YAML；只读，原件不改", 11.6, s["sub"]))
    p.append(svg_text(68, 216, "表头 applicant · matter · window", 11, s["sub"], "mono"))
    p.append(svg_text(68, 240, "rows[] · 13 个栏位", 11, s["sub"], "mono"))
    p.append(svg_text(68, 264, "第 1 行：环评审批 · 准予", 11, s["faint"]))

    p.append(svg_rect(44, 292, 286, 120, 18, s["card"], stroke=s["edge"], sw=1.5, shadow=True))
    p.append(svg_text(68, 322, "归一 · 17 个规范栏目", 13, s["text"], weight="700"))
    p.append(svg_text(68, 350, "别名：忽略大小写 / 空格 / _ / -", 11, s["sub"]))
    p.append(svg_text(68, 374, "requireAnyOf 无已知栏名 → 拒读", 11, s["sub"]))
    p.append(svg_text(68, 398, "空栏 ≠ 缺栏：空格子也记为已提供", 11, s["faint"]))

    p.append(svg_rect(44, 424, 286, 100, 18, s["card"], stroke=s["edge"], sw=1.5, shadow=True))
    p.append(svg_text(68, 452, "CONFIG · 出口闸门", 13, s["text"], weight="700"))
    p.append(svg_text(68, 476, "rulesFile · disabledRules", 11, s["sub"], "mono"))
    p.append(svg_text(68, 494, "onlyRules · skipNotes · timeoutMs", 11, s["sub"], "mono"))
    p.append(svg_text(68, 514, "停用 / only 收窄 → skipped[]", 11, s["accent"]))

    # input column merge into the rack
    p.append(f'<path d="M330 206H340M330 354H340M330 474H340M340 206V474" fill="none" stroke="{s["accent"]}" '
             f'stroke-width="1.4" opacity="0.65" stroke-linecap="round"/>')
    p.append(svg_arrow(340, 330, 347, 330, s["accent"], 1.5))

    # ---- centre: the seven-rule pack ---------------------------------------
    p.append(svg_rect(348, 132, 368, 392, 20, s["card"], stroke=s["edge"], sw=1.5, shadow=True))
    p.append(svg_rect(348, 132, 368, 56, 20, s["band"]))
    p.append(svg_rect(348, 168, 368, 20, 0, s["band"]))
    p.append(f'<line x1="348" y1="188" x2="716" y2="188" stroke="{s["edge"]}" stroke-width="1"/>')
    p.append(svg_text(372, 160, "RULE PACK", 14, s["text"], "mono", "700"))
    p.append(svg_text(372, 180, "规则包是数据，不是代码；excerpt 逐字引文或写明缺口", 11, s["faint"]))
    pill, _ = svg_pill(704, 144, "7 条 · v2026.1", s, size=11)
    p.append(pill)

    for index, (rule_id, title, severity, fields) in enumerate(RULES):
        top = 196 + index * 43
        p.append(svg_text(368, top + 18, rule_id, 13, s["accent"], "mono", "700"))
        p.append(svg_text(424, top + 17, title, 13, s["text"], weight="600"))
        p.append(svg_text(424, top + 35, fields, 11, s["faint"], "mono"))
        color = s["warn"] if severity == "warn" else s["skip"]
        p.append(f'<circle cx="660" cy="{top + 13:g}" r="3.4" fill="{color}"/>')
        p.append(svg_text(668, top + 17, severity, 11, color, "mono"))
        if index < len(RULES) - 1:
            p.append(f'<line x1="368" y1="{top + 42:g}" x2="698" y2="{top + 42:g}" stroke="{s["grid"]}" stroke-width="1"/>')
    p.append(svg_text(368, 516, "依据封顶 derived ≤ warn · institutional ≤ info", 11, s["faint"]))

    # rack -> three exits (one bus, three short branches)
    p.append(f'<path d="M716 330H724M724 330V212M724 212H734M724 330V370M724 370H734M724 330V486M724 486H734" '
             f'fill="none" stroke="{s["accent"]}" stroke-width="1.5" opacity="0.8" stroke-linecap="round"/>')
    for lane_y in (212, 370, 486):
        p.append(svg_arrow(734, lane_y, 741, lane_y, s["accent"], 1.5))

    # ---- exits --------------------------------------------------------------
    # A · issues[]
    p.append(svg_rect(744, 132, 312, 160, 18, s["card"], stroke=s["edge"], sw=1.5, shadow=True))
    p.append(svg_rect(747, 144, 4, 136, 2, s["warn"], opacity=0.85))
    p.append(svg_text(768, 162, "A · issues[]", 13, s["text"], "mono", "700"))
    pill, _ = svg_pill(1044, 146, "1 条 · warn", s, size=11, fg=s["warn"], bg=s["warn_bg"])
    p.append(pill)
    p.append(svg_text(768, 192, "PR-001 · warn · 第 1 行", 11, s["sub"], "mono"))
    p.append(svg_text(768, 216, "已提交材料为空，申请材料却有值", 13, s["text"]))
    p.append(svg_text(768, 240, "应同时填写 submittedItems", 11, s["sub"]))
    p.append(svg_text(768, 264, "locator { row: 1, field: requiredItems }", 11, s["faint"], "mono"))

    # B · skipped[]
    p.append(svg_rect(744, 304, 312, 132, 18, s["card"], stroke=s["edge"], sw=1.5, shadow=True))
    p.append(svg_rect(747, 316, 4, 108, 2, s["skip"], opacity=0.75))
    p.append(svg_text(768, 332, "B · skipped[]", 13, s["text"], "mono", "700"))
    pill, _ = svg_pill(1044, 316, "1 条", s, size=11, fg=s["skip"], bg=s["skip_bg"])
    p.append(pill)
    p.append(svg_text(768, 360, "PR-004 · values 未配置", 11, s["sub"], "mono"))
    p.append(svg_text(768, 384, "本机构口径，引擎不硬编码", 11, s["text"]))
    p.append(svg_text(768, 406, "disabledRules 停用 → 同样进这里", 11, s["faint"]))
    p.append(svg_text(768, 426, "材料没有「permitType」列 → 本条不适用", 11, s["faint"]))

    # C · quiet exit
    p.append(svg_rect(744, 448, 312, 76, 18, s["card"], stroke=s["accent"], sw=1.2, dash="5 4", shadow=True))
    p.append(svg_text(768, 474, "C · 跑过 · 未命中", 13, s["sub"], weight="700"))
    p.append(svg_text(1044, 474, "无出口", 11, s["faint"], anchor="end"))
    piece, width = svg_chip(768, 484, "PR-002 / 003 / 005 / 006 / 007", s, size=11)
    p.append(piece)
    if 768 + width > 1032:
        raise SystemExit("FATAL: quiet chip overflows the terminal")
    p.append(svg_text(768, 518, "不进 issues[]，也不进 skipped[]", 11, s["faint"]))

    # the two named channels leave through one rail into the report
    p.append(f'<path d="M1056 212H1066M1056 370H1066M1066 212V576H1060" fill="none" '
             f'stroke="{s["accent"]}" stroke-width="1.3" opacity="0.55" stroke-linecap="round"/>')
    p.append(svg_arrow(1066, 576, 1059, 576, s["accent"], 1.3))
    p.append(f'<circle cx="1056" cy="212" r="2.6" fill="{s["accent"]}" opacity="0.8"/>')
    p.append(f'<circle cx="1056" cy="370" r="2.6" fill="{s["accent"]}" opacity="0.8"/>')

    # ---- the one report both named channels converge on ---------------------
    p.append(svg_rect(44, 536, 1012, 80, 20, s["card"], stroke=s["edge"], sw=1.5, shadow=True))
    p.append(svg_text(68, 558, "report · 两栏汇入 makeReport + buildView", 11, s["faint"], "mono"))
    p.append(svg_text(68, 584, "error 0 · warn 1 · info 0", 17, s["text"], "mono", "700"))
    p.append(svg_text(68, 604, "issueCount 1 · skippedCount 1 · rulesetVersion 2026.1", 11, s["sub"], "mono"))
    p.append(f'<line x1="470" y1="550" x2="470" y2="602" stroke="{s["grid"]}" stroke-width="1"/>')
    p.append(svg_text(494, 558, "markdown + reportJson", 11.5, s["text"], weight="700"))
    p.append(svg_text(494, 582, "措辞守卫 + 免责声明：只列差异", 11, s["sub"]))
    p.append(svg_text(494, 602, "每份报告都带 disclaimer", 11, s["faint"]))
    p.append(f'<line x1="724" y1="550" x2="724" y2="602" stroke="{s["grid"]}" stroke-width="1"/>')
    p.append(svg_rect(746, 546, 54, 22, 11, s["accent_soft"]))
    p.append(svg_text(756, 561, "审核人", 11, s["accent"], weight="700"))
    p.append(svg_text(746, 586, "许可决定留给审批人", 13, s["text"], weight="700"))
    p.append(svg_text(746, 606, "不判是否合法 · 不判是否应准予", 11, s["sub"]))
    p.append(svg_text(1032, 558, "结论不在报告里", 11, s["faint"], anchor="end"))

    # ---- footnote -----------------------------------------------------------
    p.append(svg_text(44, 640, "issues[] 为空 ≠ 没问题：跑不了的进 skipped[]；跑过未命中两栏都不进。", 11.2, s["sub"]))
    p.append(svg_text(1056, 640, "7 条规则 · 5 种 check · 5 derived / 2 institutional · 无 error", 11,
                      s["faint"], anchor="end"))
    p.append('</svg>')
    return "\n".join(p) + "\n"


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for skin in ("light", "dark"):
        for lang in ("zh", "en"):
            hero(lang, skin)
    for skin in ("light", "dark"):
        target = os.path.join(OUT, f"{NAME}-flow-v5-{skin}.svg")
        with open(target, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(flow_svg(skin))
        print(f"wrote {os.path.basename(target)} (1100x660)")


if __name__ == "__main__":
    main()
