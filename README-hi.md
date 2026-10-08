# dsh-permit-report-check — प्रशासनिक अनुज्ञप्ति आवेदन रजिस्टर की पूर्णता और तिथि-संगति की जाँच

`dsh-permit-report-check` प्रशासनिक अनुज्ञप्ति के निपटारे का एक रजिस्टर (行政许可办理台账) पढ़ता है — आवेदक हेडर और प्रत्येक आवेदन की एक पंक्ति — और उसी रजिस्टर के बंद-चक्र तथा आंतरिक संगति की जाँच करता है: 申请材料 कॉलम में दर्ज प्रत्येक मद की प्रस्तुति दर्ज है या नहीं, 受理日期 决定日期 के बाद न पड़े, 决定日期 受理日期 और रजिस्टर में लिखी 承诺办结日 के बीच पड़े, 决定结果 आपके द्वारा कॉन्फ़िगर किए गए मानों में से हो, जिस प्रविष्टि का 决定结果 स्वीकृति दर्शाता है उसमें उसका 许可证号 दर्ज हो, हेडर 申请人 और 申请事项 घोषित करे, और कोई 许可事项 तालिका में दो बार दर्ज न हो।

## यह किन सवालों का जवाब देता है

| आपका सवाल | इसका जवाब |
|---|---|
| एक पंक्ति में 申请材料 दर्ज है, पर 已提交材料 खाली है — क्या यह दर्ज होता है? | हाँ। `PR-001` हर उस पंक्ति में `submittedItems` मान की अपेक्षा करता है जिसमें 申请材料 भरा हो, और प्रस्तुति कॉलम खाली होने पर उस पंक्ति को दर्ज करता है। यह रजिस्टर के अपने ही 申请材料 कॉलम को पढ़ता है और केवल यह देखता है कि प्रस्तुति दर्ज है या नहीं: यह उस सूची की तुलना उस कार्य की सेवा-निर्देशिका (service guide) से नहीं करता, और न ही आँकता है कि प्रस्तुत सामग्री पूरी है या मानक के अनुरूप है। किसी भी पंक्ति में 申请材料 भरा न हो तो यह नियम `skipped` में चला जाता है। |
| 受理日期, 决定日期 के बाद की है — क्या यह पकड़ में आता है? | हाँ। `PR-002` रजिस्टर में लिखी दोनों तिथियों की तुलना करता है — `acceptedAt` बनाम `decidedAt` — उसी दिन को बाद का नहीं मानता, और जहाँ स्वीकृति निर्णय के बाद पड़ती है वह पंक्ति दर्ज करता है। यह केवल इन दो तिथियों की तुलना करता है: यह नहीं तय करता कि स्वीकृति वैध थी या आवेदन स्वीकार होना ही चाहिए था। जो तिथि पढ़ी न जा सके वह अलग प्रविष्टि के रूप में दर्ज होती है, चुपचाप छोड़ी नहीं जाती। |
| 承诺办结日 कॉलम खाली हो तो क्या होता है — और 法定时限 कॉलम को कोई नियम पढ़ता है या नहीं? | `PR-003` `skipped` में चला जाता है: कोई भी दिन-गणना अंदर नहीं बसाई गई है, क्योंकि वैधानिक अवधियाँ कार्य-दिवसों में गिनी जाती हैं, बढ़ाई जा सकती हैं और सुनवाई या विशेषज्ञ समीक्षा का समय उनसे बाहर रखा जा सकता है — इसलिए एकमात्र आधार वही 承诺办结日 (`dueAt`) है जो रजिस्टर स्वयं बताता है। 法定时限 (`legalDays`) कॉलम को कोई नियम नहीं पढ़ता। `dueAt` भरा होने पर यह नियम देखता है कि 决定日期, 受理日期 और उस तिथि के बीच पड़ती है; प्रविष्टि का अर्थ यह है कि निर्णय आपकी दर्ज की गई समय-सीमा से मेल नहीं खाता — यह कभी नहीं कि विलंब हुआ। |
| मैंने 决定结果 में 补正后准予 लिखा है। क्या यह स्वीकार होगा? | `PR-004` 决定结果 की तुलना आपके `values` पैरामीटर में दिए मानों से करता है, और वह पैरामीटर खाली ही आता है — इसलिए जैसा दिया गया है उसी रूप में यह नियम आपकी शब्दावली पर निर्णय देने के बजाय `skipped` में चला जाता है। `values` में अपनी संस्था के दर्ज किए जाने वाले परिणाम भरें (उदाहरण 不予受理), फिर सूची से बाहर का हर मान दर्ज होगा। यह नियम केवल यह देखता है कि मान सूची में है या नहीं; यह नहीं आँकता कि निर्णय सही या वैध है। |
| एक प्रविष्टि में 准予 लिखा है, पर 许可证号 कॉलम खाली है। | `PR-005` इसे दर्ज करता है: जब 决定结果 किसी स्वीकृति-चिह्न से मेल खाता है — `conditionValues`, जो डिफ़ॉल्ट रूप से 准予 / 准予许可 / 通过 / 同意 / 已办结 / 批准 हैं — तो उस प्रविष्टि में उसका 许可证号 (`certificateNo`) होना चाहिए। यह केवल यह देखता है कि क्रमांक भरा है; यह नहीं कि प्रमाणपत्र असली, वैध या भेजा गया है। रजिस्टर में कोई पंक्ति स्वीकृति-चिह्न से मेल न खाए तो यह नियम `skipped` में चला जाता है। |
| एक ही 许可事项 दो पंक्तियों में आया है। | `PR-007` बाद वाली पंक्ति दर्ज करता है और बताता है कि वह किस पंक्ति से दोहराई गई है, क्योंकि एक ही विषय के दो पंजीकरण समय-सीमा की जाँच को अनिश्चित बना देते हैं। यह केवल अद्वितीयता देखता है, और प्रविष्टि के लिए मानवीय पुष्टि चाहिए: एक परियोजना कई विषयों के लिए आवेदन करे तो नाम समान होना संभव है — ऐसे में पंक्ति हटाने के बजाय सामग्री कॉलम में उसे अलग दिखाएँ। मान के भीतर के खाली स्थान अनदेखे रहते हैं; 许可事项 कॉलम न हो तो यह नियम `skipped` में चला जाता है। |

## यह किन मानकों पर आधारित है

| दस्तावेज़ | संख्यांक | इन्हें उद्धृत करने वाले नियम |
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

| सतह | स्थिति |
|---|---|
| Harness | peer रेंज `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — `0.2.0-rc.2` और `0.2.1-alpha.1` दोनों को स्वीकार करने के लिए सत्यापित। **`engines.dsh` जानबूझकर घोषित नहीं**: इसका कोई पाठक नहीं और यह किसी होस्ट को अस्वीकार नहीं कर सकता |
| Node | `^22.19.0 || >=24.0.0` |
| प्लेटफ़ॉर्म | सभी (शुद्ध ESM; कोई नेटिव कोड नहीं, कोई नेटवर्क नहीं, कोई मॉडल कॉल नहीं) |
| टूल मोड | `native`, `ptc` और `both` में काम करता है; पूरे फ़ोल्डर के लिए `ptc` चुनें |

## What it does

नियम-सूची, फ़ील्ड और विस्तृत व्यवहार [README.md](README.md#what-it-does) (अंग्रेज़ी मुख्य संस्करण) में हैं। यह प्लगइन केवल उद्धृत धाराओं के सामने शाब्दिक अंतर सूचीबद्ध करता है और हर न चल पाई जाँच को `skipped` में बताता है।

## Install

```sh
dsh plugin --profile <name> add dsh-permit-report-check
dsh --profile <name> --dump-config | grep 'dsh-permit-report-check'
```

## Configuration

सभी समायोज्य पैरामीटर `src/config.ts` की Schemastery स्कीमा में हैं, इसलिए कोड बदले बिना `cordis.yml` से बदले जा सकते हैं; प्रति-नियम सीमाएँ `rules/` के नियम-पैक में हैं।

| कुंजी | प्रकार | डिफ़ॉल्ट | विवरण |
|---|---|---|---|
| `rulesFile` | string | `rules/permit-report-check.yaml` | नियम-पैक का पथ, पैकेज रूट के सापेक्ष |
| `disabledRules` | string[] | `[]` | बंद करने वाले नियम id; प्रत्येक `skipped` में दिखता है |
| `onlyRules` | string[] | `[]` | केवल ये नियम चलाएँ; खाली होने पर सभी नियम चलते हैं |
| `skipNotes` | string | `""` | हर `skipped` कारण के आगे जोड़ी जाने वाली टिप्पणी |
| `timeoutMs` | number | `120000` | उपकरण का सहकारी समय-सीमा बजट |

## Material format

JSON या YAML स्वीकार्य है। पूरा फ़ील्ड उदाहरण [README.md](README.md#material-format) (अंग्रेज़ी मुख्य संस्करण) में है। पढ़ने की परत में फ़ील्ड वैकल्पिक हैं और जाँच इंजन उन्हें सत्यापित करता है, इसलिए आंशिक निर्यात पर क्रैश के बजाय "अनुपस्थित" श्रेणी के निष्कर्ष मिलते हैं।

## Rule sources

नियम-डेटा कोड से अलग है: प्रत्येक नियम में दस्तावेज़, संख्या, स्रोत की अपनी क्रमांकन-प्रणाली के अनुसार धारा, शब्दशः उद्धरण और स्रोत URL होता है। लोडर लागू करता है कि उद्धरण कम से कम आठ अक्षरों का वास्तविक उद्धरण हो, और जिस जाँच का आधार केवल सामान्य सिद्धांत (`kind: derived-from-principle`, अधिकतम `warn`) या स्थानीय नीति (`kind: institutional-configuration`, अधिकतम `info`) हो, उसे कभी `error` घोषित न किया जाए।

सत्यापित सीमाएँ और जान-बूझकर **न** कहे गए निष्कर्ष [README.md](README.md#rule-sources) (अंग्रेज़ी मुख्य संस्करण) और `rules/evidence/` में हैं।

## Troubleshooting

- **प्लगइन इंस्टॉल हो गया पर टूल दिखता नहीं**: जाँचें कि `main` `lib/index.mjs` पर जाता है और `pnpm run build` ने उसे बनाया है।
- **`dsh plugin add` असंगत बताकर मना करता है**: peer range `0.1.x` और `0.2.x` दोनों को कवर करती है; बाहर होने पर स्पष्ट छूट दें: `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`।
- **कोई नियम नहीं चला**: `skipped` सरणी देखें।
- **`check` में `manifest-peers` विफल दिखता है**: यह `dsh-plugin-dev` की ज्ञात अपस्ट्रीम समस्या है; रनटाइम इंस्टॉल के समय अनुकूलता लागू करता है।
- **समय खिसका हुआ लगता है**: सारी गणना दिए गए स्ट्रिंग पर वॉल-क्लॉक है।

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-permit-report-check
```

अंतिम कमांड `../_shared` का साझा किट `src/shared/` में कॉपी करता है; हर साझा बदलाव के बाद इसे दोबारा चलाएँ।

## License

[Apache License 2.0](LICENSE) © 2026 dsh-permit-report-check contributors.
