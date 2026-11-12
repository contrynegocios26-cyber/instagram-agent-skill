# Playbook of the winning single-function consumer AI apps (Cal AI, Quittr, Umax, Rizz, Turbo AI, Bible Chat) — notes as of 2026-11-12

> Method note for the report writer: page fetching was blocked in this session (techcrunch.com, superwall.com, screensdesign.com, macrumors.com, paddle.com, funnelfox.com and others did not resolve). Everything below comes from search-result summaries of the linked pages, not from reading the full pages. Numbers and wording should be treated as "as summarized by search", and anything load-bearing should be re-checked against the linked page. Labels used: **[SELF]** = founder/company self-reported; **[EST]** = third-party estimate (Appfigures, Sensor Tower, AppGoblin, ScreensDesign, Adapty library, Latka); **[VERIFIED]** = stated on the record by a named counterparty or regulator (Apple, MyFitnessPal, 404 Media reporting); **[VENDOR]** = from a vendor with a commercial interest (Superwall, FunnelFox, Adapty, RevenueCat).

## 1. Cal AI teardown (product, onboarding, paywall, pricing, numbers, tech, acquisition)

### Takeaway
Cal AI sells one action (photograph a meal, get calories and macros) behind a long personalization quiz (about 29 screens, 16 questions) that ends in a "custom plan" reveal and a trial-led paywall with a 3-day free trial on the annual plan, followed by discount/spin-wheel offers for people who decline. It reached 15M+ downloads and $30M+ annual revenue in under two years with about seven employees and was bought by MyFitnessPal (closed December 2025, announced March 2, 2026) for undisclosed terms.

### Cited Findings

**What it does / core loop**
- Three ways to log food: photo scan, barcode scan, or text description (review sites, 2026) — [eesel pricing guide](https://www.eesel.ai/en/blog/cal-ai-pricing); [tooldirectory review, Jul 25 2026](https://tooldirectory.ai/tools/cal-ai)
- Retention features reported by reviewers: gamified streak system, public groups, dark mode; one reviewer says the community/social challenge layer is thin and calls it "a passive tracker" (3.5/5) (2026) — [Macaron review 2026](https://macaron.im/blog/cal-ai-calorie-tracker-review-2026); [Nutrola review 2026](https://nutrola.app/en/blog/cal-ai-review-2026)
- Free tier is very limited: sources say "food scanning analysis results require a subscription" or a restricted number of scans; no source gives an exact cap (2026) — [Nutrola free vs paid](https://nutrola.app/en/blog/cal-ai-free-vs-paid-what-do-you-actually-get); [eesel](https://www.eesel.ai/blog/cal-ai-pricing)
- After the acquisition, Cal AI was integrated with MyFitnessPal's nutrition database but stays a standalone app; MFP's CEO said there are no plans to fold it into the core MFP app (Mar 2026) [VERIFIED by acquirer] — [TechCrunch, Mar 2 2026](https://techcrunch.com/2026/03/02/myfitnesspal-has-acquired-cal-ai-the-viral-calorie-app-built-by-teens)

**Onboarding (screen by screen, as far as public teardowns show)**
- Starts with a short demo video of the app; deep personalization throughout; heavy animation; asks for an App Store review mid-onboarding; generates a personalized plan; "soft paywall" strategy (X post, Mar 2026) [third-party observation] — [César Álvarez on X](https://x.com/cesaralvarezll/status/2036873854455255505)
- 29 screens sit between "Get Started" and the paywall: 16 questions plus 3 iOS permission prompts (Apple Health, notifications, tracking) (2026 teardown; attribution among the teardown pages returned was not confirmed, most likely ASOitis) — [ASOitis Cal AI teardown 2026](https://asoitis.com/case-studies/cal-ai)
- Account creation is placed right before the paywall and framed as "Save your progress" for the plan the user has just seen (2026) — [ASOitis](https://asoitis.com/case-studies/cal-ai)
- Trial reassurance screens: "No Payment Due Now" and "We'll send a reminder before your trial ends" (2026) — [ASOitis](https://asoitis.com/case-studies/cal-ai); [PaywallPro, iOS v3.2.7](https://www.paywallpro.app/apps/cal-ai-app)
- A screen-recording teardown describes the quiz as running roughly 00:15 to 02:30 of the first session, i.e. over two minutes of questions before any price appears; ScreensDesign catalogs 147 screens and estimates $1.8M/month [EST, date of estimate unclear] — [ScreensDesign Cal AI](https://screensdesign.com/apps/cal-ai-calorie-tracker/?id=1739&ts=0&vt=1); [ScreensDesign showcase](https://screensdesign.com/showcase/cal-ai-calorie-tracker)
- Yadegari has said publicly that adding extra onboarding questions raised conversion (title of a Founderpath resource; details not retrieved) [SELF] — [Founderpath](https://founderpath.com/resources/zach-yadegari-cal-ai-onboarding-tests-and-influencer-marketing)

**Paywall and pricing**
- 3-day free trial on the annual plan, shown at the end of onboarding (2026) — [ASOitis](https://asoitis.com/case-studies/cal-ai)
- Price is hidden until the end and heavily A/B-tested, so it differs by user, version and region. Reported US variants: $2.99/week, $5.99/month, ~$9.99/month, $19.99/year, $29.99/year, $49.99/year. One source reports $19.99/year with a 3-day trial offered as a discount after the user closes the first paywall (2026) — [eesel](https://www.eesel.ai/en/blog/cal-ai-pricing); [tooldirectory](https://tooldirectory.ai/tools/cal-ai); [shelog review 2026](https://www.shelog.ai/blog/cal-ai-review-2026)
- Spin-the-wheel paywall that lets the user "unlock" a discount; one of Cal AI's most-tested formats; the onboarding paywall went through 61 meaningful experiments (layout, offer framing, price presentation, urgency, creative); headline claim: monthly revenue grew 3x+ in 10 months [VENDOR] — [Superwall case study](https://superwall.com/case-studies/cal-ai)
- Web funnel version (June 2026 teardown): quiz, email capture, paywall with trial + discount, Stripe checkout. The same teardown says public sources do not reveal spend, CTR, CVR or trial-to-paid — [web2wave Cal AI teardown](https://resources.web2wave.com/calai/)
- Same-category apps copy the mechanics: Kalo shows an 85% annual discount, then a "Spin to Win" 90% one-time offer; another adds a second paywall with countdown timer for hesitators — [ScreensDesign Kalo](https://screensdesign.com/showcase/kalo-ai-calorie-tracking); [ScreensDesign calorie paywall examples](https://screensdesign.com/articles/calorie-tracker-app-paywall-examples/)

**Numbers over time**
- First influencer story post: about $2,000, about 1,000 downloads in two days, about 100 paying customers (i.e. ~10% download-to-paid on that cohort, ~$20 CAC) [SELF, Yadegari at TechCrunch Disrupt 2026 as summarized] — [Net Influencer](https://www.netinfluencer.com/cal-ai-founder-zach-yadegari-breaks-down-the-influencer-playbook-behind-his-apps-growth/)
- 100,000 downloads and $1M revenue in the first 4 months (2024) [SELF via newsletter] — [What A Startup substack](https://whatastartup.substack.com/p/two-gen-z-founders-bootstrapped-cal-ai)
- About $400K MRR stage (late 2024) described in marketing breakdowns [secondary] — [Shortimize](https://www.shortimize.com/blog/cal-ais-marketing-strategies-lessons-from-a-400k-mrr-success-story)
- February 2025: consumers spent $2M in Cal AI, its biggest month to that date [EST, Appfigures] — [Appfigures, Feb 28 2025](https://appfigures.com/resources/insights/20250228?f=4)
- Influencer-only growth plateaued around $2M/month; adding performance ads took it to $4M/month in one account and $5.7M/month in another (2025) [SELF, conflicting retellings] — [founder-playbooks](https://founder-playbooks.pages.dev/insight/influencer-to-paid-ads-growth-ladder); [Stormy.ai](https://stormy.ai/blog/scaling-cal-ai-performance-marketing-mrbeast-roi)
- At acquisition: 15M+ downloads and $30M+ annual revenue in under two years [stated by MyFitnessPal, not audited]; other coverage says $30–40M; Latka lists $40M (Mar 2026); growth-blog retellings say "$50M ARR" [SELF/secondary] — [TechCrunch](https://techcrunch.com/2026/03/02/myfitnesspal-has-acquired-cal-ai-the-viral-calorie-app-built-by-teens); [Latka](https://getlatka.com/companies/calai.app); [Superframeworks](https://superframeworks.com/case-study/cal-ai)
- AppGoblin estimates 18.7M installs and 1.3M monthly active users (2026) [EST] — [AppGoblin](https://appgoblin.info/apps/6480417616)
- Team: seven employees including co-founder/CEO Zach Yadegari, plus a small group of contractors, all retained (Mar 2026); one outlier source says ~30 people. Early on the founders describe using "$1K/month developers" [SELF] — [TechCrunch](https://techcrunch.com/2026/03/02/myfitnesspal-has-acquired-cal-ai-the-viral-calorie-app-built-by-teens); [eWeek](https://www.eweek.com/fr/news/myfitnesspal-acquires-cal-ai-teen-founders/); [Net Influencer](https://www.netinfluencer.com/cal-ai-founder-zach-yadegari-breaks-down-the-influencer-playbook-behind-his-apps-growth/)

**How the food recognition works, accuracy**
- A product teardown says it combines the phone's depth sensor (for volume) with an AI model trained on food images, and the company claims 90% accuracy on visible foods. The teardown author has no access to the code, so the mechanism is unconfirmed — [RaftLabs teardown](https://www.raftlabs.com/blog/cal-ai-product-teardown)
- The founder has called the photo feature "90 percent accurate"; press notes this is not independently verified [SELF] — [AOL](https://www.aol.com/lifestyle/swears-cracked-calorie-tracking-code-141900306.html)
- Controlled study (Hengist et al., 2026, as cited by a teardown; paper not opened): Cal AI underestimated by 345 kcal on average, and fat was underestimated by about 30 g across all four apps tested — [RaftLabs](https://www.raftlabs.com/blog/cal-ai-product-teardown)
- "90% accurate" in app marketing usually refers to lab conditions; a 2024 PLOS Digital Health study with 18 dietitians found computer-vision food apps work poorly on real-life photos (competitor-written review, 2026) — [Fitia review](https://fitia.app/learn/article/ai-calorie-photo-apps-accuracy-2026/)
- General-purpose AI models' nutrition values deviated from dietitians by as much as 45% in calories and fluctuated day to day (Nutrients, 2025; did not test Cal AI) — [MDPI Nutrients 17:3044](https://mdpi-res.com/d_attachment/nutrients/nutrients-17-03044/article_deploy/nutrients-17-03044.pdf)

**MyFitnessPal acquisition**
- Closed December 2025, announced March 2, 2026. Financial terms not disclosed; MFP's CEO noted the Cal AI team "didn't have to sell" and were happy with the offer [VERIFIED by acquirer] — [TechCrunch](https://techcrunch.com/2026/03/02/myfitnesspal-has-acquired-cal-ai-the-viral-calorie-app-built-by-teens); [The Next Web](https://thenextweb.com/news/myfitnesspal-acquires-cal-ai-the-viral-calorie-tracking-app-built-by-teens)

### Inferences
- The flow order to reproduce is: demo video, 16 goal/body/habit questions with interstitial "proof" and animation screens, mid-quiz rating prompt, 3 permission prompts, loading/"building your plan", plan reveal, sign-up framed as "save progress", trial paywall with reassurance, then a second discounted offer on decline. The second-offer-on-decline step is the one Apple later objected to (see section 6), so a 2026 builder should not copy it literally.
- Price points cluster around roughly $30–50/year with a 3-day trial as the default and a ~$20/year rescue offer; weekly pricing appears as an A/B variant, not the core plan.
- The 10% paid conversion on the first influencer cohort is a warm, creator-referred audience and should not be used as a baseline for paid traffic.

### Gaps
- Exact text of each of the 16 questions, and whether a referral-code step and "where did you hear about us" screen exist, were not confirmed by any retrieved source (ScreensDesign's 147-screen recording would answer this but could not be opened).
- No verified statement of which foundation models Cal AI calls (GPT-4o/Claude/Gemini or a fine-tune). No public figure for cost per scan.
- Acquisition price is undisclosed. "$50M exit" style headlines are unverified.
- No reliable public install-to-trial or trial-to-paid rate for Cal AI.

## 2. Brief teardowns: Quittr, Umax, RizzGPT/Rizz, Turbo AI, Bible Chat

### Takeaway
All five sell one emotionally charged outcome to a narrow audience, show the result or plan only after the user has invested effort, and charge either a cheap annual plan with a timed discount (Quittr) or a weekly subscription (Umax, Rizz, Bible Chat). Reported revenues range from about $2.5M/year (RizzGPT) to eight figures (Turbo AI), almost all self-reported.

### Cited Findings

**Quittr (quit-porn tracker, Alex Slater and Connor McLaren)**
- Founders told New York Magazine the app has 1.5M downloads and makes $500,000/month; price about $30/year [SELF, relayed in Mar 2026 coverage] — [404 Media](https://www.404media.co/viral-quittr-porn-addiction-app-exposed-the-masturbation-habits-of-hundreds-of-thousands-of-users/); [UNILAD Tech, Mar 11 2026](https://www.uniladtech.com/news/tech-news/adult-video-recovery-app-leaks-sensitive-data-users-332272-20260311)
- December 2024 profile: $50K/month, 19-year-old founder from London [SELF via Starter Story] — [Starter Story](https://www.starterstory.com/quittr-breakdown)
- Podcast description claims Slater built it in 10 days with $3,000, began by copying a competitor's onboarding flow, and scaled to $500K/month (2026) [SELF, promotional] — [Valid App Growth podcast](https://www.buzzsprout.com/2604336/episodes/18884194-what-actually-works-to-scale-a-mobile-app-in-2026-w-alex-slater-from-quittr)
- Paywall: layered, with a high-urgency "One Time Offer" at 80% off and a five-minute countdown timer — [ScreensDesign Quittr](https://screensdesign.com/showcase/quittr-quit-porn-now)
- Pricing snapshot verified September 2026: from $1.67/month billed annually ($20.04/year) — [Recurdash](https://recurdash.com/subscription-pricing/quittr)

**Umax (face rating / "looksmaxxing", Blake Anderson; Sarthak Dhawan also credited as builder)**
- Sells a facial attractiveness score from two selfies; the price ($3.99/week) is shown only after the photos are uploaded; an "invite 3 friends" free unlock exists but did not work when a Fortune reporter tested it — [RealWorldAppeal](https://realworldappeal.com/en/blog/umax-ai)
- App Store price list (2024-era): weekly $3.99 and $4.99, monthly $9.99 and $12.99; a later report says web pricing shows $9.99/week [EST/observed] — [Adapty paywall library](https://adapty.io/paywall-library/umax-become-hot/); [RealWorldAppeal](https://realworldappeal.com/en/blog/umax-ai)
- Revenue: "almost $5 million over the past year" (Starter Story interview) versus 7M downloads and $3M revenue on Anderson's own site; Dhawan-related coverage says 20M users and $6M annual revenue [SELF, inconsistent] — [Scale Nuggets](https://scalenuggets.beehiiv.com/p/23yearold-whos-making-11myear-ai-apps); [blakea.co](https://blakea.co/); [AIM Media House](https://aimmediahouse.com/ai-startups/college-dropouts-take-startup-to-5-million-users-in-just-18-months)
- Reportedly spent over $200,000 on influencer deals in three days via exclusive deals with large creators; Anderson says influencers are the most profitable channel, alongside internal UGC and paid ads [SELF, secondary] — [Stormy.ai](https://stormy.ai/blog/riz-gpt-influencer-marketing-case-study); [Scale Nuggets](https://scalenuggets.beehiiv.com/p/23yearold-whos-making-11myear-ai-apps)

**RizzGPT (Blake Anderson) and the "Rizz" category (AI replies for dating chats)**
- RizzGPT: about $2.4–2.5M annual revenue; launched by paying two little-known TikTok creators $50 each, whose videos got millions of views [SELF] — [Scale Nuggets](https://scalenuggets.beehiiv.com/p/23yearold-whos-making-11myear-ai-apps); [Stormy.ai](https://stormy.ai/blog/riz-gpt-influencer-marketing-case-study)
- RizzGPT Pro pricing: $3.99 weekly, $8.99 monthly, $44.99 annually [listing] — [TrustMRR](https://trustmrr.com/startup/ai-dating-assistant-1)
- "Rizz" app (2023 release): weekly plans at $3.99/$4.99/$6.99/$9.99, monthly $19.99, annual $69.99; about $300K/month and 200K downloads/month [EST] — [Adapty paywall library](https://adapty.io/paywall-library/rizz/)
- Another estimate for RIZZ: about $150K/month, 5-step onboarding, weekly subscription for unlimited replies, "spots remaining" urgency tactic [EST] — [ScreensDesign Rizz](https://screensdesign.com/showcase/rizz)
- Many near-identical "Rizz" apps exist; e.g. Plug AI clone estimated under $10K/month with ~204 monthly actives [EST] — [AppGoblin](https://appgoblin.info/apps/6748056633)

**Turbo AI (ex-Turbolearn; AI notes, flashcards and quizzes from lectures; Rudy Arora and Sarthak Dhawan)**
- 5M users, about 20,000 new sign-ups per day, eight-figure ARR, profitable (Oct 2025) [SELF via TechCrunch] — [TechCrunch, Oct 23 2025](https://techcrunch.com/2025/10/23/20-year-old-dropouts-built-ai-notetaker-turbo-ai-to-5-million-users)
- Business Insider-cited figure: $13M lifetime revenue with a 10-person team [SELF via press] — [Let's Data Science](https://letsdatascience.com/news/founders-scale-ai-study-app-to-13m-revenue-41e281e9)
- Students pay around $20/month — [AIM Media House](https://aimmediahouse.com/ai-startups/college-dropouts-take-startup-to-5-million-users-in-just-18-months)
- Early growth: 40+ low-cost TikTok videos made by the founders (Dec 2024 breakdown) — [Starter Story](https://www.starterstory.com/turbolearn-ai-breakdown)

**Bible Chat (AI chat and devotionals on scripture)**
- $6.3M net revenue since its 2023 launch; March 2025 was the best month at $750K net with 1.5M downloads [EST, Appfigures, Apr 18 2025] — [Appfigures](https://appfigures.com/resources/insights/20250418?f=5)
- US weekly revenue about $404K at end of September 2025 [EST, Sensor Tower] — [Sensor Tower Q3 2025](https://sensortower.com/blog/2025-q3-unified-top-5-reference%20apps-units-us-60772727241bc16eb8784bc8)
- US weekly downloads rose from 182K (late Sep 2025) to 263K (end of Dec 2025) [EST, Sensor Tower] — [Sensor Tower Q4 2025](https://sensortower.com/blog/2025-q4-ios-top-5-reference-apps-revenue-us-60772727241bc16eb8784bc8)
- Pricing: Premium weekly $4.99, monthly $12.99 (listing date unclear) — [Adapty paywall library](https://adapty.io/paywall-library/bible-chat-the-holy-scripture/)
- Paywall type is described inconsistently: Appfigures calls it a hard paywall with a prominent "Try Free" trial button; ScreensDesign calls it a soft paywall — [Appfigures](https://appfigures.com/resources/insights/20250418?f=5); [ScreensDesign](https://screensdesign.com/showcase/bible-chat-daily-devotional)

### Inferences
- Weekly pricing at $3.99–$9.99 is the norm for impulse, novelty-driven apps (face rating, dating replies, faith chat). Habit apps with a longer horizon (calories, quitting) lead with a discounted annual plan of $20–50.
- The common gate is "effort first, price second": selfies, quiz or chat screenshot are collected before the price is shown.

### Gaps
- No independent revenue figures for Quittr, Umax, RizzGPT or Turbo AI were found; all are founder statements.
- Onboarding step counts for Quittr, Umax, Turbo AI and Bible Chat were not retrieved.
- It is unclear which of several "Rizz" apps each estimate refers to.

## 3. The marketing machine (TikTok/Reels creators, UGC, paid ads)

### Takeaway
Cal AI's sequence was: founder-led DMs to fitness influencers and flat-fee multi-video deals priced backward from a target of about $5 per thousand views, scaled to 50–100+ new creators a month; then, once influencer growth plateaued near $2M/month, a separate pool of creators producing "salesy" ad-specific videos that let paid spend exceed $1M/month. Cheap in-house UGC accounts are a parallel "spray and pray" layer paid roughly $10–50 per video plus about $1–2 per thousand views.

### Cited Findings

**Influencer deals (Cal AI)** — all [SELF] unless noted
- Yadegari separates UGC ("mass spray and pray") from influencer marketing ("a sniper approach"); he personally DMed thousands of fitness influencers (talk at TechCrunch Disrupt 2026, as summarized) — [Net Influencer](https://www.netinfluencer.com/cal-ai-founder-zach-yadegari-breaks-down-the-influencer-playbook-behind-his-apps-growth/)
- Selection: creators with "very tight communities", minimum of roughly 50,000 followers, but average views weighted more than follower count — [Net Influencer](https://www.netinfluencer.com/cal-ai-founder-zach-yadegari-breaks-down-the-influencer-playbook-behind-his-apps-growth/)
- Target CPM about $5 (cost per thousand views), derived from known revenue per thousand views. Worked example from co-founder Jake Castillo: creator asks $1,000 for four posts at an expected 50,000 views each = $5 CPM; if the posts reach 2M views the same flat deal is $0.50 CPM — [Jake Castillo on X, "How we scaled Cal AI to $50M ARR with influencers"](https://x.com/jakecastilloooo/article/2104597759252717610); [Founder-playbooks](https://founder-playbooks.pages.dev/insight/influencer-to-paid-ads-growth-ladder)
- Other CPM figures: $1–2 deals were achievable early but became hard to find; about $10 CPM for some "mom" influencers was still profitable; FunnelFox cites $0.50–$3.00 [SELF/VENDOR, conflicting] — [GTM Sauce, Alfie Dickens episode, Aug 26 2026](https://gtmsauce.com/episodes/2026-08-26-alfie-dickens-meet-the-marketing-genius-behind-cal-ai); [FunnelFox blog](https://blog.funnelfox.com/cal-ai-influencer-marketing/)
- Negotiation: creators quoting a per-post fee often accept the same sum for several videos or a guaranteed-views deal. Bigger creators are preferred later because managing a 30,000-view creator takes the same work as a 500,000-view one — [Net Influencer](https://www.netinfluencer.com/cal-ai-founder-zach-yadegari-breaks-down-the-influencer-playbook-behind-his-apps-growth/); [Jake Castillo on X](https://x.com/jakecastilloooo/article/2104597759252717610)
- Volume: roughly 20–30 creators in the program when marketer Alfie Dickens joined; goal of 50+ new creators per month, later 100/month; about four videos per month per creator so followers see the app repeatedly — [GTM Sauce](https://gtmsauce.com/episodes/2026-08-26-alfie-dickens-meet-the-marketing-genius-behind-cal-ai)
- Each influencer post converted to downloads roughly linearly while creator recruitment grew exponentially for about 18 months — [Net Influencer](https://www.netinfluencer.com/cal-ai-founder-zach-yadegari-breaks-down-the-influencer-playbook-behind-his-apps-growth/)
- The winning format was simply a creator scanning a meal with the app inside their normal content — [Net Influencer](https://www.netinfluencer.com/cal-ai-founder-zach-yadegari-breaks-down-the-influencer-playbook-behind-his-apps-growth/)

**Paid ads layered on top (Cal AI)** — [SELF]
- Influencer-only growth plateaued around $2M/month. Running influencer content directly as ads capped profitable Facebook spend at about $5,000/day because organic winners did not perform as ads — [Founder-playbooks](https://founder-playbooks.pages.dev/insight/influencer-to-paid-ads-growth-ladder)
- Fix: recruit a separate set of creators to make ad-specific, more direct and "salesy" content, iterating on hooks and pain points; spend then scaled past $1M/month across TikTok Ads Manager, Meta and Google; revenue went to $4M/month (or $5.7M/month in another retelling) — [Stormy.ai](https://stormy.ai/blog/scaling-cal-ai-performance-marketing-mrbeast-roi); [Founder-playbooks](https://founder-playbooks.pages.dev/insight/influencer-to-paid-ads-growth-ladder)
- Attribution: App Store custom product pages linked from specific Facebook ads — [Founder-playbooks](https://founder-playbooks.pages.dev/insight/influencer-to-paid-ads-growth-ladder)
- Because of the 3-day trial, ad platforms are optimized on trial-start events with a modeled paid-conversion rate, since waiting 3 days for the purchase signal makes the algorithm learn too slowly — [Net Influencer](https://www.netinfluencer.com/cal-ai-founder-zach-yadegari-breaks-down-the-influencer-playbook-behind-his-apps-growth/)

**Blake Anderson (RizzGPT, Umax; early Cal AI partner)** — [SELF]
- RizzGPT launch: two unknown creators at $50 each; later shifted from external influencer promos to an internal UGC content engine for higher margins — [Stormy.ai](https://stormy.ai/blog/riz-gpt-influencer-marketing-case-study)
- Anderson's public profile credits him with RizzGPT ($2.4M ARR), Umax ($5M ARR) and Cal AI ($8M ARR at the time of the profile) — [SuperX profile](https://superx.so/creators/blakeandersonw)

**In-house UGC / slideshow ("canvas") accounts: typical pay** — [marketplace/vendor data, directional]
- Recommended structure: small base per video (example $10) plus laddered bonus per thousand views, minimum-view threshold and payout cap (example $3,000); a typical new-account TikTok gets about 300 views (guide from a 30M-view campaign, 2026) — [carlmonkft on X](https://x.com/carlmonkft/status/2108497092989661237)
- App UGC: $25–50 base per posted video plus view bonuses; job-board median $15 per video plus $1 per 1,000 views (2026) — [ugc-program.com](https://ugc-program.com/); [ugcjobs.com](https://ugcjobs.com/blog/ugc-creator-salary)
- Slideshow/canvas accounts: $1–2 per 1,000 views (range up to $2–8); one program pays $500/month flat for one post per day on TikTok and Instagram plus $1 per 1,000 views (2026) — [canvas-ugc.com](https://canvas-ugc.com/); [Rosa Verde Canvas UGC program](https://rosaverdegroup.com/canvas-ugc-program.html)

**Other founders**
- Turbo AI: founders shot 40+ TikToks themselves before scaling (2024) — [Starter Story](https://www.starterstory.com/turbolearn-ai-breakdown)
- Quittr's Alex Slater discusses what works to scale a mobile app in 2026 on the Valid App Growth podcast (content not retrieved) — [Valid App Growth](https://www.buzzsprout.com/2604336/episodes/18884194-what-actually-works-to-scale-a-mobile-app-in-2026-w-alex-slater-from-quittr)

### Inferences
- Budget math to copy: estimate revenue per thousand views from early tests, then only sign flat deals whose expected CPM is below it. At $5 CPM and Cal AI's first-post result (~$2 per download, ~$20 per paying user), the model works only when a trial-plus-annual plan yields more than about $20–30 per payer after store fees.
- Sequence: (1) founder-made videos and $50-level micro creators to find a format, (2) flat-fee multi-video deals with 50K+ follower niche creators, (3) in-house UGC accounts on base-plus-CPM pay, (4) ad-specific creator content and paid spend once organic plateaus.
- Brazil: creator rates in reais are likely lower than US figures, but so is revenue per user; the CPM rule should be recomputed from local revenue per thousand views. No Brazil creator-rate data was collected here.

### Gaps
- No reliable source on Spark Ads/whitelisting specifics, number of in-house accounts, or account warm-up routines for these apps.
- No disclosed blended CAC or payback period for Cal AI beyond the first-post anecdote.
- Apple Search Ads usage was not documented in the retrieved sources.
- Specific winning hooks beyond "scan the meal" were not retrieved.

## 4. Unit economics benchmarks

### Takeaway
Paywall-first apps convert a median of about 10.7% of downloads to paid by day 35 versus 2.1% for freemium and earn about $3.09 per install by day 60 versus $0.38, with nearly identical one-year retention (RevenueCat 2026). AI apps earn about 41% more per payer but retain worse, and web checkout cuts payment fees from 15–30% to roughly 3%.

### Cited Findings
- RevenueCat State of Subscription Apps 2026 covers about 115,000 apps and $16B+ in revenue, mostly 2025 data [VENDOR dataset] — [Subscription Insider](https://www.subscriptioninsider.com/blog/revenuecat-data-shows-subscription-app-growth-concentrating-at-the-top-news)
- Hard paywall median day-35 download-to-paid 10.7% (down from 12.1% in 2025) versus 2.1% for freemium; top decile of hard-paywall apps 38.7%. Some summaries mislabel this as "trial-to-paid". RevenueCat's "hard paywall" bucket includes trial-led apps like Cal AI (2026) — [BuildMVPFast summary](https://www.buildmvpfast.com/blog/hard-paywall-vs-free-trial-revenuecat-indie-app-2026); [RevenueCat blog](https://www.revenuecat.com/blog/growth/subscription-app-trends-benchmarks-2026)
- Revenue per install at day 60: $3.09 hard paywall versus $0.38 freemium (2026) — [Tasu summary](https://tasu.ai/library/hard-paywall-vs-free-trial-conversion)
- One-year retention: about 27% hard paywall versus 28% freemium (2026) — [Tasu summary](https://tasu.ai/library/hard-paywall-vs-free-trial-conversion)
- Trial length: trial-to-paid 25.5% for trials of 4 days or fewer versus 42.5% for 17–32 day trials; yet short trials (4 days or less) rose from 42.1% to 46.5% of apps (2026) — [RevenueCat blog](https://www.revenuecat.com/blog/growth/subscription-app-trends-benchmarks-2026); [Tasu summary](https://tasu.ai/library/hard-paywall-vs-free-trial-conversion)
- Weekly plans with a trial: 42.2% trial-to-paid and 67.7% first renewal [VENDOR, Adapty 2026, via secondary summary] — [ASOitis hard vs soft paywall](https://asoitis.com/blog/hard-paywall-vs-soft-paywall)
- Adapty 2026 trial-to-paid is quoted as a 53% median in one summary and 25.6% global average in another (different definitions) — [RocketShip HQ](https://www.rocketshiphq.com/paywall-optimization-fitness-apps/)
- AI apps: about 41% more revenue per payer over a year but about 30% faster churn (2026) — [PPC Land](https://ppc.land/ai-apps-earn-41-more-per-user-but-churn-30-faster-revenuecat-finds/); [Subscription Insider](https://www.subscriptioninsider.com/article-type/news/revenuecat-data-shows-subscription-app-growth-concentrating-at-the-top)
- Market skew: median year-over-year MRR growth 5.3%, top 10% of apps 306% (2026). A marketing blog puts the median iOS Health & Fitness app at $109/month — [Subscription Insider](https://www.subscriptioninsider.com/article-type/news/revenuecat-data-shows-subscription-app-growth-concentrating-at-the-top); [AppScout](https://appscout.web.app/blog/cal-ai-formula)
- Billing errors cause 32.2% of Google Play cancellations versus 15.2% on the App Store (2026) — [Subscription Insider](https://www.subscriptioninsider.com/blog/revenuecat-data-shows-subscription-app-growth-concentrating-at-the-top-news)
- Store fees: Apple standard 30%, 15% after a subscriber's first year; Stripe about 2.9% plus fixed fee. Example: on a $79.99 annual plan, about $2.62 via Stripe versus $24.00 at Apple's 30% — [Airbridge](https://www.airbridge.io/en/blog/does-web-to-app-improve-profitability)
- Web-to-app: 82% of top-grossing apps used web funnels in 2025, up from about 46% in 2024; 1.33x better subscription retention; first-year LTV about $100 on web versus $50 for iOS app campaigns (US, 2024) [VENDOR, FunnelFox] — [FunnelFox State of Web2App 2026](https://funnelfox.com/state-of-web2app-2026); [GlobeNewswire, Jan 20 2026](https://www.globenewswire.com/news-release/2026/01/20/3221719/0/en/FunnelFox-Releases-the-State-of-Web2app-2026-Report.html)
- Web funnel pricing pattern: 88% use intro discounts (versus 10% on iOS); average $8.24 intro price then $37.24/month renewal (2026) — [Consumer App Index](https://cai-breakdowns.pages.dev/web2app-paywalls-2026)
- Chargeback risk on web: one source says Stripe flags accounts above a 1% chargeback rate (not confirmed against Stripe documentation) — [Airbridge](https://www.airbridge.io/en/blog/web-to-app-funnels-explained)

### Inferences
- A rough planning model for a Cal AI-style app: about 10% of installs pay (median for paywall-first), about $3 revenue per install at day 60, about 27% of annual payers still subscribed at one year. Cal AI's own first cohort (10% paid) is consistent with the median, not an outlier.
- Weekly plans monetize fast but the 67.7% first-renewal figure implies steep weekly decay; annual-with-trial trades lower initial conversion for cash up front, which funds creator deals.
- The 15% Apple small-business rate (under $1M/year) was not covered by the retrieved sources; see Gaps.

### Gaps
- No sourced refund-rate benchmark, no weekly-versus-annual 12-month retention curves, and no LLM cost-per-user figure for any of these apps were found.
- Apple Small Business Program (15% under $1M) and Google Play 15% tier were not confirmed in retrieved sources during this session.
- Install-to-trial rates specifically (as opposed to download-to-paid) were not found.

## 5. Tools founders use

### Takeaway
Superwall is the one tool with a documented Cal AI case study (61 onboarding-paywall experiments, spin-wheel paywall); beyond that, the stack is inferred from which vendors publish teardowns, not from founder statements.

### Cited Findings
- Cal AI ran its paywall experiments on Superwall: 61 meaningful experiments on the onboarding paywall, spin-wheel discount paywall, "monthly revenue 3x+ in 10 months" [VENDOR] — [Superwall case study](https://superwall.com/case-studies/cal-ai)
- Cal AI attribution for paid ads used App Store custom product pages tied to individual Facebook ads [SELF] — [Founder-playbooks](https://founder-playbooks.pages.dev/insight/influencer-to-paid-ads-growth-ladder)
- Web quiz and Stripe checkout funnels are built with tools such as web2wave and FunnelFox, both of which publish Cal AI funnel teardowns as marketing [VENDOR] — [web2wave](https://resources.web2wave.com/calai/); [FunnelFox](https://blog.funnelfox.com/cal-ai-influencer-marketing/)
- Adapty maintains a paywall library with price lists for Umax, Rizz, Bible Chat and Cal AI; RevenueCat publishes the main benchmark report — [Adapty Umax](https://adapty.io/paywall-library/umax-become-hot/); [RevenueCat](https://www.revenuecat.com/state-of-subscription-apps-2026/)
- Shortimize and Stormy.ai position themselves as tracking/creator-search tools for this playbook and publish Cal AI breakdowns [VENDOR] — [Shortimize](https://www.shortimize.com/blog/cal-ais-marketing-strategies-lessons-from-a-400k-mrr-success-story); [Stormy.ai](https://stormy.ai/blog/cal-ai-tiktok-marketing-playbook-2026)

### Inferences
- Minimum stack for a clone: a remote paywall/onboarding experiment tool (Superwall or Adapty), a subscription backend (RevenueCat or Adapty), a web funnel builder with Stripe, and a view-tracking sheet or tool for creator CPM.

### Gaps
- No founder statement was found naming RevenueCat, Mixpanel, AppsFlyer or Amplitude for Cal AI, Quittr, Umax or Turbo AI.

## 6. Criticism and failure modes

### Takeaway
Cal AI was removed from the US App Store for about four days in mid-April 2026 for bypassing in-app purchase with an embedded Stripe checkout and for a paywall Apple called deceptive; Quittr left intimate data of 600,000+ users exposed for months. Clones are numerous and most earn under $10K/month.

### Cited Findings

**Cal AI App Store removal (verified)**
- Apple told TechCrunch (Apr 21, 2026) it briefly pulled Cal AI the previous week; the app was reinstated four days later after fixes and returned to #4 or #5 in Health & Fitness. MyFitnessPal and Cal AI did not comment [VERIFIED by Apple] — [TechCrunch, Apr 21 2026](https://techcrunch.com/2026/04/21/apples-cal-ai-crackdown-signals-its-still-policing-the-app-store/); [MacRumors](https://www.macrumors.com/2026/04/21/apple-cal-ai-app-store-removal/); [Cult of Mac](https://www.cultofmac.com/news/why-app-store-pulled-cal-ai-app); [9to5Mac](https://9to5mac.com/2026/04/21/popular-calorie-tracker-briefly-pulled-from-app-store-over-iap-and-billing-violations/)
- Violations Apple cited: Guideline 3.1.1 (embedded third-party Stripe payment flow with Apple's in-app purchase option removed entirely; external options are allowed for non-reader apps only alongside IAP); Guideline 3.1.2(c) (paywall showed the weekly-equivalent price more prominently than the amount actually billed; a free-trial toggle did not make auto-renewal clear); Guideline 5.6 Developer Code of Conduct (a second purchase flow shown after the user declined the first offer, described as manipulative) — [MacRumors](https://www.macrumors.com/2026/04/21/apple-cal-ai-app-store-removal/); [TechCrunch](https://techcrunch.com/2026/04/21/apples-cal-ai-crackdown-signals-its-still-policing-the-app-store/)
- Vendor write-up of the lessons for app-to-web checkout — [Paddle](https://www.paddle.com/blog/what-cal-ai-taught-us-about-app2web)

**Accuracy** — see section 1: 345 kcal average underestimate in a 2026 controlled study as cited; "90%" is a self-reported lab-style number — [RaftLabs](https://www.raftlabs.com/blog/cal-ai-product-teardown); [Fitia](https://fitia.app/learn/article/ai-calorie-photo-apps-accuracy-2026/)

**Quittr data exposure (reported by 404 Media, March 2026)**
- Misconfigured backend (reported as Google Firebase) left a database readable without proper authentication, exposing intimate data of hundreds of thousands of users (600,000+ in several outlets); roughly 100,000 reportedly minors — [404 Media](https://www.404media.co/viral-quittr-porn-addiction-app-exposed-the-masturbation-habits-of-hundreds-of-thousands-of-users/); [Tribuna do Sertão, Mar 11 2026](https://www.tribunadosertao.com.br/mundo-tech/2026/03/11/870852-falha-em-app-para-viciados-em-pornografia-expoe-dados-sensiveis-de-milhares-incluindo-menores)
- A researcher warned Quittr in September 2025; Slater said he would fix it within hours; it was still open months later; he first denied the vulnerability and suggested data could be fabricated, then fixed it before March 10, 2026 — [404 Media follow-up](https://www.404media.co/multiple-hackers-warned-anti-porn-app-quittr-about-security-issue-for-months/)
- A US law firm (Shamis & Gentile) is investigating; one listing counts 350,000 affected users; no filed suit found — [ClaimDepot](https://www.claimdepot.com/data-breach/quittr-2026)

**Paywall complaints and clones**
- Umax: price hidden until after selfies are uploaded; the "invite 3 friends" unlock failed in a Fortune test — [RealWorldAppeal](https://realworldappeal.com/en/blog/umax-ai)
- Rizz-category app analysis reports users' top complaint is the paywall blocking core features and a surge in refund requests after a shift to high-friction paywalls — [Marlvel](https://marlvel.ai/api/llm/apps/lifestyle/rizz-god-ai-pick-up-lines)
- Many Cal AI lookalikes exist with near-identical names ("CalAI: Photo Calorie Tracker", "Calorie Ai: Food Cal Counter", "Cal Me AI", "Cal Plus"); examples: Cal Me AI about 44 monthly actives, Cal Plus about 5.1K monthly actives; most show under $10K/month [EST] — [AppGoblin Cal Me AI](https://appgoblin.info/apps/6780344487); [AppGoblin Cal Plus](https://appgoblin.info/apps/6748910976)
- Latka names Cronometer and SnapCalorie as closest competitors, with Cal AI largest by revenue (2026) [EST] — [Latka](https://getlatka.com/companies/calai.app/team)
- Apple updated guidelines so some well-established app types can be removed under 4.3 (spam/saturation) if not updated or not attracting customers (2026) — [PYMNTS](https://www.pymnts.com/apple/2026/apple-updates-app-store-rules-to-remove-copycat-apps/)

### Inferences
- The exact things that maximized Cal AI's conversion (Stripe-only checkout in app, weekly-equivalent price display, second offer after decline) are the things Apple punished. A clone built in late 2026 should keep IAP present, show the billed amount as the largest price, state auto-renewal next to any trial toggle, and treat decline-offers as a review risk.
- For any app holding sensitive data (health, sexual behavior, minors), locked-down database rules and a real response process for researcher reports are part of the cost of the playbook.

### Gaps
- No count of total Cal AI clones and no category-level revenue distribution from Sensor Tower or Appfigures was found.
- No lawsuit or regulator action (FTC or state AG) against Cal AI, Umax or Quittr over subscription practices was found; a search for Cal AI class actions returned nothing relevant.
- Eating-disorder-related criticism of Cal AI was not retrieved in this session.

## 7. Legal line for a clone, and Brazil-specific differences

### Takeaway
Apple's own rules draw the line at another developer's icon, brand or product name (Guideline 4.1(c), added late 2025) and at copying an app outright; no court dispute between calorie-AI apps was found. In Brazil, Apple has allowed alternative in-app payment methods and external links since a CADE settlement (ratified December 2025, live June 18, 2026 per most outlets), which changes the store-fee math.

### Cited Findings
- Apple Guideline 4.1 (Copycats): App Review rejects apps that copy other apps and closes accounts that repeatedly submit copycats or impersonate a service — [Apple App Review help, 4.1](https://developer.apple.com/help/app-review/guideline-reference/4-1-prevent-copycat-rejection)
- November 2025 update added 4.1(c): you cannot use another developer's icon, brand or product name in your app's icon or name without their approval — [MacStories](https://www.macstories.net/linked/apple-beefed-up-its-rule-against-copycat-apps/); [Daring Fireball, Nov 26 2025](https://daringfireball.net/linked/2025/11/26/november-update-to-the-app-store-review-guidelines)
- Enforcement is inconsistent according to developer forum posts: originals stuck in review while verbatim clones were approved; rejections under 4.1 with no specific feedback (2025–2026, unverified forum reports) — [Apple forums thread 821751](https://developer.apple.com/forums/thread/821751); [Apple forums thread 793905](https://developer.apple.com/forums/thread/793905)
- Quittr's founder is described as having started by copying a competitor's onboarding flow, with no reported consequence [SELF, promotional] — [Valid App Growth](https://www.buzzsprout.com/2604336/episodes/18884194-what-actually-works-to-scale-a-mobile-app-in-2026-w-alex-slater-from-quittr)

**Brazil**
- CADE ratified a settlement with Apple in December 2025; Apple began allowing alternative payment methods inside apps, external purchase links and alternative app stores in Brazil on June 18, 2026 per most outlets (one outlet says October 18; another ties it to iOS 26.5) — [TecMundo](https://www.tecmundo.com.br/mercado/413975-apple-oficializa-lojas-externas-no-brasil-e-outros-meios-de-pagamento-na-app-store.htm); [Olhar Digital, Jun 18 2026](https://olhardigital.com.br/2026/06/18/pro/apple-agora-o-ios-e-aberto-no-brasil/); [TNH1](https://www.tnh1.com.br/noticia/nid/apple-libera-sistema-de-pagamentos-em-aplicativos-no-brasil-apos-acordo-com-o-cade/)
- Reported fee structure in Brazil: 15% "steering" commission on purchases via external links; 5% commission for apps distributed outside the App Store; another source gives bands of 15–26% for full use of Apple services and 10–15% for App Store apps using outside payments. Apple says 86% of developers in Brazil currently pay no fees. Sources differ, so check Apple's Brazil terms — [MacMagazine, Dec 23 2025](https://macmagazine.com.br/post/2025/12/23/apple-permitira-compras-externas-e-lojas-alternativas-a-app-store-no-brasil/); [Folha PE](https://www.folhape.com.br/economia/apple-abre-iphone-para-lojas-de-apps-e-sistemas-de-pagamentos-de/494923/)
- Kids-category apps may not link to transaction sites; Pix by NFC on iPhone is a separate CADE matter, with Apple signaling in June 2026 it will open the NFC chip — [TecMundo](https://www.tecmundo.com.br/mercado/413975-apple-oficializa-lojas-externas-no-brasil-e-outros-meios-de-pagamento-na-app-store.htm); [Olhar Digital, Mar 19 2026](https://olhardigital.com.br/2026/03/19/pro/cade-intima-apple-entenda-por-que-a-gigante-da-tecnologia-e-investigada-por-dificultar-o-pix-por-aproximacao-no-iphone/)

### Inferences
- Safe to copy (general principle, not sourced in this session and not legal advice): the idea and feature set, such as photo-to-calories, a long quiz, a plan reveal and a trial paywall. Not safe: the name "Cal AI" or confusingly similar names, the icon, screenshots, marketing and UI copy text, creative assets and code. Apple's 4.1(c) now makes name/icon similarity an explicit rejection ground independent of trademark law.
- The many "Cal ___ AI" names on the store show that near-name clones do get approved, but they are exposed to 4.1(c) removal and to trademark complaints, and they earn little.
- Brazil differences to model: (1) lower price points in reais, so creator CPM targets must be recalculated; (2) Android share is far higher than in the US, so Google Play billing and its higher billing-error cancellation rate matter more; (3) Pix/boleto on a web or external checkout is now permitted on iOS in Brazil with a reduced Apple commission, which makes a web-to-app funnel more attractive than in the US; (4) consumer law (CDC right of withdrawal, clear price display) and LGPD for health data apply. Points 1, 2 and 4 are general knowledge, not researched here.

### Gaps
- No documented lawsuit, DMCA or trademark takedown between calorie-AI apps or between any of the named apps and their clones was found.
- No source was retrieved on copyright/trade-dress doctrine itself (idea versus expression); the report writer should treat the "safe/not safe" list as general principle needing a lawyer's confirmation in Brazil (INPI trademark, Lei de Software, Lei de Direitos Autorais).
- Exact current Apple Brazil commission tiers and whether subscriptions via Pix recurring (Pix Automático) are supported in external checkout were not confirmed.
- Brazilian app-store revenue benchmarks, local creator rates and Portuguese-language calorie-AI competitors were not researched.
