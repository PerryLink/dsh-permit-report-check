<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-permit-report-check-hero-en-dark.webp">
  <img src="docs/assets/dsh-permit-report-check-hero-en-light.webp" width="100%" alt="dsh-permit-report-check: बाईं ओर प्लगइन का नाम, मूल्य की दो पंक्तियाँ और 7 नियम व केवल-पढ़ने की टिप्पणी है; दाईं ओर नमूना रजिस्टर की पंक्ति 1 एक अनुपातिक तिथि-अक्ष पर है — स्वीकृति 2026-03-02 → निर्णय 2026-04-20 → वचनबद्ध पूर्णता 2026-04-30 — जहाँ PR-002 और PR-003 की तिथि-जाँच पास हैं; नीचे की तीन पंक्तियाँ नमूना निष्पादन के वास्तविक परिणाम हैं: PR-001 में submitted items खाली होने से issues[] (warn), PR-004 में values सेट न होने से skipped[], और PR-005 में अनुमति-चिह्न मिला व लाइसेंस संख्या भरी है; PR-002, PR-003, PR-006 और PR-007 बिना किसी अंतर के चले और किसी सूची में नहीं गए; नीचे गिनती error 0 · warn 1 · info 0, issueCount 1, skippedCount 1 है।">
</picture>

# dsh-permit-report-check

**प्रशासनिक लाइसेंस रजिस्टर को पंक्ति-दर-पंक्ति जाँचें — आपको यह सूची मिलती है कि कौन-सी पंक्ति, कौन-सा कॉलम और क्या छूटा है; लाइसेंस का निर्णय अनुमोदक के पास ही रहता है।**

DeepSeek Harness के लिए केवल-डेटा जाँच प्लगइन: यह एक प्रशासनिक लाइसेंस रजिस्टर (आवेदक हेडर और प्रत्येक आवेदन के लिए एक पंक्ति) पढ़ता है, साथ भेजे गए संस्करणबद्ध नियम पैक (PR-001..PR-007) को लागू करता है, और केवल वही अंतर गिनाता है जिन्हें रजिस्टर के भीतर शब्दशः इंगित किया जा सके — कोई अनुपालन निर्णय नहीं, कोई दायित्व-निर्धारण नहीं।

[इंस्टॉल](#तीन-चरणों-में-शुरुआत) · [कॉन्फ़िगरेशन](#कॉन्फ़िगरेशन) · [FAQ](#faq) · [简体中文](README.md) · [English](README.en.md) · [Español](README.es.md) · [Português](README.pt.md) · [हिन्दी](README.hi.md)

[![License](https://img.shields.io/badge/license-Apache--2.0-3366CC?style=flat-square&labelColor=2B3245)](LICENSE)
[![DSH](https://img.shields.io/badge/DSH-%E2%89%A50.2.1%20%3C0.3.0-4B67B4?style=flat-square&labelColor=2B3245)](#संगतता)
[![npm](https://img.shields.io/npm/v/dsh-permit-report-check?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-permit-report-check)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-permit-report-check/ci.yml?branch=main&label=CI&style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-permit-report-check/actions/workflows/ci.yml)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-339933?style=flat-square&labelColor=2B3245)](#संगतता)

[![Stars](https://img.shields.io/github/stars/PerryLink/dsh-permit-report-check?style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-permit-report-check/stargazers)
[![npm downloads](https://img.shields.io/npm/dm/dsh-permit-report-check?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-permit-report-check)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-permit-report-check?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-permit-report-check?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-permit-report-check/badge)](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-permit-report-check)
[![DSH Market](https://img.shields.io/badge/DSH_Market-listed-4B67B4?style=flat-square&labelColor=2B3245)](https://dsh.market/)
[![Gitee](https://img.shields.io/badge/Gitee-mirror-C71D23?style=flat-square&labelColor=2B3245&logo=gitee)](https://gitee.com/perrylink/dsh-permit-report-check)

```sh
dsh plugin --profile <name> add dsh-permit-report-check
```

</div>

<sub>सामुदायिक प्लगइन, DeepSeek से संबद्ध नहीं। मूल रिपॉज़िटरी: <https://github.com/PerryLink/dsh-permit-report-check> (Gitee मिरर है)।</sub>

## यह क्या है

`dsh-permit-report-check` एक प्रशासनिक लाइसेंस रजिस्टर पढ़ता है — आवेदक हेडर और प्रत्येक आवेदन के लिए एक पंक्ति — और उसी रजिस्टर का बंद चक्र तथा आंतरिक संगति जाँचता है: सामग्री कॉलम में सूचीबद्ध प्रत्येक मद दर्ज करती है कि वह जमा हुई या नहीं, स्वीकृति तिथि निर्णय तिथि के बाद नहीं पड़ती, निर्णय तिथि स्वीकृति और रजिस्टर में लिखी वचनबद्ध पूर्णता तिथि के बीच पड़ती है, निर्णय परिणाम आपके कॉन्फ़िगर किए शब्द-भंडार से आता है, अनुमति दर्शाने वाले रिकॉर्ड में लाइसेंस संख्या भरी है, हेडर में आवेदक और विषय का उल्लेख है, और कोई विषय दो बार दर्ज नहीं है।

- **किसके लिए**: प्रशासनिक स्वीकृति काउंटर और अनुपालन अधिकारी; कमांड लाइन की ज़रूरत नहीं — सामग्री चैट में दे दें।
- **आप क्या देते हैं**: जाँच के लिए मूल सामग्री (तालिका, रजिस्टर या दस्तावेज़); मूल कभी नहीं बदला जाता। Excel को पहले JSON/YAML में बदला जा सकता है, प्लेटफ़ॉर्म समर्थन दे तो चैट में ही।
- **आपको क्या मिलता है**: «कौन-सी पंक्ति, कौन-सा कॉलम, क्या छूटा» की सूची; जो जाँच नहीं चल सकीं वे `skipped` में कारण के साथ दर्ज होती हैं।
- **यह क्या नहीं करता**: अनुपालन निर्णय नहीं, दायित्व-निर्धारण नहीं, समीक्षक का विकल्प नहीं; केवल अंतर।

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-permit-report-check-flow-v5-dark.svg">
  <img src="docs/assets/dsh-permit-report-check-flow-v5-light.svg" width="100%" alt="dsh-permit-report-check: त्रि-अवस्था वितरण बोर्ड। बाईं ओर file या material (JSON या YAML) और रजिस्टर को उपनाम-मिलान से 17 मानक कॉलमों में सामान्यीकृत किया जाता है; कोई ज्ञात कॉलम न मिले तो सामग्री अस्वीकार होती है; disabledRules और onlyRules निकास बदलते हैं। मध्य में साथ भेजा नियम पैक rules/permit-report-check.yaml (संस्करण 2026.1, सात नियम PR-001..PR-007, पाँच जाँच प्रकार) है, और हर नियम केवल एक निकास से जाता है। दाईं ओर तीन निकास: मिले अंतर issues[] में (यहाँ PR-001, एक warn); जो नहीं चल सका वह कारण के साथ skipped[] में (PR-004, values सेट नहीं); जो चला पर कुछ न मिला वह किसी सूची में नहीं (PR-002, PR-003, PR-005, PR-006, PR-007)। दोनों सूची वाले निकास एक ही रिपोर्ट में मिलते हैं: error 0 · warn 1 · info 0, issueCount 1, skippedCount 1, markdown और reportJson, शब्द-रक्षक व अस्वीकरण के साथ; लाइसेंस निर्णय समीक्षक के पास रहता है।">
</picture>

## तीन चरणों में शुरुआत

1. **इंस्टॉल** (कोई एक माध्यम चुनें):

   ```sh
   # git माध्यम (नवीनतम main; git+https://github.com/PerryLink/dsh-permit-report-check.git के बराबर)
   dsh plugin --profile <name> add github:PerryLink/dsh-permit-report-check
   # npm माध्यम (प्रकाशित संस्करण)
   dsh plugin --profile <name> add dsh-permit-report-check
   # tarball माध्यम: इस रिपॉज़िटरी में pnpm pack के बाद
   dsh plugin --profile <name> add ./dsh-permit-report-check-<version>.tgz
   ```

2. **न्यूनतम कॉन्फ़िगरेशन** (डिफ़ॉल्ट ही काम करते हैं; `config` के बिना bundle पंक्ति सभी डिफ़ॉल्ट लेती है, और नियम पैक का पथ साथ भेजे `rules/permit-report-check.yaml` की ओर इशारा करता है):

   ```yaml
   - insert:
       - id: dsh-permit-report-check
         name: dsh-permit-report-check
   ```

3. **जाँचें कि माउंट हुआ**:

   ```sh
   dsh --profile <name> --dump-config | grep 'dsh-permit-report-check'
   ```

   फिर साथ भेजा नमूना एक बार चलाएँ (पहले `pnpm run build` से `lib/` बनाएँ):

   ```sh
   node samples/quickstart/run.mjs
   ```

   आउटपुट (`samples/quickstart/expected/result.json` के अनुरूप):

   ```text
   permit_report_check: 1 issue(s) — error 0, warn 1, info 0
   skipped: 1
   ```

   स्क्रीनशॉट: `docs/assets/quickstart.png`.

**अनइंस्टॉल**: `dsh plugin --profile <name> remove dsh-permit-report-check` (या प्रोफ़ाइल पैच से पंक्ति हटा दें)।

<details>
<summary>WorkBuddy / Coze में उपयोग</summary>

WorkBuddy / Coze में «Professional Document Check Suite» खोजें (पूरा सेट; यह जाँच उसका एक भाग है; उपलब्धता स्टोर के अनुसार) — बिना कमांड लाइन वही जाँच क्षमता मिलती है।

</details>

<details>
<summary>DSH Desktop मार्केट से इंस्टॉल</summary>

सभी PerryLink प्लगइन DSH Desktop के अंतर्निहित मार्केट में देखे जा सकते हैं: **Market → Sources → Add source → चिपकाएँ** `https://perrylink-dsh-catalog.perrylink.workers.dev/catalog-source.json` **→ चुनें**। इंस्टॉल फिर भी मार्केट की npm पहचान जाँच और आपकी पुष्टि से होता है।

</details>

## मुख्य क्षमताएँ

`dsh-permit-report-check` टूल `permit_report_check` पंजीकृत करता है: एक प्रशासनिक लाइसेंस रजिस्टर (आवेदक हेडर और प्रत्येक आवेदन के लिए एक पंक्ति) पढ़ता है, संस्करणबद्ध नियम पैक लागू करता है और रिपोर्ट लौटाता है।

- **एक पैक में सात नियम** — नियम पैक डेटा है, कोड नहीं (`rules/permit-report-check.yaml`); उसे बदलने से पूरा नियम-समुच्चय बदल जाता है, TypeScript की एक पंक्ति छुए बिना।
- **सामग्री पर केवल पढ़ना** — JSON या YAML स्वीकार करता है और मूल कभी नहीं बदलता; शुद्ध ESM, कोई नेटवर्क अनुरोध नहीं, कोई मॉडल कॉल नहीं।
- **कोई गढ़ा हुआ उद्धरण नहीं** — प्रत्येक नियम में `document` / `number` / `clause` / `excerpt` / `kind` / `source` होते हैं; `excerpt` शब्दशः उद्धरण होना चाहिए, और जिस नियम का पाठ नहीं मिला वह `excerpt` में यह लिखता है और `derived-from-principle` चिह्नित होता है।
- **गंभीरता साक्ष्य के अनुसार** — `derived-from-principle` अधिकतम `warn`, संस्थागत कॉन्फ़िगरेशन (`institutional-configuration`) अधिकतम `info`, और एक टेस्ट इस सीमा की पुष्टि करता है।
- **खाली सूची ≠ कुछ गलत नहीं** — जो जाँच नहीं चल सकी वह कारण के साथ `skipped` में जाती है; जिस नियम की आवश्यक सूची सेट नहीं है वह चुपचाप पास होने के बजाय स्वयं को `skipped` में दर्ज करता है।
- **शब्दावली निर्णय नहीं देती** — रिपोर्ट केवल अंतर गिनाती है, अनुपालन, दायित्व या सत्यता पर निर्णय नहीं; एक शब्दावली-गार्ड इसे लागू करता है और प्रत्येक रिपोर्ट में अस्वीकरण रहता है।

| नियम | क्या जाँचता है | गंभीरता | आधार प्रकार |
|---|---|---|---|
| `PR-001` | सूचीबद्ध प्रत्येक सामग्री अपना जमा होना दर्ज करती है | warn | principle |
| `PR-002` | स्वीकृति निर्णय के बाद नहीं पड़ती | warn | principle |
| `PR-003` | निर्णय स्वीकृति और वचनबद्ध तिथि के बीच पड़ता है | info | local |
| `PR-004` | परिणाम आपके शब्द-भंडार से आता है (फ़ैक्टरी में बंद) | info | local |
| `PR-005` | अनुमति वाला रिकॉर्ड लाइसेंस संख्या दर्ज करता है | warn | principle |
| `PR-006` | रजिस्टर आवेदक और विषय बताता है | warn | principle |
| `PR-007` | विषय दो बार दर्ज नहीं होते | warn | principle |

### टूल सतह

`permit_report_check` चार आर्ग्युमेंट लेता है और शुरू से अंत तक केवल पढ़ता है:

| आर्ग्युमेंट | प्रकार | टिप्पणी |
|---|---|---|
| `file` | string | सामग्री फ़ाइल का पूर्ण पथ (JSON या YAML); `file` / `material` में से एक |
| `material` | string | इनलाइन सामग्री पाठ (JSON या YAML); `file` / `material` में से एक |
| `rulesFile` | string | कॉन्फ़िगर किया नियम-पैक पथ बदलता है (पैकेज रूट के सापेक्ष या पूर्ण) |
| `only` | string[] | केवल ये नियम id चलाएँ; खाली होने पर कॉन्फ़िगर किया `onlyRules` लागू रहता है |

### उदाहरण

ये प्लगइन के वास्तविक प्रवेश-बिंदु हैं; एक बार इंस्टॉल करें, फिर कोई एक चलाएँ। पहली पंक्ति विस्तृत मार्गदर्शन है, बाकी संक्षिप्त मामले।

**विस्तृत उदाहरण** — टूल `permit_report_check`, इनपुट:

```json
{"applicant":"某某公司","matter":"某某建设项目环评审批","rows":[{"序号":"1","许可事项":"建设项目环境影响评价文件审批","申请材料":"环境影响报告书全本及公众参与说明","已提交材料":""}]}
```

आउटपुट:

```json
{
  "id": "dsh-permit-report-check.PR-001.de09b5a6",
  "ruleId": "PR-001",
  "severity": "warn",
  "locator": {
    "row": 1,
    "field": "requiredItems"
  },
  "found": "第 1 行「requiredItems」为「环境影响报告书全本及公众参与说明」，但缺 submittedItems",
  "expected": "满足该条件的行应同时填写 submittedItems"
}
```

*Observed from `dsh-permit-report-check/tests/fixtures/PR-001/PR-001-unsafe.json`*

यह प्लगइन का अपने `PR-001` फ़िक्स्चर पर वास्तविक आउटपुट है, कोई चित्रण नहीं। नियम पैक उद्धरण नहीं गढ़ता, इसलिए प्रत्येक निष्कर्ष उस प्रावधान को भी बताता है जिसे वह उद्धृत करता है और यह भी कि उस प्रावधान का पाठ इस बार नहीं मिला।

| आप पूछते हैं | यह क्या उत्तर देता है |
|---|---|
| किसी पंक्ति में सामग्री कॉलम में सामग्री लिखी है, पर जमा-सामग्री कॉलम खाली है — क्या यह रिपोर्ट होता है? | हाँ। `PR-001` ऐसी हर पंक्ति पर `submittedItems` मान चाहता है जिसकी सामग्री सेल भरी हो, और जमा-कॉलम खाली होने पर उस पंक्ति को रिपोर्ट करता है। यह रजिस्टर के अपने सामग्री कॉलम को पढ़ता है और केवल यह जाँचता है कि जमा होना दर्ज है या नहीं: यह उस सूची की तुलना विषय की सेवा-गाइड से नहीं करता और यह भी नहीं आँकता कि जमा सामग्री पूर्ण या अनुरूप है। यदि कोई पंक्ति भरी सामग्री सेल नहीं रखती, तो नियम स्वयं को `skipped` में दर्ज करता है। |
| स्वीकृति तिथि निर्णय तिथि के बाद है — क्या यह पकड़ा जाएगा? | हाँ। `PR-002` रजिस्टर की अपनी दो तिथियों की तुलना करता है, `acceptedAt` बनाम `decidedAt`, उसी दिन को बाद नहीं मानता, और जहाँ स्वीकृति निर्णय के बाद आती है वह पंक्ति रिपोर्ट करता है। यह केवल उन दो तिथियों की तुलना करता है: यह नहीं आँकता कि स्वीकृति वैध थी या आवेदन स्वीकार होना चाहिए था। जो तिथि पढ़ी नहीं जा सकती वह अलग निष्कर्ष के रूप में रिपोर्ट होती है, चुपचाप छोड़ी नहीं जाती। |
| वचनबद्ध पूर्णता तिथि का कॉलम खाली हो तो क्या होता है — और क्या विधिक समय-सीमा कॉलम भी जाँचा जाता है? | `PR-003` स्वयं को `skipped` में दर्ज करता है: कोई दिन-संख्या अंदर नहीं बसाई गई, क्योंकि विधिक अवधि कार्य-दिवसों में गिनी जाती है, बढ़ाई जा सकती है, और सुनवाई या विशेषज्ञ-समीक्षा का समय उसमें नहीं गिना जा सकता — इसलिए एकमात्र आधार रजिस्टर में लिखी वचनबद्ध पूर्णता तिथि (`dueAt`) है। कोई नियम विधिक समय-सीमा (`legalDays`) कॉलम नहीं पढ़ता। `dueAt` भरा होने पर नियम जाँचता है कि निर्णय तिथि स्वीकृति और उस तिथि के बीच पड़ती है; निष्कर्ष का अर्थ है «यह आपकी दर्ज समय-सीमा से मेल नहीं खाता», कभी «यह देर से हुआ» नहीं। |
| मैंने परिणाम «सुधार के बाद अनुमति» जैसा दर्ज किया — क्या यह स्वीकार्य है? | `PR-004` निर्णय-परिणाम की तुलना उसके `values` पैरामीटर के शब्द-भंडार से करता है, और वह पैरामीटर खाली आता है — इसलिए जैसा दिया गया है वैसा ही नियम आपकी शब्दावली आँकने के बजाय स्वयं को `skipped` में दर्ज करता है। `values` में अपनी संस्था के दर्ज परिणाम भरें और सूची से बाहर का कोई भी मान रिपोर्ट होगा। नियम केवल यह जाँचता है कि मान सूची में है या नहीं; यह नहीं आँकता कि निर्णय सही या वैध है। |
| कोई रिकॉर्ड «अनुमति» कहता है, पर लाइसेंस-संख्या कॉलम खाली है। | `PR-005` इसे रिपोर्ट करता है: जब निर्णय-परिणाम किसी अनुमति-चिह्न से मेल खाता है — `conditionValues`, जिसका डिफ़ॉल्ट समुच्चय कॉन्फ़िगरेशन में दिया है — तो रिकॉर्ड में उसकी लाइसेंस संख्या (`certificateNo`) होनी चाहिए। यह केवल यह जाँचता है कि संख्या भरी है, यह नहीं कि प्रमाणपत्र असली, वैध या वितरित है। यदि कोई पंक्ति अनुमति-चिह्न से मेल नहीं खाती, तो नियम स्वयं को `skipped` में दर्ज करता है। |
| वही विषय दो पंक्तियों में आता है। | `PR-007` बाद की पंक्ति रिपोर्ट करता है और बताता है कि वह किस पंक्ति की पुनरावृत्ति है, क्योंकि एक ही विषय का दो बार पंजीकरण समय-सीमा जाँच को अस्पष्ट बना देता है। यह केवल विशिष्टता जाँचता है, और निष्कर्ष के लिए मानवीय पुष्टि चाहिए: एक परियोजना कई विषयों के लिए आवेदन कर सकती है, इसलिए पंक्ति हटाने के बजाय सामग्री कॉलम में अंतर स्पष्ट करें। रिक्त स्थान के अंतर नज़रअंदाज़ होते हैं; विषय कॉलम न होने पर नियम स्वयं को `skipped` में दर्ज करता है। |

## जिन मानकों का पालन होता है

| दस्तावेज़ | संख्या | इसे उद्धृत करने वाले नियम |
|---|---|---|
| जनवादी गणराज्य चीन का प्रशासनिक लाइसेंस कानून | वर्तमान संस्करण और अनुच्छेद संख्या इस बार सत्यापित नहीं | PR-001, PR-002, PR-005, PR-006, PR-007 |
| प्रत्येक विषय की सेवा-गाइड और वचनबद्ध समय-सीमा (संस्थागत कॉन्फ़िगरेशन) | कोई राष्ट्रीय मानक नहीं (आधार रजिस्टर में लिखी वचनबद्ध पूर्णता तिथि है) — ⚠️ विधिक ऊपरी सीमा प्रशासनिक लाइसेंस कानून के अनुच्छेद 42 में है; यह नियम उसे उद्धृत नहीं करता | PR-003 |
| इस संस्था की लाइसेंस-प्रबंधन नीति (संस्थागत कॉन्फ़िगरेशन) | कोई राष्ट्रीय मानक नहीं (आधार संस्था का परिणाम-शब्दभंडार है) — ⚠️ विधिक निर्णय-प्रकार अनुच्छेद 38 में हैं; यह नियम उन्हें उद्धृत नहीं करता | PR-004 |

**सीमा:** यह प्लगइन एक **प्रशासनिक लाइसेंस रजिस्टर** को उस बंद चक्र पर जाँचता है जो रजिस्टर से अपेक्षित है — प्रत्येक सामग्री का जमा होना दर्ज हो, स्वीकृति निर्णय के बाद न हो, निर्णय स्वीकृति और वचनबद्ध पूर्णता तिथि के बीच हो, परिणाम आपके शब्द-भंडार से हो, अनुमति में लाइसेंस संख्या दर्ज हो, रजिस्टर आवेदक और विषय बताए, और विषय दो बार दर्ज न हों। यह **नहीं** तय करता कि लाइसेंस निर्णय वैध था, सामग्री पूर्ण या अनुरूप थी, आवेदन स्वीकार होना चाहिए था, या लाइसेंस दिया जाना चाहिए था।

> ### ⚠️ जिन बातों पर यह प्लगइन जानबूझकर निर्णय नहीं देता
>
> **यह नहीं जाँचता कि सामग्री सूची पूर्ण है।** यह रजिस्टर के **अपने** सामग्री कॉलम को पढ़ता है और जाँचता है कि सूचीबद्ध प्रत्येक मद अपना जमा होना दर्ज करती है — **यह नहीं** कि वह सूची विषय की सेवा-गाइड से मेल खाती है। सूची सत्यापित करने का अर्थ उसकी गाइड से तुलना है, जो यह प्लगइन नहीं करता।
>
> **कोई विधिक अवधि अंदर नहीं बसाई गई — और कानून ही बताता है कि यही सही है।** प्रशासनिक लाइसेंस कानून शब्दशः पढ़ा गया (देखें `rules/evidence/clause-verification.md`), और उसके तीन प्रावधान अंदर बसाए किसी अंक को अव्यवहार्य बनाते हैं: **अनुच्छेद 82 कहता है कि विधिक अवधि कार्य-दिवसों में गिनी जाए, सार्वजनिक अवकाश छोड़कर**; अनुच्छेद 42 बीस दिन और दस दिन की वृद्धि देता है (संयुक्त निपटान में पैंतालीस और पंद्रह); और अनुच्छेद 45 सुनवाई, परीक्षण, निरीक्षण और विशेषज्ञ-समीक्षा का समय पूरी तरह बाहर रखता है। रजिस्टर सामान्यतः कैलेंडर तिथियाँ दर्ज करता है, इसलिए `PR-003` निर्णय तिथि की तुलना **रजिस्टर में लिखी वचनबद्ध पूर्णता तिथि** से करता है, और उस कॉलम के खाली होने पर स्वयं को `skipped` में दर्ज करता है। निष्कर्ष का अर्थ «यह आपकी दर्ज समय-सीमा से मेल नहीं खाता» है, «यह देर से हुआ» कभी नहीं।
>
> ⚠️ **पढ़ा गया पाठ 2003 का अधिनियमन था**; 2019 का संशोधन मौजूद है और **नहीं मिला**, इसलिए पैक प्रत्येक नियम पर यह टिप्पणी रखता है कि वर्तमान संस्करण और अनुच्छेद संख्या सत्यापित नहीं, और यह नहीं कहता कि कोई अनुच्छेद वर्तमान कानून है।
>
> **परिणाम-शब्दभंडार खाली आता है।** अनुमति, अस्वीकृति और समाप्ति की शब्दावली संस्था और विषय के अनुसार बदलती है, इसलिए `PR-004` कॉन्फ़िगर करने तक स्वयं को `skipped` में दर्ज करता है, और `PR-005` (जो अनुमति दर्ज होते ही लाइसेंस संख्या चाहता है) अंदर बसाई सूची के बजाय कॉन्फ़िगर करने योग्य अनुमति-चिह्न समुच्चय का उपयोग करता है।
>
> **नियम पैक का प्रत्येक `excerpt` स्पष्ट शब्दों में कहता है कि प्रावधान का पाठ नहीं मिला।** व्यवस्था प्रशासनिक लाइसेंस कानून और प्रत्येक विषय की सेवा-गाइड में है। सत्यापन चरण शब्दशः पाठ नहीं ला सका, इसलिए पैक यह कमी `excerpt` फ़ील्ड में ही लिखता है और प्रत्येक नियम `warn` या `info` पर रखता है। **पाठ मिलने पर प्रत्येक `excerpt` को वास्तविक प्रावधान से बदलें और `kind` को `direct` तक उठाएँ।**

## कॉन्फ़िगरेशन

सभी समायोज्य `src/config.ts` में Schemastery `Config` फ़ील्ड हैं (cordis.yml से बदले जा सकते हैं); प्रति-नियम सीमाएँ `rules/` के नियम पैक में रहती हैं। id-आधारित ओवरराइड पूरी पंक्ति बदल देता है — ज़रूरी सभी कुंजियाँ दोबारा लिखें।

| कुंजी | प्रकार | डिफ़ॉल्ट | विवरण |
|---|---|---|---|
| `rulesFile` | string | `rules/permit-report-check.yaml` | नियम-पैक पथ, पैकेज रूट के सापेक्ष |
| `disabledRules` | string[] | `[]` | जिन नियम id को रोकना है; प्रत्येक `skipped` में दिखेगा |
| `onlyRules` | string[] | `[]` | केवल ये नियम id चलाएँ; खाली होने पर सभी चलेंगे |
| `skipNotes` | string | `""` | प्रत्येक `skipped` कारण के साथ जोड़ी जाने वाली टिप्पणी |
| `timeoutMs` | number | `120000` | टूल का सहयोगात्मक टाइमआउट बजट |

जानने योग्य प्रति-नियम पैरामीटर:

- `PR-001` `conditionField` / `requiredFields` — कौन-सा कॉलम शर्त शुरू करता है: भरी सामग्री सेल जमा-कॉलम माँगती है।
- `PR-003` `notAfterField` — `dueAt` (वचनबद्ध पूर्णता तिथि) से तुलना; प्लगइन कभी दिन-संख्या से समय-सीमा नहीं निकालता।
- `PR-004` `values` — आपका निर्णय-परिणाम शब्दभंडार; खाली अर्थ है कोई जाँच नहीं। उदाहरण रूप:

```yaml
values: [granted, refused, not accepted, terminated, granted after correction]
```

- `PR-005` `conditionValues` — अनुमति दर्शाने वाले मान। साथ भेजा डिफ़ॉल्ट समुच्चय यह है:

```text
准予 / 准予许可 / 通过 / 同意 / 已办结 / 批准
```

- `PR-006` `fields` — हेडर में होने वाले फ़ील्ड, डिफ़ॉल्ट `[applicant, matter]`; यदि आपका फ़ॉर्म काउंटर भी दर्ज करता है तो `window` जोड़ें।
- `PR-007` `field` — जिस कॉलम की विशिष्टता चाहिए, डिफ़ॉल्ट विषय कॉलम (`permitType`)।

प्रोफ़ाइल पैच में ओवरराइड का उदाहरण:

```yaml
- insert:
    - id: dsh-permit-report-check
      name: dsh-permit-report-check
      config:
        disabledRules: [PR-004]
        timeoutMs: 180000
```

## सामग्री प्रारूप

टूल JSON या YAML स्वीकार करता है:

```yaml
applicant: 某某公司
matter: 某某建设项目环评审批
window: 综合受理窗口
rows:
  - { 序号: '1', 许可事项: 建设项目环境影响评价文件审批, 许可机关: 某某生态环境局,
      法定依据: 《中华人民共和国环境影响评价法》第二十二条,
      申请材料: 环境影响报告书全本及公众参与说明,
      已提交材料: 已提交报告书全本（含公众参与说明），受理编号 SL-2026-018,
      受理日期: 2026-03-02, 法定时限: '60', 承诺办结日: 2026-04-30,
      决定日期: 2026-04-20, 决定结果: 准予, 许可证号: 某环审〔2026〕18 号, 承办人: 王工 }
```

कॉलम नाम बड़े-छोटे अक्षर का भेद किए बिना और रिक्त स्थान, अंडरस्कोर तथा हाइफ़न छोड़कर मिलाए जाते हैं; रजिस्टर के अपने कॉलम नाम सुरक्षित रहते हैं, इसलिए निष्कर्ष वही कॉलम बताता है जो उसने पढ़ा। फ़ील्ड पढ़ने की परत में वैकल्पिक हैं और जाँच इंजन उन्हें सत्यापित करता है, इसलिए आंशिक निर्यात «मद छूटी» प्रकार के अंतर देता है, टूल टूटता नहीं।

## नियमों के स्रोत

नियम डेटा `rules/permit-report-check.yaml` में रहता है, कोड से अलग: प्रत्येक नियम में दस्तावेज़, संख्या, स्रोत की अपनी क्रम-प्रणाली के अनुसार अनुच्छेद संख्या, शब्दशः उद्धरण और स्रोत URL होते हैं। पैक का हेडर उद्धरण की कमी पूरी तरह बताता है और प्रत्येक नियम का `note` उससे जुड़ा भाग दोहराता है। लोड-समय का गार्ड सामान्यतः «उद्धरण कम से कम आठ अक्षरों का वास्तविक उद्धरण हो» लागू करता है, पर वह उद्धरण और विवरण में भेद नहीं कर सकता — इसलिए यह पैक हेडर, प्रति-नियम `note` और उस टेस्ट पर टिकता है जो सुनिश्चित करता है कि प्रत्येक `excerpt` इस कमी को स्वीकारता है। अपना आधार बढ़ा-चढ़ाकर बताने वाला पैक लोड पर विफल होता है, ठोस दिखने वाली रिपोर्ट नहीं बनाता। सत्यापन में तय सीमाएँ और जानबूझकर न निकाले गए निष्कर्ष `rules/evidence/` में साथ आते हैं।

## FAQ

<details>
<summary>क्या यह हमारे लिए अनुमति या अस्वीकृति तय करेगा?</summary>

नहीं। यह केवल वे अंतर गिनाता है जिन्हें सामग्री के भीतर इंगित किया जा सके (कौन-सी पंक्ति, कौन-सा कॉलम, क्या छूटा), कोई तथ्य-निर्णय नहीं देता और वैधता नहीं आँकता — लाइसेंस का निर्णय अनुमोदक के पास ही रहता है। शब्दावली-गार्ड रिपोर्ट का रूप सीमित करता है और प्रत्येक रिपोर्ट में अस्वीकरण रहता है।

</details>

<details>
<summary>मेरा रजिस्टर Excel में है — क्या सीधे उपयोग कर सकता हूँ?</summary>

हाँ: पहले उसे JSON या YAML में बदलें; जहाँ प्लेटफ़ॉर्म समर्थन दे वहाँ रूपांतरण चैट में भी हो सकता है। टूल केवल सामग्री पढ़ता है और मूल कभी नहीं बदलता।

</details>

<details>
<summary>विधिक अवधि के दिन अंदर क्यों नहीं बसाए गए?</summary>

क्योंकि कानून ही अंदर बसाए अंक को अव्यवहार्य बनाता है: अनुच्छेद 82 अवधि कार्य-दिवसों में गिनने को कहता है (सार्वजनिक अवकाश छोड़कर), अनुच्छेद 42 बीस दिन और दस दिन की वृद्धि देता है (संयुक्त निपटान में पैंतालीस और पंद्रह), और अनुच्छेद 45 सुनवाई, परीक्षण, निरीक्षण तथा विशेषज्ञ-समीक्षा का समय अवधि से बाहर रखता है। रजिस्टर सामान्यतः कैलेंडर तिथियाँ रखता है, इसलिए `PR-003` केवल रजिस्टर में लिखी वचनबद्ध पूर्णता तिथि (`dueAt`) से तुलना करता है; वह कॉलम खाली होने पर नियम आपके लिए समय-सीमा मानने के बजाय `skipped` में चला जाता है।

</details>

<details>
<summary>क्या खाली `issues` सूची को «कुछ गलत नहीं» माना जा सकता है?</summary>

नहीं। जो जाँच नहीं चल सकी वह `skipped` में कारण के साथ है (वचनबद्ध पूर्णता तिथि खाली, `values` सेट नहीं, नियम बंद)। रिपोर्ट पढ़ते समय `issues` और `skipped` दोनों देखें।

</details>

<details>
<summary>क्या यह नेटवर्क पर जाता है या रजिस्टर अपलोड करता है? कितना भार है?</summary>

कोई नेटवर्क नहीं, कोई मॉडल कॉल नहीं, कोई फ़ाइल लेखन नहीं: पढ़ना, तुलना और तिथि-गणित सब स्थानीय हैं, और सामग्री केवल टूल आर्ग्युमेंट से आती है। पूरी तिमाही के रजिस्टर या पूरी निर्देशिका के लिए `ptc` मोड schema लागत एक ही बार देता है; `timeoutMs` (डिफ़ॉल्ट 120000 मिसे) सहयोगात्मक टाइमआउट बजट है।

</details>

## समस्या निवारण

- **प्लगइन इंस्टॉल हुआ पर टूल दिखता नहीं।** जाँचें कि `main` `lib/index.mjs` पर जाता है और `pnpm run build` ने उसे बनाया है; गलत `main` लोडर को प्रविष्टि चुपचाप छोड़ने देता है।
- **`dsh plugin add` पैकेज को असंगत कहकर मना करता है।** peer श्रेणी `0.1.x` और `0.2.x` को कवर करती है; यदि आपका रनटाइम उससे बाहर है तो स्पष्ट छूट दें: `dsh plugin --profile <name> allow-version dsh-permit-report-check@0.1.0 --dsh-version <runtime> --accept-risk`
- **`check` में `manifest-peers` विफल आता है।** स्थिर जाँचकर्ता 0.2 श्रृंखला से पुरानी कठोर-कोडित peer श्रेणी से तुलना करता है। रनटाइम इंस्टॉल के समय peer संगतता लागू करता है, इसलिए घोषित श्रेणी सही है; यह `dsh-plugin-dev` की ज्ञात अपस्ट्रीम समस्या है।
- **कोई नियम नहीं चला।** `skipped` सरणी देखें; वह नियम id और कारण बताती है।
- **इंस्टॉल हुआ पर कोई निष्कर्ष नहीं दिखता।** पुष्टि करें कि टूल वास्तव में चला और परिणाम लौटाया — खाली परिणाम «छोड़ी गई जाँच» के बराबर नहीं; फिर नियम तालिका के अनुसार सामग्री के कॉलम नाम देखें, क्योंकि अनुपस्थित इनपुट सामान्यतः `skipped` बनता है, अनुमानित निष्कर्ष नहीं।
- **`PR-003` स्वयं को `skipped` में दर्ज करता है।** रजिस्टर में वचनबद्ध पूर्णता तिथि नहीं लिखी। अवधि विषय के अनुसार बदलती है और बढ़ाई जा सकती है, इसलिए प्लगइन अपनी ओर से एक नहीं गढ़ता।
- **`PR-003` आगा पर मुझे लगता है निपटान समय पर था।** निष्कर्ष का अर्थ है कि निर्णय तिथि रजिस्टर में दर्ज वचनबद्ध पूर्णता तिथि से मेल नहीं खाती — या समय-सीमा गलत निकाली गई, या निर्णय तिथि गलत है।
- **`PR-001` ने छूटी सामग्री नहीं पकड़ी।** यह रजिस्टर की अपनी सूची जाँचता है, सेवा-गाइड की नहीं; सूची पूर्ण है या नहीं — यह वह तुलना है जो यह प्लगइन नहीं करता।
- **`PR-004` कभी नहीं चलता।** उसका शब्दभंडार खाली आता है; अपनी संस्था के दर्ज परिणाम `values` में भरें।
- **`PR-005` अनुमति वाले रिकॉर्ड पर बिना लाइसेंस संख्या के आगा।** या तो लाइसेंस अभी जारी नहीं हुआ, या कॉलम भरना छूटा। यदि आपका रजिस्टर दूसरी अनुमति-शब्दावली रखता है तो `conditionValues` सँकरा करें।
- **किसी निष्कर्ष में कहा गया है कि प्रावधान का पाठ नहीं मिला।** नियम पैक में उद्धरण-द्वार है और वह कभी पाठ नहीं गढ़ता; पाठ उपलब्ध न होने पर निष्कर्ष `warn`/`info` पर रहता है और `excerpt` में यह बताता है। इसे सत्यापन की कमी मानें, सामग्री के अनुरूप होने का प्रमाण नहीं।
- **सभी निष्कर्ष केवल `warn` या `info` हैं।** रचना से ऐसा है — यह जाँचकर्ता विधिक निर्धारण नहीं करता; यह अंतर बताता है और क्या करना है यह व्यक्ति तय करता है।
- **समय खिसका हुआ लगता है।** सारी गणना इनपुट स्ट्रिंग्स पर वॉल-क्लॉक है; कोई टाइमज़ोन रूपांतरण नहीं होता।

## संगतता

| सतह | स्थिति |
|---|---|
| Harness | peer श्रेणी `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — `0.2.0-rc.2` और `0.2.1-rc.2` दोनों पर सत्यापित। `engines.dsh` `>=0.2.1-0 <0.3.0` घोषित है और 0.2.1 से होस्ट इसे लागू करता है |
| Node | `^22.19.0 \|\| >=24.0.0` |
| प्लेटफ़ॉर्म | सभी (शुद्ध ESM; कोई नेटिव कोड नहीं, कोई नेटवर्क नहीं, कोई मॉडल कॉल नहीं) |
| टूल मोड | `native` और `ptc` दोनों में चलता है; पूरी निर्देशिका के लिए `ptc` |

**अंतर-संचालनीयता**: पैकेज ठीक एक क्षमता घोषित करता है, `tools:register` (`package.json#dsh.capabilities`), एक ही नेमस्पेस वाला टूल `permit_report_check` पंजीकृत करता है, कोई service key नहीं देता, कोई क्लाइंट slot या `webServer` उपसर्ग पंजीकृत नहीं करता, और उसका bundle patch केवल अपनी पंक्ति `insert` करता है — किसी अंतर्निहित पंक्ति की `config` कभी नहीं बदलता। इसलिए यह अन्य प्लगइन से टूल नाम, service key, slot या HTTP रूट पर नहीं टकराता।

## पारिस्थितिकी और गुणवत्ता

- [Gitee मिरर](https://gitee.com/perrylink/dsh-permit-report-check) (समकालिक मिरर; मानक GitHub है)
- [dshfind प्लगइन पृष्ठ](https://dshfind.com/plugins/PerryLink/dsh-permit-report-check) (इंस्टॉल और रैंकिंग)
- [OpenSSF Scorecard रिपोर्ट](https://securityscorecards.dev/viewer/?uri=github.com/PerryLink/dsh-permit-report-check) ([.github/workflows/scorecard.yml](.github/workflows/scorecard.yml) से संचालित)
- [DSH Market](https://dsh.market/) (सूचीबद्ध)
- **1024 स्टोर चैनल**: एक बार `npm i -g dsh1024`, फिर `dsh1024 plugin --profile <name> add dsh-permit-report-check` ([deepseek1024.com](https://deepseek1024.com) की इंस्टॉल रैंकिंग में गिना जाता है)
- [पारिस्थितिकी ज्ञान-आधार](https://perrylink.github.io/dsh-plugin-guide/) — मापा गया डेटा, विपणन नहीं: प्लगइन विकास मार्गदर्शिका · चयन डेटा · रखरखाव के मानदंड

## विकास

```sh
pnpm install                                        # node ^22.19 || >=24
pnpm run typecheck                                  # tsc --noEmit
pnpm test                                           # vitest: साझा टेबल-प्लगइन सूट + युग्मित फ़िक्स्चर
pnpm run build                                      # tsdown -> lib/index.mjs + lib/index.d.mts
pnpm run verify:self-contained                      # निर्भरताएँ registry से हल होती हैं
pnpm run check:lockfile                             # lockfile विचलन जाँच
pnpm run check:readmes                              # पाँच-भाषा README संगति
pnpm run check:citations                            # नियम-पैक उद्धरण आधाररेखा
node ../scripts/sync-shared.mjs dsh-permit-report-check   # ../_shared से src/shared ताज़ा करें
pnpm pack                                           # प्रकाशित tarball
```

प्लगइन **केवल-डेटा** है: `src/model.ts` तालिका का आकार घोषित करता है, साझा किट पढ़ने वाला और जाँच इंजन देता है, और नियम पैक प्रत्येक जाँच घोषित करता है; मौजूदा प्रकार में फ़िट होने वाली जाँच के लिए केवल नियम पैक बदलना होता है। स्थानीय नमूना (पहले `pnpm run build`):

```sh
node samples/quickstart/run.mjs --json
# => {"tool":"permit_report_check","issueCount":1,"summary":{"error":0,"warn":1,"info":0},"skippedCount":1}
```

नमूना इनपुट `samples/quickstart/input/` में, अपेक्षित आउटपुट `samples/quickstart/expected/result.json` में और स्क्रीनशॉट `docs/assets/quickstart.png` में है। README की छवियाँ [`scripts/gen-readme-assets.py`](scripts/gen-readme-assets.py) (Python + Pillow) से प्रोग्रामेटिक रूप से बनती हैं और दोबारा चलाई जा सकती हैं: `python scripts/gen-readme-assets.py`; पुराना एकल-संस्करण प्रवाह चित्र और डेमो छवियाँ बाहरी लिंक के लिए `docs/assets/` में रहती हैं, जबकि README केवल नया लाइट/डार्क जोड़ा संदर्भित करते हैं।

Topics: `deepseek-harness`, `dsh`, `dsh-plugin`, `cordis`, `permit`, `report`

## परिवार और आभार

यह परियोजना [PerryLink](https://github.com/PerryLink) द्वारा संभाले जाने वाले DeepSeek Harness प्लगइन परिवार का सदस्य है (सभी Apache-2.0)। पूरा सूचकांक [सामग्री के अनुसार जाँचक चुनें](https://perrylink.github.io/zh/checkers/choose/) पर है। अगर यह उपयोगी लगे तो **एक star अगले व्यक्ति को इसे खोजने में मदद करता है** — इसके पीछे कुछ भी बंद नहीं है।

- [@PerryLink](https://github.com/PerryLink) — निर्माता और अनुरक्षक: केवल-डेटा नियम पैक (PR-001..PR-007), `permit_report_check` टूल, उद्धरण-सत्यापन रिकॉर्ड (`rules/evidence/`) और पाँच-भाषा दस्तावेज़।

<details>
<summary>सभी प्लगइन विस्तारित करें</summary>

| प्लगइन | स्थिति |
|---|---|
| **[dsh-aqua-input-check](https://github.com/PerryLink/dsh-aqua-input-check)** |  |
| **[dsh-archive-check](https://github.com/PerryLink/dsh-archive-check)** |  |
| **[dsh-auto-review](https://github.com/PerryLink/dsh-auto-review)** |  |
| **[dsh-autotier](https://github.com/PerryLink/dsh-autotier)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-bid-ca-precheck](https://github.com/PerryLink/dsh-bid-ca-precheck)** |  |
| **[dsh-bid-qual-check](https://github.com/PerryLink/dsh-bid-qual-check)** |  |
| **[dsh-cert-mcp](https://github.com/PerryLink/dsh-cert-mcp)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-checkpoint-rewind](https://github.com/PerryLink/dsh-checkpoint-rewind)** |  |
| **[dsh-click](https://github.com/PerryLink/dsh-click)** |  |
| **[dsh-composer-history](https://github.com/PerryLink/dsh-composer-history)** |  |
| **[dsh-contract-stance](https://github.com/PerryLink/dsh-contract-stance)** |  |
| **[dsh-customs-doc-check](https://github.com/PerryLink/dsh-customs-doc-check)** |  |
| **[dsh-data-quality](https://github.com/PerryLink/dsh-data-quality)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-demurrage-ledger](https://github.com/PerryLink/dsh-demurrage-ledger)** |  |
| **[dsh-doublecheck](https://github.com/PerryLink/dsh-doublecheck)** |  |
| **[dsh-drill-script-check](https://github.com/PerryLink/dsh-drill-script-check)** |  |
| **[dsh-eia-guide-check](https://github.com/PerryLink/dsh-eia-guide-check)** |  |
| **[dsh-emergency-plan](https://github.com/PerryLink/dsh-emergency-plan)** |  |
| **[dsh-essay-rubric-check](https://github.com/PerryLink/dsh-essay-rubric-check)** |  |
| **[dsh-evidence-check](https://github.com/PerryLink/dsh-evidence-check)** |  |
| **[dsh-export-ctl-check](https://github.com/PerryLink/dsh-export-ctl-check)** |  |
| **[dsh-fast](https://github.com/PerryLink/dsh-fast)** |  |
| **[dsh-fmea-table-check](https://github.com/PerryLink/dsh-fmea-table-check)** |  |
| **[dsh-forecast-penalty](https://github.com/PerryLink/dsh-forecast-penalty)** |  |
| **[dsh-fund-research](https://github.com/PerryLink/dsh-fund-research)** |  |
| **[dsh-github](https://github.com/PerryLink/dsh-github)** |  |
| **[dsh-gongwen-flow-check](https://github.com/PerryLink/dsh-gongwen-flow-check)** |  |
| **[dsh-gongwen-word-check](https://github.com/PerryLink/dsh-gongwen-word-check)** |  |
| **[dsh-guard-plan-qc](https://github.com/PerryLink/dsh-guard-plan-qc)** |  |
| **[dsh-hazchem-check](https://github.com/PerryLink/dsh-hazchem-check)** |  |
| **[dsh-hazplan-check](https://github.com/PerryLink/dsh-hazplan-check)** |  |
| **[dsh-hidden-risk-map](https://github.com/PerryLink/dsh-hidden-risk-map)** |  |
| **[dsh-hs-classify](https://github.com/PerryLink/dsh-hs-classify)** |  |
| **[dsh-icd-rule-check](https://github.com/PerryLink/dsh-icd-rule-check)** |  |
| **[dsh-industry-research](https://github.com/PerryLink/dsh-industry-research)** |  |
| **[dsh-lawcite-adapter](https://github.com/PerryLink/dsh-lawcite-adapter)** |  |
| **[dsh-laya](https://github.com/PerryLink/dsh-laya)** |  |
| **[dsh-lc-doc-check](https://github.com/PerryLink/dsh-lc-doc-check)** |  |
| **[dsh-learning-gap-check](https://github.com/PerryLink/dsh-learning-gap-check)** |  |
| **[dsh-library](https://github.com/PerryLink/dsh-library)** |  |
| **[dsh-local-ai](https://github.com/PerryLink/dsh-local-ai)** |  |
| **[dsh-lsp-actions](https://github.com/PerryLink/dsh-lsp-actions)** |  |
| **[dsh-mask](https://github.com/PerryLink/dsh-mask)** |  |
| **[dsh-mcp-panel](https://github.com/PerryLink/dsh-mcp-panel)** |  |
| **[dsh-medrec-qc](https://github.com/PerryLink/dsh-medrec-qc)** |  |
| **[dsh-memento](https://github.com/PerryLink/dsh-memento)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-nsfc-form-check](https://github.com/PerryLink/dsh-nsfc-form-check)** |  |
| **[dsh-nurse-record-check](https://github.com/PerryLink/dsh-nurse-record-check)** |  |
| **[dsh-observe](https://github.com/PerryLink/dsh-observe)** |  |
| **[dsh-origin-rvc-check](https://github.com/PerryLink/dsh-origin-rvc-check)** |  |
| **[dsh-ota-review-check](https://github.com/PerryLink/dsh-ota-review-check)** |  |
| **[dsh-output-styles](https://github.com/PerryLink/dsh-output-styles)** |  |
| **[dsh-paper-doc-adapter](https://github.com/PerryLink/dsh-paper-doc-adapter)** |  |
| **[dsh-permission-rules](https://github.com/PerryLink/dsh-permission-rules)** |  |
| **[dsh-permit-report-check](https://github.com/PerryLink/dsh-permit-report-check)** |  |
| **[dsh-pipeline-check](https://github.com/PerryLink/dsh-pipeline-check)** |  |
| **[dsh-pleading-draft](https://github.com/PerryLink/dsh-pleading-draft)** |  |
| **[dsh-plugin-doctor](https://github.com/PerryLink/dsh-plugin-doctor)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
| **[dsh-plugin-guide](https://github.com/PerryLink/dsh-plugin-guide)** |  |
| **[dsh-plugin-kit](https://github.com/PerryLink/dsh-plugin-kit)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
| **[dsh-plugin-upgrade](https://github.com/PerryLink/dsh-plugin-upgrade)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
| **[dsh-policy-brief-draft](https://github.com/PerryLink/dsh-policy-brief-draft)** |  |
| **[dsh-power-loss-split](https://github.com/PerryLink/dsh-power-loss-split)** |  |
| **[dsh-power-ticket-check](https://github.com/PerryLink/dsh-power-ticket-check)** |  |
| **[dsh-ppap-check](https://github.com/PerryLink/dsh-ppap-check)** |  |
| **[dsh-protest-deadline](https://github.com/PerryLink/dsh-protest-deadline)** |  |
| **[dsh-railway-window](https://github.com/PerryLink/dsh-railway-window)** |  |
| **[dsh-repair-order-qc](https://github.com/PerryLink/dsh-repair-order-qc)** |  |
| **[dsh-research-report](https://github.com/PerryLink/dsh-research-report)** |  |
| **[dsh-review-reply-check](https://github.com/PerryLink/dsh-review-reply-check)** |  |
| **[dsh-rulefile-check](https://github.com/PerryLink/dsh-rulefile-check)** |  |
| **[dsh-safety-brief-check](https://github.com/PerryLink/dsh-safety-brief-check)** |  |
| **[dsh-score](https://github.com/PerryLink/dsh-score)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-session-sync](https://github.com/PerryLink/dsh-session-sync)** |  |
| **[dsh-site-log-check](https://github.com/PerryLink/dsh-site-log-check)** |  |
| **[dsh-skill-pack-security](https://github.com/PerryLink/dsh-skill-pack-security)** |  |
| **[dsh-soe-decision-check](https://github.com/PerryLink/dsh-soe-decision-check)** |  |
| **[dsh-soilwater-check](https://github.com/PerryLink/dsh-soilwater-check)** |  |
| **[dsh-sop-sync-check](https://github.com/PerryLink/dsh-sop-sync-check)** |  |
| **[dsh-spc-gbt-adapter](https://github.com/PerryLink/dsh-spc-gbt-adapter)** |  |
| **[dsh-talk](https://github.com/PerryLink/dsh-talk)** |  |
| **[dsh-tender-extract](https://github.com/PerryLink/dsh-tender-extract)** |  |
| **[dsh-tender-matrix](https://github.com/PerryLink/dsh-tender-matrix)** |  |
| **[dsh-test-drive](https://github.com/PerryLink/dsh-test-drive)** |  |
| **[dsh-ticktick](https://github.com/PerryLink/dsh-ticktick)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
| **[dsh-translate](https://github.com/PerryLink/dsh-translate)** |  |
| **[dsh-warranty-calc](https://github.com/PerryLink/dsh-warranty-calc)** |  |
| **[dsh-budget](https://github.com/PerryLink/dsh-budget)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-claude-move](https://github.com/PerryLink/dsh-claude-move)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-defend](https://github.com/PerryLink/dsh-defend)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-draw](https://github.com/PerryLink/dsh-draw)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-reach](https://github.com/PerryLink/dsh-reach)** | 🧊 फ़्रोज़न — रेपो README देखें |
| **[dsh-background-agents](https://github.com/PerryLink/dsh-background-agents)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
| **[dsh-session-pin](https://github.com/PerryLink/dsh-session-pin)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |
| **[dsh-team-rooms](https://github.com/PerryLink/dsh-team-rooms)** | 🚫 रिटायर्ड (रेपो संग्रहीत) |

</details>

## License

[LICENSE](LICENSE) (Apache License 2.0) © 2026 dsh-permit-report-check contributors

<p align="center"><sub>Apache-2.0 · सामुदायिक प्लगइन, DeepSeek से संबद्ध नहीं।</sub></p>
