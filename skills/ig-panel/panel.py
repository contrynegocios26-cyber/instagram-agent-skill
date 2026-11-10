#!/usr/bin/env python3
"""
panel.py - the bookkeeping half of a synthetic audience panel.

A language model plays the people. This script does everything a language
model is bad at: it draws the sample, deals it into sheets, rotates the order
the posts are shown in, checks every answer came back, counts, and puts an
honest interval on the count.

What this is:  a quota sample of N simulated people built from YOUR audience
numbers, a blind answer sheet for each batch of them, and a tally that reports
ranks, head-to-heads and segment splits with the noise shown.

What this is NOT:  a forecast of reach, views or sales. Simulated people agree
with each other more than real ones do, and they are politer. So the tally
reports which option the panel preferred and how sure the panel is, never
"this will get 40,000 views". The only thing that turns a panel into evidence
is `backtest`: run it on posts you already published and see whether it ranks
them the way your real audience did.

No dependencies, no network. Nothing leaves your machine from this script.

Usage
  python3 panel.py build audience.json --n 300 --out run/panel.json
  python3 panel.py sheets run/panel.json stimuli.json --out run/
  python3 panel.py tally run/
  python3 panel.py tally run/ --json
  python3 panel.py backtest run/ --actual actual.tsv --metric "views" --save
"""

import argparse
import datetime
import hashlib
import json
import math
import os
import random
import re
import shutil
import statistics
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TRACK = os.path.expanduser("~/.claude/instagram/panel-track.json")

# The furthest thing a person did with a post, as a ladder. One answer per
# person per post keeps the sheet parseable and stops the model from handing
# everyone a like AND a save AND a follow.
LADDER = {
    "skip": 0,       # thumb never stopped
    "glance": 1,     # stopped, looked, left
    "consume": 2,    # watched most of it / swiped the slides / read the caption
    "like": 3,
    "comment": 4, "save": 4, "send": 4, "follow": 4, "profile": 4, "link": 4,
}
STRONG = ["save", "send", "comment", "follow", "profile", "link"]
ROLES = ("test", "floor", "ceiling")


def die(msg):
    sys.exit(f"panel.py: {msg}")


def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        die(f"no such file: {path}")
    except json.JSONDecodeError as e:
        die(f"{path} is not valid JSON ({e})")


# --------------------------------------------------------------------- build

def quota(weights, n):
    """Largest-remainder allocation: n seats across weighted options, exactly.

    A random draw of 300 from a 56/44 split can come back 51/49. A quota
    cannot, and the whole point of the panel is that it looks like the
    audience it was built from.
    """
    total = sum(weights.values())
    if total <= 0:
        die("a distribution has no positive weights")
    raw = {k: n * v / total for k, v in weights.items()}
    seats = {k: int(r) for k, r in raw.items()}
    left = n - sum(seats.values())
    for k in sorted(raw, key=lambda k: raw[k] - seats[k], reverse=True)[:left]:
        seats[k] += 1
    return seats


def deal(weights, n, rng):
    seats = quota(weights, n)
    out = [k for k, c in seats.items() for _ in range(c)]
    rng.shuffle(out)
    return out


def cmd_build(a):
    aud = load_json(a.audience)
    pop = load_json(a.population)
    segs = aud.get("segments") or die("audience.json needs a 'segments' list")
    for s in segs:
        if not all(k in s for k in ("id", "share", "card")):
            die("every segment needs 'id', 'share' and 'card'")
    rng = random.Random(a.seed)

    # Behaviour dimensions come from population.json, then the audience file
    # overrides or adds to them, then a segment can override again.
    base = {k: v for k, v in pop["dimensions"].items()}
    base.update(aud.get("dimensions", {}))

    seg_seats = quota({s["id"]: s["share"] for s in segs}, a.n)
    people = []
    for s in segs:
        k = seg_seats[s["id"]]
        if k == 0:
            continue
        dims = dict(base)
        dims.update(s.get("dimensions", {}))
        cols = {name: deal(w, k, rng) for name, w in dims.items()}
        for i in range(k):
            people.append({
                "segment": s["id"],
                "card": s["card"],
                "traits": {name: cols[name][i] for name in dims},
            })
    rng.shuffle(people)
    for i, p in enumerate(people, 1):
        p["pid"] = f"P{i:04d}"

    panel = {
        "account": aud.get("account", ""),
        "language": aud.get("language", "English"),
        "context": aud.get("context", ""),
        "seed": a.seed,
        "n": len(people),
        "segments": {s["id"]: s.get("label", s["id"]) for s in segs},
        "people": people,
    }
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(panel, f, ensure_ascii=False, indent=1)

    print(f"PANEL  ·  {len(people)} people  ·  seed {a.seed}  ->  {a.out}")
    print("=" * 72)
    for s in segs:
        k = seg_seats[s["id"]]
        print(f"  {k:5d}  {100 * k / a.n:5.1f}%  {s['id']}")
    for name in base:
        c = Counter(p["traits"].get(name) for p in people)
        print(f"\n  {name}")
        for val, k in c.most_common():
            print(f"  {k:5d}  {100 * k / len(people):5.1f}%  {val}")
    assumed = aud.get("assumptions")
    if assumed:
        print("\n  ASSUMED, NOT MEASURED (the panel is only as real as these):")
        for line in assumed:
            print(f"   - {line}")


# -------------------------------------------------------------------- sheets

SHEET_HEAD = """# Panel sheet {sheet:02d}  ·  {k} people  ·  {m} posts

You are running one sheet of an audience simulation. You are not a marketer,
you are not reviewing anything and nobody wants advice. Your whole job is to
be {k} different people, one at a time, each meeting {m} posts in their
Instagram feed, and to write down what each of them actually does.

Nobody on this panel knows who made these posts, which ones are being tested
or which answer anyone hopes for. Neither do you.
{context}
## How to answer

Take the people one at a time. Read the card. Then walk that person through
the posts in the order printed on this sheet, as things they scroll into
between a friend's photo and an ad.

1. **Write the thought first.** What crosses this person's mind in the first
   second, in their own words, in **{language}**, 15 words or fewer. A real
   thought, not a verdict: "ué, isso aí não empena?" and not "interesting and
   informative content".
2. **Then write what they did.** Exactly one word, the furthest they got:

   | word | meaning |
   | --- | --- |
   | `skip` | the thumb never stopped |
   | `glance` | stopped for a second, looked, moved on |
   | `consume` | took most of it in: watched, swiped the slides, read the caption |
   | `like` | consumed it and liked |
   | `save` | saved it for later |
   | `send` | sent it to a specific person |
   | `comment` | wrote a comment |
   | `follow` | followed the account |
   | `profile` | tapped through to the profile |
   | `link` | tapped the link or messaged the business |

## What real feeds are like, and this panel must be like

- **`skip` is the normal answer.** On a real feed most people pass most posts
  without stopping. If more than about a third of your rows are above
  `glance`, you have written an audience that does not exist.
- **Anything from `save` down the table is rare.** A person does one of those
  a few times a week across hundreds of posts. The card says what kind of
  user each person is. A lurker stays a lurker even when the post is good.
- **Being relevant is not the same as acting.** Someone can think "nice" and
  keep scrolling. Most people do.
- **People must differ.** The architect, the neighbour and the tired person in
  a queue do not see the same post. If your rows look alike you have written
  one person {k} times.
- **Sound is off unless the card says otherwise**, and nobody reads small text.
- A post that is bad for this person gets a blunt thought. Do not be polite on
  their behalf.

## Output

Write a tab-separated file to `{votes}` and nothing else. No header, no
commentary, no blank lines. One row per person per post, then one PICK row per
person:

```
P0001<TAB>1<TAB>skip<TAB>the thought
P0001<TAB>2<TAB>consume<TAB>the thought
P0001<TAB>PICK<TAB>2<TAB>why, in a few words
```

The second column is the post number on this sheet. The PICK row answers: "if
only one of these could have a minute of your attention today, which?" Use `0`
if the honest answer is none of them. `0` is a fine answer.

That is {rows} rows. When the file is written, reply with the single word
`done`. Do not summarise, rank or recommend.

"""


def card_line(p):
    traits = " · ".join(str(v) for v in p["traits"].values())
    return f"**{p['pid']}** · {p['card']} · {traits}"


def render_item(n, item, base, out):
    lines = [f"### Post {n}", ""]
    if item.get("surface"):
        lines.append(f"*Seen as: {item['surface']}*")
        lines.append("")
    if item.get("path"):
        src = item["path"]
        if not os.path.isabs(src):
            src = os.path.normpath(os.path.join(base, src))
        if not os.path.exists(src):
            die(f"stimulus file not found: {src}")
        # A file called "current-cover.jpg" or "flop.jpg" tells the panel
        # which answer is wanted. Copy it under a name that says nothing.
        blind = hashlib.sha1(item["id"].encode()).hexdigest()[:10]
        dst_dir = os.path.join(out, "stimuli")
        os.makedirs(dst_dir, exist_ok=True)
        dst = os.path.abspath(os.path.join(
            dst_dir, blind + os.path.splitext(src)[1].lower()))
        shutil.copyfile(src, dst)
        lines.append(f"Open this file and look at it before answering: `{dst}`")
        lines.append("")
    if item.get("text"):
        lines.append("```")
        lines.append(item["text"].rstrip())
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


def cmd_sheets(a):
    panel = load_json(a.panel)
    stim = load_json(a.stimuli)
    items = stim.get("items") or die("stimuli.json needs an 'items' list")
    ids = [it.get("id") for it in items]
    if len(set(ids)) != len(ids) or not all(ids):
        die("every stimulus needs a unique 'id'")
    for it in items:
        it.setdefault("role", "test")
        if it["role"] not in ROLES:
            die(f"role must be one of {ROLES}, got {it['role']!r}")
        if not (it.get("text") or it.get("path")):
            die(f"stimulus {it['id']} has neither 'text' nor 'path'")
    if len(items) < 2:
        die("a panel needs at least two posts. One post alone has nothing to "
            "be better than; add a floor (a real post of yours that flopped).")

    rng = random.Random(panel["seed"] * 7919 + 1)
    people = sorted(panel["people"], key=lambda p: (p["segment"], p["pid"]))
    n_sheets = max(1, math.ceil(len(people) / a.batch))
    # Deal round-robin from a segment-sorted deck so every sheet is a small
    # copy of the whole panel, not "the architects sheet".
    sheets = [people[i::n_sheets] for i in range(n_sheets)]

    order0 = list(range(len(items)))
    rng.shuffle(order0)
    base = os.path.dirname(os.path.abspath(a.stimuli))
    os.makedirs(a.out, exist_ok=True)
    key = {"question": stim.get("question", ""), "items": items,
           "sheets": {},
           "panel": os.path.relpath(os.path.abspath(a.panel),
                                    os.path.abspath(a.out))}
    ctx = stim.get("context") or panel.get("context") or ""
    ctx = f"\n**Setting:** {ctx}\n" if ctx else ""

    for s, group in enumerate(sheets, 1):
        # Cyclic rotation: across any m consecutive sheets every post sits in
        # every position once, so "it was shown first" cancels out.
        rot = (s - 1) % len(items)
        order = order0[rot:] + order0[:rot]
        votes = os.path.abspath(os.path.join(a.out, f"votes-{s:02d}.tsv"))
        body = SHEET_HEAD.format(
            sheet=s, k=len(group), m=len(items), language=panel["language"],
            context=ctx, votes=votes, rows=len(group) * (len(items) + 1))
        body += "## The people\n\n"
        body += "\n".join(f"- {card_line(p)}" for p in group)
        body += "\n\n## The posts, in the order they appear\n\n"
        for pos, idx in enumerate(order, 1):
            body += render_item(pos, items[idx], base, a.out) + "\n"
        with open(os.path.join(a.out, f"sheet-{s:02d}.md"), "w",
                  encoding="utf-8") as f:
            f.write(body)
        key["sheets"][f"{s:02d}"] = {
            "order": [items[i]["id"] for i in order],
            "people": [p["pid"] for p in group],
        }
    with open(os.path.join(a.out, "key.json"), "w", encoding="utf-8") as f:
        json.dump(key, f, ensure_ascii=False, indent=1)

    print(f"SHEETS  ·  {n_sheets} sheets of ~{a.batch}  ·  {len(items)} posts"
          f"  ->  {a.out}")
    print("=" * 72)
    if n_sheets % len(items):
        print(f"  note: {n_sheets} sheets is not a multiple of {len(items)} "
              "posts, so position is only roughly balanced.")
    print("  Give each sheet-NN.md to a fresh subagent, one sheet each, with")
    print("  no other context. Each writes votes-NN.tsv. Then: panel.py tally")


# --------------------------------------------------------------------- tally

def wilson(k, n, z=1.96):
    if n <= 0:
        return 0.0, 0.0
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def icc(groups):
    """One-way ANOVA intraclass correlation across sheets.

    Twenty-five people written in one pass by one model are not twenty-five
    independent draws. This measures how much they are not.
    """
    groups = [g for g in groups if g]
    k = len(groups)
    n = sum(len(g) for g in groups)
    if k < 2 or n <= k:
        return 0.0
    grand = sum(sum(g) for g in groups) / n
    ssb = sum(len(g) * (sum(g) / len(g) - grand) ** 2 for g in groups)
    ssw = sum((x - sum(g) / len(g)) ** 2 for g in groups for x in g)
    msb, msw = ssb / (k - 1), ssw / (n - k)
    m0 = (n - sum(len(g) ** 2 for g in groups) / n) / (k - 1)
    den = msb + (m0 - 1) * msw
    return max(0.0, (msb - msw) / den) if den > 0 else 0.0


def sign_p(w, l):
    """Two-sided exact sign test on wins and losses, ties dropped."""
    n = w + l
    if n == 0:
        return 1.0
    k = min(w, l)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def spearman(x, y):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for t in range(i, j + 1):
                r[order[t]] = (i + j) / 2 + 1
            i = j + 1
        return r
    rx, ry = rank(x), rank(y)
    mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) *
                    sum((b - my) ** 2 for b in ry))
    return num / den if den else 0.0


def read_run(run):
    key = load_json(os.path.join(run, "key.json"))
    panel = load_json(os.path.normpath(os.path.join(run, key["panel"])))
    who = {p["pid"]: p for p in panel["people"]}
    ids = [it["id"] for it in key["items"]]
    did = defaultdict(dict)        # pid -> item id -> action
    thought = defaultdict(dict)
    pick, why = {}, {}
    pos = defaultdict(dict)        # pid -> item id -> position shown
    sheet_of = {}
    problems = []
    for s, meta in sorted(key["sheets"].items()):
        path = os.path.join(run, f"votes-{s}.tsv")
        for pid in meta["people"]:
            sheet_of[pid] = s
        if not os.path.exists(path):
            problems.append(f"sheet {s}: votes file missing, "
                            f"{len(meta['people'])} people not counted")
            continue
        with open(path, encoding="utf-8") as f:
            for ln, line in enumerate(f, 1):
                line = line.rstrip("\n")
                if not line.strip() or line.startswith("```"):
                    continue
                cols = [c.strip() for c in line.split("\t")]
                if len(cols) < 3:
                    problems.append(f"sheet {s} line {ln}: not tab-separated")
                    continue
                pid = cols[0].strip("*` ")
                if pid not in who or sheet_of.get(pid) != s:
                    problems.append(f"sheet {s} line {ln}: unknown person {pid}")
                    continue
                if cols[1].upper() == "PICK":
                    m = re.match(r"\d+", cols[2])
                    n = int(m.group()) if m else -1
                    if n == 0:
                        pick[pid] = None
                    elif 1 <= n <= len(ids):
                        pick[pid] = meta["order"][n - 1]
                    else:
                        problems.append(f"sheet {s} line {ln}: bad PICK")
                        continue
                    why[pid] = cols[3] if len(cols) > 3 else ""
                    continue
                m = re.match(r"\d+", cols[1])
                act = cols[2].lower().strip("`* ")
                if not m or not 1 <= int(m.group()) <= len(ids):
                    problems.append(f"sheet {s} line {ln}: bad post number")
                    continue
                if act not in LADDER:
                    problems.append(f"sheet {s} line {ln}: unknown action {act!r}")
                    continue
                iid = meta["order"][int(m.group()) - 1]
                did[pid][iid] = act
                thought[pid][iid] = cols[3] if len(cols) > 3 else ""
                pos[pid][iid] = int(m.group())
    complete = [p for p in who if len(did[p]) == len(ids)]
    partial = [p for p in who if 0 < len(did[p]) < len(ids)]
    if partial:
        problems.append(f"{len(partial)} people answered some posts but not "
                        "all, and were dropped")
    return {"key": key, "panel": panel, "who": who, "ids": ids, "did": did,
            "thought": thought, "pick": pick, "why": why, "pos": pos,
            "sheet_of": sheet_of, "people": complete, "problems": problems}


def analyse(r):
    ids, people, did = r["ids"], r["people"], r["did"]
    role = {it["id"]: it["role"] for it in r["key"]["items"]}
    n = len(people)
    by_sheet = defaultdict(list)
    for p in people:
        by_sheet[r["sheet_of"][p]].append(p)
    m_bar = n / max(1, len(by_sheet))

    items = {}
    for iid in ids:
        lv = [LADDER[did[p][iid]] for p in people]
        stop = sum(1 for v in lv if v >= 1)
        rho = icc([[1.0 if LADDER[did[p][iid]] >= 1 else 0.0 for p in g]
                   for g in by_sheet.values()])
        deff = 1 + (m_bar - 1) * rho
        n_eff = max(1.0, n / deff)
        lo, hi = wilson(stop / n * n_eff, n_eff) if n else (0, 0)
        acts = Counter(did[p][iid] for p in people)
        picks = sum(1 for p in people if r["pick"].get(p) == iid)
        items[iid] = {
            "role": role[iid],
            "pull": 100 * statistics.mean(lv) / 4 if lv else 0.0,
            "stop": stop / n if n else 0.0,
            "stop_ci": [lo, hi],
            "consume": sum(1 for v in lv if v >= 2) / n if n else 0.0,
            "strong": sum(1 for v in lv if v >= 4) / n if n else 0.0,
            "pick": picks / n if n else 0.0,
            "actions": dict(acts),
            "icc": rho, "n_eff": n_eff,
        }

    # Head-to-head: the same person saw both, so compare within the person.
    # That cancels out "this persona likes everything".
    pairs = []
    order = sorted(ids, key=lambda i: -items[i]["pull"])
    for i, x in enumerate(order):
        for y in order[i + 1:]:
            w = sum(1 for p in people if LADDER[did[p][x]] > LADDER[did[p][y]])
            l = sum(1 for p in people if LADDER[did[p][x]] < LADDER[did[p][y]])
            deff = 1 + (m_bar - 1) * max(items[x]["icc"], items[y]["icc"])
            pv = sign_p(round(w / deff), round(l / deff))
            pairs.append({"a": x, "b": y, "a_wins": w, "b_wins": l,
                          "ties": n - w - l, "p": pv,
                          "clear": pv < 0.05 and w != l})

    segs = {}
    for sid in r["panel"]["segments"]:
        grp = [p for p in people if r["who"][p]["segment"] == sid]
        if not grp:
            continue
        segs[sid] = {"n": len(grp), "pull": {}, "pick": {}}
        for iid in ids:
            segs[sid]["pull"][iid] = 100 * statistics.mean(
                LADDER[did[p][iid]] for p in grp) / 4
            segs[sid]["pick"][iid] = sum(
                1 for p in grp if r["pick"].get(p) == iid) / len(grp)

    # Health: is this run an audience, or one voice in 300 hats?
    flags = list(r["problems"])
    k = len(ids)
    all_lv = [LADDER[did[p][i]] for p in people for i in ids]
    above = sum(1 for v in all_lv if v >= 2) / max(1, len(all_lv))
    strong = sum(1 for v in all_lv if v >= 4) / max(1, len(all_lv))
    if above > 0.45 or strong > 0.12:
        flags.append(
            f"INFLATED: {100 * above:.0f}% of all rows are 'consume' or "
            f"higher and {100 * strong:.0f}% are a save, send, comment, "
            "follow or tap. Real feeds are nowhere near that. Read the "
            "ranking only; every rate on this page is too high.")
    by_pos = defaultdict(list)
    for p in people:
        for i in ids:
            by_pos[r["pos"][p][i]].append(LADDER[did[p][i]])
    pos_pull = {q: 100 * statistics.mean(v) / 4 for q, v in by_pos.items()}
    if pos_pull and max(pos_pull.values()) - min(pos_pull.values()) > 12 \
            and len(by_sheet) % k:
        flags.append("ORDER: posts shown earlier or later scored differently "
                     "and the sheets are not a multiple of the posts, so "
                     "position is not fully cancelled.")
    herd = 0
    for g in by_sheet.values():
        if all(Counter(did[p][i] for p in g).most_common(1)[0][1]
               >= 0.9 * len(g) for i in ids):
            herd += 1
    if herd:
        flags.append(f"HERD: on {herd} sheet(s) nine in ten people gave the "
                     "same answer to every post. That is one person repeated.")
    # People who scrolled past all think "next", so only the thoughts of
    # people who stopped are checked for repetition.
    th = [re.sub(r"\W+", " ", r["thought"][p][i].lower()).strip()
          for p in people for i in ids
          if LADDER[did[p][i]] >= 1 and r["thought"][p].get(i)]
    if th and 1 - len(set(th)) / len(th) > 0.10:
        flags.append(f"ECHO: {100 * (1 - len(set(th)) / len(th)):.0f}% of the "
                     "thoughts of people who stopped are word-for-word "
                     "duplicates of another one.")
    stopped = sum(1 for v in all_lv if v >= 1) / max(1, len(all_lv))
    if stopped > 0.35 and not (above > 0.45 or strong > 0.12):
        flags.append(f"GENEROUS: {100 * stopped:.0f}% of all rows stopped the "
                     "thumb. A real feed stops far fewer. The order still "
                     "means something; the 'stopped' column does not.")
    worst = max(items, key=lambda i: items[i]["icc"])
    if items[worst]["icc"] > 0.15:
        flags.append(f"SHEETS DISAGREE: on '{worst}' the sheets differ from "
                     "each other far more than chance would allow, so the "
                     f"effective sample is about {items[worst]['n_eff']:.0f}, "
                     f"not {n}. More sheets of fewer people would help more "
                     "than more people.")
    floors = [i for i in ids if role[i] == "floor"]
    ceils = [i for i in ids if role[i] == "ceiling"]
    if floors and ceils:
        if max(items[i]["pull"] for i in floors) >= \
                min(items[i]["pull"] for i in ceils):
            flags.append("ANCHORS: the panel scored your known flop at or "
                         "above your known hit. It cannot tell them apart, "
                         "so it cannot judge the new ones. Discard this run.")
    if n < len(r["who"]):
        flags.append(f"{len(r['who']) - n} of {len(r['who'])} people are "
                     "missing from the count.")

    return {"n": n, "sheets": len(by_sheet), "order": order, "items": items,
            "pairs": pairs, "segments": segs, "position_pull": pos_pull,
            "flags": flags, "question": r["key"].get("question", "")}


def bar(frac, width=20):
    full = round(max(0.0, min(1.0, frac)) * width)
    return "#" * full + "." * (width - full)


def track_line():
    if not os.path.exists(TRACK):
        return ("UNCALIBRATED. This panel has never been checked against "
                "posts you already published.\n  Run `panel.py backtest` once "
                "before you let it change a decision.")
    t = load_json(TRACK)
    runs = t.get("runs", [])
    if not runs:
        return "UNCALIBRATED."
    last = runs[-1]
    return (f"TRACK RECORD: last backtest {last['date']}, {last['items']} "
            f"real posts, rank correlation {last['rho']:+.2f}, "
            f"{last['concordant']}/{last['pairs']} pairs ordered correctly "
            f"against {last['metric']}.")


def cmd_tally(a):
    r = read_run(a.run)
    if not r["people"]:
        for p in r["problems"]:
            print("  -", p)
        die("no complete answers to count")
    res = analyse(r)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return
    it, n = res["items"], res["n"]
    w = max(len(i) for i in res["order"])
    print(f"PANEL  ·  {n} people  ·  {res['sheets']} sheets  ·  "
          f"{len(res['order'])} posts")
    if res["question"]:
        print(f"Q: {res['question']}")
    print("=" * 78)
    print(f"  {'':{w}}  {'PULL':>5}  {'stopped':>7}  {'95% interval':>13}  "
          f"{'took in':>7}  {'acted':>5}  {'1st pick':>8}")
    for i in res["order"]:
        d = it[i]
        tag = "" if d["role"] == "test" else f"  [{d['role']}]"
        print(f"  {i:{w}}  {d['pull']:5.1f}  {100 * d['stop']:6.0f}%  "
              f"{100 * d['stop_ci'][0]:5.0f}-{100 * d['stop_ci'][1]:<3.0f}%"
              f"{'':3}  {100 * d['consume']:6.0f}%  {100 * d['strong']:4.0f}%  "
              f"{100 * d['pick']:7.0f}%{tag}")
    none = sum(1 for p in r["people"] if r["pick"].get(p, 0) is None)
    print(f"  {'(picked none)':{w}}  {'':5}  {'':7}  {'':13}  {'':7}  {'':5}  "
          f"{100 * none / n:7.0f}%")
    neff = min(d["n_eff"] for d in it.values())
    print(f"\n  PULL is the average rung reached on the skip-to-action ladder,"
          f" 0 to 100.\n  Effective sample after sheet clustering: about "
          f"{neff:.0f} of {n}. The interval is the\n  panel's own noise. It "
          "says nothing about how far the panel is from real people.")

    print("\nWHAT THEY DID")
    for i in res["order"]:
        acts = it[i]["actions"]
        strong = ", ".join(f"{acts[k]} {k}" for k in STRONG if acts.get(k))
        print(f"  {i:{w}}  {bar(it[i]['stop'])}  "
              f"{acts.get('skip', 0)} skip · {acts.get('glance', 0)} glance · "
              f"{acts.get('consume', 0)} consume · {acts.get('like', 0)} like"
              + (f" · {strong}" if strong else ""))

    print("\nHEAD TO HEAD  (same person, both posts)")
    for p in res["pairs"]:
        verdict = "CLEAR" if p["clear"] else "too close to call"
        print(f"  {p['a']:{w}} beat {p['b']:{w}}  {p['a_wins']:4d} to "
              f"{p['b_wins']:<4d} ({p['ties']} level)   {verdict}")

    if len(res["segments"]) > 1:
        print("\nBY SEGMENT  (PULL; * marks a segment whose favourite is not "
              "the overall one)")
        top = res["order"][0]
        head = "  ".join(f"{i[:10]:>10}" for i in res["order"])
        sw = max(len(s) for s in res["segments"])
        print(f"  {'':{sw}}  {'n':>4}  {head}")
        for sid, s in res["segments"].items():
            fav = max(res["order"], key=lambda i: s["pull"][i])
            row = "  ".join(f"{s['pull'][i]:10.1f}" for i in res["order"])
            mark = " *" if fav != top and s["n"] >= 12 else ""
            small = "  (too few to read)" if s["n"] < 12 else ""
            print(f"  {sid:{sw}}  {s['n']:4d}  {row}{mark}{small}")

    if a.quotes:
        rng = random.Random(1)
        print("\nIN THEIR WORDS")
        for i in res["order"]:
            print(f"  {i}")
            for label, test in (("stayed", lambda v: v >= 2),
                                ("left", lambda v: v <= 1)):
                pool = [p for p in r["people"]
                        if test(LADDER[r["did"][p][i]]) and r["thought"][p][i]]
                rng.shuffle(pool)
                seen = set()
                shown = 0
                for p in pool:            # one voice per segment first
                    seg = r["who"][p]["segment"]
                    if seg in seen and len(seen) < len(res["segments"]):
                        continue
                    seen.add(seg)
                    print(f"    {label:6}  {r['did'][p][i]:8} {seg[:14]:14} "
                          f"\"{r['thought'][p][i]}\"")
                    shown += 1
                    if shown >= a.quotes:
                        break

    print("\nHEALTH")
    if res["flags"]:
        for f in res["flags"]:
            print(f"  - {f}")
    else:
        print("  - No structural problems found. That is a statement about "
              "the bookkeeping,\n    not about whether simulated people are "
              "right.")
    print(f"  - {track_line()}")


# ------------------------------------------------------------------ backtest

def cmd_backtest(a):
    r = read_run(a.run)
    res = analyse(r)
    actual = {}
    with open(a.actual, encoding="utf-8") as f:
        for line in f:
            cols = line.rstrip("\n").split("\t")
            if len(cols) >= 2 and cols[0] in res["items"]:
                try:
                    actual[cols[0]] = float(cols[1].replace(",", ""))
                except ValueError:
                    pass
    ids = [i for i in res["order"] if i in actual]
    if len(ids) < 4:
        die("a backtest needs at least 4 posts with a real number each "
            "(id<TAB>number per line, ids matching stimuli.json)")
    px = [res["items"][i]["pull"] for i in ids]
    ay = [actual[i] for i in ids]
    rho = spearman(px, ay)
    conc = pairs = 0
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            if ay[i] == ay[j] or px[i] == px[j]:
                continue
            pairs += 1
            conc += (px[i] > px[j]) == (ay[i] > ay[j])
    print(f"BACKTEST  ·  {len(ids)} real posts  ·  panel PULL against "
          f"{a.metric}")
    print("=" * 72)
    w = max(len(i) for i in ids)
    print(f"  {'':{w}}  {'panel':>6}  {'real':>10}")
    for i in sorted(ids, key=lambda i: -actual[i]):
        print(f"  {i:{w}}  {res['items'][i]['pull']:6.1f}  {actual[i]:10,.0f}")
    print(f"\n  rank correlation   {rho:+.2f}")
    print(f"  pairs in order     {conc}/{pairs}"
          f"  ({100 * conc / max(1, pairs):.0f}%, a coin gets 50%)")
    if len(ids) < 8:
        print(f"\n  {len(ids)} posts is a small test. With this few, +0.5 can "
              "happen by luck.\n  Add posts until there are 10 or more before "
              "trusting the number.")
    if rho >= 0.6 and conc / max(1, pairs) >= 0.7:
        verdict = ("The panel ranks your past posts roughly the way your "
                   "audience did. Use it to choose between options.")
    elif rho >= 0.3:
        verdict = ("Weak agreement. Use the panel to kill the worst option "
                   "and to read objections, not to pick between good ones.")
    else:
        verdict = ("The panel does not rank your past posts the way your "
                   "audience did. Fix audience.json before using it, or do "
                   "not use it.")
    print(f"\n  {verdict}")
    if a.save:
        t = load_json(TRACK) if os.path.exists(TRACK) else {"runs": []}
        t["runs"].append({
            "date": datetime.date.today().isoformat(), "items": len(ids),
            "rho": round(rho, 3), "concordant": conc, "pairs": pairs,
            "metric": a.metric, "n": res["n"]})
        os.makedirs(os.path.dirname(TRACK), exist_ok=True)
        with open(TRACK, "w", encoding="utf-8") as f:
            json.dump(t, f, indent=1)
        print(f"\n  saved to {TRACK}")


def main():
    ap = argparse.ArgumentParser(
        description="Synthetic audience panel: sample, sheets, tally, backtest.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="draw the quota sample")
    b.add_argument("audience")
    b.add_argument("--n", type=int, default=300)
    b.add_argument("--seed", type=int, default=1)
    b.add_argument("--out", default="run/panel.json")
    b.add_argument("--population",
                   default=os.path.join(HERE, "population.json"))
    b.set_defaults(fn=cmd_build)

    s = sub.add_parser("sheets", help="write one blind answer sheet per batch")
    s.add_argument("panel")
    s.add_argument("stimuli")
    s.add_argument("--batch", type=int, default=25)
    s.add_argument("--out", default="run/")
    s.set_defaults(fn=cmd_sheets)

    t = sub.add_parser("tally", help="count the votes")
    t.add_argument("run")
    t.add_argument("--quotes", type=int, default=3,
                   help="thoughts to print per post per side (0 for none)")
    t.add_argument("--json", action="store_true")
    t.set_defaults(fn=cmd_tally)

    k = sub.add_parser("backtest", help="score the panel against real results")
    k.add_argument("run")
    k.add_argument("--actual", required=True)
    k.add_argument("--metric", default="real views")
    k.add_argument("--save", action="store_true")
    k.set_defaults(fn=cmd_backtest)

    a = ap.parse_args()
    if getattr(a, "n", 1) < 1 or getattr(a, "batch", 1) < 1:
        die("--n and --batch must be positive")
    a.fn(a)


if __name__ == "__main__":
    main()
