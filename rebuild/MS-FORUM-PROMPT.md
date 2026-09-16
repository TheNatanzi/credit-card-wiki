# MS forum deep sweep — find debit-payable cards + learn the community's criteria

Context: we run a Costco gold-bar buying operation. We buy ~$10k–$50k/month of gold bars at Costco warehouse (MCC 5300) on a credit card, then sell the gold. Profit = card rewards. We have a Taekus rewards DEBIT card that pays ~1.8% and want to ALSO pay the credit-card bill with it, stacking rewards. So the single most valuable fact is: **which US credit cards let you pay the bill with a debit card in 2026** — and what the MS community has learned about doing it.

Search these communities hard (use WebSearch with site: filters and WebFetch on the threads you find):
- reddit.com/r/churning, r/manufacturedspending, r/CreditCards, r/awardtravel
- doctorofcredit.com (comments matter as much as posts)
- flyertalk.com (Manufactured Spending forum, Citi/Chase/Amex forums)
- myfico.com forums, creditcardforum.com, milestalk.com, frequentmiler.com, us-creditcardguide.com
- Discord/Telegram write-ups that show up in search results

## PART 1 — the list (primary deliverable)
Find EVERY US credit card / issuer that accepts a **debit card** as a bill-payment method in 2026, and every one that recently STOPPED. Look for the exact terms people use: "pay credit card with debit card", "debit card payment", "pay by phone debit", "CheckFreePay", "in-branch debit payment", "Walmart bill pay", "MoneyGram", "Western Union pay a credit card", "Plastiq" (note: Plastiq is a credit rail, not debit — flag it), "pay card at the register".
For each finding record: issuer, which products, channel (online / app / phone-IVR / phone-agent / branch / store register / third-party), fee, dollar/day limits, how the payment CODES (purchase MCC vs bill-pay vs AFT MCC 6012/6051), and dated reports of it working or failing.
Pay special attention to **Citi** (a cardholder confirmed Double Cash personal no longer takes debit in 2026 — find the date and scope), **Synchrony**, **Discover** (post-Capital One acquisition), **Target/Sam's/store cards paid at the register**, and small issuers/credit unions people mention.

## PART 2 — what MS people actually optimize for (the lesson)
Summarize, in the community's own framing, how experienced MS practitioners evaluate a play. Cover at least:
- the metrics they rank on (net cents per dollar after fees, liquidity/unwind cost, velocity, cycle time)
- risk vocabulary: shutdown, clawback, FR (financial review), 5/24, "blood in the water", velocity flags, adverse action, SAR/CTR and structuring cautions
- which issuers are known-sensitive vs tolerant for high-volume/cash-like spend
- how they treat caps, tiers and "up to X%" marketing
- what specifically kills a play (coding change, MCC reclass, terms rewrite, cap added)
- anything they say about buying **gold/bullion/precious metals on a card** and Costco specifically
- anything about **Taekus** (invite-only rewards debit card) — does it pay on bill payments, is there a monthly cap, how do people describe its rewards mechanism

## Output
Write strict JSON to the path in your task:
```
{
 "debit_pay_findings": [
   {"issuer":"...","cards":"...","works":"Y"|"N"|"mixed","channel":"...","fee_usd":<number>,"limit_note":"...",
    "codes_as":"purchase"|"bill-pay"|"AFT"|"unknown","as_of":"<YYYY-MM or 'undated'>","evidence":"<=200 chars quote-free summary","url":"..."}
 ],
 "stopped_accepting": [ {"issuer":"...","when":"...","scope":"...","url":"..."} ],
 "new_card_leads": [ {"card":"...","issuer":"...","why_interesting":"<=140 chars","url":"..."} ],
 "ms_criteria": [ {"topic":"...","what_they_look_for":"<=200 chars","why":"<=160 chars","url":"..."} ],
 "gold_costco_notes": [ {"note":"<=200 chars","url":"..."} ],
 "taekus_notes": [ {"note":"<=200 chars","url":"..."} ],
 "confidence":"high"|"med"|"low"
}
```
Rules: every entry needs a url. Prefer 2025–2026 posts; mark older ones in `as_of`. Do not invent threads — if a search returns nothing, say so with an empty array. Validate the JSON with python json.load before finishing.
Reply with ONLY: counts per array, then the 5 most useful findings as one line each.
