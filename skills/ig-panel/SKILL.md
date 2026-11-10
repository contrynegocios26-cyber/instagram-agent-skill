---
name: ig-panel
description: >-
  Test a post on a simulated audience before it is published - a quota sample
  of 100 to 1,000 synthetic people built from the user's real audience
  numbers, each reacting blind to two or more options, tallied with honest
  intervals and checked against the account's own history. Use whenever the
  user asks "which one is better", "test this before I post", "will this
  work", "what would people think", wants an A/B test without spending reach
  or money, or mentions a synthetic audience, simulated users, a focus group,
  "AI that pretends to be 1000 people", or pre-testing a hook, cover, caption,
  ad, product, price or landing page.
---

# ig-panel

The pre-test. Everything else in this pack writes a post or reads the results
afterwards. This one sits in between: it shows the options to a simulated
audience and reports which one that audience preferred, why, and who
disagreed.

One tool lives in this folder and it runs. The model plays the people. The
script does everything a model is bad at: the sample, the blinding, the
rotation, the counting and the error bars.

```bash
python3 panel.py build audience.json --n 300 --out run/panel.json
python3 panel.py sheets run/panel.json stimuli.json --out run/
python3 panel.py tally run/
python3 panel.py backtest run/ --actual actual.tsv --save
```

## What this can and cannot tell you

Say this to the user before the first run, in your own words, once.

**It can** rank options against each other, kill the weakest one, show which
segment disagrees with the rest, and hand back the objection in a sentence a
customer would say. That is most of what a real pre-test buys, for the price
of a few minutes.

**It cannot** forecast reach, views, sales or a conversion rate. Simulated
people agree with each other more than real people do, and they are politer.
Every percentage on the tally is too high. Read the order, never the height.

**It has not earned trust on this account until it has been backtested.** The
tally prints `UNCALIBRATED` until `panel.py backtest` has been run against
posts the user already published. A panel that cannot rank last month's posts
the way the real audience did has no business ranking next week's.

Nothing here replaces the real test. Instagram's Trial Reels show a post to
non-followers first; that is ground truth and it is free. The panel's job is
to decide what is worth putting in front of real people.

## Before you run it

1. **Find the audience file.** `~/.claude/instagram/audience.json`. If it does
   not exist, build it from `templates/audience.json` with the user, from
   evidence in this order:
   - Their Insights: gender, age bands, top cities, follower versus
     non-follower reach. Screenshots are fine. These go in as numbers.
   - Their own words about who buys: read `voice.md`, their DMs and comments
     if they paste them. These become the segment cards.
   - Anything else is a guess. Segment sizes almost always are. Write every
     guess into the `assumptions` list in the file. `build` prints that list
     on every run so nobody forgets which parts are invented.
2. **A segment card is a situation, not a demographic.** "Is renovating now,
   has two quotes, afraid of paying for something that warps" behaves
   differently from "woman, 34". Three to six segments. Always include the
   people who will never buy: peers, friends, the curious. They are most of
   any feed and they are who a post has to get past.
3. **Leave out the audience that is not there.** Bought or foreign followers
   do not see the post. Do not simulate them.
4. **Get two or more options.** One post alone has nothing to be better than.
   If the user brings one, write two honest alternatives with the right skill
   (`/ig-reel` for hooks, `/ig-caption`, `/ig-carousel`) and test all three.
5. **Add anchors from the account's own history.** A `floor`: a real post of
   theirs that flopped, or a faithful composite of their weakest habit. A
   `ceiling`: a real post that travelled, if it can be shown in the same form
   as the options. Anchors are what make a score mean something: "beats your
   usual post for most of the panel" is a finding, "scored 31" is not. If the
   panel rates the flop above the hit, `tally` says to discard the run.

## The loop

**1. Write `stimuli.json`.** Each item is what a person would actually see, in
the form they would see it, and nothing more:

```json
{
  "question": "Which cover opens Friday's carousel?",
  "items": [
    {"id": "current", "role": "test", "path": "covers/a.jpg",
     "surface": "carousel cover in feed, first of 8",
     "text": "handle  first 125 characters of the caption... more"},
    {"id": "usual-post", "role": "floor", "path": "covers/old.jpg",
     "surface": "carousel cover in feed, first of 8",
     "text": "handle  the caption that post really had... more"}
  ]
}
```

- **Change one thing between options** where you can. If the covers differ
  and the captions differ, you will not know which did it.
- **Same form for every item.** A rendered image against a line of text is a
  test of images against text.
- **Never describe an item to the panel.** No "option A, our new bold
  version". The `id` and `role` stay in the key file; `sheets` copies each
  image to a meaningless filename so the path gives nothing away either.
- **Two to six items.** Past six, the last ones are judged by tired people.
- **No twins on one sheet.** Two items that differ only in colour, crop or
  one word contaminate each other: whichever is seen second gets "same as the
  other" and a skip, and rotation cannot fix that because the damage is in
  both directions. Test a small variation as two separate runs with the same
  seed and the same other items, one twin in each, and compare the runs.

What can go in: a hook line, a cover, a caption's visible 125 characters, the
slides of a carousel, a Reel described beat by beat with its first frame as an
image, a static ad, a product photo with its price, a screenshot of a landing
page. For a page or a product, say in `context` where the person came from.

**2. Build and deal.**

```bash
python3 panel.py build ~/.claude/instagram/audience.json --n 300 --out run/panel.json
python3 panel.py sheets run/panel.json stimuli.json --out run/
```

| size | sheets | use it for |
| --- | --- | --- |
| `--n 100` | 4 | a quick look, two options, one obvious loser |
| `--n 300` | 12 | the default. Segment splits become readable. |
| `--n 1000` | 40 | when a segment of 10% or less is the one that matters |

More people shrink the panel's noise. They do nothing for its bias. Going from
300 to 1,000 makes a wrong answer more precise, so spend the effort on the
audience file and the backtest first. Make the number of sheets a multiple of
the number of items and every item sits in every position equally often.

**3. Run the sheets.** One sheet, one fresh subagent, no other context. The
prompt is only: read this file, do what it says, write the file it names.
Launch them in parallel. The separation is the method, not a convenience:

- The subagent has not seen the conversation, so it does not know which
  option the user likes or which one you wrote.
- Different sheets cannot copy each other, which is where the spread between
  people comes from.
- A cheaper, faster model is fine for sheets and is often less agreeable.

No subagent tool? Use `--n 50 --batch 25`, do the two sheets yourself one at a
time, and tell the user the run was not blind. Never fill in a sheet for an
option you have already argued for in the same conversation and call it a
test.

**4. Tally.**

```bash
python3 panel.py tally run/
```

Then read the output in this order:

1. **HEALTH first.** `INFLATED`, `GENEROUS`, `HERD`, `ECHO`, `ORDER`,
   `SHEETS DISAGREE` and `ANCHORS` each
   mean something specific and each is printed with what it means. An
   `ANCHORS` flag ends the analysis. Missing sheets get re-run, not ignored.
2. **HEAD TO HEAD**, not the top table. Each person saw every option, so this
   compares within the person and cancels out "this persona likes
   everything". A pair marked `too close to call` is a tie. Report it as a
   tie. Do not pick the one with the bigger number.
3. **BY SEGMENT.** A star means a segment's favourite is not the overall
   favourite. If the starred segment is the one that buys, that is the
   headline, not the overall winner.
4. **The thoughts.** Read every `votes-*.tsv`, not just the sample the tally
   prints. Group the reasons people left into three or four objections and
   quote one real line for each. This is usually worth more than the ranking,
   because it says what to fix.

**5. Report.** Print the tally, then:

```
PANEL READY
question:   which cover opens Friday's carousel
panel:      300 people, 12 blind sheets, 5 segments, seed 26
winner:     "never-here", clear over 3 of 4, tied with "question"
buyers:     the renovating segment prefers "question"
why left:   1) reads as an ad  2) no idea what MDF is  3) dark, no photo
vs usual:   every option beat the floor
trust:      UNCALIBRATED, treat as a hypothesis for a Trial Reel
next:       fix objection 2 on the winner, then post

Reply "yes" to log it, or tell me what to change.
```

**6. Close the loop.** On "yes", append the question, the options and the
panel's ranking to `~/.claude/instagram/log.md`. When the post has real
numbers, `/ig-audit` compares them to the prediction. A panel nobody checks
drifts into a confident habit.

## The backtest, which is the part that makes it real

Do this once before the panel is allowed to change a decision, and again
whenever `audience.json` changes much.

1. Take 8 to 12 posts the account already published, of **one format**, spread
   from worst to best by outlier multiple (see `/ig-audit`). Not the top
   twelve. The panel has to tell good from bad.
2. Put them in `stimuli.json` exactly as the feed showed them. Strip like
   counts, dates and anything else that reveals the result.
3. Run the loop. The subagents must not see the results. You already have, so
   you do not fill in any sheet.
4. Write `actual.tsv`, one `id<TAB>number` per line, using reach or outlier
   multiple, and run:

```bash
python3 panel.py backtest run/ --actual actual.tsv --metric "non-follower reach" --save
```

It prints the rank correlation and how many pairs of posts the panel put in
the right order, where a coin gets half. The verdict line says what the panel
is fit for: choosing between options, only killing the worst one, or nothing.
Believe it. If the answer is nothing, the fix is in the segment cards, and if
a second attempt still fails, tell the user this account is one the panel
cannot read yet.

Posts published in a flood, boosted with ads or carried by a trending audio
have numbers the content did not earn. Leave them out of the backtest.

## Why it is built this way

Each rule in the sheet exists because of a way simulated audiences are known
to go wrong.

- **The thought comes before the action.** Models asked for a rating go
  straight to the comfortable middle. Asked to write what the person thinks
  and only then what they do, the spread looks much more like people. This is
  the main finding of the purchase-intent work that got closest to real survey
  data.
- **`skip` is the default and the base rates are on the card.** A persona with
  no stated habits behaves like a volunteer in a focus group. Most real users
  lurk, so most cards say so, and a lurker is told to stay one.
- **Nobody is told what is being tested.** A model that knows which option is
  yours will find reasons to like it.
- **The order rotates.** Whatever is shown first gets more attention.
- **One ladder, one answer.** Asking for likes and saves and follows
  separately gets all three handed out to everyone.
- **Quotas, not random draws.** The panel matches the audience numbers
  exactly, every time, and the seed makes it reproducible.
- **The interval is widened for clustering.** Twenty-five people written in
  one pass are not twenty-five independent people. `tally` measures how alike
  each sheet is and shrinks the effective sample to match. The interval is
  still only the panel's own noise.

## Rules

- **Never report a panel number as a forecast.** No "this will get", no
  projected reach, no expected sales. Ranks, ties, segments, objections.
- **Never invent the audience.** A number that did not come from Insights goes
  in `assumptions`.
- **A tie is a result.** Say "the panel cannot separate these" and suggest the
  real test.
- **Do not re-run until the answer changes.** Same seed, same sheets. If the
  user wants a second opinion, change the seed once and report both.
- **Do not use it on things people are bad at predicting about themselves or
  that depend on execution**: whether a face holds attention, whether an edit
  is too slow, whether a trending audio lands. It reads what is on the page.
- **Do not simulate real, named individuals.** Segments, not people.
- **Sensitive calls need humans.** Pricing changes, health or money claims and
  anything about a vulnerable group get a real test, whatever the panel says.
