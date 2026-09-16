# Codex overnight prompt — Credit Card Master Wiki, 2026-09-17

Paste everything below the line into Codex. Working folder: `C:\Claude\credit-card-wiki`.

---

You are running unattended overnight. Nobody will answer questions. Work until all four jobs are done or you run out of budget, and write every result to disk as you go so a crash loses nothing.

## 0. Read first (in this order)

1. `HANDOFF-2026-09-16.md` — what the wiki is, the standing rules, current state.
2. `MS-FORUM-FINDINGS-2026-09-15.md` — what the community already knows, including the 2022 dating error and the AFT threat.
3. `rebuild/DEBITPAY-DISCOVERY-PROMPT.md` — the research method and the rule of evidence.
4. `rebuild/build.py` — how the score is computed. Note `TAEKUS`, `MAX_SWIPE`, `SANITY`.
5. `cards.json` — the 287 cards as the page shows them.
6. `rebuild/dp_out_*.json` — every debit-pay verdict so far. The `dp_out_z_*` files are yesterday's sweep by Claude. `dp_out_z_sync.json` may or may not exist yet.
7. `rebuild/all-names.txt` — every card name already known. Use it to avoid re-adding cards.

## What the wiki is for (one paragraph)

Medi buys gold bars at a Costco warehouse (merchant category code **MCC 5300**, warehouse club — NOT 5411 grocery) with credit cards, roughly $10,000–$50,000 a month. He then pays the credit-card bill **with a rewards debit card** (today: Taekus) so the debit card earns a second reward on top. The wiki ranks cards by:

```
Upside% = Costco% at $50k/month + debit-pay stack (1.80%) − annual fee
```

Two things decide whether a card is worth opening: (a) what it really pays at MCC 5300 after caps, and (b) whether its bill can be paid with a debit card AND whether that payment earns anything on the debit side.

## Standing rules — these override anything you find

1. **Never score by the headline rate.** Payment rail and MCC 5300 decide value.
2. **Costco = MCC 5300.** Most grocery bonuses exclude it.
3. **Never kill a lead.** No explicit statement either way = `?`. `N` needs the issuer to say no, or an exhaustive official payment-methods list that omits debit. "It settles by ACH" is NOT a no.
4. **Non-US is a hurdle, not a disqualifier.** Record it; do not drop the card.
5. **Medi's word is the record.** `rebuild/medi-rulings.json` beats every source. Citi Costco Anywhere DOES take Taekus. Citi Double Cash does not. Do not argue with these.
6. **Evidence.** `Y` needs the issuer's own page/agreement/app screen/IVR, or a DATED first-hand report. WalletHub user answers, content farms, and AI search summaries are never evidence on their own — yesterday an AI summary turned a 2022 forum post into "April 2026" and it propagated through three files. **Read the date off the page itself.**
7. **No guessed numbers.** If a rate, cap, or fee is not written somewhere you can cite, leave it null and say so.
8. **Card-rate only.** Never fold the 1.80 debit stack into a card's own percentage. The build adds it. (A past agent double-counted it.)
9. **Do the work yourself.** Do not spawn sub-agents. Two past agents delegated and exited without writing their file.
10. **Do not edit** `cards.json`, `index.html`, `artifact.html`, `rebuild/build.py`, `rebuild/template.html`, `rebuild/medi-rulings.json`, or any existing `dp_out_*.json`. Write ONLY inside `codex/2026-09-17/`. Claude reviews and merges in the morning.
11. **Do not commit or push.**

## Output folder

Create `C:\Claude\credit-card-wiki\codex\2026-09-17\`. Everything goes there. Validate every JSON file with
`python -c "import json,io;json.load(io.open(PATH,encoding='utf-8'))"` before moving on.

---

## JOB 1 — Adversarial audit of Claude's work (do this first)

Assume Claude made mistakes. Your job is to find them. Yesterday's sweep resolved 29 of 64 unknown credit-card rails; the files are `rebuild/dp_out_z_boa.json`, `dp_out_z_wfciti.json`, `dp_out_z_cu.json`, `dp_out_z_biz.json`, `dp_out_z_crypto.json`, and `dp_out_z_sync.json` if present.

For **every** `Y` and **every** `N` in those files:
- Open each cited source yourself. Does it actually say what the note claims? Quote the exact sentence.
- Is the source dated? Is the date real (read off the page, not a search snippet)?
- Is an `N` a genuine explicit refusal / exhaustive list, or an inference dressed up? Rule 3 applies.
- Is a `Y` the issuer's own words, or a third party (doxo, WalletHub, a blog)?
- Is the verdict per-product, or was an issuer-wide statement applied to a card it does not cover?

Specific things Claude was unsure about — check these hardest:
- **Consumers Credit Union = Y.** The fee page says "loan", not "credit card". Is the credit card inside that payment flow? Is the rail currently down (a maintenance banner said "currently unavailable")?
- **Bank of America = 13 N.** The verdict rests on "You have 5 options" + an Online Banking agreement. Is the "5 options" list truly exhaustive? BoA also lists **Western Union** as a payment route, and WU takes debit cards. Is BoA an enrolled WU biller? If yes, that is a third-party debit rail, and the verdict needs a note.
- **Wells Fargo = 7 N.** Confirm the "personal check, money order, or cashier's check" clause is in each card's own agreement, not one shared page.
- **The 2022 dating fix.** Confirm FlyerTalk thread 1550209 post #1546 is dated 2022-04-23. Then search every file in this repo for any other date that came from a search summary rather than a page, and list them.
- **The `-` ("no bill") state for ether.fi and Step.** Is it true neither card ever produces an amount owed that could be paid from outside? ether.fi Borrow Mode is a loan against collateral — can that loan be repaid by debit card?
- **The 48 debit/prepaid cards** Claude excluded from the rail question because "a debit card has no bill". Check each is really debit/prepaid and not a mislabelled credit or charge card.

Also audit the **pipeline** (`rebuild/build.py`):
- Does any card get the 1.80 stack when it should not (non-credit product, `-`, dead status)?
- Does the merge order let an old, weaker verdict overwrite a newer, stronger one? (Later files win, sorted by filename.)
- Are there cards whose top-level `debit_pay` disagrees with their `deep.debit_pay`? List them and say which one has the better evidence.
- Spot-check the **top 20 by Upside%**: recompute each one's Costco% at $10k and $50k by hand from its tiers and caps. Report any that are off by more than 0.05.

**Write:** `codex/2026-09-17/audit.md` (plain words, one finding per bullet, most severe first, each with the file, the claim, what the source really says, and a suggested fix) and `codex/2026-09-17/audit-verdicts.json`:

```json
[{"card":"exact name","current":"Y|N|?|-","should_be":"Y|N|?|-","agree":true,"evidence":"<=200 chars with the quoted sentence","source":"url","source_date":"YYYY-MM-DD or null","confidence":"high|med|low"}]
```

---

## JOB 2 — The debit side: which debit cards actually PAY on a bill payment?

This is the question that decides whether the whole ranking is real. Everything so far asked "can the bill be paid by debit?". Almost nobody asked "does the debit card earn anything when it does?".

Evidence already against it:
- The FlyerTalk megathread's list of debit cards that WORK at Citi is annotated "no miles", "no cb", "no 1% cb" (Alaska, SunTrust, UFB Direct, M1 Plus, PayPal Business).
- Taekus reportedly paid ~0% on an Amazon reload, ~2% on a hotel.
- A card-bill payment by debit card likely codes as an **AFT** (Account Funding Transaction — a Visa/Mastercard transaction type for moving money, often MCC 6012 or 6051), and rewards programs routinely exclude AFTs.

Do this:
1. **Establish how a debit-card bill payment codes, per issuer where possible.** Purchase, bill-pay, or AFT? MCC? Look for: Visa/Mastercard AFT rules and the "funds disbursement / account funding" docs, issuer terms that mention "payments to other credit accounts", processor docs (ACI Speedpay, Fiserv/CheckFree, Paymentus), and dated data points where someone read the MCC off their statement.
2. **Build the list of rewards debit cards** — every US debit card that pays cashback or points on spend. Start with the 48 debit/prepaid cards already in `cards.json` (`product` = debit or prepaid), then find more. For each, find the **fine print on exclusions**: does it exclude AFTs, "quasi-cash", "payments to credit accounts", MCC 6012/6051/6540, money transfers, bill payments? Quote the clause.
3. **Taekus specifically.** Read Taekus's own rewards terms (personal AND business products). What exactly is excluded? Any dated data point of Taekus earning on a credit-card bill payment? Taekus sells personal, business and corporate cards — Citi blocked **commercial** debit cards as a payment source on 2026-01-30, so note which Taekus products are commercial.
4. **Rank the debit cards** by "reward on a debit-card bill payment", with `unknown` wherever the fine print is silent. Silent ≠ excluded (rule 3).

**Write:** `codex/2026-09-17/debit-side.md` (plain words) and `codex/2026-09-17/debit-cards.json`:

```json
[{"card":"","issuer":"","network":"visa|mastercard|other","commercial":true,"reward_pct_purchase":null,"pays_on_bill_payment":"Y|N|unknown","excludes_aft":"Y|N|silent","exclusion_quote":"exact clause or null","codes_as":"purchase|bill-pay|AFT|unknown","monthly_cap_usd":null,"fee_usd":null,"in_wiki":true,"as_of":"YYYY-MM","evidence":"<=200 chars","sources":["url"],"confidence":"high|med|low"}]
```

---

## JOB 3 — Find more cards, especially the bizarre ones

The wiki has 287 cards (`rebuild/all-names.txt`). Find the ones it is missing. Priority is the strange end of the market, because the obvious cards are already covered and already bad at MCC 5300:

- **Crypto cards**: self-custody / DeFi cards (Gnosis Pay style), exchange cards, stablecoin cards (USDC/USDT/PYUSD spend cards), Solana/Ethereum wallet cards, "borrow against crypto" credit lines with a card, cards issued by offshore issuers that still work in the US.
- **Fintech credit and charge cards**: new 2025–2026 launches, cards tied to a brokerage or neobank, cards with an unusual reward (stock, gold, bitcoin, points into a brokerage), invite-only or waitlist cards, cards for creators/gig workers.
- **Business and corporate cards** from spend-management startups.
- **Store-agnostic cards with a flat rate ≥ 2%** that anybody has not yet listed.
- **Cards with a debit-pay rail documented in their own terms** — these are worth more than a higher headline rate.
- **Anything that pays at Costco warehouse specifically** (MCC 5300), or that pays a bonus on "warehouse clubs".

For each new card, capture the same fields the wiki uses (look at one record in `cards.json` for the shape — at minimum `card, issuer, network, product, biz, status, reward_unit, cpp_max, cpp_floor, base_x, costco_x_max, costco_x_min, costco_cap_usd, cap_period, reward_cap_usd_month, min_txn_usd, fee_usd, fx_pct, debit_pay, lockup_usd, source, confidence, needs_research`), plus the fine print: MCC exclusions, precious-metals exclusions, "gift card / cash equivalent" exclusions, monthly caps, lockup/staking requirements, US eligibility, and the debit-pay rail. Put any field you could not find in `needs_research` and leave it null.

Also look for **fine print on cards already in the wiki** that changes their score: precious-metal exclusions (Robinhood Gold already has one), warehouse-club exclusions, reward caps that were added in 2026, products closed to new applicants, and 2026 devaluations.

**Write:** `codex/2026-09-17/new-cards.json` (same shape as `cards.json` records), `codex/2026-09-17/fine-print-changes.json`:

```json
[{"card":"exact wiki name","field":"","current":"","should_be":"","quote":"exact clause","source":"url","as_of":"YYYY-MM","confidence":"high|med|low"}]
```

and `codex/2026-09-17/discovery.md` listing where you searched and what came up empty.

---

## JOB 4 — The remaining unknown rails

About 35 credit cards still have `debit_pay = "?"`. List them with:

```
python -c "import json,io;[print(c['upside50'],c['card']) for c in sorted(json.load(io.open('cards.json',encoding='utf-8')),key=lambda c:-(c.get('upside50') or 0)) if c['status']=='active' and c.get('product')=='credit' and c['debit_pay']=='?']"
```

Work them top-down by `upside50` using `rebuild/DEBITPAY-DISCOVERY-PROMPT.md`. Robinhood Gold (the #1 lead) and the Citi cards matter most. Try the routes Claude could not: Reddit (r/churning, r/manufacturedspending — try old.reddit, search-engine cache, mirrors), the myFICO threads that returned 403, the Wayback Machine for payment pages, and processor biller directories (Western Union, CheckFreePay, MoneyGram).

**Write:** `codex/2026-09-17/dp_out_codex.json` in exactly the shape of `rebuild/dp_out_z_cu.json` (one object per card, `fixes.debit_pay` = `Y`/`N`/`?`).

---

## Finish

Write `codex/2026-09-17/SUMMARY.md` last. Plain words, short lines, Medi reads it on his phone and has ADD:

1. One line: the single most important thing you found.
2. A table: Job → files written → counts.
3. Every place you disagree with Claude, one line each.
4. Every phone number a human should call, with what to listen for.
5. What you could not reach (blocked sites) — say so plainly, never fill the gap with a guess.
