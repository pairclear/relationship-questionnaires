#!/usr/bin/env python3
"""Validate the questionnaires and build generated files. Run: python3 build.py

Sources:  data/questionnaires/*.json, data/questionnaires/_common.json, data/validated-scales.json, src/template.html
Outputs:  questionnaires/<id>.en.md, questionnaires/<id>.ru.md, data/questionnaires.json, docs/licence-check.md, index.html
"""
import json, pathlib

ROOT = pathlib.Path(__file__).parent
QDIR = ROOT / "data/questionnaires"
UTM = "utm_source=github&utm_medium=readme&utm_campaign=relationship-questionnaires"
LANGS = ("en", "ru")

common = json.loads((QDIR / "_common.json").read_text(encoding="utf-8"))
scales = json.loads((ROOT / "data/validated-scales.json").read_text(encoding="utf-8"))
ORDER = ["couple-pulse", "conflict-pattern", "contact-changes", "effort-balance",
         "relationship-clarity", "mental-load", "after-breakup"]


def utm(url, medium="readme"):
    return url + ("&" if "?" in url else "?") + UTM.replace("utm_medium=readme", "utm_medium=" + medium)


def check(q):
    subs = {s["id"] for s in q["subscales"]}
    ids = set()
    for it in q["items"]:
        assert it["id"] not in ids, (q["id"], it["id"])
        ids.add(it["id"])
        assert it["sub"] in subs or it.get("flag") == "safety", (q["id"], it["id"])
        for l in LANGS:
            assert it[l].strip(), (q["id"], it["id"], l)
    for s in q["subscales"]:
        n = sum(1 for it in q["items"] if it["sub"] == s["id"])
        assert n >= 3, f"{q['id']}/{s['id']} has {n} items"
        for b in ("low", "mid", "high"):
            assert all(s[b][l] for l in LANGS)
    for k in ("title", "intro", "timeframe"):
        assert all(q[k][l] for l in LANGS)
    assert all(q["links"][l] for l in LANGS)


qs = []
for qid in ORDER:
    q = json.loads((QDIR / f"{qid}.json").read_text(encoding="utf-8"))
    check(q)
    q["validated"] = False
    q["licence"] = "CC BY 4.0"
    qs.append(q)
extra = sorted(p.stem for p in QDIR.glob("*.json") if not p.stem.startswith("_"))
assert set(extra) == set(ORDER), f"add new questionnaires to ORDER: {set(extra) - set(ORDER)}"

L = {
    "en": {"time": "Think about", "scale": "Answer scale", "rev": "reverse-scored", "safety": "safety question, not scored",
           "score": "Scoring", "score_txt": "Reverse the marked items (4 becomes 0, 3 becomes 1). Average the items of each part to get a 0-4 score. Under 1.5 is low, 1.5 to 2.5 is in the middle, above 2.5 is high. These are not norms or cut-offs: the questionnaire is not validated. Use the result to start a conversation, not to judge.",
           "parts": "Parts", "reflect": "Questions to think about", "more": "On PairClear", "item": "Statement", "part": "Part",
           "banner": "Self-reflection, not diagnosis. Written by PairClear, not validated in research. It measures how things go between two people, not anyone's psyche.",
           "crisis": "If you are afraid of your partner, are being threatened or controlled, or are thinking about hurting yourself: call emergency services (112 in Europe, 911 in the US and Canada) or find a free helpline at https://findahelpline.com.",
           "online": "Take it online (runs in your browser, sends nothing)"},
    "ru": {"time": "Вспомни", "scale": "Шкала ответов", "rev": "обратный пункт", "safety": "вопрос о безопасности, не считается в баллы",
           "score": "Подсчёт", "score_txt": "Переверни отмеченные пункты (4 становится 0, 3 становится 1). Посчитай среднее по пунктам каждой части: получится балл от 0 до 4. Ниже 1,5 низко, от 1,5 до 2,5 середина, выше 2,5 высоко. Это не нормы и не пороги: опросник не валидирован. Используй результат, чтобы начать разговор, а не чтобы выносить оценку.",
           "parts": "Части", "reflect": "Вопросы для размышления", "more": "На PairClear", "item": "Утверждение", "part": "Часть",
           "banner": "Саморефлексия, а не диагностика. Написано PairClear, в исследованиях не валидировано. Измеряет то, что происходит между двумя людьми, а не чью-то психику.",
           "crisis": "Если ты боишься партнёра, тебе угрожают или тебя контролируют, или есть мысли навредить себе: звони в экстренную службу (112) или найди бесплатную линию помощи на https://findahelpline.com. В России для женщин, пострадавших от насилия: 8-800-7000-600.",
           "online": "Пройти онлайн (работает в браузере, ничего не отправляет)"},
}

(ROOT / "questionnaires").mkdir(exist_ok=True)
for q in qs:
    for l in LANGS:
        t = L[l]
        sub_name = {s["id"]: s[l] for s in q["subscales"]}
        md = [f"# {q['title'][l]}", "",
              f"[{t['online']}](https://pairclear.github.io/relationship-questionnaires/?q={q['id']}&lang={l})", "",
              f"> {t['banner']}", "", q["intro"][l], "",
              f"**{t['time']}:** {q['timeframe'][l]}.", "",
              f"**{t['scale']}:** " + ", ".join(f"{i} = {x}" for i, x in enumerate(common["scale"]["labels"][l])), "",
              f"| # | {t['item']} | {t['part']} |", "|---|---|---|"]
        for i, it in enumerate(q["items"], 1):
            part = sub_name.get(it["sub"], "") if it["sub"] else f"*{t['safety']}*"
            if it.get("rev"):
                part += f" ({t['rev']})"
            md.append(f"| {i} | {it[l]} | {part} |")
        md += ["", f"## {t['score']}", "", t["score_txt"], "", f"## {t['parts']}", ""]
        for s in q["subscales"]:
            md += [f"**{s[l]}**", "", f"- low: {s['low'][l]}", f"- mid: {s['mid'][l]}", f"- high: {s['high'][l]}", ""]
        if any(it.get("flag") == "safety" for it in q["items"]):
            md += [f"> {t['crisis']}", ""]
        md += [f"## {t['reflect']}", ""] + [f"- {x}" for x in q["reflect"][l]] + ["", f"## {t['more']}", ""]
        md += [f"- [{x['title']}]({utm(x['url'])})" for x in q["links"][l]]
        md += ["", "---", "", "CC BY 4.0 · PairClear · " + ("Written with AI assistance." if l == "en" else "Написано с помощью ИИ."), ""]
        (ROOT / f"questionnaires/{q['id']}.{l}.md").write_text("\n".join(md), encoding="utf-8")

bundle = {"common": common, "questionnaires": qs}
(ROOT / "data/questionnaires.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf-8")

# docs/licence-check.md
(ROOT / "docs").mkdir(exist_ok=True)
md = ["# Licence check of validated relationship scales", "",
      f"Checked: **{scales['checked']}**. Generated from `data/validated-scales.json`.", "", scales["about"], "",
      "| Scale | Measures | What we found | Included | Why |", "|---|---|---|---|---|"]
for s in scales["scales"]:
    md.append(f"| [{s['name']}]({s['source']})<br>{s['authors']} | {s['measures']} | {s['terms_found']} | {'yes' if s['included'] else 'no'} | {s['why']} |")
md += ["", scales["also_excluded_by_policy"], ""]
(ROOT / "docs/licence-check.md").write_text("\n".join(md), encoding="utf-8")

tpl = (ROOT / "src/template.html").read_text(encoding="utf-8")
payload = json.dumps(bundle, ensure_ascii=False).replace("</", "<\\/")
(ROOT / "index.html").write_text(tpl.replace("/*DATA*/null", payload), encoding="utf-8")
print("ok:", len(qs), "questionnaires,", sum(len(q["items"]) for q in qs), "items")
